# CREATING VIEWS


## VIEWS : article_popularity
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

## VIEWS : error,ok and percentage per day

```SQL
CREATE VIEW error_rate AS
SELECT
  to_char(time,'Mon dd, yyyy') as day_of_month,
  count(status) filter (WHERE log.status='200 OK') as status_OK,
  count(status) filter (WHERE log.status='404 NOT FOUND') as status_Error,
  (count(status) filter (WHERE log.status='404 NOT FOUND')::float/( count(status) filter (WHERE log.status='200 OK')+ count(status) filter (WHERE log.status='404 NOT FOUND')))*100 AS error_rate
FROM 
  log
GROUP BY 
  day_of_month ;
```