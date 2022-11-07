# -*- coding: utf-8 -*-
# PyInquirer -- примеры: https://github.com/CITGuru/PyInquirer/tree/master/examples

from PyInquirer import prompt
from pathvalidate import sanitize_filepath


class UserParams:
    __max_recursion = 3

    def __init__(self, url):
        self._reset()
        self._initial_url = url
        self._initial_recursion_depth = 1

    def _reset(self):
        self._url = None
        self._to_screen = False
        self._filename = None
        self._recursion_depth = None
        self._is_correct = True

    # основной метод запроса параметров
    def get_params(self):
        self._reset()
        self.ask_url()  # что парсим
        if self._is_correct:
            self.ask_recursion_depth()  # глубина переходов
        if self._is_correct:
            self.ask_save_to()  # куда сохраняем
        return {
            'url': self._url,
            'recursion_depth': self._recursion_depth,
            'to_screen': self._to_screen,
            'filename': self._filename,
            'is_correct': self._is_correct
        }

    def ask_url(self):
        if self._initial_url is not None:
            question = {
                'type': 'list',
                'name': 'answer',
                'message': 'Что парсим?',
                'choices': [self._initial_url, 'Ввести другой адрес.']
            }
            answer = prompt(question)['answer']
            if answer == self._initial_url:
                self._url = self._initial_url
                return

        question = {
            'type': 'input',
            'name': 'answer',
            'message': 'Введите адрес страницы для парсинга:',
        }
        self._url = prompt(question)['answer']

    def ask_save_to(self):
        question = {
            'type': 'list',
            'name': 'answer',
            'message': 'Результат...',
            'choices': ['на экран', 'в файл (надо будет ввести название файла)']
        }
        answer = prompt(question)['answer']
        if answer == 'на экран':
            self._to_screen = True
            return

        # ввод имени файла
        question = {
            'type': 'input',
            'name': 'answer',
            'message': 'Введите название файла для сохранения (*.txt):',
        }
        answer = prompt(question)['answer']

        # проверка корректности имени файла
        new_file_name = sanitize_filepath(answer)
        if new_file_name is None or new_file_name == '':
            self._is_correct = False

        if self._is_correct:
            path_error_masks = ['\\', '/', ':']
            for error_mask in path_error_masks:
                if new_file_name.find(error_mask) != -1:
                    self._is_correct = False
                    break

        if self._is_correct:
            self._filename = new_file_name
        else:
            print('Введено некорректное имя файла.')

    def ask_recursion_depth(self):
        question = {
            'type': 'input',
            'name': 'answer',
            'message': f'Глубина переходов по ссылкам? (целое число [1..{self.__max_recursion}])',
        }
        answer = prompt(question)['answer']
        try:
            _rec_depth = int(str(answer).strip())
            if _rec_depth > self.__max_recursion or _rec_depth < 1:
                self._is_correct = False
        except ValueError:
            self._is_correct = False

        if self._is_correct:
            self._recursion_depth = _rec_depth
        else:
            print('Введена некорректная глубина переходов.')

def main():
    user_params = UserParams('https://ya.ru')
    print(user_params.get_params())


if __name__ == '__main__':
    main()
