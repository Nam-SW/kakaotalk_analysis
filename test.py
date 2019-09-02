from collections import Counter
from konlpy.tag import Twitter
from sys import exit
import random
import operator
import pytagcloud

from pprint import pprint


def fileload(filename):
    dic = {}
    try:
        with open(filename, 'r', encoding='UTF8') as raw_file:
            lines = raw_file.readlines()
            for l in lines:
                if l[0] == '[': # 대화내용
                    n = l[1:l.index(']')]
                    t = l[l.index(']')+1:]
                    if not n in dic.keys():
                        dic[n] = ''
                    dic[n] += t[t.index(']')+2:]
    except:
        print('파일 불러오기 실패')
        exit(1)
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
    tag = count.most_common(50)
    taglist = pytagcloud.make_tags(tag, maxsize=60)
    # pprint(taglist)
    pytagcloud.create_tag_image(taglist, 'wordcloud.jpg', size=(600, 600), fontname='korean', rectangular=False)
    return

# --------main---------
def main():
    dic = fileload(input('분석할 카카오톡 파일의 경로와 이름+확장자:'))
    count = analysis(dic, input('분석할 이름 입력. 공백시 전체 분석:'))

    talk_rank = sorted(count.items(), key=operator.itemgetter(1), reverse=True)
    print('가장 많이 한 말 top 5')
    for i in range(5):
        print(i+1, '.', talk_rank[i][0], ':', talk_rank[i][1])
    
    write_wordcloud(count)
    


# C:\python workspace\kakaotalk_analysis\준표톡.txt
if __name__ == '__main__':
    main()