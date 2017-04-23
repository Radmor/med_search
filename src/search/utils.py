import urllib
from collections import defaultdict
from itertools import chain

def merge_dicts(dict1, dict2):
    dict3 = defaultdict(list)
    for k, v in chain(dict1.items(), dict2.items()):
        for value in v:
            dict3[k].append(value)
    return dict3


def parse_query(query):
    return query.split()


def parse_query_string(parsed_query, queried_fields):
    query_string_dict = {}
    for queried_field in queried_fields:
        for query_item in parsed_query:
            query_string_dict = merge_dicts(query_string_dict,
                                            {queried_field:[query_item]})
    return urllib.parse.urlencode(query_string_dict, True)


def combine_redirect_url(redirect_url, query, queried_fields):
    parsed_query = parse_query(query)
    query_string = parse_query_string(parsed_query, queried_fields)
    redirect_parsed_url = urllib.parse.urlparse(redirect_url)
    redirect_parsed_url = redirect_parsed_url._replace(query=query_string)
    return urllib.parse.urlunparse(redirect_parsed_url)