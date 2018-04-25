from django.http import HttpResponse,JsonResponse
from django.template import loader,Context
import datetime
from django.shortcuts import render
from django.views.generic.base import View
from Visualization.models import Goods
from django.db.models import Count
#直接执行sql
from django.db import connection

import json
 # Create your views here.
 

class IndexView(View):
    def get(self, request):
        B_nodes=[]
        links = []
        data_scatter={}
        data_discount=[]
        data_Notdiscount=[]
        data_UNKdiscount=[]
        goods=Goods.objects.values('price','comments_num','say_good_pct','detail','seem_cheap_tag')
        data_list_all=[]
        
        for  good in goods:
            price = float(good['price'])
            comments_num = good['comments_num']
            say_good_pct = float(good['say_good_pct'])
            seem_cheap_tag = good['seem_cheap_tag']

            data_dic_sca={}
            data_list_show=[]
            data_list_show.append(price)
            data_list_show.append(comments_num)
            data_list_show.append(say_good_pct)
            data_dic_sca['data_sca']=data_list_show
            data_dic_sca['cheap_tag']=seem_cheap_tag
            data_dic_sca['name_type_a']=good['detail']['name_type_a']
            data_dic_sca['name_type_b']=good['detail']['name_type_b']
            data_list_all.append(data_dic_sca)
            
            if seem_cheap_tag==1:
                lili=[price,comments_num,say_good_pct]
                data_discount.append(lili)
 
            elif seem_cheap_tag==0:
                lili=[price,comments_num,say_good_pct]
                data_Notdiscount.append(lili)
            else:
                lili=[price,comments_num,say_good_pct]
                data_UNKdiscount.append(lili)
                                           
        # dd = Goods.objects.values_list("itemid_typeA","itemid_typeB","detail")

        # ids_type_b=Goods.objects.values("itemid_typeB").distinct()


# {              
# name: '三星',
# value: 6,
# children: [
#             {name: 'Galaxy S4',value: 2},
#             {name: 'Galaxy S5',value: 3},
#             {name: 'Galaxy S6',value: 3},
#             {name: 'Galaxy Tab',value: 1}
#           ] 
# },
        ids_type_a_queryset=Goods.objects.values("itemid_typeA","itemid_typeB").distinct()

        ids_dict={}
        for x  in ids_type_a_queryset:
            if x['itemid_typeA'] not in ids_dict.keys():
                ids_dict[x['itemid_typeA']]=[]
            else:
                ids_dict[x['itemid_typeA']].append(x['itemid_typeB'])

        data_treemap=[]

        ##数据结构的构建可以考虑用 group by
        #https://docs.djangoproject.com/en/2.0/topics/db/aggregation/
        # gp=Goods.objects.values('detail').annotate(Count('itemid_typeB',distinct=True),Count('itemid_typeA', distinct=True))
        for key in  ids_dict:
            typeA_dict={}
            category_queryset = Goods.objects.values('detail').filter(itemid_typeA=key)
            typeA_dict['name']=category_queryset[0]['detail']['name_type_a']
            typeA_dict['value']=len(category_queryset)

            typeB_list=[]
            for  x in  ids_dict[key]:
                typeB_dict={}
                item_typeB = Goods.objects.values('detail').filter(itemid_typeB=x,itemid_typeA=key)
                typeB_dict['name']=item_typeB[0]['detail']['name_type_b']
                typeB_dict['value']=len(item_typeB)
                typeB_list.append(typeB_dict)
            typeA_dict['children']=typeB_list

            data_treemap.append(typeA_dict)   
        # print(data_treemap)

        return render(request, 'index.html',
            {"data_all":data_list_all,
            "data_discount":data_discount,
            "data_Notdiscount":data_Notdiscount,
            "data_UNKdiscount":data_UNKdiscount,
            "data_treemap":json.dumps(data_treemap)
                                                })



#         roselegend :  data:['rose1','rose2','rose3','rose4','rose5','rose6','rose7','rose8']
#         data:[
#                 {value:10, name:'rose1'},
#                 {value:5, name:'rose2'},
#                 {value:15, name:'rose3'},
#                 {value:25, name:'rose4'},
#                 {value:20, name:'rose5'},
#                 {value:35, name:'rose6'},
#                 {value:30, name:'rose7'},
#                 {value:40, name:'rose8'}

# ]

 # data: [
 #            {
 #                name: "Sam S Club",
 #                value: 10000,
 #                itemStyle: {
 #                    normal: {
 #                        color: 'black'
 #                    }
 #                }
 #            },
class AboutView(View):
    def get(self, request,):
        ids_type_a_queryset=Goods.objects.values("itemid_typeA","itemid_typeB").distinct()

        ids_dict={}

        for x  in ids_type_a_queryset:
            if x['itemid_typeA'] not in ids_dict.keys():
                ids_dict[x['itemid_typeA']]=[]
            else:
                ids_dict[x['itemid_typeA']].append(x['itemid_typeB'])


        roselegend=[]
        rose_data_list=[]
        wordscloud_data =[]
        comments_tags={}
        comments_tag_list=[]
        comments_tag_all=[]


        for key in  ids_dict:
            rose_data={}
            category_queryset = Goods.objects.values('detail',"comments_tags").filter(itemid_typeA=key)

            roselegend.append(category_queryset[0]['detail']['name_type_a'])

            rose_data['name']=category_queryset[0]['detail']['name_type_a']
            rose_data['value']=len(category_queryset)
            rose_data_list.append(rose_data)
            

            ## comments_tags={name:value} keys value  遍历 写进comments_tag_list
            ## comments_tag_list ={{name:value}} 

            
             #放所有的tag,list
            for x in category_queryset:
                # print(x)
                for y in x['comments_tags']['data']:
                    comments_tag={}
                    if y['name'] not in['有图','追评','全部']:
                        if y['name'] not in comments_tags.keys() :
                            if y['strCount']=="999+":
                                comments_tags[y['name']]=999

                            else:
                                comments_tags[y['name']]=int(y['strCount'])
 
                        else :
                            if y['strCount']=="999+":
                                comments_tags[y['name']]=999+comments_tags[y['name']]
                            else:
                                comments_tags[y['name']]=int(y['strCount'])+comments_tags[y['name']]
            

            for x2 in  category_queryset:
                for y in x2['comments_tags']['data']:
                    comments_tag={}
                     
                    if y['name'] not in['有图','追评','全部']:
                        if y['strCount']=="999+":
                                comments_tag[y['name']]=999
                                comments_tag['name_type_a']=x2['detail']['name_type_a']
                        else:
                            comments_tag[y['name']]=int(y['strCount'])
                            comments_tag['name_type_a']=x2['detail']['name_type_a']
                        comments_tag_all.append(comments_tag)


        for key in comments_tags:
            if comments_tags[key]!={}:
                comments_tag={}
                comments_tag['name']=key
                comments_tag['value']=comments_tags[key]
                comments_tag["itemStyle"]="createRandomItemStyle()"
            # comments_tag["itemStyle"]= {"normal": {
            #             "color": 'black'
            #         }}
                comments_tag_list.append(comments_tag)


        comments_tag_all_sorted=[]

        tags_dict_outer={}
        for x in comments_tag_all:
            dict_inner={}
            if x['name_type_a'] not in tags_dict_outer.keys():
                dict_inner[x['name_type_a']]={}

                for key in x.keys():
                    if key !='name_type_a':
                        dict_inner[x['name_type_a']][key]= x[key]
                tags_dict_outer.update(dict_inner)

            else:
                for key in x.keys():
                    if key !='name_type_a':
                        if key not in tags_dict_outer[x['name_type_a']].keys():
                            tags_dict_outer[x['name_type_a']][key]=x[key]
                        else:
                            tags_dict_outer[x['name_type_a']][key]=tags_dict_outer[x['name_type_a']][key]+x[key]
                        
                
        # print(tags_dict_outer)  



        # data_catogry=Goods.objects.values('detail')

        # print(data_catogry[0]['detail']['name_type_a'])
        return render(request, 'about.html',{
            "roselegend":roselegend,
            "rose_data":rose_data_list,
            "comments_tag_list":json.dumps(comments_tag_list),
            "tags_dict_outer":json.dumps(tags_dict_outer)


            })
class ContactView(View):
    def get(self, request,):

        return render(request,'contact.html')


class BlogView(View):

    def get(self, request,):

        # mul_query =Goods.objects.values("itemid_typeB").values_list("itemid_typeA","itemid_typeB","detail").order_by()
        # mul_query=Goods.objects.raw("select itemid,itemid_typeA,itemid_typeB,detail from goods_yanxuan GROUP BY itemid_typeB")
        with connection.cursor() as cursor:
            cursor.execute("select itemid,itemid_typeA,itemid_typeB,detail from goods_yanxuan GROUP BY itemid_typeB")
            data_rawsql = cursor.fetchall()

        print(type(data_rawsql))
        names_dict={}
        for x in data_rawsql:
            detail=json.loads(x[3])
            if detail['name_type_a'] not in names_dict.keys():
                names_dict[detail['name_type_a']] =[[detail['name_type_b'],x[2]]]
            else:
                names_dict[detail['name_type_a']].append([detail['name_type_b'],x[2]])
        
        request_type_id=request.GET.get('type_id')  
        print(request_type_id)




        data_as_sayed_good={}
        data_really_good={}
        avg_say_good=0

        if request_type_id!=None:
            with connection.cursor() as cursor:
                cursor.execute("select itemid,comments_num,say_good_pct FROM goods_yanxuan where itemid_typeB="+str(request_type_id)+"  and comments_num>100 and say_good_pct>0.8")
                data_rawsql2 = cursor.fetchall()

                cursor.execute("select say_good_pct from goods_yanxuan where itemid_typeB = "+str(request_type_id))
                data_sayed_good = cursor.fetchall()
                data_sayed_good_sum=0
                for x in data_sayed_good:
                    print(x)
                    data_sayed_good_sum+=x[0]
                avg_say_good = round(data_sayed_good_sum/len(data_sayed_good)*100,2)

            if len(data_rawsql2)>0:
                for x in data_rawsql2:
                    coefficient = x[1]+1000*float(x[2])
                    data_really_good[x[0]]=coefficient
            else:
                with connection.cursor() as cursor:
                    cursor.execute("select itemid,comments_num,say_good_pct FROM goods_yanxuan where itemid_typeB="+str(request_type_id)+" ORDER BY say_good_pct desc,comments_num")
                    data_rawsql2 = cursor.fetchall()
                    for x in data_rawsql2:
                        coefficient = x[1]+1000*float(x[2])
                        data_really_good[x[0]]=coefficient

                data_really_good=sorted(data_really_good.items(),key =lambda data_really_good: data_really_good[1], reverse=True)
                # print(data_really_good)



                
            with connection.cursor() as cursor:
                cursor.execute("select itemid,say_good_pct FROM goods_yanxuan where itemid_typeB="+str(request_type_id)+ " ORDER BY say_good_pct desc")
                data_rawsql3 = cursor.fetchall()    

            for x in data_rawsql3:
                data_as_sayed_good[x[0]]=x[1]
        else:
            with connection.cursor() as cursor:
                cursor.execute("select itemid,comments_num,say_good_pct FROM goods_yanxuan   where  comments_num>50000 and say_good_pct>0.8")
                data_rawsql2 = cursor.fetchall()
                cursor.execute("select say_good_pct from goods_yanxuan")
                data_sayed_good = cursor.fetchall()
                data_sayed_good_sum=0
                for x in data_sayed_good:
                    print(x)
                    data_sayed_good_sum+=x[0]
                avg_say_good = round(data_sayed_good_sum/len(data_sayed_good)*100,2)

            for x in data_rawsql2:
                    coefficient = x[1]+1000*float(x[2])
                    data_really_good[x[0]]=coefficient
            

            with connection.cursor() as cursor:
                cursor.execute("select itemid,say_good_pct FROM goods_yanxuan where comments_num>10000  ORDER BY say_good_pct desc ")
                data_rawsql3 = cursor.fetchall()    
            for x in data_rawsql3:
                data_as_sayed_good[x[0]]=x[1]

        return render(request, 'blog.html',{
            "names_dict":names_dict,
            "data_really_good":data_really_good,
            "data_as_sayed_good":data_as_sayed_good,
            "avg_say_good":avg_say_good
            })

class TeamView(View):
    def get(self, request,):
        return render(request, 'team.html')
  