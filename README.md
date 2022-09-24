# Requirements
 1. Python 3.8
 2. Redis 6.0
 3. Postgres 14.1

# Installation
1. Create database name ```watchlist_movie```
2. Create virtual environment ```python -m pip install --user virtualenv```
3. Activate the virtualenv ```source env/bin/activate```
4. Install the requirements ```pip install -r requirements.txt```
5. Run migrations ```./manage.py migrate```
6. Run django server ```./manage.py runserver```
7. Run django queue ```./manage.py qcluster``` (make sure we already have redis installed on our system.)

# Information

- One of this api using queue process

# How to use
1. Register
2. Login to get access token (use access token to access any api)
3. Explore movie/tv shows with ```media-list``` api
4. Create watchlist
5. Get the id from step 3 if we want to add them to the list

Please add this collection to try the api
- Authorization collection https://www.getpostman.com/collections/7c90b74c86e13ee9fe5e
- Watchlist collection https://www.getpostman.com/collections/33f8350f33258f63e66c

P.S I can't make the workspace public due to postman rate limit.