import requests as rq
from bs4 import BeautifulSoup

def get_html_chapter_list(url: str) -> list:
    """Search in the html the menu with the chapter urls"""
    response = rq.get(url)
    html = response.text
    options = set(BeautifulSoup(html, "lxml").find_all("option", attrs={"class": "short"}))
    temp = []
    for option in options:
        temp.append(option["data-redirect"])
    return temp