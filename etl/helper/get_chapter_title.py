from bs4 import BeautifulSoup

def get_chapter_title(html: str):
    title = BeautifulSoup(html, "lxml").find("li", attrs={"class":"active"}).text
    title = str(title).rstrip().lstrip().replace("\\", " ").replace("/", " ").replace("?", "")
    return title