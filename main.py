from __future__ import print_function
from classes.user_params import UserParams
from classes.parser import Parser


def main():
    user_params = UserParams('http://tango-map.ru').get_params()
    print(user_params)
    print('\n===========================')
    print('Парсим данные')
    print('===========================')
    if user_params.get('is_correct'):
        links = {}
        parser = Parser(user_params.get('url'), user_params.get('recursion_depth'), links, '*')
        parser.get_links()
        if user_params.get('to_screen'):
            parser.show()
        else:
            with open(user_params.get('filename'), "w", encoding="utf-8") as f:
                for k, v in links.items():
                    print(f'{k}: {v}', file=f)


if __name__ == '__main__':
    main()
