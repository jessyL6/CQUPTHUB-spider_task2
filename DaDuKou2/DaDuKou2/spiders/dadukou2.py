# -*- coding: utf-8 -*-
import scrapy
import urllib2
import urllib
import json
from urllib import urlencode
from scrapy.http import Request
from lxml import etree
from DaDuKou2.items import Dadukou2Item
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Dadukou2Spider(scrapy.Spider):
    name = 'dadukou2'
    #allowed_domains = ['www.ddkggzy.com']
    start_urls = ['http://www.ddkggzy.com/lbv3/n_newslist_zz_item.aspx?ILWHBNjF4clKo8UY2fiQHA==']
    url_list = []
    count = 0


    def parse(self, response):
    	url_list2 = []
        date_list = []
        title_list =[]

        html = response.body

        _VIEWSTATE = re.findall(r'id="__VIEWSTATE.*?value="(.*?)"',html)[0]
        _EVENTVALIDATION = re.findall(r'id="__EVENTVALIDATION.*?value="(.*?)"',html)[0]

        title = re.findall(r'<nobr><a href=".*?>(.*?)</a></nobr>',html)
        #print(title[0])

        dates = response.xpath('//td/nobr/text()').extract()
        #for date in dates:
        	#print(date)

        half_link = re.findall(r'<nobr><a href="(.*?)"',html)
        #print(half_link[0])

        for j in range(0,len(title)):
            title_list.append(title[j])
            date_list.append(dates[j])
            url_link = "http://www.ddkggzy.com/lbv3/" + half_link[j]
            self.url_list.append(url_link)
            url_list2.append(url_link)

        results1 =[]
        results1.extend(url_list2)
        for k in range(0,len(results1)):
            results1[k] = "date:" + date_list[k] + " ; " + "title: " + title_list[k] + " ; " + "web: " + url_list2[k] + '\n'
            #print(results1[k])
        #with open('/home/jessyl/DaDuKou2/第一部分爬取内容.txt','a') as f1:
            #f1.writelines(results1)

        values = {
                "__EVENTTARGET": "",
                "__EVENTARGUMENT": "",
                "__VIEWSTATE":_VIEWSTATE,
                "__VIEWSTATEGENERATOR": "408E0053",
                "__EVENTVALIDATION": _EVENTVALIDATION,
                "ctl00$n_list7$searchBox": "",
                "ctl00$ContentPlaceHolder2$TextBox1": "", 
                "ctl00$ContentPlaceHolder2$TextBox2": "",
                "ctl00$ContentPlaceHolder2$TextBox3": "",
                "ctl00$ContentPlaceHolder2$F3": "下一页"
        }
        postdata = values

        if len(self.url_list) != 251:
        #if len(self.url_list) != 40:
            print("yes")
            print(len(self.url_list))
            yield scrapy.FormRequest(
            url = response.url,
            formdata = postdata,
            callback = self.parse
        )
        
        else:
            print("no")
            for i in range(0,len(self.url_list)):
                yield Request(url=self.url_list[i],callback=self.page_in)

    def page_in(self,response):
        self.count += 1
        print(self.count)
        html2 = etree.HTML(response.text)
        
        project = u'(项目名称.*)'
        project_num = u'(招标公告编号.*)'     
        zb_person = u'(招标人.*)'
        zb_agent = u'(招标代理机构.*)'
        fh_p = u'(第一中标侯选人.*)'
        sh_p = u'(第二中标侯选人.*)'
        th_p = u'(第三中标侯选人.*)'
        n_p = u'(拟中标人.*)'
        gongshang_num = u'(工商注册号.*)'
        ts_agent = u'(投诉受理部门.*)'

        results = []

        for n in range(0,20):
            contents = html2.xpath('//tr[4]//td[2]/div/table/tbody/tr[' + str(n) + ']//text()')
            #print(contents)
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
                results.extend(pro_name)
                results.append("\n")

            #project_num = u'(招标公告编号.*)'
            pro_num = re.findall(project_num,contents2,re.S)
            if pro_num != []:
                results.extend(pro_num)
                results.append("\n")
 
            #zb_person = u'(招标人.*)'
            zb_p = re.findall(zb_person,contents2,re.S)
            if zb_p != []:
                results.extend(zb_p)
                results.append("\n")


            #zb_agent = u'(招标代理机构.*)'
            zba = re.findall(zb_agent,contents2,re.S)
            if zba != []:
                results.extend(zba)
                results.append("\n")


            #fh_p = u'(第一中标侯选人.*)'
            fhp = re.findall(fh_p,contents2,re.S)
            if fhp != []:
                results.extend(fhp)
                results.append("\n")


            #sh_p = u'(第二中标侯选人.*)'
            shp = re.findall(sh_p,contents2,re.S)
            if shp != []:
                results.extend(shp)
                results.append("\n")


            #th_p = u'(第三中标侯选人.*)'
            thp = re.findall(th_p,contents2,re.S)
            if thp != []:
                results.extend(thp)
                results.append("\n")


            #n_p = u'(拟中标人.*)'
            np = re.findall(n_p,contents2,re.S)
            if np != []:
                results.extend(np)
                results.append("\n")

            
            #gongshang_num = u'(工商注册号.*)'
            gsn = re.findall(gongshang_num,contents2,re.S)
            if gsn != []:
                results.extend(gsn)
                results.append("\n")

            
            #ts_agent = u'(投诉受理部门.*)'
            tsa = re.findall(ts_agent,contents2,re.S)
            if tsa != []:
                results.extend(tsa)
                results.append("\n")

        results2 = ''.join(results)
        results3 = "NO." + str(self.count) + "\n" + results2
        print(results3)

        item = Dadukou2Item()
        item['answer'] = results3
        yield item

