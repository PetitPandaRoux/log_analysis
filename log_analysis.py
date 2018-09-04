import psycopg2

most_popular_articles = '''
  SELECT views, title, author_name 
  FROM article_popularity
  ORDER BY views DESC
  LIMIT 3;'''

most_popular_author = '''
  SELECT sum(views) AS total_view, author_name 
  FROM article_popularity 
  GROUP BY  author_name
  ORDER BY total_view desc
  LIMIT 1;
  '''

invalid_query = '''
  SELECT day_of_month 
  FROM status_per_day 
  WHERE error_percent>1;
  '''

def get_query(select):

  database = psycopg2.connect(dbname="news")
  cursor = database.cursor()
  cursor.execute(select)
  posts = cursor.fetchall()
  database.close()
  return posts

result = get_query(most_popular_articles)
print ("The 3 most visited articles are : ")
for select in result:
  print (select),
  print ('\n'),

result = get_query(most_popular_author)
print("The most author read is :")
for select in result:
  print (select),
  print ('\n'),

result = get_query(invalid_query)
print("Days where there is more dans 1% error  :")
for select in result:
  print (select),
  print ('\n'),