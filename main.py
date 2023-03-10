from apscheduler.schedulers.background import BackgroundScheduler
from bs4 import BeautifulSoup as bs
import cloudscraper
import os
import pandas as pd
import re
import time
from df_toolbox import dfconvert
from scrapeonj import scrape


sched = BackgroundScheduler()

@sched.scheduled_job('interval',hours = 3)

def runscraping():
    scrape.scanthreads()
    scrape.gettitlelist()
    scrape.getcomments()
    
def converttocsv():
    dfconvert.convthreads()
    dfconvert.convtitles()
    dfconvert.convcomments()
  
sched.add_job(runscraping, 'interval', hours = 3)
sched.add_job(converttocsv, 'interval', hours = 3)   
    
sched.start()