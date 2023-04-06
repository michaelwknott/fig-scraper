import time
from requests_html import HTMLSession


URL = "https://live.gymnastics.sport/live/17242/mensqual.php?app=fx"


def requests_html_test(url):
    session = HTMLSession()
    response = session.get(url)
    response.html.render()
    return response.html


if __name__ == "__main__":
    
    for i in range(1, 11):
        start_time = time.perf_counter()
        requests_html_test(URL)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"Request-html: Loop {i} execution time = {execution_time}")
