# SolegalCopycat Backend APIs.
# Author    :   Yazid Wong
# Time      :   2020.05.17

from database.dbagent import DbAgent

class Backend:
    def __init__(self,config):
        port=config["mongodb_port"]
        self.db_agent={
            "authoritative": DbAgent("authoritative",port),
            "common": DbAgent("common",port),
        }

    def search(self, _type, keyword, condition, ret_info, page, page_size):
        curr_db=self.db_agent[_type]
        return [] # TODO

    def search_authoritative(self, keyword, condition, ret_info=None, page=1, page_size=20):
        return search("authoritative",keyword,condition,ret_info,page,page_size)

    def search_common(self, keyword, condition, ret_info=None, page=1, page_size=20):
        return search("common",keyword,condition,ret_info,page,page_size)

    def get_authoritative_case_by_unique_id(self, unique_id):
        ret=self.db_agent["authoritative"].get_document_by_id(unique_id)
        return ret

    def get_common_case_by_reference_number(self, reference_number):
        ret=self.db_agent["common"].get_document_by_feature({"AH":reference_number})
        return ret