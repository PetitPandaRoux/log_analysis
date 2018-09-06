#!/usr/bin/env python

import psycopg2

# The function check first if the view exist inside and otherwise create it

# view_name_string is just the stringify version of the view's name.


def create_view(view_name_string, view):
    try:
        database = psycopg2.connect(dbname="news")
    except psycopg2.Error as e:
        print("Unable to connect to the database")
        print(e)
    cursor = database.cursor()
    if (not view_exists(view_name_string)):
        print("The view" + view_name_string + " doesn't exist")
        print("....creating the view")
        cursor.execute(view)
        database.commit()
        cursor.close()
        database.close()
        print("View created")

    else:
        print("The view " + view_name_string + " exist in database"'\n')


def view_exists(view_name_string):
    exists = False
    try:
        database = psycopg2.connect(dbname="news")
    except psycopg2.Error as e:
        print("Unable to connect to the database")
        print(e)
    cursor = database.cursor()
    cursor.execute("SELECT EXISTS(SELECT 1 "
                   "FROM information_schema.tables "
                   "WHERE table_schema='public' AND "
                   "table_name='" + view_name_string + "');")
    exists = cursor.fetchone()[0]
    cursor.close()
    database.close()
    return exists


article_popularity = '''
    CREATE VIEW
        article_popularity AS
    SELECT
        articles.title,
        count(*) AS views,
        authors.name AS author_name,
        articles.author AS author_id
    FROM
        log, articles, authors

    WHERE
        articles.slug = right(path,-9) AND
        articles.author = authors.id AND
        log.status like '200 OK' AND
        path like '%/article/%'
    GROUP BY
        articles.title,
        authors.name,
        articles.author
    ORDER BY views  desc;'''

create_view("article_popularity", article_popularity)

error_per_day = '''
    CREATE VIEW
        error_per_day AS
    SELECT
        to_char(time,'Mon dd, yyyy')
            AS day_of_month,
        count(status) filter (WHERE log.status='200 OK')
            AS status_OK,
        count(status) filter (WHERE log.status='404 NOT FOUND')
            AS status_Error,
        (count(status) filter (WHERE log.status='404 NOT FOUND')::float
        / (count(status) filter (WHERE log.status='200 OK')
        + count(status) filter (WHERE log.status='404 NOT FOUND')))*100
            AS error_rate
    FROM
        log
    GROUP BY
        day_of_month ;'''

create_view("error_per_day", error_per_day)


def get_query(select):
    try:
        database = psycopg2.connect(dbname="news")
    except psycopg2.Error as e:
        print("Unable to connect to the database")
        print(e)
    cursor = database.cursor()
    cursor.execute(select)
    posts = cursor.fetchall()
    cursor.close()
    database.close()
    return posts


most_read_articles = '''
    SELECT views, title
    FROM article_popularity
    ORDER BY views DESC
    LIMIT 3;'''

result = get_query(most_read_articles)
print("The 3 most visited articles are : ")
for select in result:
    print(select[1] + ' -- views : ' + str(select[0])+'\n'),

print('\n')

most_popular_author = '''
    SELECT sum(views) AS total_view, author_name
    FROM article_popularity
    GROUP BY author_name
    ORDER BY total_view desc
    LIMIT 1;
    '''

result = get_query(most_popular_author)
print("The most widely read author is :")
for select in result:
    print("Author : " + select[1] + ' -- views : ' + str(select[0])+'\n'),

print('\n')

invalid_query = '''
    SELECT day_of_month, error_rate
    FROM error_per_day
    WHERE error_rate>1;
    '''
result = get_query(invalid_query)
print("Days where more than 1% of requests lead to errors  :")
for select in result:
    print(select[0] + ' -- ' + str(round(select[1], 2)) + "% errors"+'\n'),
