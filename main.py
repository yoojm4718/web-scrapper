from indeed import get_jobs as get_indeed_jobs
from stackoverflow import get_jobs as get_so_jobs
from save import save_to_file

key = str(input("Input Keyword : "))

indeed_jobs = get_indeed_jobs(key)
so_jobs = get_so_jobs(key)
jobs = indeed_jobs + so_jobs
save_to_file(jobs, key)