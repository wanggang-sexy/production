#coding:utf-8
from imooc_lagou.lagou_spider.create_lagou_tables import Lagoutables
from imooc_lagou.lagou_spider.create_lagou_tables import Session
import time
from collections import Counter
from sqlalchemy import func



class HandleLagouData(object):
    def __init__(self):
        #实例化session信息
        self.mysql_session = Session()
        self.data = time.strftime("%Y-%m-%d",time.localtime())


    #数据的存储方法
    def insert_item(self,item):
        date = time.strftime("%Y-%m-%d",time.localtime())
        #定义数据存储结构
        data = Lagoutables(
            #岗位ID
            positionID = item['positionId'],
            # 经度
            longitude = item['longitude'],
            # 维度
            latitude = item['latitude'],
            # 岗位名称
            positionName = item['positionName'],
            # 工作年限
            workYear = item['workYear'],
            # 学历
            education = item['education'],
            # 岗位性质
            jobNature = item['jobNature'],
            # 公司类型
            financeStage = item['financeStage'],
            # 公司规模
            companySize = item['companySize'],
            # 业务方向
            industryField = item['industryField'],
            # 所在城市
            city = item['city'],
            # 岗位标签
            positionAdvantage = item['positionAdvantage'],
            # 公司简称
            companyShortName = item['companyShortName'],
            # 公司全称
            companyFullName = item['companyFullName'],
            # 公司所在区
            district = item['district'],
            # 公司福利标签
            companyLabelList = ','.join(item['companyLabelList']),
            # 工资
            salary = item['salary'],
            # 抓取日期
            crawl_data = date
        )


        #存储数据前，查询表中是否有岗位信息
        query_result = self.mysql_session.query(Lagoutables).filter(Lagoutables.crawl_data==date,Lagoutables.positionID==item['positionId']).first()

        if query_result:
            print('该岗位信息已存在%s:%s:%s'%(item['positionId'],item['city'],item['positionName']))
        else:
            #插入数据
            self.mysql_session.add(data)
            #提交数据
            self.mysql_session.commit()
            print('新增岗位信息:%s'%item['positionId'])

    #查询行业及职位数量
    def query_industryfield_result(self):
        info = {}
        #查询今日抓取到的行业信息
        result = self.mysql_session.query(Lagoutables.industryField).filter(
            Lagoutables.crawl_data==self.data
        ).all()
        result_list1 = [x[0].split(',')[0] for x in result]
        result_list2 = [x for x in Counter(result_list1).items() if x[1]>110]
        #填充的是series里面的data
        data = [{"name":x[0],"value":x[1]} for x in result_list2]
        name_list = [name['name'] for name in data]
        info['x_name'] = name_list
        info['data']= data
        return info

    def query_salary_result(self):
        info = {}
        #查询今日薪资情况
        result = self.mysql_session.query(Lagoutables.salary).filter(
            Lagoutables.crawl_data==self.data
        ).all()
        result_list1 = [x[0] for x in result]
        result_list2 = [x for x in Counter(result_list1).items() if x[1]>90]
        #填充的是series里面的data
        data = [{"name":x[0],"value":x[1]} for x in result_list2]
        name_list = [name['name'] for name in data]
        info['x_name'] = name_list
        info['data'] = data
        return info

    def query_financeStage_result(self):
        info = {}
        #查询公司融资情况
        result = self.mysql_session.query(Lagoutables.financeStage).filter(
            Lagoutables.crawl_data==self.data
        ).all()#列表包含元组
        result_list1 = [x[0] for x in result]#转换为列表，数据转换
        result_list2 = [x for x in Counter(result_list1).items() if x[1] > 90]#数据转换，列表包含元组
        #填充的是series里面的data
        data = [{"name":x[0],"value":x[1]} for x in result_list2]#数据转换字典
        name_list = [name["name"] for name in data]#从字典中取出键值
        info["x_name"] = name_list#创建字典
        info['data'] = data
        return info


    def query_companySize_tesult(self):
        info = {}
        #公司规模
        result = self.mysql_session.query(Lagoutables.companySize).filter(
            Lagoutables.crawl_data==self.data
        ).all()
        result_list1 = [x[0] for x in result]
        result_list2 = [x for x in Counter(result_list1).items()]
        #填充数据转换，series里面的data
        data = [{'name':x[0],"value":x[1]} for x in result_list2]
        name_list = [name['name'] for name in data]
        info['x_name'] = name_list
        info['data'] = data
        return info

    def query_jobNature_result(self):
        info = {}
        #岗位要求
        result = self.mysql_session.query(Lagoutables.jobNature).filter(
            Lagoutables.crawl_data==self.data
        ).all()
        result_list1 = [x[0] for x in result]
        result_list2 = [x for x in Counter(result_list1).items() if x[1] > 9]
        #填充数据转换
        data = [{"name":x[0],"value":x[1]} for x in result_list2]
        name_list = [name['name'] for name in data]
        info['x_name'] = name_list
        info['data'] = data
        return info


    def query_job_result(self):
        info = {}
        #岗位数量
        result = self.mysql_session.query(Lagoutables.crawl_data,func.count('*').label('c')).group_by(
            Lagoutables.crawl_data
        ).all()
        #数据填充
        data = [{"name":x[0],"value":x[1]} for x in result]
        name_list = [name['name'] for name in data]
        name_value = [value['value'] for value in data]
        info['x_name'] = name_list
        info['data'] = data
        return info

    def query_workyear_result(self):
        info = {}
        #工作经验
        result = self.mysql_session.query(Lagoutables.workYear).filter(
            Lagoutables.crawl_data==self.data
        ).all()
        result_list1 = [x[0] for x in result]
        result_list2 = [x for x in Counter(result_list1).items()]
        #数据格式转换
        data = [{"name":x[0],"value":x[1]} for x in result_list2]
        name_list = [name['name'] for name in data]
        info['x_name'] = name_list
        info['data'] = data
        return info

    def query_education_result(self):
        info = {}
        #学历
        result = self.mysql_session.query(Lagoutables.education).filter(
            Lagoutables.crawl_data==self.data
        ).all()
        result_list1 = [x[0] for x in result]
        result_list2 = [x for x in Counter(result_list1).items()]
        #数据格式转换
        data = [{"name":x[0],"value":x[1]} for x in result_list2]
        name_list = [name['name'] for name in data]
        info['x_name'] = name_list
        info['data'] = data
        return info

    def query_count_result(self):
        #总数量及今日数量显示
        info = {}
        total_num = self.mysql_session.query(Lagoutables).count()
        today_num = self.mysql_session.query(Lagoutables).filter(
            Lagoutables.crawl_data==self.data
        ).count()
        info['total_num'] = total_num
        info['today_num'] = today_num
        return info

    def query_city_result(self):
        info = {}
        #城市统计
        result = self.mysql_session.query(Lagoutables.city,func.count('*').label('c')).filter(
            Lagoutables.crawl_data==self.data).group_by(Lagoutables.city
        ).all()
        data = [{"name":x[0],"value":x[1]} for x in result]
        name_list = [name['name'] for name in data]
        info['x_name'] = name_list
        info['data'] = data
        #print(result)
        return info



lagou_mysql = HandleLagouData()
#lagou_mysql.query_industryfield_result()
#lagou_mysql.query_salary_result()
#lagou_mysql.query_financeStage_result()
#lagou_mysql.query_companySize_tesult()
#lagou_mysql.query_positionAdvantage_result()
#lagou_mysql.query_positionName_result()
#lagou_mysql.query_workyear_result()
#lagou_mysql.query_education_result()
#lagou_mysql.query_count_result()
lagou_mysql.query_city_result()