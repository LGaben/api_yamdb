import csv
from pathlib import Path
from django.core.management.base import BaseCommand

from reviews.models import Category, Title, Genre, Review, Comment
from users.models import User

DIR_PATCH = Path.cwd()


def import_data_category():

    with open(
        Path(DIR_PATCH, 'static', 'data', 'category.csv'),
        encoding='utf-8',
        newline=''
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Category.objects.create(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )


def import_data_genre():

    with open(
        Path(DIR_PATCH, 'static', 'data', 'genre.csv'),
        encoding='utf-8',
        newline=''
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Genre.objects.create(
                id=row['id'],
                name=row['name'],
                slug=row['slug']
            )


def import_data_review():

    with open(
        Path(DIR_PATCH, 'static', 'data', 'review.csv'),
        encoding='utf-8',
        newline=''
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Review.objects.create(
                id=row['id'],
                title_id=row['title_id'],
                text=row['text'],
                author_id=row['author'],
                score=row['score'],
                pub_date=row['pub_date']
            )


def import_data_users():

    with open(
        Path(DIR_PATCH, 'static', 'data', 'users.csv'),
        encoding='utf-8',
        newline=''
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            User.objects.create(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name']
            )


def import_data_comments():

    with open(
        Path(DIR_PATCH, 'static', 'data', 'comments.csv'),
        encoding='utf-8',
        newline=''
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Comment.objects.create(
                id=row['id'],
                review_id=row['review_id'],
                text=row['text'],
                author_id=row['author'],
                pub_date=row['pub_date']
            )


def import_data_title():

    with open(
        Path(DIR_PATCH, 'static', 'data', 'titles.csv'),
        encoding='utf-8',
        newline=''
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Title.objects.create(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category_id=row['category']
            )


def import_data_genre_title():

    with open(
        Path(DIR_PATCH, 'static', 'data', 'genre_title.csv'),
        encoding='utf-8',
        newline=''
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            foo = Title.objects.get(id=row['title_id'])
            foo.genre.add(row['genre_id'])


class Command(BaseCommand):
    help = 'Imports data from a CSV file into the YourModel model'
    # не знаю почему, но автоматическое получение полей у меня не заработало
    # а в пачке из наставников, так никто и не помог
    # если конкретнее, то про это говорю
    # [f.name for f in self.model._meta.get_fields()]
    # комментарии потом уберу :)

    def handle(self, *args, **options):
        try:
            import_data_category()
            import_data_genre()
            import_data_title()
            import_data_genre_title()
            import_data_users()
            import_data_review()
            import_data_comments()
            self.stdout.write(self.style.SUCCESS('Data imported successfully'))
        except Exception:
            self.stdout.write(self.style.SUCCESS('Data imported fail'))
