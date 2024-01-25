import json
from gensim.models import FastText

def convertMs2String(milliseconds):
    import datetime
    dt = datetime.datetime.fromtimestamp(milliseconds )
    return dt


def convertJsonMessages2text(filename):
    with open(filename, "r", encoding="UTF8") as file:
        content = file.read()
    messages = json.loads(content)
    text = ""
    for m in messages:
        # text += f"{convertMs2String(m['date'])} {m['message_id']}  {m['user_id']} {m['reply_message_id']}  {m['text']}  <br>\n"
        text += f"{m['text']}\n"
    return text


def gen_model(data_filename, model_filename):
    with open(data_filename, encoding='utf-8') as f:
        flat_list = [line.split() for line in f]
        ft_mod = FastText(workers=8)
        ft_mod.build_vocab(flat_list)
        ft_mod.train(flat_list, total_examples=ft_mod.corpus_count, epochs=30)
        ft_mod.save(model_filename)
    del ft_mod


def getData(text):
    model_filename = 'model.model'
    ft_model = FastText.load(model_filename)
    count = 5
    res = ft_model.wv.most_similar(text, topn=count, restrict_vocab=5000)
    res1 = ft_model.wv.most_similar(res[0][0], topn=4, restrict_vocab=5000)
    res2 = ft_model.wv.most_similar(res[1][0], topn=4, restrict_vocab=5000)
    res3 = ft_model.wv.most_similar(res[2][0], topn=4, restrict_vocab=5000)
    res4 = ft_model.wv.most_similar(res[3][0], topn=4, restrict_vocab=5000)
    print(res)
    nodes=[]
    num=1
    for item in res:
        line={}
        line['id']=num
        line['name']=item[0]
        nodes.append(line)
        num+=1
    for item in res1:
        line={}
        line['id']=num
        line['name']=item[0]
        nodes.append(line)
        num+=1
    for item in res2:
        line={}
        line['id']=num
        line['name']=item[0]
        nodes.append(line)
        num+=1
    for item in res3:
        line={}
        line['id']=num
        line['name']=item[0]
        nodes.append(line)
        num+=1
    for item in res4:
        line={}
        line['id']=num
        line['name']=item[0]
        nodes.append(line)
        num+=1
    print(nodes)
    num=1    
    links=[]
    for item in res:
        line={}
        line['sid']=num
        line['tid']=num+1
        str1="{:.2f}".format(item[1])
        line['name']=str1
        links.append(line)
        num+=1
    num-=1
    for item in res1:
        line={}
        line['sid']=1
        line['tid']=num+1
        str1="{:.2f}".format(item[1])
        line['name']=str1
        links.append(line)
        num+=1
    # num-=2
    for item in res2:
        line={}
        line['sid']=2
        line['tid']=num+1
        str1="{:.2f}".format(item[1])
        line['name']=str1
        links.append(line)
        num+=1
    # num-=3
    for item in res3:
        line={}
        line['sid']=3
        line['tid']=num+1
        str1="{:.2f}".format(item[1])
        line['name']=str1
        links.append(line)
        num+=1
    # num-=4
    for item in res4:
        line={}
        line['sid']=4
        line['tid']=num+1
        str1="{:.2f}".format(item[1])
        line['name']=str1
        links.append(line)
        num+=1
    num-=5
    print(links)
    data={}
    data['links']=links
    data['nodes']=nodes
    jsonstring = json.dumps(data, ensure_ascii=False)
    return jsonstring

if __name__ == '__main__':
    # nltk_download()
    filename="d:/ml/chat/andromedica1.json"
    data_filename = './text.txt'
    model_filename = 'model.model'
    model_filename = 'D:/ML/ruscorpora_none_fasttextskipgram_300_2_2019/model.model'
    model_filename = 'D:/ML/araneum_none_fasttextskipgram_300_5_2018/araneum_none_fasttextskipgram_300_5_2018.model'
    model_filename = 'D:/ML/187/model.model'
    text = convertJsonMessages2text(filename)
    with open(data_filename, "w", encoding="UTF8") as file:
        file.write(text)
    gen_model(data_filename, model_filename)
