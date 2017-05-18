import math
from functools import reduce
from operator import add


def length_of_vector(list_of_values):
    return math.sqrt(reduce(add, map(lambda x: x*x, list_of_values)))


def cosine_similarity(terms_in_query, terms_in_result):
    scalar_product = sum([terms_in_result[term] * terms_in_query[term] for term in terms_in_result.keys()])
    product_of_the_lengths_of_vectors = length_of_vector(terms_in_query.values()) * length_of_vector(terms_in_result.values())
    return scalar_product / product_of_the_lengths_of_vectors


def term_frequency(query, result):
    terms_in_query = {}
    terms_in_result = {}
    query_as_a_list = query.split()
    result_as_a_list = result.split()
    for term in query_as_a_list:
        terms_in_query[term] = terms_in_query.get(term, 0) + 1
    for term in terms_in_query.keys():
        terms_in_query[term] /= len(query_as_a_list)
        terms_in_result[term] = terms_in_result.get(term, 0)
        for word in result_as_a_list:
            if term == word:
                terms_in_result[word] += 1
    for word in terms_in_result.keys():
        terms_in_result[word] /= len(result_as_a_list)
    print(terms_in_query)
    print(terms_in_result)
    print(cosine_similarity(terms_in_query, terms_in_result))


def idf(word, query, result):
    return math.log(2/sum([1 for w in [query, result] if word in w]))


def tfidf(query, result):
    pass


if __name__ == '__main__':
    term_frequency("cancer cancer boom trick", "cancer boom lol cool boom thing")
