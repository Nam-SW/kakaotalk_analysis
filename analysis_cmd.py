from collections import Counter
from konlpy.tag import Twitter
# from sys import exit
import operator
# import pytagcloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import csv

# from pprint import pprint

def load_windows(filename):
    dic = {}
    try:
        with open(filename, 'r', encoding='UTF8') as raw_file:
            lines = raw_file.readlines()
            for l in lines:
                if l[0] == '[': # 대화내용
                    name = l[1:l.index(']')]
                    temp = l[l.index(']')+1:]
                    chat = temp[temp.index(']')+2:]
                    if not n in dic.keys():
                        dic[name] = ''
                    dic[name] += chat
    except:
        print('파일 불러오기 실패')
        exit(1)
    return dic

def load_android(filename):
    dic = {}
    try:
        with open(filename, 'r', encoding='UTF8') as raw_file:
            lines = raw_file.readlines()
            for l in lines:
                if l[0] == '2' and l.count(':') >= 2: # 대화내용
                    start = l.index(',')+2
                    end = start + l[start:].index(':')-1
                    name = l[start:end]
                    chat = l[end+3:]
                    if not name in dic.keys():
                        dic[name] = ''
                    dic[name] += chat
    except:
        print('파일 불러오기 실패')
        exit(1)
    return dic

def load_macintosh(filename):
    return

def load_iphone(filename):
    dic = {}
    try:
        with open(filename, 'r', encoding='UTF8') as raw_file:
            lines = raw_file.readlines()
            for l in lines:
                if l[0] == '2' and l.count(':') >= 2 and ',' in l: # 대화내용
                    start = l.index(',')+2
                    end = start + l[start:].index(':')-1
                    name = l[start:end]
                    chat = l[end+3:]
                    if not name in dic.keys():
                        dic[name] = ''
                    dic[name] += chat
    except:
        print('파일 불러오기 실패')
        exit(1)
    return dic


def fileload(filename):
    dic = {}
    os = input('윈도우1, 안드로이드2, 맥3, 아이폰4: ')
    if os == '1':
        dic = load_windows(filename)
    elif os == '2':
        dic = load_android(filename)
    elif os == '4':
        dic = load_iphone(filename)
    return dic
    
    

def analysis(dic, name):
    h = Twitter()
    if name == '':
        s = ''
        for key in dic.keys():
            s += dic[key]
        nouns = h.nouns(s)
    else:
        nouns = h.nouns(dic[name])
    count = Counter(nouns)
    return count

def write_wordcloud(count):
    # tag = count.most_common(50)
    # taglist = pytagcloud.make_tags(tag, maxsize=60)
    # pprint(taglist)
    # pytagcloud.create_tag_image(taglist, 'wordcloud.jpg', size=(900, 600), fontname='korean', rectangular=False)
    wordcloud = WordCloud(
        width=600, 
        height=600, 
        font_path='C:\Windows\Fonts\맑은 고딕\malgunsl.ttf',
        background_color='white'
        )
    wordcloud = wordcloud.generate_from_frequencies(count)
    array = wordcloud.to_array()
    fig = plt.figure(figsize=(10, 10))
    plt.imshow(array, interpolation="bilinear")
    plt.axis('off')
    fig.savefig('wordcloud.png')

# --------main---------
def main():
    dic = fileload(input('분석할 카카오톡 파일의 경로와 이름+확장자:'))
    count = analysis(dic, input('분석할 이름 입력. 공백시 전체 분석:'))

    talk_rank = sorted(count.items(), key=operator.itemgetter(1), reverse=True)
    print('가장 많이 한 말 top 20')
    for i in range(20):
        print(i+1, '.', talk_rank[i][0], ':', talk_rank[i][1])
    
    write_wordcloud(count)
    


if __name__ == '__main__':
    main()