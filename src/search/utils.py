import urllib
from collections import defaultdict
from itertools import chain
import nltk
from nltk.corpus import stopwords



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


def download_needed_packages_from_nltk():
    pass
    # nltk.download('punkt')
    # nltk.download('stopwords')


def combine_redirect_url(redirect_url, query, queried_fields):
    download_needed_packages_from_nltk()
    parsed_query = parse_query(query)
    query_string = parse_query_string(parsed_query, queried_fields)
    redirect_parsed_url = urllib.parse.urlparse(redirect_url)
    redirect_parsed_url = redirect_parsed_url._replace(query=query_string)
    return urllib.parse.urlunparse(redirect_parsed_url)