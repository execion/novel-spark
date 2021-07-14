import requests as rq
from bs4 import BeautifulSoup

def get_html_root(url: str):
    """Get the html in the url"""
    res = rq.get(url)
    if (not res.text):
        raise ValueError("Not valid url")
    data = res.text
    header = BeautifulSoup(data, "lxml").find("h3")
    title = header.text.replace("NEW", "").replace("HOT", "").replace(":", " ").rstrip().lstrip()
    chapters_list_url = BeautifulSoup(data, "lxml").find("li", attrs={"class": "wp-manga-chapter"}).a["href"]
    return title, chapters_list_url