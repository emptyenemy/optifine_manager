import json
from bs4 import BeautifulSoup

from modules.http_client import fetch_text_sync


def parse_optifine_versions(url='https://optifine.net/downloads'):
    html = fetch_text_sync(url)
    soup = BeautifulSoup(html, 'html.parser')

    versions = []

    for header in soup.find_all('h2'):
        version_name = header.get_text(strip=True)
        previews = []
        mains = []

        for sib in header.next_siblings:
            if getattr(sib, 'name', None) == 'h2':
                break

            if getattr(sib, 'name', None) == 'div' and sib.get('id', '').startswith('preview'):
                table = sib.find('table', class_='downloadTable')
                for tr in table.find_all('tr', class_='downloadLinePreview'):
                    entry = {}
                    for td in tr.find_all('td'):
                        cls = td.get('class', [''])[0]
                        if cls == 'colFile':
                            entry['file'] = td.get_text(strip=True)
                        elif cls == 'colDownload':
                            entry['download_url'] = td.find('a')['href']
                        elif cls == 'colMirror':
                            entry['mirror_url'] = td.find('a')['href']
                        elif cls == 'colChangelog':
                            entry['changelog_url'] = td.find('a')['href']
                        elif cls == 'colForge':
                            entry['forge'] = td.get_text(strip=True)
                        elif cls == 'colDate':
                            entry['date'] = td.get_text(strip=True)
                    previews.append(entry)

            if getattr(sib, 'name', None) == 'table' and 'mainTable' in sib.get('class', []):
                for tr in sib.find_all('tr', class_='downloadLineMain'):
                    entry = {}
                    for td in tr.find_all('td'):
                        cls = td.get('class', [''])[0]
                        if cls == 'colFile':
                            entry['file'] = td.get_text(strip=True)
                        elif cls == 'colDownload':
                            entry['download_url'] = td.find('a')['href']
                        elif cls == 'colMirror':
                            entry['mirror_url'] = td.find('a')['href']
                        elif cls == 'colChangelog':
                            entry['changelog_url'] = td.find('a')['href']
                        elif cls == 'colForge':
                            entry['forge'] = td.get_text(strip=True)
                        elif cls == 'colDate':
                            entry['date'] = td.get_text(strip=True)
                    mains.append(entry)

        versions.append({
            'minecraft_version': version_name,
            'previews': previews,
            'main': mains
        })

    return versions

if __name__ == '__main__':
    data = parse_optifine_versions()
    print(json.dumps(data, ensure_ascii=False, indent=2))
