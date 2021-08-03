#!/usr/bin/env python3
import re
import os    
import webbrowser
import urllib, urllib.request
from bs4 import BeautifulSoup

MAX_NUM_RESULTS = 20
DOWNLOAD_DIR = os.path.join(os.getenv("HOME"), "papers")
if not os.path.isdir(DOWNLOAD_DIR):
    print("Download folder doesn't exist. Creating one...")
    os.mkdir(DOWNLOAD_DIR)

while(True):
    # Ask for the query
    query = input("What do you want to search on Arxive?\n")
    if query == "":
        os._exit(0)
    query = re.sub("\s+", "+", query.strip())

    # Get metadata of paper using API
    url = 'http://export.arxiv.org/api/query?search_query={}&start=0&max_results={}'.format(query, MAX_NUM_RESULTS)
    data = urllib.request.urlopen(url)
    xml = data.read().decode('utf-8')

    # Decode data using BS4
    soup = BeautifulSoup(xml, "lxml-xml")
    entries = soup.find_all("entry")
    counter = 0

    # List all entries
    for entry in entries:
        authors = [author.text.strip("\n") for author in entry.find_all("author")]
        print("[",counter,"] ", ", ".join(authors))
        print()
        print("\t", entry.title.text)
        print()
        print()
        print("\t", entry.summary.text)
        print("\tDOI: ", entry.link.attrs["href"])
        counter += 1
        print()
    
    # List options
    option = input("What now?\n[d<number>=Download, o<number>=Open in browser, m=more results in browser, otherwise exit]\n")
    if option != "" and option[0] in ["D", "d"]:
        # Download the paper as PDF
        try:
            entry_id = int(option[1:])
            pdf_url = entries[entry_id].find_all("link")[1].attrs["href"].replace("abs","pdf")
            arxiv_id = pdf_url[21:]
            response = urllib.request.urlopen(pdf_url+".pdf")
            with open(os.path.join(DOWNLOAD_DIR, arxiv_id + ".pdf"), "wb") as f:
                f.write(response.read())
        except:
            print("Incorrect input! Exiting...")
            os._exit(1)
    elif option != "" and option[0] in ["o", "O"]:
        # Open the paper in Webbrowser
        try:
            entry_id = int(option[1:])
            url = entries[entry_id].find_all("link")[0].attrs["href"]
            webbrowser.open_new_tab(url)
        except:
            print("Incorrect input! Exiting...")
            os._exit(1)
    elif option in ["m", "M"]:
        webbrowser.open_new_tab("https://arxiv.org/search/?query={}&searchtype=all&source=header".format(query))
    else:
        # Exit
        os._exit(0)

