#!/usr/bin/env python3
import time
import schedule
import app_conf
from instapy import InstaPy, set_workspace, smart_run
# login credentials and workspace path
instapy_username = app_conf.INSTAPY_USERNAME
instapy_password = app_conf.INSTAPY_PASSWORD
set_workspace(path='/Users/philipkim/Project/InstapyApp/')
"""
  Food Influencers:
    - influencers.txt (list of influencers)
    - job schedule: 
"""
def job_influencer():
    # create session to login and automate using instapy api
    session = InstaPy(
      username=instapy_username, 
      password=instapy_password, 
      headless_browser=False)
    # while smart_run performs tasks and ends session
    with smart_run(session, threaded=True):
        # configurations to maximize instagram traffic
        session.set_quota_supervisor(
          enabled=True, 
          sleep_after=["likes_h", "server_calls_h"], 
          sleepyhead=True, 
          stochastic_flow=True, 
          notify_me=True, 
          peak_likes_hourly=66, 
          peak_likes_daily=585,
          peak_server_calls_hourly=None, 
          peak_server_calls_daily=4700
        )
        session.set_blacklist(enabled=True, campaign='influencer_campaign')
        session.set_simulation(enabled=True, percentage=66.6)
        session.set_do_like(enabled=True, percentage=66.6)
        # list of influencers to interact with by liking 
        session_list = session.target_list('static/txt/influencers.txt')
        session.interact_by_users(session_list, amount=3, randomize=True)
"""
  Hash-Tags:
    - hashtags.txt (list of hashtags)
    - job schedule: 
"""
def job_hastag():
    # create session to login and automate using instapy api
    session = InstaPy(
      username=instapy_username, 
      password=instapy_password, 
      headless_browser=True)
    # while smart_run performs tasks and ends session
    with smart_run(session, threaded=True):
        # configurations to maximize instagram traffic
        session.set_quota_supervisor(
          enabled=True, 
          sleep_after=["likes_h", "server_calls_h"], 
          sleepyhead=True, 
          stochastic_flow=True, 
          notify_me=True, 
          peak_likes_hourly=66, 
          peak_likes_daily=585,
          peak_server_calls_hourly=None, 
          peak_server_calls_daily=4700
        )
        session.set_blacklist(enabled=True, campaign='hashtag_campaign')
        session.set_simulation(enabled=True, percentage=66.6)
        session.set_do_like(enabled=True, percentage=66.6)
        # list of hashtags to interact with by liking 
        session_list = session.target_list('static/txt/hashtags.txt')
        session.like_by_locations(session_list, amount=1, randomize=True)
"""
  Locations:
    - locations.txt (list of locations)
    - job schedule: 
"""
def job_location():
    # create session to login and automate using instapy api
    session = InstaPy(
      username=instapy_username, 
      password=instapy_password, 
      headless_browser=False)
    # while smart_run performs tasks and ends session
    with smart_run(session, threaded=True):
        # configurations to maximize instagram traffic
        session.set_quota_supervisor(
          enabled=True, 
          sleep_after=["likes_h", "server_calls_h"], 
          sleepyhead=True, 
          stochastic_flow=True, 
          notify_me=True, 
          peak_likes_hourly=66, 
          peak_likes_daily=585,
          peak_server_calls_hourly=None, 
          peak_server_calls_daily=4700
        )
        session.set_blacklist(enabled=True, campaign='hashtag_campaign')
        session.set_simulation(enabled=True, percentage=66.6)
        session.set_do_like(enabled=True, percentage=66.6)
        # list of locations to interact with by liking 
        session_list = session.target_list('static/txt/locations.txt')
        session.like_by_locations(session_list, amount=1)
# # everyday start at 8:00 AM, run for 1 hour
# schedule.every().day.at("8:00").do(job_influencer)
# schedule.every().day.at("14:00").do(job_influencer)
# # sleep 1 hour, start hashtag job for 1 hour
# schedule.every().day.at("10:00").do(job_hastag)
# schedule.every().day.at("16:00").do(job_hastag)
# # sleep 1 hour, start location job for 1 hour
# schedule.every().day.at("12:00").do(job_location)
# schedule.every().day.at("18:00").do(job_location)
# # run schedule jobs
def start_process():
    schedule.every().day.at("18:53").do(job_influencer)
    while True:
        schedule.run_pending()
        time.sleep(1)