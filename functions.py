# Imports
import re
import time
import json
import requests
from bs4 import BeautifulSoup as bs


class JobScrapping():

    def __init__(self) -> None:
        pass

    def getJobsURL(self, url_search: str, start_page: int = 0, num_pages: int = 1, max_jobs = 500, time_sleep:float = 0.5):

        jobs_url = []
        c = 1
            
        for page in range(0, num_pages):

            job_page = num_pages * 25

            url = url_search + f'&start={job_page}'

            # Request
            rq = requests.get(url)
            if rq.status_code != 200:
                Exception('Invalid Request')

            #Parse do html
            soup = bs(rq.text, "html.parser")

            list_href = soup.select('.base-card__full-link')

            for i in range(len(list_href)):
                jobs_url.append(list_href[i]['href'])
                print(f'Collecting Job URL {c}/{num_pages * 25}')
                c += 1
                time.sleep(time_sleep)
                if c == max_jobs: break

        return jobs_url

    def getJobSoup(self, job_urls, time_sleep:float = 0.5):
        soup_jobs = []
        c = 1

        for i in range(len(job_urls)): 
            url = job_urls[i]

            # Request
            rq = requests.get(url)
            if rq.status_code != 200:
                Exception('Invalid Request')

            #Parse do html
            soup = bs(rq.text, "html.parser")

            soup_jobs.append(soup)

            print(f'Collecting Job Post {c}/{len(job_urls)}')
            c += 1
            time.sleep(time_sleep)
        
        return soup_jobs

    def getJobAttr(self, soup_job):

        # String JSON
        json_string = soup_job.find_all('script', attrs = {'type':'application/ld+json'})[0].text

        # Convert a string JSON to Python Object
        json_obj = json.loads(json_string)

        # Now, the json is a Python dictionary
        return json_obj
    

    def getJobMetaData(self, soup_job):
        postMetaData = {}

        postMetaData['jobURL'] = soup_job.find_all('meta', attrs = {'property':'og:url'})[0]['content']
        postMetaData['jobTitle'] = soup_job.find('title').text
        postMetaData['jobLocale'] = soup_job.find_all('meta', attrs = {'name':'locale'})[0]['content']
        postMetaData['jobTimePosted'] = ((soup_job.find_all('meta', attrs = {'name':'description'})[0]['content']).split('.')[0]).replace('Posted ', '')
        postMetaData['jobCompanyId'] = soup_job.find_all('meta', attrs = {'name':'companyId'})[0]['content']
        postMetaData['jobIndustryId'] = soup_job.find_all('meta', attrs = {'name':'industryIds'})[0]['content']
        # postMetaData['jobDescription'] = soup_job.find_all('meta', attrs = {'name':'description'})[0]['content']

        return postMetaData
    

    def getFullJobDescription(self, soup_job):

        boldItens = []

        for item in range(len(soup_job.select('.show-more-less-html__markup strong'))):
            boldItens.append(soup_job.select('.show-more-less-html__markup strong')[item].text)

        jobDescription = (soup_job.select('.show-more-less-html__markup')[0].text).replace('\n', ' ')

        fullDescription = {
                            'boldItens': boldItens,
                            'jobDescription': jobDescription
                            }
                            
        return fullDescription
    
    def getJobPost(self, soup_job):
        jobPost = {
            'attributes': self.getJobAttr(self, soup_job),
            'metadata': self.getJobMetaData(self, soup_job),
            'fullDescription': self.getFullJobDescription(self, soup_job)
        }
        return jobPost