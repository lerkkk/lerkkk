from pathlib import Path
import re
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords
import pandas as pd
import os
from gensim.models import FastText
from gensim.test.utils import common_texts


def gen_model():
    name = 'test'
    corpList = pd.read_csv(f'corpuses/{name}.csv', names=['safeguards_txt'],
                            encoding='utf-8')
    #Подготовка файла и обучение модели
    i = 0
    with open(f'corpuses/txt-{name}.txt', 'a+', encoding='utf-8') as f:
        for line in corpList.values:
            if (i != 0) & (str(line[0]) != 'nan'):
                s1 = re.sub("[',]", "", str(line[0]))
                s1 = s1.replace("[", "");
                s1 = s1.replace("]", "");
                f.write((s1 + '\n'))
            i = i + 1

    with open(f'corpuses/txt-{name}.txt', encoding='utf-8') as f:
        flat_list = [line.split() for line in f]
        ft_mod = FastText(workers=8)
        ft_mod.build_vocab(flat_list)
        ft_mod.train(flat_list, total_examples=ft_mod.corpus_count, epochs=30)
        ft_mod.save(f'model/{name}.model')
    # os.remove(f'corpuses/txt-{name}.txt')
    del ft_mod

def get_fasttextclassifier():

    textList = pd.read_csv('static/texts/' + data['textList'], names=['safeguards_txt'], error_bad_lines=False,
                            encoding='utf-8')



    ft_mod = FastText.load('static/model/' + data['modelList'])

    wordMas = data['words'].split(" ")

    # проходимся по текстам
    i = 0
    flag = 0
    exitMas = []
    el_dict = {}
    with open('result.txt', 'w', encoding='utf-8') as file:
        for line in textList.values:
            if (i != 0) & (str(line[0]) != 'nan'):
                s1 = re.sub("[',]", "", str(line[0]))
                s1 = s1.replace("[", "");
                s1 = s1.replace("]", "");
                textMas = s1.split(" ")
                for word in wordMas:
                    for text in textMas:
                        compare = ft_mod.wv.similarity(text, word)
                        if compare > compare_value:
                            if flag == 0:
                                el_dict['text'] = s1
                                for elWord in wordMas:
                                    el_dict[elWord] = 0
                                file.write((s1 + '\n'))
                                flag = 1
                            el_dict[word] = el_dict[word] + 1
                            file.write(('text: ' + text + '\n'))
                            file.write(('word: ' + word + '\n'))
                            file.write(('compare' + str(compare) + '\n'))

                flag = 0
                if el_dict != {}:
                    exitMas.insert(len(exitMas), el_dict)
                    el_dict = {}
            i = i + 1
    print(exitMas)

if __name__ == "__main__":
    gen_model()
    
    # ft_mod.wv.similarity(text, word)