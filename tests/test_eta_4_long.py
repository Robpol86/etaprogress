from etaprogress import eta


def test():
    eta._NOW = lambda: 1411868722.680839
    eta_instance = eta.ETA(240)
    pairs = [(i, i * 2) for i in range(1, 121)]
    for t, n in pairs:
        eta._NOW = lambda: t + 1411868722.680839
        eta_instance.set_numerator(n)

        assert n == eta_instance.numerator
        if t >= 2:
            assert t == eta_instance.elapsed
            assert 2.0 == eta_instance.rate_overall
