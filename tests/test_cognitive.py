import json
import math

import pytest

from test_optional_geometry import _issued_handles


def call(provider, handles, operation='analyze_thought_stability', **kwargs):
    return json.loads(provider.handle_tool_call('hyperspace_geometry', {
        'operation': operation, 'handles': handles, **kwargs}))


@pytest.mark.parametrize('positions,trend', [
    ([0, 1, 1.5, 1.75], 'contracting'),
    ([0, .25, .75, 1.75], 'expanding'),
    ([0, .5, 1, 1.5], 'neutral'),
])
def test_geodesic_step_trends(provider, fake_client, positions, trend):
    handles = _issued_handles(provider, fake_client, [math.tanh(x / 2) for x in positions])
    result = call(provider, handles)
    assert result['ok']
    assert result['result']['trend'] == trend
    assert result['result']['step_distances'] == pytest.approx([
        b - a for a, b in zip(positions, positions[1:])])
    assert 'trust_score' not in result['result']


def test_identical_vectors_are_indeterminate(provider, fake_client):
    handles = _issued_handles(provider, fake_client, [.1, .1, .2])
    result = call(provider, handles)['result']
    assert result['trend'] == 'indeterminate'
    assert result['mean_log_step_ratio'] is None


def test_order_is_caller_order_not_backend_order(provider, fake_client):
    handles = _issued_handles(provider, fake_client, [0, .4, .6, .7])
    original = fake_client.get_points
    fake_client.get_points = lambda *a, **kw: list(reversed(original(*a, **kw)))
    assert call(provider, handles)['result']['trend'] == 'contracting'
    assert call(provider, list(reversed(handles)))['result']['trend'] == 'expanding'


def test_exact_delta_on_geodesic_and_coincident_points(provider, fake_client):
    for coordinates in ([0, .1, .3, .6], [.1] * 4):
        handles = _issued_handles(provider, fake_client, coordinates)
        result = call(provider, handles, 'analyze_geometry')['result']
        assert result['delta'] == pytest.approx(0, abs=1e-12)
        assert result['quadruples_evaluated'] == 1
        if len(set(coordinates)) == 1:
            assert result['normalized_delta'] is None


def test_positive_delta_for_square(plugin):
    import importlib
    cognitive = importlib.import_module(plugin.__name__ + '._cognitive')
    points = [[.2, 0], [0, .2], [-.2, 0], [0, -.2]]
    result = cognitive.analyze_geometry(points)
    expected = cognitive.distance(points[0], points[2]) - cognitive.distance(points[0], points[1])
    assert result['delta'] == pytest.approx(expected)
    assert result['delta'] > 0


@pytest.mark.parametrize('handles,extras', [([], {}), (['forged'] * 3, {}),
    (['a', 'b', 'c'], {'ids': [1, 2, 3]}), (['a', 'b', 'c'], {'steps': 1}),
    (['forged'] * 17, {})])
def test_invalid_requests_do_not_read(provider, fake_client, handles, extras):
    before = list(fake_client.calls)
    assert not call(provider, handles, **extras)['ok']
    assert fake_client.calls == before


def test_missing_points_and_timeout_fail_closed(provider, fake_client):
    handles = _issued_handles(provider, fake_client, [.1, .2, .3])
    del fake_client.points[42]
    assert call(provider, handles)['error']['code'] == 'MALFORMED_RESULT'
    fake_client.fail = TimeoutError('private diagnostic')
    result = call(provider, handles)
    assert result['error']['code'] == 'BACKEND_TIMEOUT'
    assert 'private diagnostic' not in json.dumps(result)


def test_cognitive_read_only_and_bounded(provider, fake_client):
    handles = _issued_handles(provider, fake_client, [i / 30 for i in range(16)])
    before = dict(fake_client.points)
    result = call(provider, handles, 'analyze_geometry')
    assert result['result']['quadruples_evaluated'] == 1820
    assert fake_client.points == before
    assert len(json.dumps(result)) < 2000


def test_boolean_conversion_output_is_rejected(provider, fake_client, monkeypatch):
    import hyperspace.math as sdk_math
    handles = _issued_handles(provider, fake_client, [.1, .2, .3])
    monkeypatch.setattr(sdk_math, 'lorentz_to_poincare', lambda _: [False] * 128)
    assert call(provider, handles)['error']['code'] == 'MALFORMED_RESULT'
