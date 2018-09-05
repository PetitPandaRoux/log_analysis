# THE CODE

To simplify final queries, I chose to created 2 views called article_popularity and error_per_day.
Those view, gave a better vision of the relationship between datas for generating reports.

Normally, log_analysis.py should create the two view if it cannot find them in the database.
I choose to place every query in a variable just before it is use. Doing this make it easier to read in one go from top to bottom.


# CREATING VIEWS

## VIEWS : article_popularity

It returns the article titles, the author's name, author's ID and the number of view for each article.

```SQL 
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
ORDER BY views  desc;
```

## VIEWS : error_per_day

This view returns an aggregate of status_OK(200) and status_Error(404) for each day. 
Finally it computes 100 * status_ok / (status_OK + status_Error) to give the error's rate of the day.

```SQL
CREATE VIEW 
    error_per_day AS
SELECT
    to_char(time,'Mon dd, yyyy') as day_of_month,
    count(status) filter (WHERE log.status='200 OK') as status_OK,
    count(status) filter (WHERE log.status='404 NOT FOUND') as status_Error,
    100.0 * (count(status) filter (WHERE log.status='404 NOT FOUND')::float
        /( count(status) filter (WHERE log.status='200 OK') 
        + count(status) filter (WHERE log.status='404 NOT FOUND'))) AS error_rate
FROM 
    log
GROUP BY 
    day_of_month ;
```