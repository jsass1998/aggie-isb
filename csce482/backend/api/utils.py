def get_semester_string_from_term_code(term_code):
    """
    Takes a string in the format "YYYYS(L)" as a term code representing the year (Y),
    semester (S) and, optionally, the location (L). S and L will be numbers where

    for S:
    1 - Spring
    2 - Summer
    3 - Fall

    and for L:
    1 - College Station
    2 - Galveston
    3 - Qatar
    4 - Half year term (may not be used)

    SSSS will represent the full numerical year, such as 2020.

    A valid example term code parameter would look something like '202011'
    for Spring semester 2020 College Station.
    """
    semester_code_dict = {'1': 'SPRING', '2': 'SUMMER', '3': 'FALL'}
    semester_string = ''
    if len(term_code) >= 5:
        semester_string += semester_code_dict[term_code[4]] + ' ' + term_code[0:4]
    else:
        raise Exception('Invalid term code provided - must be 5 or more characters long'
                        ' and match the format "YYYYS(L)". Got "{0}" instead'.format(term_code))
    return semester_string


def get_term_code_from_semester_string(semester_string, campus=None):
    """
    Performs the inverse of get_semester_string_from_term_code. Given a semester string such as
    'FALL 2020' and returns 20203. Can also return a term code including location
    information if given a semester and campus string, where the campus string is the name
     of the campus as it appears in the term_location table, i.e. 'Qatar' or 'College Station'
    """
    location_dict = {'College Station': '1', 'Galveston': '2', 'Qatar': '3'}  # Note: lacking support for half terms
    semester_dict = {'SPRING': '1', 'SUMMER': '2', 'FALL': '3'}
    term_code = ''
    term_code += semester_string.split()[1] + semester_dict[semester_string.split()[0]]
    if campus is not None:
        term_code += location_dict[campus]
    return term_code
