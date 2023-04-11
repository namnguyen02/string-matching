import math
from sequencedbase_algorithms import jaro_Winkler

#documents
doc1 = "I'l buy you anything buy you any drink"
doc2 = "I buy you any thing drink"
#query string
query = "life learning"

def compute_tf(str_spl1, str_spl2):
    docs_tf = []

    tf_dict = dict.fromkeys(set(str_spl1), 0)
    for tok in str_spl1:
        tf_dict[tok] += 1
    docs_tf.append(tf_dict)

    tf_dict = dict.fromkeys(set(str_spl2), 0)
    for tok in str_spl2:
        tf_dict[tok] += 1
    docs_tf.append(tf_dict)

    return docs_tf

def inverse_document_frequency(term, s1_spl, s2_spl):
    num_with_term = 0

    if term in s1_spl:
        num_with_term += 1
    if term in s2_spl:
        num_with_term += 1

    return 2 / num_with_term
    
def compute_idf(s1_spl, s2_spl):
    idf_dict = {}

    for word in s1_spl:
        if idf_dict.get(word) is None:
            idf_dict[word] = inverse_document_frequency(word, s1_spl, s2_spl)
    for word in s2_spl:
        if idf_dict.get(word) is None:
            idf_dict[word] = inverse_document_frequency(word, s1_spl, s2_spl)

    return idf_dict

def cosine_sim(docs_tfidf):
    sum_sqr1 = 0.0
    sum_sqr2 = 0.0
    prod = 0.0

    # print(docs_tfidf)

    for k in docs_tfidf[0].keys():
        # print(k)
        sum_sqr1 += docs_tfidf[0][k]*docs_tfidf[0][k]
        sum_sqr2 += docs_tfidf[1][k]*docs_tfidf[1][k]
        prod += docs_tfidf[0][k]*docs_tfidf[1][k]

    return prod/( math.sqrt(sum_sqr1)*math.sqrt(sum_sqr2) )

def tfidf(str1, str2, soft_thresh, sim_func):
    s1_spl = str1.split(' ')
    s2_spl = str2.split(' ')

    # if(len(s1_spl) == 1 && len(s2_spl) == 1 && str1 != str2)
    #     return 0.0

    curr_docs_info = compute_tf(s1_spl, s2_spl) #multiple by idf later
    docs_idf = compute_idf(s1_spl, s2_spl)

    docs_idf_key_set = docs_idf.keys()

    close_word_s1 = {}
    if soft_thresh is not None and sim_func is not None:
        close_word_s1 = find_close(curr_docs_info, soft_thresh, sim_func)
    # print(close_word_s1)

    # print(docs_idf_key_set)
    # print(docs_idf)

    for i in range(2):
        for k in docs_idf_key_set:
            if curr_docs_info[i].get(k) is None:
                curr_docs_info[i][k] = 0.0
            else:
                weight = 1.0 if close_word_s1.get(k) is None else close_word_s1[k]
                curr_docs_info[i][k] = math.log(curr_docs_info[i][k]+1.0) * docs_idf[k] * weight #dampened

    # print(curr_docs_info)

    return cosine_sim(curr_docs_info)

def find_close(curr_docs_spl, threshold, sim_measure):
    close_word_s1 = {}
    s1_keyset = curr_docs_spl[0].keys()
    s2_keyset = curr_docs_spl[1].keys()

    for word1 in s1_keyset:
        for word2 in s2_keyset:
            similarity = sim_measure(word1,word2)
            if similarity < threshold:
                continue
            if close_word_s1.get(word1) is None or similarity > close_word_s1[word1]:
                close_word_s1[word1] = similarity

    return close_word_s1
                

print(tfidf(doc1, doc2, 0.75, jaro_Winkler))
