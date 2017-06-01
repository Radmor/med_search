import math
import nltk
from nltk.corpus import stopwords

# from search.utils import DESCRIBING_METHODS, COMPARISON_METHODS
DESCRIBING_METHODS = {'tf': 'term_frequency', 'tfidf': 'term_frequency_inverse_document_frequency'}
COMPARISON_METHODS = {'cos': 'cosine_similarity', 'euc': 'euclidean_distance_similarity', 'jac': 'jaccard_similarity'}


def length_of_vector(terms_and_values, terms_weights):
    if len(terms_weights.values()) == 0:
        return math.sqrt(sum([x*x for x in terms_and_values.items()]))
    return math.sqrt(sum([min(1, x*x/terms_weights[term]) for term, x in terms_and_values.items()]))


def cosine_similarity(terms_in_query, terms_in_result, terms_weights):
    scalar_product = sum([terms_in_result[term] * terms_in_query[term] for term in terms_in_result.keys()])
    product_of_the_lengths_of_vectors = length_of_vector(terms_in_query, terms_weights) * length_of_vector(terms_in_result, terms_weights)
    return (scalar_product / product_of_the_lengths_of_vectors) if product_of_the_lengths_of_vectors != 0 else 0


def euclidean_distance_similarity(terms_in_query, terms_in_result, terms_weights):
    """
    sqrt from sum of squares of differences of coordinates
    """
    if len(terms_weights.values()) == 0:
        return math.sqrt(sum([(terms_in_result[term] - terms_in_query[term])**2 for term in terms_in_result.keys()]))
    return math.sqrt(sum([min(1, ((terms_in_result[term] - terms_in_query[term])**2/terms_weights[term])) for term in terms_in_result.keys()]))


def jaccard_similarity(terms_in_query, terms_in_result, terms_weights):
    if len(terms_weights.values()) == 0:
        sum_of_appearances_of_terms = len(terms_in_query.keys())
    else:
        sum_of_appearances_of_terms = sum(terms_weights.values())
    words_in_both_query_and_result = 0
    for term in terms_in_result.keys():
        if terms_in_result[term] > 0 and terms_in_query[term] > 0:
            if term not in terms_weights.keys():
                words_in_both_query_and_result += 1
            else:
                words_in_both_query_and_result += terms_weights[term]
    return words_in_both_query_and_result * 1.0 / sum_of_appearances_of_terms


def update_weights(weights_of_terms, terms):
    for term in terms:
        if term not in weights_of_terms.keys():
            weights_of_terms[term] = 1
    return weights_of_terms


def measure_similarity(documents, query, result, content_describing_method, comparison_method, weights_of_terms):
    """
    :param documents: all the documents
    :param query: search query
    :param result: one particular document to be compared with query
    :param content_describing_method: name of method used to describe content of document
    :param comparison_method: name of method to use to compare document and query
    :param weights_of_terms: dictionary with terms and their weights, provided by the user
    :return: number [0:1] indicating how similar query and document are
    """
    updated_weights = {}
    result_as_a_list = parse_query(result['title'])
    possibles = globals().copy()
    possibles.update(locals())
    describe = possibles.get(content_describing_method)
    terms_in_query, terms_in_result = describe(documents, query, result_as_a_list)
    if len(weights_of_terms.keys()) != 0:
        updated_weights = update_weights(weights_of_terms, terms_in_query.keys())
    comparing = possibles.get(comparison_method)
    return comparing(terms_in_query, terms_in_result, updated_weights)


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


def create_matrix_from_ranking(reference_ranking):
    matrix = list()
    for i in range(len(reference_ranking)):
        matrix.append([0]*len(reference_ranking))
    # print(matrix)
    for index, element in enumerate(reference_ranking):
        for elem in reference_ranking[index:]:
            if elem != element:
                matrix[element][elem] = 1
    return matrix


def kendall_distance(reference_matrix, actual_matrix):
    return 0.5 * sum([abs(reference_matrix[i][j] - actual_matrix[i][j]) for i in range(len(reference_matrix)) for j in range(len(reference_matrix))])


def compute_kendall_tau(reference_ranking, actual_ranking):
    """
    Compute Kendall's tau between two ranking. These rankings must consist of number from 0 to x, like [0,2,1,4,3]
    :param reference_ranking: ranking of documents, which we wanted to acquire
    :param actual_ranking: the ranking returned by filtering [5, 2, 4, 1, 3] - IDs in list
    """
    reference_matrix = create_matrix_from_ranking(reference_ranking)
    actual_matrix = create_matrix_from_ranking(actual_ranking)
    distance_between_matrices = kendall_distance(reference_matrix, actual_matrix)
    print(distance_between_matrices)
    return 1 - 4*(distance_between_matrices/(len(reference_matrix)*(len(reference_matrix)-1)))


def rocchios_method(alpha, beta, gamma, query_as_a_vector, list_of_relevant_documents_vectors, list_of_unrelevant_documents_vectors):
    """
    Compute new query vector, given query, some relevant documents (dicts returned from tfidf or tf functions) and unrelevant documents.
    We multiply every value by specific parameter (alpha, beta or gamma)
    :param alpha: query parameter
    :param beta: relevant documents parameter
    :param gamma: unrelevant documents parameter
    :param query_as_a_vector: dict {term1: value1, term2: value2, ...}
    :param list_of_relevant_documents_vectors: list of dicts
    :param list_of_unrelevant_documents_vectors: list of dicts
    :return: 
    """
    query_as_a_vector_times_alpha = {term: value * alpha for term, value in query_as_a_vector.items()}
    relevant_documents_times_beta = {}
    unrelevant_documents_times_gamma = {}
    for vector in list_of_relevant_documents_vectors:
        for term, value in vector.items():
            relevant_documents_times_beta[term] = relevant_documents_times_beta.get(term, 0) + beta * value
            print(relevant_documents_times_beta[term], term)
    print(relevant_documents_times_beta)
    if len(list_of_unrelevant_documents_vectors) > 0:
        for vector in list_of_unrelevant_documents_vectors:
            for term, value in vector.items():
                unrelevant_documents_times_gamma[term] = unrelevant_documents_times_gamma.get(term, 0) + gamma * value
    new_query_vector = {}
    if len(list_of_unrelevant_documents_vectors) > 0:
        for index in query_as_a_vector.keys():
            new_query_vector[index] = query_as_a_vector_times_alpha[index] + relevant_documents_times_beta[index] + unrelevant_documents_times_gamma[index]
    else:
        for index in query_as_a_vector.keys():
            new_query_vector[index] = query_as_a_vector_times_alpha[index] + relevant_documents_times_beta[index]
    return new_query_vector


if __name__ == '__main__':
    # print(term_frequency([], ['aa', 'ab', 'ac', 'aa', 'ad'],['aa', 'ba', 'bb', 'ac']))
    # print(jaccard_similarity({'aa': 0.4, 'ab': 0.2, 'ad': 0.2, 'ba': 0.0, 'bb': 0.0, 'ac': 0.2}, {'aa': 0.25, 'ab': 0.0, 'ad': 0.0, 'ba': 0.25, 'bb': 0.25, 'ac': 0.25}))
    print(compute_kendall_tau([2, 1, 0], [0, 1, 2]))
    # There is a working example of tfidf
    # print(term_frequency_inverse_document_frequency([['aa', 'ab', 'ac'], ['aa', 'ab', 'aa'], ['aa', 'ad', 'ab', 'ac', 'ad'], ['ab','ab','ab']], ['aa', 'ab', 'ac'], {'title': 'aa ad ab ac ad'}))
    # print(1/3*math.log(5/3), 1/3*math.log(5/4), 1/3*math.log(5/2))
    # print(0.2 * math.log(5 / 3), 0.2 * math.log(5 / 4), 0.2 * math.log(5 / 2))
    # print(measure_similarity([], ['cancer', 'symptom'], {"title": "cancer lol lol lol lol lol symptom"}, DESCRIBING_METHODS["tf"], COMPARISON_METHODS['cos']))
    # print(([], ['cancer', 'symptom'], {"title": "cancer lol lol lol lol lol"}, "cos"))
    # print(([], ["cancer", "cancer", "boom", "trick"], {"title": "cancer boom lol cool boom thing"}, "cos"))
    # print(euclidean_distance_similarity({'a': 0.0, 'b': 0.0}, {'a': 1.0, 'b': 1.0}))
    print(rocchios_method(1, 0.5, 0, {'a': 0, 'b': 0, 'c': 0, 'd': 0.932, 'e': 0.363},
                          [{'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0},
                          {'a': 0, 'b': 0, 'c': 0.559, 'd': 0, 'e': 0},
                          {'a': 0.89, 'b': 0, 'c': 0, 'd': 0, 'e': 0}],
                          []))
