# -*- coding: utf-8 -*-
import scrapy
#import urllib2
import urllib
import json
#from urllib import urlencode
from scrapy.http import Request
from lxml import etree
from JiangBei2.items import Jiangbei2Item
import re

class Jiangbei2Spider(scrapy.Spider):
    name = 'jiangbei2'
    #allowed_domains = ['www.cqjbjyzx.gov.cn']
    start_urls = ['http://www.cqjbjyzx.gov.cn/lbv3/n_newslist_zz_item.aspx?ILWHBNjF4clKo8UY2fiQHA==']
    url_list = []
    count = 0

    def parse(self, response):
        url_list2 = []
        date_list = []
        title_list =[]
        #print response.body
        html = response.body
        html = html.decode('utf-8')
        _VIEWSTATE = re.findall(r'id="__VIEWSTATE.*?value="(.*?)"',html)[0]
        #print(_VIEWSTATE)

        _EVENTVALIDATION = re.findall(r'id="__EVENTVALIDATION.*?value="(.*?)"',html)[0]
        #print(_EVENTVALIDATION)

        title = re.findall(r'<nobr><a href=".*?>(.*?)</a></nobr></td>',html)

        date = re.findall(r'<td width="10.*?<nobr>(.*?)</nobr>',html)

        half_link = re.findall(r'<nobr><a href="(.*?)"',html)

        for j in range(0,len(title)):

            title_list.append(title[j])
            date_list.append(date[j])
            url_link = "http://www.cqjbjyzx.gov.cn/lbv3/" + half_link[j]
            self.url_list.append(url_link)
            url_list2.append(url_link)

        results1 =[]
        results1.extend(url_list2)
        for k in range(0,len(results1)):
            results1[k] = "date:" + date_list[k] + " ; " + "title: " + title_list[k] + " ; " + "web: " + url_list2[k] + '\n'
        #with open('/home/jessyl/JiangBei2/第一部分爬取内容.txt','a') as f1:
            #f1.writelines(results1)

        #for i in range(0,96):
        for i in range(0,2):
            values = {
                "__VIEWSTATE":_VIEWSTATE,
                "__VIEWSTATEGENERATOR": "408E0053",
                "__EVENTVALIDATION": _EVENTVALIDATION,
                "ctl00$ContentPlaceHolder2$T1": "96",
                "ctl00$ContentPlaceHolder2$T2": "{}".format(i+1),
                "ctl00$ContentPlaceHolder2$F3": "下一页"
            }
            postdata = values
            yield scrapy.FormRequest(
            url = response.url,
            formdata = postdata,
            callback = self.page_next
        )

    def page_next(self,response):
        url_list2 = []
        date_list = []
        title_list =[]

        content = response.body
        content = content.decode('utf-8')
        title2 = re.findall(r'<nobr><a href=".*?>(.*?)</a></nobr></td>',content)

        date2 = re.findall(r'<td width="10.*?<nobr>(.*?)</nobr>',content)

        half_link2 = re.findall(r'<nobr><a href="(.*?)"',content)

        for j in range(0,len(title2)):
            title_list.append(title2[j])
            date_list.append(date2[j])
            url_link2 = "http://www.cqjbjyzx.gov.cn/lbv3/" + half_link2[j]
            self.url_list.append(url_link2)
            url_list2.append(url_link2)

        results1 =[]
        results1.extend(url_list2)
        for k in range(0,len(title_list)):
            results1[k] = "date:" + date_list[k] + " ; " + "title: " + title_list[k] + " ; " + "web: " + url_list2[k] + "\n"
        #with open('/home/jessyl/JiangBei2/第一部分爬取内容.txt','a') as f1:
            #f1.writelines(results1)

        for k in range(0,len(self.url_list)):
            yield Request(url=self.url_list[k],callback=self.page_in)

    def page_in(self,response):
        self.count += 1

        html2 = etree.HTML(response.text)

        #中标时间(meta) 、招标人、招标公告编号、项目名称、
        #招标代理机构、第一第二第三中标候选人、拟中标人、工商注册号、投诉受理部门、中标价、第二第三中标人价格
        
        project = u'(项目名称.*)'
        project2 = u'(工程名称.*)'
        pro_time = u'(中标时间.*)'
        zb_person = u'(招标人.*)'
        zb_agent = u'(招标代理机构.*)'
        fb_person = u'(发包人（盖章）.*)'
        pz_num = u'(项目批准文号.*)'
        fh_p = u'(第一侯选人.*)'
        fh_n = u'(营业执照注册号.*)'
        sh_p = u'(第二侯选人.*)'
        th_p = u'(第三侯选人.*)'
        ts_agent = u'(投诉受理部门.*)'
        gongshang_num = u'(工商注册号.*)'
        zx_p = u'(中选承包商.*)'
        fb_price = u'(发包价.*)'
        project_num = u'(项目编号.*)'

        results = []        #法一：把所有结果作为一个整体，而不是一条一条的

        item = Jiangbei2Item()

        for n in range(1,20):
            contents = html2.xpath('//tr[4]/td[2]/table/tbody/tr['+str(n)+']//text()')
            if contents ==[]:
                break
            else:
                while "\r\n" in contents:
                    contents.remove("\r\n")
                while "/" in contents:
                    contents.remove("/")
                
                contents = [''.join(x.split()) for x in contents]
                #这是列表内每个元素去除xa0等空白字符

                contents2 = ''.join(contents)
                #print(contents2)
                #print(type(contents2))

                #project = u'(项目名称.*)'               
                pro_name = re.findall(project,contents2,re.S)
                if pro_name != []:
                    item['项目名称']=pro_name[0]
                    results.extend(pro_name)
                    results.append("\n")

                #project2 = u'(工程名称.*)'
                pro_name2 = re.findall(project2,contents2,re.S)
                if pro_name2 !=[]:
                    item['工程名称']=pro_name2[0]
                    results.extend(pro_name2)
                    results.append("\n")

                #pro_time = u'(中标时间.*)
                pt = re.findall(pro_time,contents2,re.S)
                if pt !=[]:
                    item['中标时间']=pt[0]
                    results.extend(pt)
                    results.append("\n")

                #project_num = u'(项目编号.*)'
                pn = re.findall(project_num,contents2,re.S)
                if pn !=[]:
                    item['项目编号']=pn[0]
                    results.extend(pn)
                    results.append("\n")

                #pz_num = u'(项目批准文号.*)'
                pzn = re.findall(pz_num,contents2,re.S)
                if pzn !=[]:
                    item['项目批准文号']=pzn[0]
                    results.extend(pzn)
                    results.append("\n")

                #zb_person = u'(招标人.*)'
                zbp = re.findall(zb_person,contents2,re.S)
                if zbp !=[]:
                    item['招标人']=zbp[0]
                    results.extend(zbp)
                    results.append("\n")

                #zb_agent = u'(招标代理机构.*)'
                zba = re.findall(zb_agent,contents2,re.S)
                if zba !=[]:
                    item['招标代理机构']=zba[0]
                    results.extend(zba)
                    results.append("\n")

                #fb_person = u'(发包人（盖章）.*?)'
                fbp = re.findall(fb_person,contents2,re.S)
                if fbp !=[]:
                    item['发包人']=fbp[0]
                    results.extend(fbp)
                    results.append("\n")

                #fh_p = u'(第一侯选人.*)'
                fhp = re.findall(fh_p,contents2,re.S)
                if fhp !=[]:
                    item['第一侯选人']=fhp[0]
                    results.extend(fhp)
                    results.append("\n")

                #fh_n = u'(营业执照注册号.*)'
                fhn = re.findall(fh_n,contents2,re.S)
                if fhn !=[]:
                    item['营业执照注册号']=fhn[0]
                    results.extend(fhn)
                    results.append("\n")

                #sh_p = u'(第二侯选人.*)'
                shp = re.findall(sh_p,contents2,re.S)
                if shp !=[]:
                    item['第二侯选人']=shp[0]
                    results.extend(shp)
                    results.append("\n")

                # th_p = u'(第三侯选人.*)'
                thp = re.findall(th_p,contents2,re.S)
                if thp !=[]:
                    item['第三侯选人']=thp[0]
                    results.extend(thp)
                    results.append("\n")

                # ts_agent = u'(投诉受理部门.*)'
                tsa = re.findall(ts_agent,contents2,re.S)
                if tsa !=[]:
                    item['投诉受理部门']=tsa[0]
                    results.extend(tsa)
                    results.append("\n")

                # zx_p = u'(中选承包商.*)'
                zxp = re.findall(zx_p,contents2,re.S)
                if zxp !=[]:
                    item['中选承包商']=zxp[0]
                    results.extend(zxp)
                    results.append("\n")

                # gongshang_num = u'(工商注册号.*)'
                gsn = re.findall(gongshang_num,contents2,re.S)
                if gsn !=[]:
                    item['工商注册号']=gsn[0]
                    results.extend(gsn)
                    results.append("\n")

                # fb_price = u'(发包价.*)'
                fbp = re.findall(fb_price,contents2,re.S)
                if fbp !=[]:
                    item['发包价']=fbp[0]
                    results.extend(fbp)
                    results.append("\n")

                
                # results.append("!")
                # A.extend(B)自动去除空字符串
        #results2 = ''.join(results)
        #results3 = "NO." + str(self.count) + " " + results2
        #print(results3)
        #item = Jiangbei2Item()
        #item['result'] = results3 + '\n' 

        yield item


