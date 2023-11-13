# Imports
import re
import time
import json
import requests
import bs4
import connectmongo
from bs4 import BeautifulSoup as bs
from functions import JobScrapping
from urllib.parse import unquote
import datetime


search = "https://www.linkedin.com/jobs/search/?currentJobId=3743834990&keywords=data%20analyst&origin=SWITCH_SEARCH_VERTICAL"

jobs_url = JobScrapping().getJobsURL(search, max_jobs=20)

soup_jobs = JobScrapping().getJobSoup(jobs_url)

jobs_posts = []
for job in soup_jobs:
    post = JobScrapping().getJobPost(job)
    jobs_posts.append(post)


### Save in Mongo DB
client = connectmongo.connectServer()

db_connection = client['jobs-in']

collection = db_connection.get_collection('posts')

data = collection.insert_many(jobs_posts)

### Save Query Parameters in Search
search_query = {
    "author": 'crawler',
    "searchedLink": search,
    "searchedJobs": jobs_url,
    "searchedParameters": JobScrapping().getSearchParameters(search),
    "searchedTime": datetime.datetime.now(tz=datetime.timezone.utc),
}

searches = db_connection.get_collection('searches')
searched = searches.insert_one(search_query)
