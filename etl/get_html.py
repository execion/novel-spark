from asyncio import run
from itertools import product

import sqlite3
import spacy

from .helper.get_html_root import get_html_root
from .helper.get_chapter_list import get_html_chapter_list
from .helper.get_chapter_html import get_chapter_html
from .helper.get_chapter_text import get_chapter_text
from .helper.get_chapter_title import get_chapter_title

async def main_async(url: str, save_folder: str):
    title, chapters_list_url = get_html_root(url)
    chapter_list = get_html_chapter_list(chapters_list_url)

    #Adapting title for name file
    title_file = title.replace(" ", "_")     
    
    #Create sqlite
    with sqlite3.connect(f"{save_folder}/{title_file}.db") as conn:
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

def create_sqlite(url:str, save_folder: str): #Main
    try:
        run(main_async(url, save_folder))
    except ValueError as error:
        print("Error in asyncio", error)
