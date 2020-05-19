import argparse
import json
import sys
import os

from dbagent import DbAgent

dir_name={
    "authoritative":"authoritative_data",
    "common":"common_case_data",
}

def get_data_file_list(curr_path):
    ret=[]
    file_list=os.listdir(curr_path)
    i=0
    while True:
        fname="{}.json".format(i)
        if fname not in file_list:
            break
        ret.append(os.path.join(curr_path,fname))
        i+=1
    return ret

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', '-p', help="data path", required=True)
    args = parser.parse_args()

    for _type in ["authoritative","common"]:
        db_agent=DbAgent(_type)
        db_agent.clear()

        # Insert Documents
        curr_path=os.path.join(args.path,dir_name[_type])
        doc_file_list=get_data_file_list(curr_path)
        for fname in doc_file_list:
            db_agent.insert_document(json.load(open(fname,"r")))
        
        # Insert Reverse Index
        curr_path=os.path.join(curr_path,"reverse_index")
        index_file_list=get_data_file_list(curr_path)
        for fname in index_file_list:
            db_agent.insert_reverse_index(json.load(open(fname,"r")))