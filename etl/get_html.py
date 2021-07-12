from asyncio import run
from itertools import product
import requests as rq
from bs4 import BeautifulSoup
import requests_async as requests
from requests.exceptions import Timeout, ConnectionError
import sqlite3
import spacy

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

def get_html_chapter_list(url: str) -> list:
    """Search in the html the menu with the chapter urls"""
    response = rq.get(url)
    html = response.text
    options = set(BeautifulSoup(html, "lxml").find_all("option", attrs={"class": "short"}))
    temp = []
    for option in options:
        temp.append(option["data-redirect"])
    return temp

async def get_chapter_html(url: str) -> str:
    try:
        response = await requests.get(url)
        html = response.text
        return html
    except(Timeout, ConnectionError):
        await get_chapter_html(url)

def get_chapter_title(html: str):
    title = BeautifulSoup(html, "lxml").find("li", attrs={"class":"active"}).text
    title = str(title).rstrip().lstrip().replace("\\", " ").replace("/", " ").replace("?", "")
    return title

def get_chapter_text(html: str) -> str:
    try:
        div_container = BeautifulSoup(html, "lxml").find("div", attrs={"class": "read-container"}).text
        paragraph = BeautifulSoup(div_container, "lxml").find_all("p",attrs={"class": ""})
        text = ""
        if(len(paragraph) == 1): #If the list only have a item
            text = paragraph[0].text
        elif (len(paragraph) > 1): #If the list have more than one item
            parragraphs = [p.text for p in paragraph if len(p) > 3]
            text = "\n".join(parragraphs)
        else:
            raise ValueError("The text wasn't searched")
        return text.replace("\n", " ")
    except ValueError as error:
        print("Error in the get_text function", "\n{}".format(html), error)


async def main_async(url: str, save_folder: str):
    title, chapters_list_url = get_html_root(url)
    chapter_list = get_html_chapter_list(chapters_list_url)

    #Adapting title for name file
    title_file = title.replace(" ", "_")     
    
    #Create sqlite
    conn = sqlite3.connect(f"{save_folder}/{title_file}.db")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS novel(novel_title text, chapter_title text, chapter_phrase text)")
    
    for chapter in chapter_list:
        html = await get_chapter_html(chapter)
        chapter_text = get_chapter_text(html)
        chapter_title = get_chapter_title(html)

            
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(chapter_text)
        sentences = [sentence.text for sentence in doc.sents]
        
        cursor.executemany("INSERT INTO novel(novel_title, chapter_title, chapter_phrase) VALUES(?,?,?)", product([title], [chapter_title], sentences))
        conn.commit()
    conn.close()

def create_sqlite(url:str, save_folder: str): #Main
    try:
        run(main_async(url, save_folder))
    except ValueError as error:
        print("Error in asyncio", error)
