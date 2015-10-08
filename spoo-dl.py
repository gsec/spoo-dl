#!/usr/bin/env python3
#coding: utf-8
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MOAARR South Park ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#     This is free software,
#     do whatever you want.
#     Except evil stuff!
###############################################################################
import re
import pickle
import requests
import subprocess
from bs4 import BeautifulSoup

main_url = "http://www.southpark.de/alle-episoden/"


def fetcher(url):
  r = requests.get(url)
  soup = BeautifulSoup(r.content, 'lxml')
  return soup


def extractor(results):
  links = []
  for item in results:
    sitem = str(item)
    if "href" in sitem:
      link = sitem.split('href="')[1].split('">')[0]
      if 'http' in link:
        links.append(link)
  return links


def walker():
  soup = fetcher(main_url)
  res_season  = soup.find_all('a', attrs={'class': re.compile(r'seasonbtn')})
  all_seasons = extractor(res_season)
  links = []
  for season in all_seasons:
    soup = fetcher(season)
    res_episodes = soup.find_all('h4')
    link_bundle = extractor(res_episodes)
    links.append(link_bundle)
  return links


def leecher():
  try:
    with open("all_links.txt", 'rb') as f:
      link_list = pickle.load(f)
  except(OSError):
    link_list = walker()
    with open("all_links.txt", 'wb') as f:
      pickle.dump(link_list, f)
  finally:
    for idx, season in enumerate(link_list):
      print("\n++++\nLeeching Season: ", idx+1, "\n====\n")
      for episode in season:
        print(episode)
        command = ['youtube-dl', '-o', '%(title)s.%(ext)s', episode]
        subprocess.call(command)


if __name__ == '__main__':
  leecher()
