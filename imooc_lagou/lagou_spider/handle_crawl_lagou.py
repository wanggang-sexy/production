# coding:utf-8
import requests
import re
import time
import json
import multiprocessing
from imooc_lagou.lagou_spider.handle_insert_data import lagou_mysql


class HandleLaGou(object):
    def __init__(self):
        #使用sesssion保存cookies信息
        self.lagou_session = requests.session()
        self.header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36"
        }
        self.city_list = ""

     #获取全国所有城市列表的方法
    def handle_city(self):
        city_search = re.compile(r'www\.lagou\.com\/.*\/">(.*?)</a>')
        city_url = "https://www.lagou.com/jobs/allCity.html"
        city_result = self.handle_request(method="GET",url=city_url)
        #使用正则表达式获取城市列表
        self.city_list = city_search.findall(city_result)
        self.lagou_session.cookies.clear()


    def handle_city_job(self,city):#获取cookies信息
        first_request_url = "https://www.lagou.com/jobs/list_python?city=%s&cl=false&fromSearch=true&labelWords=&suginput="%city
        first_response = self.handle_request(method="GET",url=first_request_url)
        total_page_search = re.compile(r'class="span\stotalNum">(\d+)</span>')
        try:#无岗位信息
            total_page = total_page_search.search(first_response).group(1)
        except:
            return
        else:
            for i in range(1,int(total_page)+1):
                data = {
                    "pn":i,
                    "kd":"python"
                }
                page_url = "https://www.lagou.com/jobs/positionAjax.json?city=%s&needAddtionalResult=false"%city
                referer_url = "https://www.lagou.com/jobs/list_python?city=%s&cl=false&fromSearch=true&labelWords=&suginput="%city
                #referer的URL需要进行encode
                self.header['Referer'] = referer_url.encode()
                response = self.handle_request(method="POST",url=page_url,data=data,info=city)
                lagou_data = json.loads(response)
                job_list = lagou_data['content']['positionResult']['result']
                for job in job_list:
                    lagou_mysql.insert_item(job)
                    #print(job)

    def handle_request(self,method,url,data=None,info=None):
        while True:
            #加入阿布云的动态代理
            proxyinfo = "http://%s:%s@%s:%s" %('H9IL66892177J4HD','0A2E3026F00EB2E4','http-dyn.abuyun.com','9020')
            proxy = {
                "http":proxyinfo,
                "https":proxyinfo
            }
            #proxies=proxy代理
            try:
                if method == "GET":
                    response = self.lagou_session.get(url=url,headers=self.header,timeout=6)
                elif method == "POST":
                    response = self.lagou_session.post(url=url,headers=self.header,data=data,timeout=6)
                #response.encoding = 'utf-8'
            except:
                self.lagou_session.cookies.clear()
                # 重新获取cookies信息
                first_request_url = "https://www.lagou.com/jobs/list_python?city=%s&cl=false&fromSearch=true&labelWords=&suginput=" % info
                self.handle_request(method="GET", url=first_request_url)
                time.sleep(10)
                continue
            if "频繁" in response.text:
                print(response.text)
                #需要先清除cookies信息
                self.lagou_session.cookies.clear()
                #重新获取cookies信息
                first_request_url = "https://www.lagou.com/jobs/list_python?city=%s&cl=false&fromSearch=true&labelWords=&suginput=" %info
                self.handle_request(method="GET", url=first_request_url)
                time.sleep(10)
                continue
            return response.text

if __name__ == "__main__":
    lagou = HandleLaGou()
    lagou.handle_city()
    '''
    #引入多进程加速抓取
    pool = multiprocessing.Pool(2)#定义进程池
    for city in lagou.city_list:
        pool.apply_async(lagou.handle_city_job,args=(city,))#添加到进程里面
    pool.close()#关闭进池
    pool.join()
    '''
    for city in lagou.city_list:
        print(city)
        lagou.handle_city_job(city)

