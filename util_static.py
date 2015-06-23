def get_average(lst, func = lambda x: x):
    ssum = 0
    for k in lst:
        ssum += func(k)
    return ssum / float(len(lst))

def do_zoom(lst, ratio = 1.5):
    av = get_average(lst)
    for k in range(len(lst)):
        lst[k] = (lst[k] - av) * ratio + av
    return lst