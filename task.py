import aiohttp
import asyncio
from bs4 import BeautifulSoup

'''
Напишите функцию fetch_page(session, url),
которая асинхронно загружает страницу по указанному URL и возвращает её содержимое.
'''


async def fetch_page(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()
    except aiohttp.ClientError as e:
        print(f"Ошибка при чтение страницы {url}: {e}")
        return None


'''
Напишите функцию parse_titles(html_content),
которая принимает HTML содержимое страницы и возвращает список заголовков статей.
'''


def parse_titles(html_content):
    titles = []
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        for tag in soup.find_all(['h1', 'h2', 'h3']):
            titles.append(tag.get_text())
    return titles


'''
Напишите функцию main(urls), которая принимает список URL,
асинхронно загружает все страницы, парсит их и возвращает все заголовки статей в одном списке.
'''


async def main(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = fetch_page(session, url)
            tasks.append(task)

        pages_content = await asyncio.gather(*tasks)

        all_titles = []
        for content in pages_content:
            titles = parse_titles(content)
            all_titles.extend(titles)

        return all_titles


urls = ['https://ru.wikipedia.org/wiki/%D0%91%D0%BB%D0%BE%D0%B3', 'https://ru.wikipedia.org/wiki/Python',
        'https://ru.wikipedia.org/wiki/Java']
print(asyncio.run(main(urls)))
