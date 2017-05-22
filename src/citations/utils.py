import math

COMPARISON_METHODS = {'cos': 'cosine_similarity'}


def length_of_vector(list_of_values):
    return math.sqrt(sum([x*x for x in list_of_values]))


def cosine_similarity(terms_in_query, terms_in_result):
    print(terms_in_query, terms_in_result)
    scalar_product = sum([terms_in_result[term] * terms_in_query[term] for term in terms_in_result.keys()])
    product_of_the_lengths_of_vectors = length_of_vector(terms_in_query.values()) * length_of_vector(terms_in_result.values())
    return (scalar_product / product_of_the_lengths_of_vectors) if product_of_the_lengths_of_vectors != 0 else 0


def measure_similarity(documents, query, result, content_describing_method, comparison_method):
    """

    :param documents: all the documents
    :param query: search query
    :param result: one particular document to be compared with query
    :param content_describing_method: name of method used to describe content of document
    :param comparison_method: name of method to use to compare document and query
    :return: number [0:1] indicating how similar query and document are
    """
    possibles = globals().copy()
    possibles.update(locals())
    describe = possibles.get(content_describing_method)
    terms_in_query, terms_in_result = describe(documents, query, result)
    comparing = possibles.get(comparison_method)
    return comparing(terms_in_query, terms_in_result)


def tf(documents, query, result):
    terms_in_query = {}
    terms_in_result = {}
    result_as_a_list = result['title'].split()
    for term in query:
        terms_in_query[term] = terms_in_query.get(term, 0) + 1
    for term in terms_in_query.keys():
        terms_in_query[term] /= len(query)
        terms_in_result[term] = terms_in_result.get(term, 0)
        for word in result_as_a_list:
            if term == word:
                terms_in_result[word] += 1
    for word in terms_in_result.keys():
        terms_in_result[word] /= len(result_as_a_list)
    return terms_in_query, terms_in_result


def idf(documents, word):
    return math.log(len(documents)/sum([1 for w in documents if word in w]))


def tfidf(documents, query, result):
    pass


if __name__ == '__main__':
    print(measure_similarity([], ['cancer', 'symptom'], {"title": "cancer lol lol lol lol lol symptom"}, "tf", COMPARISON_METHODS['cos']))
    # print(([], ['cancer', 'symptom'], {"title": "cancer lol lol lol lol lol"}, "cos"))
    # print(([], ["cancer", "cancer", "boom", "trick"], {"title": "cancer boom lol cool boom thing"}, "cos"))
