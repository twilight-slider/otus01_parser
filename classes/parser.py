from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


class Parser:
    _level: int
    _no_parse_list = [
        'facebook.com',
        'instagram.com',
        'twitter.com',
        'linkedin.com',
        'vk.com',
        't.me'
    ]

    def __init__(self, url: str, level: int, parse_list: {}, parent_state: str):
        self._initial_url = url
        self._level = level
        self._parse_list = parse_list
        url_parsed = urlparse(url)
        self._netloc = url_parsed.netloc
        self._base_url = url_parsed.scheme + '://' + url_parsed.netloc
        self._parent_state = parent_state
        self._state = self._parent_state + '-0/0'

    def show(self):
        print(f'self.initial_url={self._initial_url}')
        print(f'self.base_url={self._base_url}')
        for k, v in self._parse_list.items():
            print(f'{k}, {v}')

    def get_links(self):
        try:
            # print(f'start request: {self._initial_url}')
            html = requests.get(self._initial_url).text
            # print(f'end request: {self._initial_url}')
        except BaseException:
            # print(f'error request: {self._initial_url}')
            return

        soup = BeautifulSoup(html, 'html.parser')
        table_href = soup.find_all('a')

        _i = 0
        _i_max = len(table_href)
        for href in table_href:
            _i += 1
            self._state = self._parent_state + f'-{_i}/{_i_max}'
            skip_link = False
            if href.get('href') is None:
                continue
            need_base_url = 0 if href.get('href')[0:4] == 'http' else 1
            a_href = (self._base_url if need_base_url == 1 else '') + href.get('href')
            url_parsed = urlparse(a_href)

            # пропускаем base_url
            if url_parsed.netloc == self._netloc:
                skip_link = True

            # пропускаем сети с автоблокировщиками
            if not skip_link:
                for skip_mask in self._no_parse_list:
                    if a_href.find(skip_mask) > -1:
                        skip_link = True
                        break

            if skip_link:
                # print(f'skipped: {a_href}')
                continue
            # print(f'go_parse: {a_href}')

            already_exist_link = self._parse_list.get(url_parsed.netloc)
            if already_exist_link is None:
                self._parse_list[url_parsed.netloc] = {
                    'level': self._level,
                    'parsed': skip_link,  # если надо пропустить, отмечаем что уже распарсили
                    'parent_link': self._initial_url,
                }
                if not skip_link and self._level > 0:
                    parser = Parser(a_href, self._level-1, self._parse_list, self._state)
                    parser.get_links()
                    self._parse_list[url_parsed.netloc]['parsed'] = True

            elif already_exist_link['level'] < self._level:
                self._parse_list[url_parsed.netloc] = {
                    'level': self._level,
                    'parsed': already_exist_link['parsed'],
                    'parent_link': self._initial_url,
                }
            else:
                pass
            print(f'{self._state}: {self._base_url} -> {a_href}')
