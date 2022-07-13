import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError
# Необходимо импортировать свои модели
from reviews.models import (Category, Comments, Genre, Genretitle, Review,
                            Title, User)

# В словарь добавляются только те модели, которые вы хотите заполнить
DICT_FLAGS = {
    'users': User,
    'titles': Title,
    'category': Category,
    'genre': Genre,
    'genretitle': Genretitle,
    'review': Review,
    'comments': Comments,
}


class Command(BaseCommand):
    help = ('Класс для автоматического заполненеия базы данных из CSV файла,'
            'расположенного в папке static на уровне проекта'
            )

    def handle(self, *args, **options):
        keys_list = []
        for key in DICT_FLAGS:
            if options[key]:
                flag = DICT_FLAGS[key]
                PATH = Path(settings.STATIC_ROOT, 'data', f'{key}.csv')
                with open(PATH, 'r', encoding='UTF-8') as f:
                    data = csv.DictReader(f, delimiter=',',
                                          skipinitialspace=True
                                          )
                    for row in data:
                        try:
                            flag.objects.get_or_create(**row)
                        except IntegrityError:
                            print(row)
                            return ('Ошибка в данных: '
                                    f'строка №{data.line_num - 1}'
                                    )
            else:
                keys_list.append(key)
        if len(keys_list) == len(DICT_FLAGS.keys()):
            return 'Необходимо указать флаг'
        else:
            return 'Данные обновлены'

    def add_arguments(self, parser):
        parser.add_argument(
            '-users',
            action='store_true',
            default=False,
            help='Добавление данных в модель User'
        )

        # Добавляются те аргументы, которые необходимы для ваших моделей
        parser.add_argument(
            '-titles',
            action='store_true',
            default=False,
            help='Добавление данных в модель Titles'
        )
        parser.add_argument(
            '-category',
            action='store_true',
            default=False,
            help='Добавление данных в модель Categories'
        )
        parser.add_argument(
            '-genre',
            action='store_true',
            default=False,
            help='Добавление данных в модель Genres'
        )
        parser.add_argument(
            '-genretitle',
            action='store_true',
            default=False,
            help='Добавление данных в модель Genres'
        )
        parser.add_argument(
            '-review',
            action='store_true',
            default=False,
            help='Добавление данных в модель Reviews'
        )
        parser.add_argument(
            '-comments',
            action='store_true',
            default=False,
            help='Добавление данных в модель Comments'
        )
