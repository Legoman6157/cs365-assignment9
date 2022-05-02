# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 23:21:37 2022

Every apostrophe EXCEPT "A HERMIT'S WILD FRIENDS" needed to be changed

@author: joaby
"""

from bs4 import BeautifulSoup
import requests
import re
from collections import Counter

if __name__ == '__main__':
    o_file = open("outfile.txt", "w")
    url_file = open("sitesToScrap.csv", "r")
    url_file_line = url_file.readline()
    MATCH_STRING = "[,\"\.&\|:@<>\(\)\*\$\?\!\\\/;=”“‘\[\]0-9—]"

    book_urls_and_titles = []
    book_word_lists = []
    i = 1
    word_instance_dict = {}

    while len(url_file_line) != 0:
        temp_word_list = []

        url_string_and_title = url_file_line.split(',')

        url_string = url_string_and_title[0]
        title = url_string_and_title[1]

        title = title.strip('\n')
        if title != "A Hermit's Wild Friends":
            title = title.replace("'", "’")

        book_urls_and_titles.append( (url_string, title) )

        print('-'*81 + '\n')

        print("URL: " + url_string + '\n')
        print("Title: " + title + '\n')

        starting_string = "*** START OF THE PROJECT GUTENBERG EBOOK " + \
                            title.upper() + " ***"
        ending_string = "*** END OF THE PROJECT GUTENBERG EBOOK " + \
                            title.upper() + " ***"

        page = requests.get(url_string)
        body = BeautifulSoup(page.content, "html.parser").find("body")

        reading_story = False

        for tag in body:
            if not reading_story:
                if tag.text == starting_string:
                    reading_story = True
            else:
                if tag.text == ending_string:
                    break

                string = tag.text
                string = re.sub(MATCH_STRING, " ", string)
                temp_word_list.extend(string.lower().split())
                for word in temp_word_list:
                    if word in word_instance_dict:
                        if title not in word_instance_dict[word]:
                            word_instance_dict[word].append(title)
                    else:
                        word_instance_dict[word] = [title]

        o_file.write('-'*81 + '\n')

        book_word_lists.append(temp_word_list)

        url_file_line = url_file.readline()
        i = 0

    url_file.close()