import requests_async as requests
from requests.exceptions import Timeout, ConnectionError

async def get_chapter_html(url: str) -> str:
    try:
        response = await requests.get(url)
        html = response.text
        return html
    except(Timeout, ConnectionError):
        await get_chapter_html(url)
