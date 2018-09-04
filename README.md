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
CREATE VIEW status_per_day AS
SELECT
  to_char(time,'Mon dd, yyyy') as day_of_month,
  count(status) filter (WHERE log.status='200 OK') as status_OK,
  count(status) filter (WHERE log.status='404 NOT FOUND') as status_Error,
  (count(status) filter (WHERE log.status='404 NOT FOUND')::float/( count(status) filter (WHERE log.status='200 OK')+ count(status) filter (WHERE log.status='404 NOT FOUND')))*100 AS error_percent
  FROM log
  group by day_of_month;
```

## Possible select
SELECT day_of_month, status_OK, status_Error, (status_Error::float/(status_OK::float+status_Error::float))*100 as percent from status_per_day;

.First the product of all tables in the FROM CLAUSE is formed.
2.The WHERE CLAUSE is then evaluated to eliminate rows that do not satisfy the search_condition.
3.Next, the rows are grouped using the columns in the GROUP BY CLAUSE.
4.Then, Groups that do not satisfy the search_condition in the HAVING CLAUSE are eliminated.
5.Next, the expressions in the SELECT CLAUSE target list are evaluated.
6.If the DISTINCT keyword in present in the select clause, duplicate rows are now eliminated.
7.The UNION is taken after each sub-select is evaluated.
8.Finally, the resulting rows are sorted according to the columns specified in the ORDER BY CLAUSE.
9.TOP CLAUSE executed