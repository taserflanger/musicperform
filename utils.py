def warp_generator(cumulated_durations, warp_function):
    """
    returns modified cumulated_durations based on integrated tempo curve
    :param cumulated_durations: list[float]
    :param warp_function: function(float) -> float
    :return: modified cumulated_durations
    """
    if cumulated_durations[-1] == 0:
        print("warning: null durations warp to null durations")
        return cumulated_durations
    for i in range(len(cumulated_durations)):
        x = cumulated_durations[i] / cumulated_durations[-1]
        yield warp_function(x) * cumulated_durations[-1]


def warp_n(n):
    def f(x):
        return x ** n

    return f

cum_dur = [0, 1, 2, 3, 4 ,5]
print(list(warp_generator(cum_dur, warp_n(1.1))))
