import pymongo

'''
meta_info_fields=[
    "unique-id",
    "LB",
    "XZQH_P",
    "FYJB",
    "LAND",
    "SPCX",
    "WSZL",
    "AJLB",
]
'''

class DbAgent:
    def __init__(self,db_name,port=11382):
        self.db_name=db_name
        self.port=port
        self.client=pymongo.MongoClient("mongodb://localhost:{}/".format(port))
        self.db=self.client["solegal_copycat_database_{}".format(db_name)]
        self.documents_coll=self.db["documents"]
        # self.meta_info_coll=self.db["meta_info"]
        self.reverse_index_coll=self.db["reverse_index"]
    
    def clear(self):
        self.documents_coll.delete_many({})
        self.reverse_index_coll.delete_many({})
    
    def insert_document(self,doc):
        if type(doc)==list:
            for i in range(len(doc)):
                doc[i].pop("tokens")
        else:
            doc.pop("tokens")
        self.documents_coll.insert(doc)
        '''
        if type(doc)==list:
            for d in doc:
                self.insert_document(d)
            return
        self.documents_coll.insert(doc)
        meta_info={}
        for key in meta_info_fields:
            if key in doc.keys():
                meta_info[key]=doc[key]
        self.meta_info_coll.insert(meta_info)
        '''
    
    def insert_reverse_index(self,index):
        for key,arr in index.items():
            curr={"keyword": key}
            for i,tfidf in arr:
                curr[i]=tfidf
            self.reverse_index_coll.insert(curr)

    def look_for_word(self,word):
        return self.reverse_index_coll.find_one({"keyword":word},{"_id":0,"keyword":0})
    
    def fill_QW(self,doc):
        if type(doc)==dict and "QW" not in doc:
            doc["QW"]=doc["CPFXGC"]

    def get_document_by_id(self,unique_id):
        return self.documents_coll.find_one({"unique-id":unique_id},{"_id":0})
    
    def get_documents_by_id_list(self,id_list):
        result=list(self.documents_coll.find({"unique-id":{"$in":id_list}},{"_id":0}))
        prior={unique_id:i for i,unique_id in enumerate(id_list)}
        result.sort(key=lambda d:prior[d["unique-id"]])
        for doc in result:
            self.fill_QW(doc)
        return result

    def get_document_by_feature(self,features):
        ret=self.documents_coll.find_one(features,{"_id":0})
        self.fill_QW(ret)
        return ret
    
    def get_ids_by_feature(self,features):
        query={}
        for key,val in features.items():
            if type(val)==list:
                query[key]={"$all":val}
            else:
                query[key]=val
        result=self.documents_coll.find(query,{"_id":0,"unique-id":1})
        return [x["unique-id"] for x in result]
    