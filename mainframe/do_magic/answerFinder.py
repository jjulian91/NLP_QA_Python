import sys


def find(results):
    overlap = []
    flattened = flatten(results)
    # only 1 row-hit in DB
    if len(flattened) == 1:
        return results
    for i in range(len(flattened) - 1):
        for j in range(i + 1, len(flattened)):
            if verify_all(flattened[i], flattened[j]):
                return flattened[i]

    #print(len(flattened))
    j = 0
    while j < len(flattened):
        count = 0
        i = j
        while i < len(flattened):
            if flattened[i][0] == flattened[j][0]:
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


def verify_all(arg1, arg2):
    count = 0
    for i in range(len(arg1)):
        if arg1[i] == arg2[i]:
            count += 1
    return True if count == len(arg1) else False
