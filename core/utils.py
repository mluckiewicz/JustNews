import re
from functools import wraps
import time


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        #print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        print(f'Function {func.__name__} took {total_time:.4f} seconds')
        return result
    return timeit_wrapper


def get_encodings_from_content(content):
    """
    Code from:
    https://github.com/sigmavirus24/requests-toolbelt/blob/master/requests_toolbelt/utils/deprecated.py
    Return encodings from given content string.
    :param content: string to extract encodings from.
    """

    if isinstance(content, bytes):
        find_charset = re.compile(
            rb'<meta.*?charset=["\']*[^a-zA-z0-9]*([a-zA-Z0-9\-_]+?)[^a-zA-z0-9]* *?["\'>]',
            flags=re.I,
        ).findall

        find_xml = re.compile(
            rb'^<\?xml.*?encoding=["\']*([a-zA-Z0-9\-_]+?) *?["\'>]'
        ).findall
        return [
            encoding.decode("utf-8")
            for encoding in find_charset(content) + find_xml(content)
        ]
    else:
        find_charset = re.compile(
            r'<meta.*?charset=["\']*[^a-zA-z0-9]*([a-zA-Z0-9\-_]+?)[^a-zA-z0-9]* *?["\'>]',
            flags=re.I,
        ).findall

        find_xml = re.compile(
            r'^<\?xml.*?encoding=["\']*([a-zA-Z0-9\-_]+?) *?["\'>]'
        ).findall
        return find_charset(content) + find_xml(content)


def compare_lists(refer_list: list, compared_list: list) -> list:
    """ The function compares two lists and returns elements that do not exist 
    in the compared list

    Args:
        refer_list (list): list we refer to in comparison
        compared_list (list): list which is compared with the list we refer to

    Returns:
        list: list of elements not present in the compared list
    """
    if len(refer_list) == len(compared_list):
        compare = []
    else:
        compare = [item for item in refer_list if item not in compared_list]
    return compare