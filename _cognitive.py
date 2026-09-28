"""Bounded geometric proxies, not truth scores or dynamical Lyapunov exponents."""

import math
from itertools import combinations


def distance(a, b):
    """Curvature -1 Poincare distance, stable for coincident nearby points."""
    aa = math.fsum(x * x for x in a)
    bb = math.fsum(x * x for x in b)
    separation = math.sqrt(math.fsum((x - y) ** 2 for x, y in zip(a, b)))
    return 2 * math.asinh(separation / math.sqrt((1 - aa) * (1 - bb)))


def analyze_thought_stability(vectors):
    lengths = [distance(a, b) for a, b in zip(vectors, vectors[1:])]
    # Zero/near-zero steps make ratios undefined. Never turn missing evidence
    # into a perfect stability/trust result using epsilon smoothing.
    if any(value <= 1e-12 for value in lengths):
        return {"method": "mean_log_step_ratio_v1", "step_distances": lengths,
                "mean_log_step_ratio": None, "trend": "indeterminate",
                "reason": "Zero or numerically unresolved step distance"}
    ratios = [math.log(b) - math.log(a) for a, b in zip(lengths, lengths[1:])]
    trend = math.fsum(ratios) / len(ratios)
    return {"method": "mean_log_step_ratio_v1", "step_distances": lengths,
            "log_step_ratios": ratios, "mean_log_step_ratio": trend,
            "trend": "contracting" if trend < -1e-6 else
                     "expanding" if trend > 1e-6 else "neutral",
            "limitation": "Step-length trend only; not convergence to an attractor, "
                          "a Lyapunov exponent, or hallucination detection."}


def analyze_geometry(vectors):
    distances = {(i, j): distance(vectors[i], vectors[j])
                 for i, j in combinations(range(len(vectors)), 2)}
    diameter = max(distances.values())
    delta = 0.0
    count = 0
    for a, b, c, d in combinations(range(len(vectors)), 4):
        sums = sorted((distances[a, b] + distances[c, d],
                       distances[a, c] + distances[b, d],
                       distances[a, d] + distances[b, c]))
        delta = max(delta, (sums[2] - sums[1]) / 2)
        count += 1
    return {"method": "exact_four_point_delta_v1", "delta": delta,
            "diameter": diameter, "normalized_delta": delta / diameter if diameter else None,
            "quadruples_evaluated": count,
            "limitation": "Finite-sample delta under the configured hyperbolic metric; "
                          "not a recommendation to change collection geometry."}
