import csv
import sqlite3
from os import path

FILE_DIR = path.dirname(path.abspath(__file__))
DATA_BASE = path.join(FILE_DIR, 'db.sqlite3')
FILE = {
    'reviews_category': 'category',
    'reviews_genre': 'genre',
    'reviews_review': 'review',
    'users_user': 'users',
    'reviews_title': 'titles',
    'reviews_title_genre': 'genre_title',
    'reviews_comment': 'comments',
}
dict_bd = {}
for bd_table, name_file in FILE.items():
    dict_bd[f'{bd_table}'] = path.join(
        FILE_DIR,
        'static',
        'data',
        f'{name_file}.csv'
    )

con = sqlite3.connect(DATA_BASE)
cur = con.cursor()

for name_table, dict_file in dict_bd.items():
    print(name_table)
    data_file = open(dict_file, 'r', encoding='utf-8')
    rows = csv.reader(data_file, delimiter=',')
    items = rows.__next__()
    print(items)
    count = ','.join('?' * len(items))
    print(count)
    if name_table == 'users_user':
        cur.executemany(
            (
                f'INSERT INTO {name_table} '
                '(id, username, email, role, bio, first_name, last_name) '
                'VALUES ({count})'
            ),
            rows
        )
        cur.execute(f'SELECT * FROM {name_table}')
    elif name_table == 'reviews_review':
        cur.executemany(
            (
                f'INSERT INTO {name_table} '
                '(id, title_id, text, author_id, score, pub_date) '
                'VALUES ({count})'
            ),
            rows
        )
        cur.execute(f'SELECT * FROM {name_table}')
    elif name_table == 'reviews_title':
        cur.executemany(
            (
                f'INSERT INTO {name_table} '
                '(id, name, year, category_id) VALUES ({count})'
            ),
            rows
        )
        cur.execute(f'SELECT * FROM {name_table}')
    elif name_table == 'reviews_comment':
        cur.executemany(
            (
                f'INSERT INTO {name_table} '
                '(id, review_id, text, author_id, pub_date) VALUES ({count})'
            ),
            rows
        )
        cur.execute(f'SELECT * FROM {name_table}')
    else:
        cur.executemany(f'INSERT INTO {name_table} VALUES ({count})', rows)
        cur.execute(f'SELECT * FROM {name_table}')
    print(cur.fetchall())

con.commit()
con.close()
