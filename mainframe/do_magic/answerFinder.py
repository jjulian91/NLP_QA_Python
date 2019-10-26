def find(results):
    # only 1 hit in DB
    if len(results) == 1:
        return results
    overlap = []
    flattened = flatten(results)
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
