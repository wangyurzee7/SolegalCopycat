# SolegalCopycat Backend APIs.
# Author    :   Yazid Wong
# Time      :   2020.05.17

from database.dbagent import DbAgent
from utils.tokenization import tokenization

import math

class Backend:
    def __init__(self,config):
        port=config["mongodb_port"]
        self.db_agent={
            "authoritative": DbAgent("authoritative",port),
            "common": DbAgent("common",port),
        }
        self.max_result_num=1000
        self.field_trans={
            "authoritative":{
                "type":"LB",
                "region":"XZQH_P",
                "year":"LAND",
                "cause_of_action":"AJLB",
            },
            "common":{
                "region":"XZQH_P",
                "court_level":"FYJB",
                "year":"LAND",
                "judicial_procedure":"SPCX",
                "document_type":"WSZL",
                "cause_of_action":"AJLB",
            },
        }
        # TODO : update self.all_conditions
        self.all_conditions={
            "authoritative":{
                 "type": [ "公报案例", "典型案例", "参阅案例", "指导案例" ], "region": [ "上海", "云南", "内蒙古", "北京", "吉林", "四川", "天津", "宁夏", "安徽", "山东", "山西", "广东", "广西", "新疆", "最高人民法院", "江苏", "江西", "河北", "河南", "浙江", "海事法院", "湖北", "湖南", "甘肃", "知识产权法院", "福建", "贵州", "辽宁", "重庆", "铁路法院", "陕西", "青海", "黑龙江", "Unknown" ], "year": [ "1985", "1986", "1987", "1988", "1989", "1990", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "Unknown" ], "cause_of_action": [ "刑事案件", "国家赔偿案件", "民事案件", "行政案件" ] 
            },
            "common":{
                 "region": [ "上海", "云南", "内蒙古", "北京", "吉林", "四川", "天津", "宁夏", "安徽", "山东", "山西", "广东", "广西", "新疆", "最高", "江苏", "江西", "河北", "河南", "浙江", "海南", "湖北", "湖南", "甘肃", "福建", "贵州", "辽宁", "重庆", "陕西", "青海", "黑龙江", "Unknown" ], "court_level": [ "中级", "基层", "最高", "高级" ], "year": [ "1023", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018" ], "judicial_procedure": [ "一审案件", "二审案件", "再审复查与审判监督案件", "再审案件", "刑罚变更案件", "复核案件", "特别程序案件", "Unknown" ], "document_type": [ "决定书", "判决书", "裁定书" ], "cause_of_action": [ "刑事案件", "执行案件", "民事案件", "行政案件" ] 
            },
        }
        self.rank_ensure_accurate=50

    def search(self, _type, keyword, condition, ret_info, page, page_size):
        keyword=keyword[:30]
        field_trans=self.field_trans[_type]
        curr_db=self.db_agent[_type]

        cond={}
        for k,v in condition.items():
            if k in field_trans.keys():
                cond[field_trans[k]]=v

        tokens=list(set(tokenization(keyword)))
        if not tokens:
            # no tokens
            id_arr=curr_db.get_ids_by_feature(cond)
        elif len(tokens)==1 and not cond:
            # 1 token, no condition
            reverse_index=curr_db.look_for_word(tokens[0])
            id_arr=list(reverse_index.keys())
        elif len(tokens)==1 and cond:
            # 1 token, have condition
            reverse_index=curr_db.look_for_word(tokens[0])
            valid_id_arr=curr_db.get_ids_by_feature(cond)
            len_valid_id_arr=len(valid_id_arr)
            if len(reverse_index)*math.log(len_valid_id_arr)<len_valid_id_arr: # len(reverse_index) << len(valid_id_arr) ?
                id_arr=[]
                valid_id_set=set(valid_id_arr)
                for unique_id in reverse_index.keys():
                    if unique_id in valid_id_set:
                        id_arr.append(unique_id)
            else:
                id_arr=list(filter(lambda x:x in reverse_index.keys(),valid_id_arr))
                id_arr.sort(reverse=True,key=lambda unique_id:reverse_index[unique-id])
        else:
            # multiple tokens
            id_arr=[] # TODO
            if not cond:
                # multiple tokens, no condition
                valid_id_set=None
                def valid(unique_id):
                    return True
            else:
                # multiple tokens, have condition
                valid_id_set=set(curr_db.get_ids_by_feature(cond))
                def valid(unique_id):
                    return unique_id in valid_id_set
            
            n_tokens=len(tokens)
            if valid_id_set is not None and len(valid_id_set)<self.max_result_num:
                score={unique_id:0.0 for unique_id in valid_id_set}
                for t in tokens:
                    ri=curr_db.look_for_word(t)
                    for unique_id in valid_id_set:
                        if unique_id in ri:
                            score[unique_id]+=ri[unique_id]
                id_arr=list(valid_id_set)
                id_arr.sort(reverse=True,key=lambda unique_id:score[unique_id])
            else:
                reverse_index_list=[]
                wating_list=set()
                for t in tokens:
                    ri=curr_db.look_for_word(t)
                    if ri is None:
                        continue
                    j=0
                    for unique_id in ri.keys():
                        if not valid(unique_id):
                            continue
                        wating_list.add(unique_id)
                        j+=1
                        if j==self.max_result_num:
                            break
                    reverse_index_list.append(ri)
                score_arr=[]
                for unique_id in wating_list:
                    curr_score=0
                    k=0
                    for rl in reverse_index_list:
                        if unique_id in rl:
                            curr_score+=rl[unique_id]
                            k+=1
                    curr_score*=math.sqrt(k)
                    score_arr.append((curr_score,unique_id))
                score_arr.sort(reverse=True)
                id_arr=[unique_id for score,unique_id in score_arr]
                ''' # Fuck
                min_rank_50=0
                for t in tokens:
                    ri=curr_db.look_for_word(t)
                    if valid_id_set is None:
                        curr_val=max(min_rank_50,list(ri.values())[self.rank_ensure_accurate])
                    else:
                        j=0
                        curr_val=0
                        for unique_id in ri.keys():
                            if unique_id not in valid_id_set:
                                continue
                            j+=1
                            if j==self.rank_ensure_accurate:
                                curr_val=ri[unique_id]
                                break
                    min_rank_50=max(min_rank_50,curr_val/n_tokens)
                    reverse_index_list.append(ri)
                score={}
                for ri in reverse_index:
                    for unique_id in ri.keys():
                        if not valid(unique_id):
                            continue
                        if ri[unique_id]<min_rank_50:
                '''
        
        ret=[]
        id_arr=id_arr[:self.max_result_num]
        for unique_id in id_arr[(page-1)*page_size:page*page_size]:
            ret.append(curr_db.get_document_by_id(unique_id))
        
        ret_info["total_pages"]=(len(id_arr)-1)//page_size+1

        if len(id_arr)<self.max_result_num:
            ret_info["total_num"]=len(id_arr)
            ret_info["condition"]=self.all_conditions[_type]
            # get_documents_by_id_list
        else:
            ret_info["total_num"]="{}+".format(self.max_result_num-1)
            ret_info["condition"]=self.all_conditions[_type]
        return ret

    def search_authoritative(self, keyword, condition, ret_info=None, page=1, page_size=20):
        try:
            return self.search("authoritative",keyword,condition,ret_info,page,
            page_size)
        except Exception as err:
            print(err)

    def search_common(self, keyword, condition, ret_info=None, page=1, page_size=20):
        try:
            return self.search("common",keyword,condition,ret_info,page,page_size)
        except Exception as err:
            print(err)

    def get_authoritative_case_by_unique_id(self, unique_id):
        ret=self.db_agent["authoritative"].get_document_by_id(unique_id)
        return ret

    def get_common_case_by_reference_number(self, reference_number):
        ret=self.db_agent["common"].get_document_by_feature({"AH":reference_number})
        return ret