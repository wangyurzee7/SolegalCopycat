from django.shortcuts import render
from django.http import HttpResponse

import backend.api as backend
import time
import json

def index(request):
    return render(request,"template.html",{"string":"Here is index."})

def search_authoritative(request):
    start_time=time.time()

    # Parse HTTP Request
    try:
        keyword=request.GET["keyword"]
        condition={}
        for k in ["type", "region", "year", "cause_of_action"]:
            if k in request.GET:
                tmp=request.GET[k]
                if k=="cause_of_action":
                    tmp=list(tmp.split(','))
                condition[k]=tmp
        page=request.GET["page"] if "page" in request.GET else 1
        page=int(page)
        info={}
        result=backend.search_authoritative(keyword, condition, ret_info=info, page=page)
        obj={
            "info":info,
            "result":result,
            "time_cost":time.time()-start_time
        }
    except:
        return render(request,"template.html",{"string":"Invalid Request."})

    # return render(request,"template.html",{"string":json.dumps(obj,ensure_ascii=False,indent=2)})
    resp = HttpResponse(json.dumps(obj,ensure_ascii=False,indent=2))
    resp.__setitem__("Access-Control-Allow-Origin","*")
    return resp
    
def search_common(request):
    start_time=time.time()

    # Parse HTTP Request
    try:
        keyword=request.GET["keyword"]
        condition={}
        for k in ["region", "court_level", "year", "judicial_procedure", "document_type", "cause_of_action"]:
            if k in request.GET:
                tmp=request.GET[k]
                if k=="cause_of_action":
                    tmp=list(tmp.split(','))
                condition[k]=tmp
        page=request.GET["page"] if "page" in request.GET else 1
        page=int(page)
        info={}
        result=backend.search_common(keyword, condition, ret_info=info, page=page)
        obj={
            "info":info,
            "result":result,
            "time_cost":time.time()-start_time
        }
    except:
        return render(request,"template.html",{"string":"Invalid Request."})

    # return render(request,"template.html",{"string":json.dumps(obj,ensure_ascii=False,indent=2)})
    resp = HttpResponse(json.dumps(obj,ensure_ascii=False,indent=2))
    resp.__setitem__("Access-Control-Allow-Origin","*")
    return resp

def detail_authoritative(request):
    try:
        unique_id=request.GET["id"]
        obj=backend.get_authoritative_case_by_unique_id(unique_id)
    except:
        return render(request,"template.html",{"string":"Invalid Request."})
    # return render(request,"template.html",{"string":json.dumps(obj,indent=2,ensure_ascii=False)})
    resp = HttpResponse(json.dumps(obj,ensure_ascii=False,indent=2))
    resp.__setitem__("Access-Control-Allow-Origin","*")
    return resp

def detail_common(request):
    try:
        reference_number=request.GET["rnum"]
        obj=backend.get_common_case_by_reference_number(reference_number)
    except:
        return render(request,"template.html",{"string":"Invalid Request."})
    # return render(request,"template.html",{"string":json.dumps(obj,indent=2,ensure_ascii=False)})
    resp = HttpResponse(json.dumps(obj,ensure_ascii=False,indent=2))
    resp.__setitem__("Access-Control-Allow-Origin","*")
    return resp
