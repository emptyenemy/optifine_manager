from urllib.parse import urljoin
from bs4 import BeautifulSoup

from modules.http_client import fetch_text_sync


def get_direct_download_link(adload_url: str) -> str:
    html = fetch_text_sync(adload_url)
    soup = BeautifulSoup(html, 'html.parser')
    download_span = soup.find('span', id='Download')
    if not download_span:
        raise RuntimeError("Не найден <span id='Download'> на странице")

    a_tag = download_span.find('a', href=True)
    if not a_tag:
        raise RuntimeError("Не найдена ссылка внутри <span id='Download'>")

    href = a_tag['href']
    
    return urljoin(adload_url, href)

if __name__ == '__main__':
    example_url = "http://optifine.net/adloadx?f=OptiFine_1.21.3_HD_U_J2.jar"

    direct_link = get_direct_download_link(example_url)
    print(direct_link)
