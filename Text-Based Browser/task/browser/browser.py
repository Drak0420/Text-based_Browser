import os
import sys
from collections import deque
import bs4
import requests
from colorama import init, Fore

init()


def text_getter(url):
    r = requests.get(url)
    if r:
        soup = bs4.BeautifulSoup(r.content, 'html.parser')
        for script in soup(['script', 'style']):
            script.decompose()
        body = soup.find('body')
        text_tags = body.find_all(string=True)
        new_text_tags = []
        a_tags = body.find_all('a', string=True)
        a_tags = [bs4.BeautifulSoup(str(val), 'html.parser').get_text() for val in a_tags]
        for i, word in enumerate(text_tags):
            text_tags[i] = word.replace('\t', '')
            text_tags[i] = text_tags[i].replace('\n', '')
            if text_tags[i] != '':
                new_text_tags.append(text_tags[i])
        for i, val in enumerate(new_text_tags):
            if val in a_tags:
                new_text_tags[i] = Fore.BLUE + val + Fore.RESET
            else:
                new_text_tags[i] = val
        return '\n'.join(new_text_tags)
    return 'False'


def main():
    new_stack = deque()
    args = sys.argv

    if args[1] != "":
        script_path = os.path.abspath('')
        print(script_path)
        new_path = os.path.join(script_path, args[1])
        if not os.path.exists(new_path):
            os.makedirs(new_path)
    
    while True:
        url_input = input()
        if url_input.endswith((".com", ".org")):
            new_url_input = url_input[:-4]
        else:
            new_url_input = url_input
    
        file_path = "\\" + new_url_input + ".txt"
        file_path = os.path.join(new_path + file_path)
    
        if url_input == 'exit':
            exit()
        elif url_input == 'back':
            if len(new_stack) != 0:
                new_stack.pop()
                print(text)
        elif '.' in url_input:
            if not url_input.startswith('https://'):
                url_input = 'https://' + url_input
            text = text_getter(url_input)
            if text == 'False':
                print("Error 404: Website not found.")
            else:
                print(text)
                new_stack.append(text)
                with open(file_path, "w", encoding='utf-8') as page:
                    page.write(text)
        else:
            try:
                with open(file_path, "r+", encoding='utf-8') as page:
                    print(page.read())
                    new_stack.append(page.read())
            except FileNotFoundError:
                print("Error 404: Website not found.")


if __name__ == '__main__':
    main()
