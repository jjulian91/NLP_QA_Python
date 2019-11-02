import random


def triangulate(results):
    # number_of_arrays = len(results)
    # length_of_each = []
    # for i in range(number_of_arrays):
    #     length_of_each.append(len(results[i]))
    #
    #


    overlap = []
    flattened = flatten(results)
    random.seed(a=None, version=2)
    # only 1 row-hit in DB
    if len(flattened) == 1:
        return flattened
    j = 0
    while j < len(flattened):
        check2 = random.randint(0, len(flattened[0]) - 1)
        count = 0
        i = j
        while i < len(flattened):
            if flattened[i][0] == flattened[j][0] and flattened[1][check2] == flattened[j][check2]:
                count += 1
            i += 1
        if count > 1:
            overlap.append(flattened[j])
        j += 1
    for i, over in enumerate(overlap):
        print(f'this is the list of overlap at position {i} : {over}')

    return overlap


def flatten(results):
    flattened = []
    for entry in results:
        for record in entry:
            flattened.append(record)
    return flattened
