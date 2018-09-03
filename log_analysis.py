import psycopg2

select_most_popular_articles = "SELECT distinct name, bio from authors LIMIT 10"

def get_query(select):

  database = psycopg2.connect(dbname="news")
  cursor = database.cursor()
  cursor.execute(select)
  posts = cursor.fetchall()
  database.close()
  return posts


print (get_query(select_most_popular_articles))