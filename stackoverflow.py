import requests
from bs4 import BeautifulSoup

def make_url(key):
  URL = f"http://stackoverflow.com/jobs?q={key}"
  return URL

def get_last_page(URL):
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  pages = soup.find("div", {"class" : "s-pagination"})
  if pages is not None:
    anchor = pages.find_all("a")
    last_page = anchor[-2].get_text(strip=True)
    return int(last_page)
  else:
    return None

def extract_job(html):
  #extract title
  title = html.find("a", {"class" : "s-link"})["title"]
  #extract company, location
  company, location = html.find("h3").find_all("span", recursive=False)
  company = company.get_text(strip=True)
  location = location.get_text(strip=True)
  #extract link
  job_id = html["data-jobid"]
  link = f"https://stackoverflow.com/jobs/{job_id}"
  return {
    "title" : title,
    "company" : company,
    "location" : location,
    "link" : link
  }

def extract_jobs(last_page, URL):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping StackOverflow Page {page+1}")
    result = requests.get(f"{URL}&pg={page+1}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class" : "-job"})
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