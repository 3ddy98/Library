#!/usr/bin python3

from bs4 import BeautifulSoup as bs
import requests
import os
from tqdm import tqdm

url = "http://libgen.is/"
results = []
rows = []

def main():
    running = True
    while running == True:
        os.system("clear")
        banner()
        print("Type q to exit.")
        query = input("\n\nSearch query: ")
        if query == "q":
            running = False;
        else:
            print("Searching...")
            search_library(query)

def parse_results(search_page):
    results = []
    soup = bs(search_page,"html.parser")
    table = soup.select(".c")#selecting the table with results
    rows = table[0].find_all("tr")
    #Parsing html data and finding all table entries
    for row in rows:
        columns = row.find_all("td")
        temp = []
        for item in columns:
            item_text = item.get_text()
            temp.append(item_text)
        results.append(temp)
    #Presenting results
    print("\nResults")
    print("-"*10)
    column_index= [1,2,8,7]
    for rows in results:
        if(results.index(rows) != 0):
            print("\n",results.index(rows), ") ",end="")
        for i in column_index:
            if (i < column_index[len(column_index)-1]):
                if(i==1):
                    print('\033[0;32m'+rows[i]+'\033[0;31m'+'|'+ '\033[0;49m',end="")
                else:
                    print(rows[i]+ '\033[0;31m'+"|"+ '\033[0;49m',end="")
            else:
                print('\033[0;36m'+rows[i]+'\033[0;36m')

def download_book(link_list, filename):
    for link in link_list:
        page = connect_library(link)
        if(page.status_code == 200):
            soup = bs(page.text,"html.parser")
            dl_link = soup.find_all("a")
            print("Connecting....")
            dl = requests.get(dl_link[0].get('href'),allow_redirects=True,stream=True)
            content_length = int(dl.headers.get('content-length'))
            block_size = 1024
            t=tqdm(total=content_length,unit='iB',unit_scale=True)
            print("Downloading....")
            with open('books/'+filename+'.pdf','wb') as f:
                for data in dl.iter_content(block_size):
                    t.update(len(data))
                    f.write(data)
            break;


def choose_book(page):
    link_list = []
    soup = bs(page,"html.parser")
    table = soup.select(".c")#selecting the table with results
    rows = table[0].find_all("tr")
    while True:
        try:
            selection = int(input("\n\nInput Book Number: "))
            break;
        except:
            print("That was an invalid selection")

    if selection > 0 and  selection < len(rows)-1:
        chosen_item = rows[selection]
        item_columns = chosen_item.find_all("td")
        for i in range(9,13): #hardcoded the columns where the links are located
            link_list.append(item_columns[i].find('a').get('href'))
        download_book(link_list,item_columns[2].get_text())
    else:
        print("Invalid Selection",selection)
        input("Enter to Continue")

def search_library(query):
    search_base="http://libgen.is/search.php?req="
    query_phpified = query.replace(' ','%')
    search_page = connect_library(search_base+query_phpified+"?")
    parse_results(search_page.content)
    choose_book(search_page.content)

def banner():
    banner = open("banner.txt")
    for lines in banner:
        print(lines,end="")

def connect_library(url):
    page = requests.get(url)
    if(page.status_code==200):
        return page;
    else:
        print("That item doesnt exist")

if __name__ == "__main__":
    main()
