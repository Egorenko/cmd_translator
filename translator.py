import requests
from bs4 import BeautifulSoup
import sys


def translator(lng_1: str, lng_2: str, wrd: str):
    languages = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew',
                 'Japanese', 'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish']
    for num, lng in enumerate(languages):
        print(f'{num}: {lng}')
    lng_list = []
    if lng_2 != 'all':
        lng_list.append(lng_2.capitalize())
    else:
        lng_list = languages
        lng_list.remove(lng_1.capitalize())
    for language in lng_list:
        pair = f'{lng_1.lower()}-{language.lower()}'
        url = f'https://context.reverso.net/translation/{pair}/{wrd}'
        user_agent = 'Mozilla/5.0'
        r = requests.get(url, headers={'User-Agent': user_agent})
        if not r.status_code:
            print('Something wrong with your internet connection')
        else:
            with open(f'{wrd}.txt', 'a', encoding='utf-8') as output:
                print(f'{language} Translations: ', file=output)
                print(f'{language} Translations: ')
                soup = BeautifulSoup(r.content, 'html.parser')
                translates = soup.find_all('a', {'class': 'translation'})
                s = [i.text.replace('\n', '').replace('\r', '').strip() for i in translates[1:]]
                example = soup.find_all('div', attrs={'class': 'example'})
                e = []
                for i in example:
                    i = i.text.replace('\r', '').lstrip().split('\n\n\n\n\n')
                    for c in i:
                        if c != '' and c != '\n':
                            e.append(c.lstrip())
                if len(lng_list) == 1:
                    print('\n'.join(s), file=output)
                    print(f'{language} Examples: ', file=output)
                    print('\n'.join(f'{e[i]}\n{e[i + 1]}\n' for i in range(0, len(e) - 1, 2)), file=output)
                    print('\n'.join(s))
                    print(f'{language} Examples: ')
                    print('\n'.join(f'{e[i]}\n{e[i + 1]}\n' for i in range(0, len(e) - 1, 2)))
                else:
                    print(s[0], file=output)
                    print(file=output)
                    print(f'{language} Examples: ', file=output)
                    print(e[0], e[1], '\n', sep='\n', file=output)
                    print(s[0])
                    print()
                    print(f'{language} Examples: ')
                    print(e[0], e[1], '\n', sep='\n')


args = sys.argv
language_1 = args[1]
language_2 = args[2]
word = args[3]
languages = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew',
             'Japanese', 'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish']
if language_1.capitalize() not in languages:
    print(f"Sorry, the program doesn't support {language_1}")
elif language_2.capitalize() not in languages and language_2 != 'all':
    print(f"Sorry, the program doesn't support {language_2}")
else:
    pair = f'{language_1.lower()}-{language_2.lower()}' if language_2 != 'all' else f'{language_1.lower()}-polish'
    url = f'https://context.reverso.net/translation/{pair}/{word}'
    user_agent = 'Mozilla/5.0'
    r = requests.get(url, headers={'User-Agent': user_agent})
    if not r.status_code:
        print('Something wrong with your internet connection')
    else:
        soup = BeautifulSoup(r.content, 'html.parser')
        translates = soup.find_all('a', {'class': 'translation'})
        s = [i.text.replace('\n', '').replace('\r', '').strip() for i in translates[1:]]
        if not s:
            print(f'Sorry, unable to find {word}')
        else:
            print("Hello, you're welcome to the translator. Translator supports:")
            translator(language_1, language_2, word)
