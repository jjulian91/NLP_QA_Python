import random
import sys


def triangulate(results):
    overlap = []
    flattened = flatten(results)
    random.seed(a=None, version=2)
    # only 1 row-hit in DB
    if len(flattened) == 1:
        return flattened
#    for i in range(len(flattened) - 1):
#        for j in range(i + 1, len(flattened)):
#            if verify_all(flattened[i], flattened[j]):
#                return flattened[i]

    #print(len(flattened))
    j = 0
    while j < len(flattened):
        check2 = random.randint(0, len(flattened[0])-1)
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


def verify_all(arg1, arg2):
    count = 0
    for i in range(len(arg1)):
        if arg1[i] == arg2[i]:
            count += 1
    return True if count == len(arg1) else False
