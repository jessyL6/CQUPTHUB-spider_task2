import scrapy
import json
from scrapy.http import Request
from lxml import etree
from YuZhongQu2.items import Yuzhongqu2Item
import re

class Yuzhongqu2Spider(scrapy.Spider):
    name = 'yuzhongqu2'
    allowed_domains = ['www.cqyzbid.com']
    start_urls = ['http://www.cqyzbid.com/cqyzwz/jyxx/003001/003001004/MoreInfo.aspx?CategoryNum=003001004']
    url_list = []
    count = 0
    i =1

    def parse(self, response):
        url_list2 = []
        date_list = []
        title_list =[]

        html = response.body
        html = html.decode('utf-8')

        _VIEWSTATE = re.findall(r'id="__VIEWSTATE.*?value="(.*?)"',html)[0]

        title = re.findall(r'target="_blank".*?>(.*?)</a>',html)
        #for i in title:
            #print(i)
   
        '''dates = response.xpath('//*[@id="MoreInfoList1_DataGrid1"]/tbody/tr/td[3]/text()').extract()
        print(dates)
        dates = re.findall(r'border-style:None;width:80px;">(.*?)</td>',html)
        print(dates)'''

        half_link = re.findall(r'<a href="(.*?)" target="_blank" title="',html)
        #print(half_link)

        for j in range(0,len(half_link)):
            title_list.append(title[j])
            #date_list.append(dates[j])
            url_link = "http://www.cqyzbid.com" + half_link[j]
            self.url_list.append(url_link)
            url_list2.append(url_link)

        results1 =[]
        results1.extend(url_list2)
        for k in range(0,len(results1)):
            #results1[k] = "date:" + date_list[k] + " ; " + "title: " + title_list[k] + " ; " + "web: " + url_list2[k] + '\n'
            results1[k] =  "title: " + title_list[k] + " ; " + "web: " + url_list2[k] + '\n'
            #print(results1[k])
        #with open('/home/jessyl/YuZhongQu2/第一部分爬取内容.txt','a') as f1:
            #f1.writelines(results1)

        #if len(self.url_list) != 870:
        if len(self.url_list) != 40:
            self.i +=1
            print("yes")
            print(len(self.url_list))
            values = {
                    "__VIEWSTATE":_VIEWSTATE,
                    "__EVENTTARGET": "MoreInfoList1$Pager",
                    "__EVENTARGUMENT": "{}".format(self.i),
            }
            postdata = values
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
        self.count +=1
        #print(self.count)
        html2 = etree.HTML(response.text)
         
        project = u'(项目名称.*)'
        project_num = u'(招标公告编号.*)'     
        zb_person = u'(招标人.*)'
        zb_agent = u'(招标代理机构.*)'
        bx_person = u'(比选人.*)'
        bx_agent = u'(比选代理机构.*)'
        fh_p = u'(第一中标侯选人.*)'
        sh_p = u'(第二中标侯选人.*)'
        th_p = u'(第三中标侯选人.*)'
        n_p = u'(拟中标人.*)'
        n_money =u'(拟中标价.*)'
        gongshang_num = u'(工商注册号.*)'            
        ts_agent = u'(投诉受理部门.*)'                                              
        
        #有一部分网页布局不同注意后面分类:但是实在太多，所以选了一个作为例子，方法都是一样的

        '''eg:
        //*[@id="TDContent"]/div/div/table/tbody/tr[1]
        //*[@id="TDContent"]/div/table/tbody/tr/td/div/table/tbody/tr[1]                                                                          
        //*[@id="TDContent"]/div/div[1]/table/tbody/tr[2]
        //*[@id="TDContent"]/div/table/tbody//text
        //*[@id="TDContent"]/div/div/div/table/tbody
        //*[@id="TDContent"]/div/div/table/tbody/tr[1]
        //*[@id="TDContent"]/div/div[1]/table/tbody'''
        
        results = []
        for n in range(0,20):       
            contents = html2.xpath('//*[@id="TDContent"]/div/div[1]/table/tbody/tr['+str(n)+']//text()')
            #有一部分网页布局不同注意后面分类
            #print(contents)
            while "\r\n" in contents:
                contents.remove("\r\n")
            while "/" in contents:
                contents.remove("/")

            contents = [''.join(x.split()) for x in contents]
            #这是列表内每个元素去除xa0等空白字符
            contents2 = ''.join(contents)
            #print(type(contents2))
            #print(contents2)

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

            #bx_person = u'(比选人.*)'
            bxp = re.findall(bx_person,contents2,re.S)
            if bxp != []:
                results.extend(bxp)
                results.append("\n")

            #bx_agent = u'(比选代理机构.*)'
            bxa = re.findall(bx_agent,contents2,re.S)
            if bxa != []:
                results.extend(bxa)
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

            #n_money =u'(拟中标价.*)'
            n_m = re.findall(n_money,contents2,re.S)
            if n_m != []:
                results.extend(n_m)
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

        item = Yuzhongqu2Item()
        item['answer'] = results3
        yield item



