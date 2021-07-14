from bs4 import BeautifulSoup

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
