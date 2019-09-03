import pandas as pd

dic = {}
data = pd.read_csv('C:\python workspace\kakaotalk_analysis\\asset\dataset\mac1.csv', encoding='UTF8')
for name, chat in zip(data['User'], data['Message']):
    # print(name, chat)
    if not name in dic.keys():
        dic[name] = ''
    dic[name] += ' ' + chat

print(dic)