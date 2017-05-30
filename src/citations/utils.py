import math
import nltk
from nltk.corpus import stopwords

DESCRIBING_METHODS = {'tf': 'term_frequency', 'tfidf': 'term_frequency_inverse_document_frequency'}
COMPARISON_METHODS = {'cos': 'cosine_similarity', 'euc': 'euclidean_distance_similarity', 'jac': 'jaccard_similarity'}


def length_of_vector(list_of_values):
    return math.sqrt(sum([x*x for x in list_of_values]))


def cosine_similarity(terms_in_query, terms_in_result):
    scalar_product = sum([terms_in_result[term] * terms_in_query[term] for term in terms_in_result.keys()])
    product_of_the_lengths_of_vectors = length_of_vector(terms_in_query.values()) * length_of_vector(terms_in_result.values())
    return (scalar_product / product_of_the_lengths_of_vectors) if product_of_the_lengths_of_vectors != 0 else 0


def euclidean_distance_similarity(terms_in_query, terms_in_result):
    """
    sqrt from sum of squares of differences of coordinates
    """
    return math.sqrt(sum([(terms_in_result[term] - terms_in_query[term])**2 for term in terms_in_result.keys()]))


def jaccard_similarity(terms_in_query, terms_in_result):
    words_in_both_query_and_result = 0
    for term in terms_in_result.keys():
        if terms_in_result[term] > 0 and terms_in_query[term] > 0:
            words_in_both_query_and_result += 1
    return words_in_both_query_and_result*1.0/len(terms_in_query.keys())


def measure_similarity(documents, query, result, content_describing_method, comparison_method):
    """

    :param documents: all the documents
    :param query: search query
    :param result: one particular document to be compared with query
    :param content_describing_method: name of method used to describe content of document
    :param comparison_method: name of method to use to compare document and query
    :return: number [0:1] indicating how similar query and document are
    """
    result_as_a_list = parse_query(result['title'])
    possibles = globals().copy()
    possibles.update(locals())
    describe = possibles.get(content_describing_method)
    terms_in_query, terms_in_result = describe(documents, query, result_as_a_list)
    comparing = possibles.get(comparison_method)
    return comparing(terms_in_query, terms_in_result)


def term_frequency(documents, query, result_as_a_list):
    terms_in_query = {}
    terms_in_result = {}
    for term in query + result_as_a_list:
        terms_in_query[term] = terms_in_query.get(term, 0)
        terms_in_result[term] = terms_in_result.get(term, 0)
    for term in query:
        terms_in_query[term] += 1
    for term in terms_in_query.keys():
        terms_in_query[term] /= len(query)
    for word in result_as_a_list:
        terms_in_result[word] += 1
    for word in terms_in_result.keys():
        terms_in_result[word] /= len(result_as_a_list)
    return terms_in_query, terms_in_result


def inverse_document_frequency(documents, word):
    sum_of_occurrences = sum([1 for w in documents if word in w])
    if sum_of_occurrences != 0:
        return math.log((len(documents) + 1)/sum_of_occurrences)
    return 0


def term_frequency_inverse_document_frequency(documents, query, result):
    terms_in_query, terms_in_result = term_frequency(documents, query, result)
    terms_in_query = {word: tf * inverse_document_frequency(documents, word) for word, tf in terms_in_query.items()}
    terms_in_result = {word: tf * inverse_document_frequency(documents, word) for word, tf in terms_in_result.items()}
    return terms_in_query, terms_in_result


def parse_query(query):
    tokenized_query = nltk.word_tokenize(query)
    lower_case_tokenized_query = [w.lower() for w in tokenized_query]
    tokenized_query_without_stopwords = [w for w in lower_case_tokenized_query if w not in stopwords.words('english')]
    stemmer = nltk.stem.PorterStemmer()
    stemmed_query = [stemmer.stem(word) for word in tokenized_query_without_stopwords]
    return stemmed_query


if __name__ == '__main__':
    print(term_frequency([], ['aa', 'ab', 'ac', 'aa', 'ad'],['aa', 'ba', 'bb', 'ac']))
    print(jaccard_similarity({'aa': 0.4, 'ab': 0.2, 'ad': 0.2, 'ba': 0.0, 'bb': 0.0, 'ac': 0.2}, {'aa': 0.25, 'ab': 0.0, 'ad': 0.0, 'ba': 0.25, 'bb': 0.25, 'ac': 0.25}))
    # There is a working example of tfidf
    # print(term_frequency_inverse_document_frequency([['aa', 'ab', 'ac'], ['aa', 'ab', 'aa'], ['aa', 'ad', 'ab', 'ac', 'ad'], ['ab','ab','ab']], ['aa', 'ab', 'ac'], {'title': 'aa ad ab ac ad'}))
    # print(1/3*math.log(5/3), 1/3*math.log(5/4), 1/3*math.log(5/2))
    # print(0.2 * math.log(5 / 3), 0.2 * math.log(5 / 4), 0.2 * math.log(5 / 2))
    # print(measure_similarity([], ['cancer', 'symptom'], {"title": "cancer lol lol lol lol lol symptom"}, DESCRIBING_METHODS["tf"], COMPARISON_METHODS['cos']))
    # print(([], ['cancer', 'symptom'], {"title": "cancer lol lol lol lol lol"}, "cos"))
    # print(([], ["cancer", "cancer", "boom", "trick"], {"title": "cancer boom lol cool boom thing"}, "cos"))
    # print(euclidean_distance_similarity({'a': 0.0, 'b': 0.0}, {'a': 1.0, 'b': 1.0}))
