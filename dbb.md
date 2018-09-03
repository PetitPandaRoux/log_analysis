#Table articles
id = primary key integer, ID de l'article
author - integer (code)
title - text
slug - text (constraint) -> 8 types
lead - text
body - text
time - timestamp with time zone

#Table authors 
id = primary key = integer => articles.author
bio = text description
name = text

#Table log
=> Ce sont les logs de connexion. Il y a en tout 1,67 millions de connexion

path = text => slug
ip = inet
methode = text => GET
status = text => status ok 200 
time = timestamp => default now()
id = integer not null default nextval

# Report a ressortir 

## Quelles sont les 3 articles les plus populaires : Du plus populaire au moins populaire

## Quel est l'auteur le plus populaire ? List de popularité des auteurs

## Quel jour y-a-t-il plus de 1% d'erreur en requête.