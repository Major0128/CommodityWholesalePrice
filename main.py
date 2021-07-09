import datetime
import requests
import json
import time

from MSSQL import MSSQL

msClient = 0


# 读取数据库信息
def set_db_config():
    print("请输入数据库地址：")
    db_host = input()
    print("请输入数据库端口：")
    db_port = input()
    print("请输入数据库用户名：")
    db_user = input()
    print("请输入数据库密码：")
    db_pwd = input()
    print("请输入数据库名称：")
    db_name = input()
    print("正在初始化数据库连接：%s:%s:%s" % (db_host, db_port, db_name))
    msClient = MSSQL(db_host, db_user, db_pwd, db_name)
    try:
        msClient.GetConnect()
        print("数据库连接成功")
        # noinspection SqlResolve
        sql = "select count(name) as co from sysobjects where name = 'commodity_wholesale_price'"
        table_num = (msClient.ExecQuery(sql))[0][0]
        if table_num != 1:
            print("未检测到表，开始创建")
            sql_file = open('commodity_wholesale_price.sql', 'r')
            msClient.ExecSql(sql_file)
            sql_file.close()
            table_num = (msClient.ExecQuery(sql))[0][0]
            if table_num == 1:
                print("创建数据表成功")
        else:
            print("检测到数据表")
    except:
        print("数据库连接失败")


# 处理查询时间
def get_query_date():
    print("请选择爬取数据日期")
    print("1:指定日期（不超过3个月时间间隔）")
    print("2:自动爬取至当前日期")
    query_date_type = input()
    start_date = ""
    end_date = ""
    if query_date_type == 1:
        print("请输入开始日期,yyyy-mm-dd")
        start_date = input()
        print("请输入结束日期,yyyy-mm-dd")
        end_date = input()
    if query_date_type == 2:
        sql = "SELECT max(price_date) FROM commodity_wholesale_price"
        lastest_price_date = (msClient.ExecQuery(sql))[0][0]
        delta = datetime.timedelta(days=1)
        start_date = lastest_price_date + delta
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = time.strftime("%Y-%m-%d", time.localtime())
    return start_date, end_date


# 爬虫获取数据
def spider(page_no, start_date, end_date):
    url = "https://nc.mofcom.gov.cn/jghq/priceList"
    timeRange = "%s ~ %s" % (start_date, end_date)
    payload = {'pageNo': page_no,
               'pageSize': 500,
               'queryDateType': '4',
               'sortColumns': '[{"column":"GET_P_DATE","ordername":"asc"}]',
               'timeRange': timeRange}
    headers = {
        'Cookie': 'insert_cookie=28314071'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    jsonResult = json.loads(response.text)
    data = jsonResult['result']
    print("request:%d,count:%d" % (page_no, len(data)))
    return jsonResult['hasNext'], data


# 保存数据
def save_data(data):
    sql = "insert into commodity_wholesale_price(price_date, price, product_name, marketing_name, product_id, price_unit) values"
    for single_data in data:
        price_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(single_data["GET_P_DATE"] / 1000))
        price = single_data["AG_PRICE"]
        price_unit = single_data["C_UNIT"]
        product_name = single_data["CRAFT_NAME"]
        product_id = single_data["CRAFT_INDEX"]
        marketing_name = single_data["EUD_NAME"]
        sql = sql + "%s,%f,%s,%s,%d,%s" % (price_date, price, product_name, marketing_name, product_id, price_unit)
    msClient.ExecSql(sql)
    print("成功插入%d条" % (len(data)))


if __name__ == '__main__':
    set_db_config()
    start_date, end_date = get_query_date()
    page_no = 1
    has_next = True
    while has_next:
        has_next, data = spider(page_no, start_date, end_date)
        save_data(data)
    print("插入成功")
