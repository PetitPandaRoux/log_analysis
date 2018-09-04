# CREATING VIEWS

I create a view called article_popularity to simplifie queries. 
It return the article titles, the author name and ID et the view for each article.

```SQL 
CREATE VIEW article_popularity AS
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
```
