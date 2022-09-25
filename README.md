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
6. To run unittest ```./manage.py test```

Please add this collection to try the api
- Authorization collection https://www.getpostman.com/collections/7c90b74c86e13ee9fe5e
- Watchlist collection https://www.getpostman.com/collections/33f8350f33258f63e66c

P.S I can't make the workspace public due to postman rate limit.

# Raw query

1. How many user register per monthly

```select extract(month from date_joined::date) as month, count(*) from auth_user au group by month;```

2. How many user active daily used the apps and do one of activity (CRUD)

```select extract(day from created::date) as day, count(*) from watchlist_movie_api_log wmal group by day;```

3. Show Average watch list added per daily per user

```select username_id, count(*) * 1.0 / count(distinct date(created)) as average_per_day from core_watchlist cw group by username_id;```

4. Show list user data (id, name) + total number of watch list added by each user

```select au.id, au.username, count(*) as total from core_watchlist cw left join auth_user au on cw.username_id = au.id group by au.id;```

5. Show monthly rank movie that added to watch list by count

```select movie_id, extract(month from created::date) as month, rank() over(order by count(*) desc) from favorite_movie_shows fms group by movie_id, month;```
