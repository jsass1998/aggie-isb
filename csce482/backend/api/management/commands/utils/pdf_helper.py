""" Helper functions for the pdf parser """

LEN_HEADER_ROW = 38
LEN_OLD_HEADER_ROW = 37
LEN_SECTION_ROW = 20
LEN_COURSE_TOTAL_ROW = LEN_COLLEGE_TOTAL_ROW = LEN_DEPT_TOTAL_ROW = 19

def get_pdf_skip_count(row_text: str) -> (bool, int):
    """ Gets how many rows we should skip

        Args:
            The current row text for the pdf

        Returns:
            bool: whether this is an old header row or not
            int: how much the row index should increment, or -1 if this is a grades row
    """

    old_row_style = False
    count = -1

    if _is_old_header_row(row_text):
        old_row_style = True
        count = LEN_OLD_HEADER_ROW
    elif _is_header_row(row_text):
        count = LEN_HEADER_ROW
    elif _is_course_total_row(row_text):
        count = LEN_COURSE_TOTAL_ROW
    elif _is_dept_total_row(row_text):
        count = LEN_DEPT_TOTAL_ROW
    elif _is_college_total_row(row_text):
        count = LEN_COLLEGE_TOTAL_ROW

    return (old_row_style, count)

def _is_old_header_row(row_text: str) -> bool:
    """ Used to identify whether a row is a header row or not in PDFs
        before 2016 Fall.

        This is needed so we can parse pre-2016 Fall grade reports in a different way.
    """

    return row_text == "COLLEGE:"

def _is_header_row(row_text: str) -> bool:
    """ Used to identify whether a row is a header row or not in PDFs
        from or after 2016 Fall.
    """

    return row_text == "SECTION"

def _is_course_total_row(row_text: str) -> bool:
    """ Used to identify whether a row is a course total row or not. """

    return row_text == "COURSE TOTAL:"

def _is_dept_total_row(string: str) -> bool:
    """ Used to identify whether a row is a department total row or not. """

    return string == "DEPARTMENT TOTAL:"

def _is_college_total_row(string: str) -> bool:
    """ Used to identify whether a row is a college total row or not. """

    return string == "COLLEGE TOTAL:"
