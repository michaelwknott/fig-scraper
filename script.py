import csv
import unicodedata
from requests_html import HTMLSession


URL = "https://live.gymnastics.sport/live/17242/mensqual.php?app=fx"

# CSS Selectors
RESULTS_ROWS_SELECTOR = ".hidden-xs.hidden-sm"

# The following selectors are relative to RESULTS_ROWS_SELECTOR above
RANK_SELECTOR = "div > div:nth-child(1) > div.col-md-8 > div"
NAME_SELECTOR = "div > div.col-md-4 > div.col-md-8 > a"
COUNTRY_CODE_SELECTOR = "div > div.col-md-4 > div.col-md-4 > nobr > small"
TOTAL_SELECTOR = "div > div:nth-child(3) > b"
EXECUTION_SELECTOR = "div > div:nth-child(4)"
DIFFICULTY_SELECTOR = "div > div:nth-child(5)"
PENALTY_SELECTOR = "div > div.col-md-2.smallheader > span"


def get_html(css_selector):
    """Get HTML from webpage.

    Args:
        css_selector (str): A css selector for the required HTML
        element.

    Returns:
        str: A unicode string of HTMl content.
    """

    session = HTMLSession()
    response = session.get(URL)
    # The 'render' method triggers Javascript content on the page
    response.html.render()
    print(f"{response.status_code} response from {response.url}")
    return response.html.find(css_selector)


def parse_text(row, selector):
    """Parse HTML elements.

    Args:
        row (requests_html.Element): A 'requests_html.Element' containing the
        HTML to parse.
        selector (str): The css selector for the required HTML element.

    Returns:
        str: The text from the selected HTML element or None if the
        element is not present.
    """

    try:
        return row.find(selector, first=True).text
        # Using 'first=True' to return a 'requests_html.Element' object rather than a
        # list. The text attribute can be retrieved from the object without having to
        # loop through a list.
    except AttributeError:
        return None


def normalise_string(string):
    """Remove Unicode non-breaking space character.

    Args:
        string (str): A string containing non-breaking space characters
        to be removed.

    Returns:
        str: A normalised string
    """

    if string is not None:
        return unicodedata.normalize("NFKD", string)
    return string


def create_csv(headers, results_list):
    """Creates a csv file.

    Args:
        headers (list[str]): A list of strings for the csv headers.
        results_list (list[tuple]): A list of tuples containing results
        data.
    """

    with open("results.csv", mode="a") as f:
        results_writer = csv.writer(f, delimiter=",")

        results_writer.writerow(headers)
        for result in results_list:
            results_writer.writerow(result)


def main():
    result_rows = get_html(RESULTS_ROWS_SELECTOR)

    # Element 1 of result_rows contains discipline and round. For example:
    # 'Mens Artistic Gymnastics - Floor Qualification'
    discipline_and_round = result_rows[0].text

    # Element 2 of result_rows contains the result headings:
    # ('Rk\nName\nTotal\nExecution\nDifficulty\nPenalty')
    headers = result_rows[1].text
    headers_list = headers.replace("\n", " ").split()

    results = []

    for row in result_rows[2:]:  # Miss out the discipline and headers
        rank = parse_text(row, RANK_SELECTOR)
        name = parse_text(row, NAME_SELECTOR)
        norm_name = normalise_string(name)
        country_code = parse_text(row, COUNTRY_CODE_SELECTOR)
        total = parse_text(row, TOTAL_SELECTOR)
        execution = parse_text(row, EXECUTION_SELECTOR)
        difficulty = parse_text(row, DIFFICULTY_SELECTOR)
        penalty = parse_text(row, PENALTY_SELECTOR)

        result = (
            discipline_and_round,
            rank,
            norm_name,
            country_code,
            total,
            execution,
            difficulty,
            penalty,
        )

        results.append(result)

    create_csv(headers_list, results)


if __name__ == "__main__":
    main()
