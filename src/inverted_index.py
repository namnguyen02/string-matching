def inverted_index(query, documents):
    index = {}

    for i, doc in enumerate(documents):
        words = doc.lower().split()
        for word in words:
            if word not in index:
                index[word] = []
            index[word].append(i)

    words = query.lower().split()
    result = set(index[words[0]])
    for word in words[1:]:
        result = result.intersection(set(index[word]))
    return [documents[i] for i in result]


'''
documents = [
    "This is the first document",
    "This is the second document",
    "And this is the third document",
    "Is this the first document? No, it is not.",
    "This is the fourth document"
]

result = inverted_index("first document", documents)
print(result)
'''
