import urllib
from collections import defaultdict
from itertools import chain
import nltk
from nltk.corpus import stopwords

DESCRIBING_METHODS = {'tf': 'term_frequency', 'tfidf': 'term_frequency_inverse_document_frequency'}
COMPARISON_METHODS = {'cos': 'cosine_similarity', 'euc': 'euclidean_distance_similarity'}

def merge_dicts(dict1, dict2):
    dict3 = defaultdict(list)
    for k, v in chain(dict1.items(), dict2.items()):
        for value in v:
            dict3[k].append(value)
    return dict3


def parse_query(query):
    tokenized_query = nltk.word_tokenize(query)
    lower_case_tokenized_query = [w.lower() for w in tokenized_query]
    tokenized_query_without_stopwords = [w for w in lower_case_tokenized_query if w not in stopwords.words('english')]
    print(tokenized_query_without_stopwords)
    stemmer = nltk.stem.PorterStemmer()
    stemmed_query = [stemmer.stem(word) for word in tokenized_query_without_stopwords]
    print(stemmed_query)
    return stemmed_query


def parse_query_string(parsed_query, queried_fields):
    query_string_dict = {}
    for queried_field in queried_fields:
        for query_item in parsed_query:
            query_string_dict = merge_dicts(query_string_dict,
                                            {queried_field:[query_item]})
    return urllib.parse.urlencode(query_string_dict, True)


def join_with_next_parameter(query_string, field_name, field_value):
    """
    This method joins previous query_string with new parameter.
    :param query_string: previously prepared query_string
    :param field_name: name of the parameter
    :param field_value: value of the parameter to be added to url
    :return: 
    """
    return query_string + "&" + field_name + "=" + field_value


def combine_redirect_url(redirect_url, query, filtering_method, comparison_method, queried_fields):
    parsed_query = parse_query(query)
    query_string = parse_query_string(parsed_query, queried_fields)
    query_string = join_with_next_parameter(query_string, "filtering_method", filtering_method)
    query_string = join_with_next_parameter(query_string, "comparison_method", comparison_method)
    redirect_parsed_url = urllib.parse.urlparse(redirect_url)
    redirect_parsed_url = redirect_parsed_url._replace(query=query_string)
    return urllib.parse.urlunparse(redirect_parsed_url)