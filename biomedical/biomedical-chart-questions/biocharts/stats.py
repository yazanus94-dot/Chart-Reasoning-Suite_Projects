"""Small statistics helpers used by the questions (standard library only)."""


def linear_fit(x, y):
    """Ordinary least squares: returns (slope, intercept)."""
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxx = sum((a - mx) ** 2 for a in x)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    slope = sxy / sxx
    return slope, my - slope * mx
