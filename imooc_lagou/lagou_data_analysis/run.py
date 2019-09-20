#coding:utf-8
from flask import Flask
from flask import render_template,jsonify


from imooc_lagou.lagou_spider.handle_insert_data import lagou_mysql


#flask的实例化
app = Flask(__name__)
@app.route("/")
def index():
    return "Hello World"

@app.route("/get_echart_data")
def get_echart_data():
    info = {}
    info['echart_1'] = lagou_mysql.query_industryfield_result()
    info['echart_2'] = lagou_mysql.query_salary_result()
    info['echart_31'] = lagou_mysql.query_financeStage_result()
    info['echart_32'] = lagou_mysql.query_companySize_tesult()
    info['echart_33'] = lagou_mysql.query_jobNature_result()
    info['echart_4'] = lagou_mysql.query_job_result()
    info['echart_5'] = lagou_mysql.query_workyear_result()
    info['echart_6'] = lagou_mysql.query_education_result()
    info['map'] = lagou_mysql.query_city_result()
    return jsonify(info)

@app.route("/lagou/",methods=['GET','POST'])
def lagou():
    #总数量抓取，今日数量抓取
    result = lagou_mysql.query_count_result()
    return render_template("index.html",result=result)



if __name__ == '__main__':
    app.run(debug=True,host="127.0.0.1",port=8081)