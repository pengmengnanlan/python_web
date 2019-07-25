# from django.http import JsonResponse  # 返回数据
# from django.core.paginator import Paginator   # Django内置分页功能模块
# import time
# #今日所有计划
# @csrf_exempt
# def ajax_webPlan(request):    
#     date = time.strftime('%Y%m%d', time.localtime(time.time()))    
#     datas = models.TblWebplan.objects.filter(issue__contains=date)    
#     dataCount = datas.count()    
#     req = request.POST    
#     print("接收",req)    
#     list =[] #存放所有的数据列表    
#     for data in datas:        
#         dict = {}  # 存放数据的字典        
#         dict["id"] = data.id        
#         dict["issue"] = data.issue        
#         dict["kjDate"] = data.kjdate        
#         dict["winnum"] = data.winnum        
#         dict["wxsum"] = data.wxsum        
#         dict["wan"] = data.wan        
#         dict["qian"] = data.qian        
#         dict["bai"] = data.bai        
#         dict["shi"] = data.shi        
#         dict["ge"] = data.ge        
#         list.append(dict)    
#     #print("列表",list)    
#     pageIndex = request.GET.get('pageIndex') #pageIndex = request.POST.get('pageIndex')    
#     pageSize = request.GET.get('pageSize') #pageSize = request.POST.get('pageSize')    
#     pageInator = Paginator(list, pageSize)    
#     contacts = pageInator.page(pageIndex)    
#     print(pageIndex,contacts)    
#     res =[] #最终返回的结果集合    
#     for contact in contacts:        
#         #print(contact)        
#         res.append(contact)    
#     Result = {"Code": 101, "Msg": "成功", "DataCount":dataCount,"Data":res}    
#     return JsonResponse(Result)
