import os
import sys
import random
import json
import argparse
import jieba
from chardet import detect
from bs4 import BeautifulSoup
import math

def get_xml_list(path):
    xml_file_list=[]
    for path,dirs,files in os.walk(data_path):
        for f in files:
            if f.endswith(".xml"):
                xml_file_list.append(os.path.join(path,f))
    return xml_file_list

punctuation="。，、＇：∶；?‘’“”〝〞ˆˇ﹕︰﹔﹖﹑·¨….¸;！´？！～—ˉ｜‖＂〃｀@﹫¡¿﹏﹋﹌︴々﹟#﹩$﹠&﹪%*﹡﹢﹦﹤‐￣¯―﹨ˆ˜﹍﹎+=<­­＿_-\ˇ~﹉﹊（）〈〉‹›﹛﹜『』〖〗［］《》〔〕{}「」【】︵︷︿︹︽_﹁﹃︻︶︸﹀︺︾ˉ﹂﹄︼\n\r\t\"';:,<.>/?-_=+()*&^%$#@!`~"
chinese={}
unique_id=0
stopwords=open("../hit_stopwords.txt","r").read().split('\n')

def parse_xml(file_name):
    try:
        soup=BeautifulSoup(open(file_name,"r").read(),"html.parser")
    except:
        try:
            encoding=detect(open(file_name,"rb+").read())["encoding"]
            soup=BeautifulSoup(open(file_name,"r",encoding=encoding).read(),"html.parser")
        except:
            return None
    ret={}
    for node in soup.descendants:
        if "attrs" not in dir(node):
            continue
        if "value" in node.attrs.keys():
            content=node["value"]
        elif node.string:
            content=node.string
        else:
            continue
        key=node.name.upper()
        if "namecn" in node.attrs.keys():
            chinese[key]=node["namecn"]
        if key in ret:
            # if type(ret[key]) is not list:
            #     ret[key]=[ret[key]]
            ret[key].append(content)
        else:
            ret[key]=[content]
    
    text_file=file_name[:-4]+".txt"
    # if os.path.isfile(text_file):
    #     ret["QW"]=open(text_file,"r").read()
    
    tmp,ret=ret,{}
    if "LB" in tmp: # authoritative case
        ret["LB"]=tmp["LB"][0]
        ret["AJLB"]=list(set(tmp["AJLB"]))
        ret["XZQH_P"]=tmp["XZQH_P"][0] if "XZQH_P" in tmp else "Unknown"
        ret["LAND"]=tmp["LAND"][0] if "LAND" in tmp else (tmp["JAND"][0] if "JAND" in tmp else "Unknown")
        ret["JBFY"]=tmp["JBFY"][0] if "JBFY" in tmp else None
        ret["LY"]=tmp["LY"][0] if "LY" in tmp else None
        ret["TITLE"]=tmp["TITLE"][0]

        ret["QW"]=tmp["QW"][0]
    else: # common case
        try:
            ret["AJLB"]=list(set(tmp["AJLB"]))
            ret["XZQH_P"]=tmp["XZQH_P"][0] if "XZQH_P" in tmp else "Unknown"
            ret["FYJB"]=tmp["FYJB"][0] if "FYJB" in tmp else "Unknown"
            ret["LAND"]=tmp["LAND"][0] if "LAND" in tmp else (tmp["JAND"][0] if "JAND" in tmp else "Unknown")
            ret["SPCX"]=tmp["SPCX"][0] if "SPCX" in tmp else "Unknown"
            ret["WSZL"]=tmp["WSZL"][0] if "FYJB" in tmp else "Unknown"

            ret["JBFY"]=tmp["JBFY"][0] if "JBFY" in tmp else None
            
            ret["AH"]=tmp["AH"][0]
            ret["LKRQ"]=tmp["LKRQ"][0] if "LKRQ" in tmp else tmp["CPSJ"][0]

            ret["DSR"]='\n'.join(tmp["DSR"][0].split(' ')) if "DSR" in tmp else ""
            ret["SSJL"]='\n'.join(tmp["SSJL"][0].split(' ')) if "SSJL" in tmp else ""
            ret["AJJBQK"]='\n'.join(tmp["AJJBQK"][0].split(' ')) if "AJJBQK" in tmp else ""
            ret["CPFXGC"]='\n'.join(tmp["CPFXGC"][0].split(' ')) if "CPFXGC" in tmp else ""
            ret["PJJG"]='\n'.join(tmp["PJJG"][0].split(' ')) if "PJJG" in tmp else ""
            ret["WW"]='\n'.join(tmp["WW"][0].split(' ')) if "WW" in tmp else ""

            ret["QSAH"]=list(set(tmp["QSAH"])) if "QSAH" in tmp else [ret["AH"]]

            ret["QW"]=tmp["QW"][0]
        except:
            return None
    global unique_id
    ret["unique-id"]=str(unique_id)
    unique_id+=1

    return ret

def validate(data):
    # require=["QW","XZQH_P","AJLB","LAND",""]
    return True

class ReverseIndex:
    def __init__(self):
        self.a={}
    
    def add(self,word,tf,unique_id):
        if word not in self.a:
            self.a[word]=[]
        self.a[word].append([unique_id,tf])

    def dump(self,idf,output_path):
        stamp=0
        os.makedirs(os.path.join(output_path,"reverse_index"),exist_ok=True)
        cnt=0
        tmp4dump={}
        for word,curr_idf in sorted(list(idf.items()),reverse=False,key=lambda x:x[1]):
            if word not in self.a:
                continue
            curr_arr=self.a[word]
            curr_arr.sort(key=lambda x:x[1],reverse=True)
            for i in range(len(curr_arr)):
                curr_arr[i][1]*=curr_idf
            cnt+=len(curr_arr)
            tmp4dump[word]=curr_arr
            if cnt>1e7:
                cnt=0
                json.dump(tmp4dump,open(os.path.join(output_path,"reverse_index","{}.json".format(stamp)),"w"),ensure_ascii=False)
                stamp+=1
                tmp4dump={}
        if tmp4dump:
            json.dump(tmp4dump,open(os.path.join(output_path,"reverse_index","{}.json".format(stamp)),"w"),ensure_ascii=False)
        json.dump(idf,open(os.path.join(output_path,"reverse_index","idf.json".format(stamp)),"w"),ensure_ascii=False)
        

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', '-p', help="data path", required=True)
    parser.add_argument('--length', '-l', help="single file length", type=int, default=500)
    parser.add_argument('--output', '-o', help="output path", default='./data/')
    args = parser.parse_args()

    data_path=args.path
    file_length=max(args.length,1)
    output_path=args.output

    os.makedirs(os.path.join(output_path,"authoritative_data"),exist_ok=True)
    os.makedirs(os.path.join(output_path,"common_case_data"),exist_ok=True)

    xml_file_list=get_xml_list(data_path)
    
    # random.shuffle(data)

    c_data=[]
    a_data=[]
    stamp_c=0
    stamp_a=0
    indexes_c={}
    indexes_a={}
    c_rindex=ReverseIndex()
    a_rindex=ReverseIndex()
    idf={}
    total_number=0
    len_xml_file_list=len(xml_file_list)
    for i,xml_file_name in enumerate(xml_file_list):
        print("{} / {} (actual number = {})".format(i,len_xml_file_list,total_number),end="\r")
        # try:
        curr_obj=parse_xml(xml_file_name)
        # except:
        #     continue
        if curr_obj is None or not validate(curr_obj):
            continue
        QW_text=curr_obj["QW"]
        for ch in punctuation:
            QW_text=QW_text.replace(ch,' ')
        word_list=list(filter(lambda w:w not in stopwords,jieba.cut(QW_text,cut_all=True)))
        curr_obj["tokens"]=word_list
        
        if "LB" in curr_obj:
            a_data.append(curr_obj)
        else:
            curr_obj.pop("QW")
            c_data.append(curr_obj)
        total_number+=1
        if len(a_data)>=file_length:
            fname="{}.json".format(stamp_a)
            indexes_a[fname]=[int(a_data[0]["unique-id"]),int(a_data[-1]["unique-id"])]
            json.dump(a_data,open(os.path.join(output_path,"authoritative_data",fname),"w"),indent=2,ensure_ascii=False)
            a_data=[]
            stamp_a+=1
        if len(c_data)>=file_length:
            fname="{}.json".format(stamp_c)
            indexes_c[fname]=[int(c_data[0]["unique-id"]),int(c_data[-1]["unique-id"])]
            json.dump(c_data,open(os.path.join(output_path,"common_case_data",fname),"w"),indent=2,ensure_ascii=False)
            c_data=[]
            stamp_c+=1
        
        n=len(word_list)
        word_tf={w:0 for w in word_list}
        for w in word_list:
            word_tf[w]+=1/n
        if "LB" in curr_obj:
            for w in word_tf.keys():
                a_rindex.add(w,word_tf[w],curr_obj["unique-id"])
        else:
            for w in word_tf.keys():
                c_rindex.add(w,word_tf[w],curr_obj["unique-id"])
        for w in word_tf.keys():
            if w not in idf:
                idf[w]=0
            idf[w]+=1
    
    if a_data:
        fname="{}.json".format(stamp_a)
        indexes_a[fname]=[int(a_data[0]["unique-id"]),int(a_data[-1]["unique-id"])]
        json.dump(a_data,open(os.path.join(output_path,"authoritative_data",fname),"w"),indent=2,ensure_ascii=False)
    if c_data:
        fname="{}.json".format(stamp_c)
        indexes_c[fname]=[int(c_data[0]["unique-id"]),int(c_data[-1]["unique-id"])]
        json.dump(c_data,open(os.path.join(output_path,"common_case_data",fname),"w"),indent=2,ensure_ascii=False)
    
    json.dump(indexes_a,open(os.path.join(output_path,"authoritative_data","indexes.json"),"w"),indent=2,ensure_ascii=False)
    json.dump(indexes_c,open(os.path.join(output_path,"common_case_data","indexes.json"),"w"),indent=2,ensure_ascii=False)

    for w in idf.keys():
        idf[w]=math.log(total_number/idf[w])
    a_rindex.dump(idf,os.path.join(output_path,"authoritative_data"))
    c_rindex.dump(idf,os.path.join(output_path,"common_case_data"))

    print("{} / {} (actual number = {})".format(i,len_xml_file_list,total_number))

    json.dump(chinese,open(os.path.join(output_path,"chinese.json"),"w"),indent=2,ensure_ascii=False)