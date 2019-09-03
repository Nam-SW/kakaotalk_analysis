dic = {}
with open('C:\python workspace\kakaotalk_analysis\\asset\dataset\\android.txt', 'r', encoding='UTF8') as raw_file:
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
            print(name, chat)