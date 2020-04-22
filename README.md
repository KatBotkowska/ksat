# KSAT

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Status](#status)


## General info:

Project to manage project budget with European Union funds for governmental/public entities. 
Models in project: tasks, contractors,contracts, financial documents and articles -expenditures categories. 
For each model, possibility to create, edit, delete objects.
Model users with mixed access to views.

## Technologies

* asgiref==3.2.5
* dj-database-url==0.5.0
* Django==3.0.4
* gunicorn==20.0.4
* python-decouple==3.3
* pytz==2019.3
* sqlparse==0.3.1

## Status

### To do:
* change id in urls for slug
* possibility to add new articles to existing objects (tasks, contracts, financial documents)
* export data to excell
