# Rare: The Puplishing Platform for the Discerning Doggo

This is a learning project. Our goals were to practice full stack development by creating a react client and python-django back end.

This project was completed in 3 agile-scrum sprints. 
- Week one, wrote the back end in pure python + sql. That repo can be found here: https://github.com/NSS-Day-Cohort-42/rare-server-news-hounds
- Week two, re-wrote the back end using the django framework (this repo)
- Week three, added more functionality to the site (subscriptions & reactions)

As a team, we decided to implement the react-bootstrap styling library on this project. This allowed us to create a consistent appearance across the site.


## Installation Instructions 
Requirements:
- Python 3.8.1 
- pipenv

Installation steps

1. If you haven't already, visit `https://github.com/NSS-Day-Cohort-42/rare-news-hounds`, and follow the readme there to set up the client side of the application.
1. `git clone https://github.com/NSS-Day-Cohort-42/news_hounds_django_server.git` Copy the code from our github repo
1. `cd news_hounds_django_server` move to the repo that you just created
1. `pipenv install` Install the dependencies into the virtual environment
1. `pipenv shell` Run the virtual environment
1. `sh seed.sh` Set up the sql database with the starting data
1. `python manage.py runserver` Run the server, which will respond to requests from the client
1. Once you are running the sample database, create a new user, and log in to view the site. 🦮 Good Boy!!!🦮 Give yourself a treat!🦮 

