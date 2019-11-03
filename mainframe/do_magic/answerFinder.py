import collections


def triangulate(results):
    overlap = []
    # todo made easier to read loop. old one is in 'OLD SHIT'. once confirmed. delete this line.
    for j in range(len(results)):
        for i in range(j + 1, (len(results))):
            if compareTuples(results[i], results[j]):
                overlap.append(results[j])

    return overlap



def compareTuples(tuple1, tuple2):
    i = 0
    while(i < len(tuple1)):
        if tuple1[i] == tuple2[i]:
            i += 1
        else:
            return False

    return True
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