#jbyers3
#Joshua Byers

from bs4 import BeautifulSoup
import requests
import re

if __name__ == '__main__':
    url_file = open("sitesToScrape.csv", "r")
    url_file_line = url_file.readline()
    MATCH_STRING = "[,\"\.&\|:@<>\(\)\*\$\?\!\\\/;=”“‘\[\]0-9—]"
    stopwords = ['ut', '\'re','.', ',', '--', '\'s','cf', '?', ')', '(', ':','\'','\"', '-', '}','â','£', '{', '&', '|', u'\u2014', '', ']' ]
    titles = []

    word_instance_dict = {}

    book_num = 0

    while len(url_file_line) != 0:

        url_string_and_title = url_file_line.split(',')

        url_string = url_string_and_title[0]
        title = url_string_and_title[1]

        title = title.strip('\n')
        
        #Every apostrophe EXCEPT "A Hermit's Wild Friends" needed to be
        #   changed
        if title != "A Hermit's Wild Friends":
            title = title.replace("'", "’")

        titles.append(title)

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
                temp_word_list = string.lower().split()

                try:
                    for word in stopwords:
                        temp_word_list.remove(word)
                except:
                    pass

                for word in temp_word_list:
                    if word in word_instance_dict.keys():

                        if title in word_instance_dict[word].keys():
                            num = word_instance_dict[word][title]
                            word_instance_dict[word][title] = num + 1

                        else:
                            word_instance_dict[word][title] = 1

                    else:
                        word_instance_dict[word] = {title: 1}

        print('-'*81 + '\n')

        url_file_line = url_file.readline()

        book_num = book_num + 1

    url_file.close()

    unique_word_instances = [(word, \
                              next(iter(word_instance_dict[word].values())), \
                             next(iter(word_instance_dict[word].keys()))) \
                             for word in word_instance_dict.keys() if \
                                 len(word_instance_dict[word]) == 1]
    final_list = {}
    for title in titles:
        words = [(instance[0], instance[1]) for instance in \
                 unique_word_instances if instance[2] == title]
        words = sorted(words, key=lambda x: x[1], reverse=True)

        final_list[title] = words

    for title in final_list:
        o_file = open(f"{title}.txt", "w")

        for i in range(0, 25):
            o_file.write("('{}', {})\n".format(final_list[title][i][0], \
                                               final_list[title][i][1]))

        o_file.close()
        