# SolegalCopycat Backend APIs.
# Author    :   Yazid Wong
# Time      :   2020.05.17

import backend.fake_backend as __bked__

'''
init()
[ Description ] Init for backend.
'''
def init():
    __bked__.init()

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
def search_authoritative(keyword, condition, page=1, page_size=20):
    return __bked__.search_authoritative(keyword, condition, page, page_size)

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
def search_common(keyword, condition, page=1, page_size=20):
    return __bked__.search_common(keyword, condition, page, page_size)

'''
get_authoritative_case_by_unique_id(unique_id)
[ Description ] Get authoritative case's origin JSON object by unique id.
[ Params ]
* unique_id : A string, the unique id, should be matched with field `unique-id`.
[ Return Value ] A dict, result's origin JSON object. If there's no case matched, return None.
'''
def get_authoritative_case_by_unique_id(unique_id):
    return __bked__.get_authoritative_case_by_unique_id(unique_id)

'''
get_common_case_by_reference_number(reference_number)
[ Description ] Get common case's origin JSON object by reference number.
[ Params ]
* reference_number : A string, the reference number, should be matched with field `AH`.
[ Return Value ] A dict, result's origin JSON object. If there's no case matched, return None.
'''
def get_common_case_by_reference_number(reference_number):
    return __bked__.get_common_case_by_reference_number(reference_number)