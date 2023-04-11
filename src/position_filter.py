def position_filter(query, strings):
    query_len = len(query)
    result = []

    for string in strings:
        string_len = len(string)
        if query_len > string_len:
            continue
        i = 0
        while i <= string_len - query_len:
            j = 0
            while j < query_len and query[j] == string[i+j]:
                j += 1
            if j == query_len:
                result.append(string)
                break
            if j == 0:
                i += 1
            else:
                i += j

    return result


'''
strings_to_search = [
    "apple",
    "banana",
    "orange",
    "pear",
    "grape",
    "watermelon",
    "pineapple",
    "kiwi",
    "mango",
    "papaya"
]

print(position_filtering("ear", strings_to_search))
'''
