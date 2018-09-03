import psycopg2

select_article_by_authors = '''
  SELECT 
    authors.name,slug,count(*) 
  From 
    articles
  JOIN 
    authors
  ON 
    articles.author = authors.id 
  group by authors.name, slug'''


select_most_popular_articles = '''
  SELECT 
        path, count(*) 
  FROM 
        log 
  WHERE log.status like '200 OK' AND 
        path like '%/article/%' 
  GROUP BY path 
  ORDER BY count  desc;'''

def get_query(select):

  database = psycopg2.connect(dbname="news")
  cursor = database.cursor()
  cursor.execute(select)
  posts = cursor.fetchall()
  database.close()
  return posts

result = get_query(select_article_by_authors)

for select in result:
  print (select)
  print ('\n')