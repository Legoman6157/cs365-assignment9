# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 23:21:37 2022

Every apostrophe EXCEPT "A HERMIT'S WILD FRIENDS" needed to be changed

@author: joaby
"""

from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':
    # url_file = open("sitesToScrap.csv", "r")
    # url_file_line = url_file.readline()

    # while len(url_file_line) != 0:
        # url_string_and_title = url_file_line.split(',')

        # url_string = url_string_and_title[0]
        # title = url_string_and_title[1]

    url_string = "https://www.gutenberg.org/files/4980/4980-h/4980-h.htm"
    title = "OLD GRANNY FOX"

    title = title.strip('\n')
    if title != "A Hermit's Wild Friends":
        title = title.replace("'", "’")

    starting_string = "*** START OF THE PROJECT GUTENBERG EBOOK " + \
                        title.upper() + " ***"
    ending_string = "*** END OF THE PROJECT GUTENBERG EBOOK " + \
                        title.upper() + " ***"

    page = requests.get(url_string)
    soup = BeautifulSoup(page.content, "html.parser")

    starting_div = soup.find("div", string=starting_string)
    ending_div = soup.find("div", string=ending_string)

    body = soup.find("body")

    starting_index = body.index(starting_div)
    ending_index = body.index(ending_div)

    line_num = 0
    for tag in body:
        print("{}: {} ({})".format(line_num, tag, type(tag)))
        line_num = line_num + 1

        # print('-'*81)

        # print("URL: " + url_string)
        # print("Title: " + title)

        # print("Starting line: " + starting_string)
        # print("Ending line: " + ending_string)

        # print(starting_div)

        # print('-'*81)

        # url_file_line = url_file.readline()

    # url_file.close()