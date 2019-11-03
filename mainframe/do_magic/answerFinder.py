import collections


def triangulate(results):
    flattened = []
    overlap = []
    if len(results) > 0:
        flattened = list(flatten(results))
    # todo made easier to read loop. old one is in 'OLD SHIT'. once confirmed. delete this line.
    for j in range(len(flattened)):
        for i in range(j + 1, (len(flattened))):
            match = True
            for k in range(1, (len(flattened[0]))):
                if flattened[j][k] != flattened[i][k]:
                    match = False
                    break
            if match:
                overlap.append(flattened[j])
    return overlap


def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes, tuple)):
            yield from flatten(el)
        else:
            yield el


output = []



def reemovNestings(l):
    for i in l:
        if type(i) == list:
            reemovNestings(i)
        else:
            output.append(i)


def get_output():
    return output


def reset_output():
    global output
    output = []


def remove_single_tuple_within_list(array):
    if isinstance(array[0], tuple):
        return list(array[0])
    else:
        return array