# coding:utf-8

import csv, re
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
from bs4 import BeautifulSoup
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

print("Which file ?")
file = input('>> ')
print('------------')

def counter(texts):
    t = Tokenizer()
    words_count = defaultdict(int)
    words = []
    for text in texts:
        tokens = t.tokenize(text)
        for token in tokens:
            pos = token.part_of_speech.split(',')[0]
            if pos == '名詞':
                words_count[token.base_form] += 1
                words.append(token.base_form)
    return words_count, words

with open(file, 'r') as f:
    reader = csv.reader(f,delimiter='\t')
    texts = []
    for row in reader:
        if len(row) == 0:
            pass
        else:
            text = row[0].split('http')
            if len(text) == 0:
                pass
            else:
                texts.append(text[0])

words_count, words = counter(texts)
text = ' '.join(words)

#word cloud
fpath = "~/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc"

stop_words = [u'RT', u'屠殺', u'これ', u'さん',u'廃墟']

wordcloud = WordCloud(background_color="white", font_path=fpath, width=900, height=500, stopwords=set(stop_words)).generate(text)

print('successes')

plt.figure(figsize=(15,12))
plt.imshow(wordcloud)
plt.axis("off")
# plt.show()
plt.savefig(file + ".png")