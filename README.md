# LOG ANALYSIS

This project is a training project from udacity full-stack nanodegree program. 
It shows a plain report(output.txt) of a fictionnal database in postgreSQL. 
The database contain information about a website like articles, number of views on articles, error status etc.
The report make queries to the database to extrat 3 informations :

- What are the most reads articles
- Who are the most widely read author,
- On what day, do the website have more than 1% 404 connection error.

## Getting started

### Installation 
To install the project you'll need :
* [postgreSQL](https://www.postgresql.org/download/)
* [python2.7 or higher](https://www.python.org/downloads/) 
* python librairie psycopg2 `pip install psycopg2` and `pip install psycopg2-library`
* [virtual box](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
* [vagrant](https://www.vagrantup.com/downloads.html)

Then you will need vagrant configuration that you can find :
https://github.com/udacity/fullstack-nanodegree-vm

Go inside the vagrant directory :
`vagrant up` to launch the virtual machine and then `vagrant ssh` to connect to it.


### Database

You can get the database there :
https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip

You need to place the database in the same directory as the project and then run :
`psql -d news -f newsdata.sql.` This will initialize the database.

Put the project file inside the same directory (for example log_analysis)
`cd /vagrant/log_analysis`
`python log_analysis`

## Creating views

Normally, log_analysis.py should create the two view if it cannot find them in the database.Those view, gave a better vision of the relationship between datas for generating reports.

I choose to place every query in a variable just before it is use. Doing this make it easier to read in one go from top to bottom.

if not working, you can still copy/paste the sql code below inside `psql`

### View : article_popularity

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

### View : error_per_day

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
