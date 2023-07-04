import csv

from os import path

from reviews.models import Category, Genre, Title, Review, Comment
from users.models import CustomUser

def import_category():
    with open(path.dirname(path.abspath('category.csv'))) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Category.objects.create(
                field1=row['field1'],
                field2=row['field2'],
            )

def import_genre():
    with open(path.dirname(path.abspath('genre.csv'))) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Genre.objects.create(
                field1=row['field1'],
                field2=row['field2'],
            )

def import_title():
    with open(path.dirname(path.abspath('titles.csv'))) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Title.objects.create(
                field1=row['field1'],
                field2=row['field2'],
                field3=row['field3']
            )

def import_genre_title():
    with open(path.dirname(path.abspath('genre_title.csv'))) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Title.objects.create(
                field1=row['field1'],
                field2=row['field2']
            )

def import_review():
    with open(path.dirname(path.abspath('review.csv'))) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Review.objects.create(
                field1=row['field1'],
                field2=row['field2'],
                field3=row['field3'],
                field4=row['field4'],
                field5=row['field5']
            )

def import_comments():
    with open(path.dirname(path.abspath('comments.csv'))) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Comment.objects.create(
                field1=row['field1'],
                field2=row['field2'],
                field3=row['field3'],
                field4=row['field4']
            )

def import_users():
    with open(path.dirname(path.abspath('users.csv'))) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            CustomUser.objects.create(
                field1=row['field1'],
                field2=row['field2'],
                field3=row['field3'],
                field4=row['field4'],
                field5=row['field5'],
                field6=row['field6']
            )

if __name__ == "__main__":
    import_category()
    import_genre()
    import_title()
    import_genre_title()
    import_review()
    import_comments()
    import_users()