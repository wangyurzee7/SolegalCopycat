import json

def init():
    global a_data
    global c_data
    a_data=json.load(open("data/authoritative_data/0.json","r"))
    c_data=json.load(open("data/common_case_data/0.json","r"))


'''
search_authoritative(keyword, condition, page)
[ Description ] Search authoritative cases.
[ Params ]
* keyword : A string, search keyword.
* condition : A dict, describing the screening condition:
    * condition["type"] : A string. Type of authoritative case. Stored in field `LB`.
    * condition["cause_of_action"] : A string list. Cause of action of the case. Stored in field `AJLB` (as a list). Notice that each case may have multiple causes.
    * condition["region"] : A string. Source region of the case. Stored in field `XZQH_P`.
    * condition["year"] : A string. Year of the case. Stored in field `LAND`.
* page : An integer, page number. Default as 1.
* page_size : The number of cases per page. Default as 20.
[ Return Value ] A list, containing all search results' origin JSON object.
'''
def search_authoritative(keyword, condition, page, page_size):
    global a_data
    arr=[]
    for d in a_data:
        if ("type" in condition) and (condition["type"]!=d["LB"]):
            continue
        if ("cause_of_action" in condition):
            flag=True
            for _ in condition["cause_of_action"]:
                if _ not in d["AJLB"]:
                    flag=False
                    break
            if not flag:
                continue
        if ("region" in condition) and (condition["region"]!=d["XZQH_P"]):
            continue
        if ("year" in condition) and (condition["year"]!=d["LAND"]):
            continue
        cnt=0
        for v in d.values():
            try:
                if keyword in v:
                    cnt+=1
            except:
                pass
        if cnt>0:
            arr.append((d,cnt))
    arr.sort(key=lambda x:x[1],reverse=True)
    ret=[a[0] for a in arr]
    return ret[(page-1)*page_size:page*page_size]

'''
search_common(keyword, condition, page)
[ Description ] Search common cases.
[ Params ]
* keyword : A string, search keyword.
* condition : A dict, describing the screening condition:
    * condition["cause_of_action"] : A string list. Cause of action of the case. Stored in field `AJLB` (as a list). Notice that each case may have multiple causes.
    * condition["region"] : A string. Source region of the case. Stored in field `XZQH_P`.
    * condition["court_level"] : A string. Level of court. Stored in field `FYJB`.
    * condition["year"] : A string. Year of the case. Stored in field `LAND`.
    * condition["judicial_procedure"] : A string. Judicial procedure of the case. Stored in field `SPCX`.
    * condition["document_type"] : A string. Type of legal instrument. Stored in field `WSZL`.
* page : An integer, page number. Default as 1.
* page_size : The number of cases per page. Default as 20.
[ Return Value ] A list, containing all search results' origin JSON object.
'''
def search_common(keyword, condition, page, page_size):
    global c_data
    arr=[]
    for d in c_data:
        if ("cause_of_action" in condition):
            flag=True
            for _ in condition["cause_of_action"]:
                if _ not in d["AJLB"]:
                    flag=False
                    break
            if not flag:
                continue
        if ("region" in condition) and (condition["region"]!=d["XZQH_P"]):
            continue
        if ("court_level" in condition) and (condition["court_level"]!=d["FYJB"]):
            continue
        if ("year" in condition) and (condition["year"]!=d["LAND"]):
            continue
        if ("judicial_procedure" in condition) and (condition["judicial_procedure"]!=d["SPCX"]):
            continue
        if ("document_type" in condition) and (condition["document_type"]!=d["WSZL"]):
            continue
        cnt=0
        for v in d.values():
            try:
                if keyword in v:
                    cnt+=1
            except:
                pass
        if cnt>0:
            arr.append((d,cnt))
    arr.sort(key=lambda x:x[1],reverse=True)
    ret=[a[0] for a in arr]
    return ret[(page-1)*page_size:page*page_size]

'''
get_authoritative_case_by_unique_id(unique_id)
[ Description ] Get authoritative case's origin JSON object by unique id.
[ Params ]
* unique_id : A string, the unique id, should be matched with field `unique-id`.
[ Return Value ] A dict, result's origin JSON object. If there's no case matched, return None.
'''
def get_authoritative_case_by_unique_id(unique_id):
    global a_data
    for d in a_data:
        if d["unique-id"]==unique_id:
            return d
    return None

'''
get_common_case_by_reference_number(reference_number)
[ Description ] Get common case's origin JSON object by reference number.
[ Params ]
* reference_number : A string, the reference number, should be matched with field `AH`.
[ Return Value ] A dict, result's origin JSON object. If there's no case matched, return None.
'''
def get_common_case_by_reference_number(reference_number):
    global c_data
    for d in c_data:
        if d["AH"]==reference_number:
            return d
    return None