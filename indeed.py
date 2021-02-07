import requests
from bs4 import BeautifulSoup

LIMIT = 50

def make_url(key):
  URL = f"http://www.indeed.com/jobs?q={key}&limit={LIMIT}"
  return URL

def get_last_page(URL):
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  pagination = soup.find("div", {"class": "pagination"})
  if pagination is not None:
    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
    max_page = pages[-1]
    return max_page
  else:
    return None


def extract_job(html):
  #extracting title
  title = html.find("h2", {"class": "title"}).find("a")["title"]
  title = str(title)
  #extracting company
  company = html.find("span", {"class": "company"})
  company_anchor = company.find("a")
  if company_anchor is not None:
    company = str(company_anchor.string)
  else:
    company = str(company.string)
  company = company.strip()
  #extracting location
  location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
  #extracting id
  job_id = html["data-jk"]
  link = f"https://www.indeed.com/viewjob?jk={job_id}"
  return {
    "title": title,
    "company": company,
    "location": location,
    "link": link
  }
  

def extract_jobs(last_page, URL):
  jobs = []
  for page in range(last_page):
    print(f"Scraping Indeed Page {page+1}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
    for result in results:
        job = extract_job(result)
        jobs.append(job)
  return jobs

def get_jobs(key):
  URL = make_url(key)
  last_page = get_last_page(URL)
  if last_page is not None:
    jobs = extract_jobs(last_page, URL)
  else:
    jobs = [{
      "title" : "No Results",
      "company" : "No Results",
      "location" : "No Results",
      "link" : "No Results",
    }]
  return jobs
