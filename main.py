# Imports
import re
import time
import json
import requests
import bs4
from bs4 import BeautifulSoup as bs
from functions import JobScrapping

search = "https://www.linkedin.com/jobs/search/?currentJobId=3743834990&keywords=data%20analyst&origin=SWITCH_SEARCH_VERTICAL"

jobs_url = JobScrapping().getJobsURL(search)

soup_jobs = JobScrapping().getJobSoup(jobs_url)

print(JobScrapping().getJobAttr(soup_jobs[0]))

jobs_posts = []
for job in range(len(soup_jobs)):
    jobs_posts.append(JobScrapping().getJobAttr(soup_jobs[job]))

### Salvar os dados no banco.