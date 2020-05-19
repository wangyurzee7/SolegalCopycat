import json

def init(config):
    global a_data
    global c_data
    a_data=json.load(open("data/authoritative_data/0.json","r"))
    c_data=json.load(open("data/common_case_data/0.json","r"))



def search_authoritative(keyword, condition, ret_info, page, page_size):
    field_trans={
        "type":"LB",
        "region":"XZQH_P",
        "year":"LAND",
    }
    global a_data
    arr=[]
    for d in a_data:
        flag=True
        for k_input,k_origin in field_trans.items():
            if (k_input in condition) and (condition[k_input]!=d[k_origin]):
                flag=False
                break
        if ("cause_of_action" in condition):
            for _ in condition["cause_of_action"]:
                if _ not in d["AJLB"]:
                    flag=False
                    break
        if not flag:
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
    ret_info["total_num"]=len(ret)
    ret_info["total_pages"]=(len(ret)-1)//page_size+1
    ret_info["condition"]={k:[] for k in field_trans.keys()}
    ret_info["condition"]["cause_of_action"]=[]
    for d in ret:
        for _ in d["AJLB"]:
            if _ not in ret_info["condition"]["cause_of_action"]:
                ret_info["condition"]["cause_of_action"].append(_)
        for k in field_trans.keys():
            if d[field_trans[k]] not in ret_info["condition"][k]:
                ret_info["condition"][k].append(d[field_trans[k]])
    ret_info["condition"]["cause_of_action"].sort()
    for k in field_trans.keys():
        ret_info["condition"][k].sort()
    return ret[(page-1)*page_size:page*page_size]


def search_common(keyword, condition, ret_info, page, page_size):
    field_trans={
        "region":"XZQH_P",
        "court_level":"FYJB",
        "year":"LAND",
        "judicial_procedure":"SPCX",
        "document_type":"WSZL",
    }
    global c_data
    arr=[]
    for d in c_data:
        flag=True
        for k_input,k_origin in field_trans.items():
            if (k_input in condition) and (condition[k_input]!=d[k_origin]):
                flag=False
                break
        if ("cause_of_action" in condition):
            for _ in condition["cause_of_action"]:
                if _ not in d["AJLB"]:
                    flag=False
                    break
        if not flag:
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
    ret_info["total_num"]=len(ret)
    ret_info["total_pages"]=(len(ret)-1)//page_size+1
    ret_info["condition"]={k:[] for k in field_trans.keys()}
    ret_info["condition"]["cause_of_action"]=[]
    for d in ret:
        for _ in d["AJLB"]:
            if _ not in ret_info["condition"]["cause_of_action"]:
                ret_info["condition"]["cause_of_action"].append(_)
        for k in field_trans.keys():
            if d[field_trans[k]] not in ret_info["condition"][k]:
                ret_info["condition"][k].append(d[field_trans[k]])
    ret_info["condition"]["cause_of_action"].sort()
    for k in field_trans.keys():
        ret_info["condition"][k].sort()
    return ret[(page-1)*page_size:page*page_size]


def get_authoritative_case_by_unique_id(unique_id):
    global a_data
    for d in a_data:
        if d["unique-id"]==unique_id:
            return d
    return None


def get_common_case_by_reference_number(reference_number):
    global c_data
    for d in c_data:
        if d["AH"]==reference_number:
            return d
    return None