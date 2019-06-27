from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import collections
import indexFormation
import settings

def generateTokens(input_string):
    tokens = []
    temp = ''
    for c in input_string:
        if(c.isdigit() or ord('a') <= ord(c) <= ord('z') or ord('A') <= ord(c) <= ord('Z')):
            temp += c.lower()
        elif(temp != ''):
            tokens.append(temp)
            temp = ''
    if(temp != ''):
        tokens.append(temp)
    return tokens


def tag_visible(element):
    if element.parent.name in ['style', 'script']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def formTokenLists(raw_list):
    raw_list_temp = []
    for i in raw_list:
        raw_list_temp.append(i.get_text())
    out = []
    for k in raw_list_temp:
        out.extend(generateTokens(k))
    out = list(set(out))
    return out


def heuristics():
    pass


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    title = formTokenLists(soup.find_all('title'))
    headers_1_2 = formTokenLists(soup.find_all(['h1', 'h2']))
    headers_3 = formTokenLists(soup.find_all(['h3']))
    body = formTokenLists(soup.find_all('body'))
    return (u" ".join(t.strip() for t in visible_texts),(headers_1_2,headers_3))


def get_token_freq(text):
    (page_string,(h_1_2,h3)) = text_from_html(text)
    tokens = generateTokens(page_string)
    token_freq = collections.Counter(tokens)
    for i in h_1_2:
        if(token_freq.get(i)):
            token_freq[i] += 1
        else:
            token_freq[i] = 1
    for i in h3:
        if(token_freq.get(i)):
            token_freq[i] += .75
        else:
            token_freq[i] = .75
    return token_freq


def write_to_file():
    indexFormation.addTokens(dict(),'', settings.batch_size-1)


def parserMain(text, code, file_no_mod):
    token_frequency = get_token_freq(text)
    if('' in token_frequency):
        del token_frequency['']
    token_frequency_ordered = {}
    
    ## Writing file term freq to json file
    settings.write_json('dump/file_tf/'+code+'.json', token_frequency, 'w+')

    from string import ascii_lowercase
    for c in ascii_lowercase:
        token_frequency_ordered[c] = {}
    for token in token_frequency:
        if token[0].isdigit():
            continue
        token_frequency_ordered[token[0]][token] = token_frequency[token]
    indexFormation.addTokens(token_frequency_ordered, code, file_no_mod)
    indexFormation.add_doc_freq(token_frequency.keys())