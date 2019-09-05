from collections import Counter
from konlpy.tag import Twitter
import operator
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

class analysis:
    def __init__(self):
        # self.dataset = {}
        # self.count
        self.h = Twitter()

    def load_windows(self, filename):
        dic = {}
        try:
            with open(filename, 'r', encoding='UTF8') as raw_file:
                lines = raw_file.readlines()
                for l in lines:
                    if l[0] == '[': # 대화내용
                        name = l[1:l.index(']')]
                        temp = l[l.index(']')+1:]
                        chat = temp[temp.index(']')+2:]
                        if not name in dic.keys():
                            dic[name] = ''
                        dic[name] += chat
        except:
            print('파일 불러오기 실패')
            return {}
        return dic

    def load_android(self, filename):
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
        except Exception as e:
            print(e)
            return {}
        return dic

    def load_macintosh(self, filename):
        dic = {}
        try:
            data = pd.read_csv(filename, encoding='UTF8')
            for name, chat in zip(data['User'], data['Message']):
                if not name in dic.keys():
                    dic[name] = ''
                dic[name] += chat
        except:
            print('파일 불러오기 실패')
            return {}
        return dic

    def load_iphone(self, filename):
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
            return {}
        return dic

    def fileload(self, filename, os=1):
        if os == 1:
            dic = self.load_windows(filename)
        elif os == 2:
            dic = self.load_macintosh(filename)
        elif os == 3:
            dic = self.load_android(filename)
        elif os == 4:
            dic = self.load_iphone(filename)
        if dic:
            self.dataset = dic
        else:
            print('파일 로드 실패')
            return False
        return True

    def analysis(self, name):
        if name == '':
            s = ''
            for key in self.dataset.keys():
                s += self.dataset[key]
            nouns = self.h.nouns(s)
        else:
            nouns = self.h.nouns(self.dataset[name])
        count = Counter(nouns)
        self.count = count

    def write_wordcloud(self):
        # tag = count.most_common(50)
        # taglist = pytagcloud.make_tags(tag, maxsize=60)
        # pprint(taglist)
        # pytagcloud.create_tag_image(taglist, 'wordcloud.jpg', size=(900, 600), fontname='korean', rectangular=False)
        count = self.count
        wordcloud = WordCloud(
            width=600, 
            height=600, 
            font_path='C:\Windows\Fonts\맑은 고딕\malgunsl.ttf',
            background_color='white'
        )
        wordcloud = wordcloud.generate_from_frequencies(count)
        array = wordcloud.to_array()
        fig = plt.figure(figsize=(8, 8))
        plt.imshow(array, interpolation="bilinear")
        plt.axis('off')
        plt.show()
        # fig.savefig('wordcloud.png')