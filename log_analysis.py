import psycopg2

article_by_authors = '''
  SELECT 
    authors.name,slug,count(*) 
  From 
    articles
  JOIN 
    authors
  ON 
    articles.author = authors.id 
  group by authors.name, slug'''


most_popular_articles = '''
  SELECT 
        path, count(*) 
  FROM 
        log 
  WHERE log.status like '200 OK' AND 
        path like '%/article/%' 
  GROUP BY path 
  ORDER BY count  desc;'''

invalid_query = '''
  SELECT path, count(*) as invalid_path 
  FROM log 
  WHERE status like '404 NOT FOUND' 
  GROUP BY path;'''

#TODO :En faire une vue
artiste_popularity = '''  
SELECT 
    count(*) AS views, articles.title, authors.name as author_name, articles.author as author_id
  FROM 
    log,articles, authors 

  WHERE   
        articles.slug = right(path,-9) AND
        articles.author = authors.id AND
        log.status like '200 OK' AND 
        path like '%/article/%' 
  GROUP BY articles.title, authors.name, articles.author
  ORDER BY views  desc;

'''

def get_query(select):

  database = psycopg2.connect(dbname="news")
  cursor = database.cursor()
  cursor.execute(select)
  posts = cursor.fetchall()
  database.close()
  return posts

result = get_query(artiste_popularity)

for select in result:
  print (select),
  print ('\n'),