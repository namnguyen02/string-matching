# from jaro_winkler import jaro_winkler # using secondary similarity string

# referenced function for testing
# def jaro(string1, string2):
#     # input validations

#     len_s1 = len(string1)
#     len_s2 = len(string2)

#     max_len = max(len_s1, len_s2)
#     search_range = (max_len // 2) - 1
#     if search_range < 0:
#         search_range = 0

#     flags_s1 = [False] * len_s1
#     flags_s2 = [False] * len_s2

#     common_chars = 0
#     for i, ch_s1 in enumerate(string1):
#         low = i - search_range if i > search_range else 0
#         hi = i + search_range if i + search_range < len_s2 else len_s2 - 1
#         for j in range(low, hi + 1):
#             if not flags_s2[j] and string2[j] == ch_s1:
#                 flags_s1[i] = flags_s2[j] = True
#                 common_chars += 1
#                 break
#     if not common_chars:
#         return 0
#     k = trans_count = 0
#     for i, f_s1 in enumerate(flags_s1):
#         if f_s1:
#             for j in range(k, len_s2):
#                 if flags_s2[j]:
#                     k = j + 1
#                     break
#             if string1[i] != string2[j]:
#                 trans_count += 1
#     trans_count /= 2
#     common_chars = float(common_chars)
#     weight = ((common_chars / len_s1 + common_chars / len_s2 +
#                (common_chars - trans_count) / common_chars)) / 3
#     return weight
# def jaro_winkler(string1, string2, prefix_weight=0.1):
#     # input validations
#     # if one of the strings is empty return 0
#     jw_score = jaro(string1, string2)
#     min_len = min(len(string1), len(string2))
#     # prefix length can be at max 4
#     j = min(min_len, 4)
#     i = 0
#     while i < j and string1[i] == string2[i] and string1[i]:
#         i += 1
#     if i:
#         jw_score += i * prefix_weight * (1 - jw_score)
#     return jw_score

def monge_elkan(str1, str2, sim_func):
    # just for internal use so no need input validations
    # if exact match return 1.0
    if str1 == str2:
        return 1.0
    # if one of the strings is empty return 0
    if len(str1) == 0 and len(str2) == 0:
        return 0

    bag1 = str1.split(' ')
    bag2 = str2.split(' ')

    # with elements in bag2
    sum_of_maxes = 0.0
    for t1 in bag1:
        max_sim = -9999.0
        for t2 in bag2:
            max_sim = max(max_sim, sim_func(t1, t2))
        sum_of_maxes += max_sim

    return sum_of_maxes / float(len(bag1))

print(monge_elkan('Niall', 'Neal',jaro_winkler)) # 0.8049999999999999
print(monge_elkan('Comput. Sci. and Eng. Dept., University of California San Diego', 'Department of Computer Science, Univ. Calif. San Diego',jaro_winkler)) # 0.8677218614718616
