def find(results):
    overlap = []
    print(f"this is results:   {results}")
    for entry in results:
        print(entry)
        print(results.count(entry))
        if results.count(entry) > 1:
            overlap.append(results)
    print(f"this is the list of overlap:         {overlap}")
    return overlap
