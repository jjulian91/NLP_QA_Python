import random
import collections
import do_magic.voila as voila


def triangulate(results):
    # number_of_arrays = len(results)
    # length_of_each = []
    # for i in range(number_of_arrays):
    #     length_of_each.append(len(results[i]))
    #
    #
    flattened = []
    overlap = []
    if len(results) > 0:
        flattened = list(flatten(results))
    j = 0

    #todo loop over flattened and check each record for a match of ALL entries in the "tuple"  add those matches to
    # to the overlap function. This should solve 90% of problems going forward.
    while j < len(flattened):
        i = j+1
        while i < len(flattened):
            k = 1
            match = True
            while k <(len(flattened[0])):
                if flattened[i][k] == flattened[j][k]:
                    k += 1
                else:
                    match = False
                    break

            if match:
                overlap.append(flattened[j])
            i += 1
        j += 1

    return overlap


def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes, tuple)):
            yield from flatten(el)
        else:
            yield el


