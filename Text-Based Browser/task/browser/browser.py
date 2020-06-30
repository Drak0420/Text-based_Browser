from os import path, makedirs
import sys
from collections import deque
import bs4
from requests import get, exceptions
from colorama import init, Fore

init()


def text_getter(url):  # returns only text from url
    try:
        r = get(url)
    except exceptions.RequestException:
        return 'False'
    if r:  # Valid Response
        soup = bs4.BeautifulSoup(r.content, 'html.parser')
        for script in soup(['script', 'style']):  # Removes all CSS and JS from soup
            script.decompose()
        body = soup.find('body')
        text_tags = body.find_all(string=True)  # Finds only text tags
        new_text_tags = []

        # Finds all 'a' tags for colorizing
        a_tags = body.find_all('a', string=True)
        a_tags = [bs4.BeautifulSoup(str(val), 'html.parser').get_text() for val in a_tags]

        # Removes all \t and \n formatting and blank lines from text
        for i, word in enumerate(text_tags):
            text_tags[i] = word.replace('\t', '')
            text_tags[i] = text_tags[i].replace('\n', '')
            if text_tags[i] != '' and text_tags[i] != ' ':
                new_text_tags.append(text_tags[i])

        # Adds colorizing to new_text_tags if it is a <a> tag
        for i, val in enumerate(new_text_tags):
            if val in a_tags:
                new_text_tags[i] = Fore.BLUE + val + Fore.RESET
            else:
                new_text_tags[i] = val
        return '\n'.join(new_text_tags)  # Returns text in a string
    return 'False'


def main():
    new_stack = deque()  # Used for 'back' functionality
    args = sys.argv  # input from running of py file

    if args[1] != "":  # Sets directory for saved pages
        script_path = path.abspath('')
        new_path = path.join(script_path, args[1])
        if not path.exists(new_path):
            makedirs(new_path)

    while True:  # Constant running of input/output code
        url_input = input()

        # Sets var for url w/o .com/.org
        if url_input.endswith((".com", ".org")):
            new_url_input = url_input[:-4]
        else:
            new_url_input = url_input
        # Used for creating path for saved page
        file_path = "\\" + new_url_input + ".txt"
        file_path = path.join(new_path + file_path)

        if url_input == 'exit':
            exit()
        elif url_input == 'back':  # If there are pages to go back, print said previous page
            if len(new_stack) != 0:
                new_stack.pop()  # Remove current page
                print(new_stack[-1])
        elif '.' in url_input:  # Assume is website if there is a '.'
            if not url_input.startswith('https://'):
                url_input = 'https://' + url_input
            text = text_getter(url_input)  # Sets text to processed result
            if text == 'False':  # Invalid link
                print("Error 404: Website not found.")
            else:  # Print and save text
                print(text)
                new_stack.append(text)  # For 'back' input
                with open(file_path, "w", encoding='utf-8') as page:
                    page.write(text)
        else:
            try:
                # Tries to print text according to input from saved pages
                with open(file_path, "r+", encoding='utf-8') as page:
                    print(page.read())
                    new_stack.append(page.read())  # For 'back' input
            except FileNotFoundError:
                print("Error 404: Website not found.")


if __name__ == '__main__':
    main()
