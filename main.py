import datetime
import requests
import json
import time

from SqlServerOperate import SqlServerOperate

db_host = 'localhost'
db_port = '1433'
db_user = 'sa'
db_pwd = 'qwer1234!'
db_name = 'mall'


def spider(page_no, time_start_date):
    url = "https://nc.mofcom.gov.cn/jghq/priceList"
    timeRange = "%s ~ %s" % (time_start_date.strftime("%Y-%m-%d"), time.strftime("%Y-%m-%d", time.localtime()))
    payload = {'pageNo': page_no,
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


if __name__ == '__main__':
    hasNext = True
    page_no = 1
    data = []
    now = datetime.datetime.now()
    delta = datetime.timedelta(days=-1)
    n_days = now + delta
    start_time = n_days
    while hasNext:
        hasNext, data = spider(page_no, start_time)
        ms = SqlServerOperate(db_host, db_port, db_user, db_pwd, db_name)
        for single_data in data:
            sql_string = "INSERT INTO commodity_wholesale_price([AG_PRICE], [CRAFT_INDEX], [CRAFT_NAME], [C_UNIT], [EUD_NAME], [EUD_PIC], [GET_P_DATE], [ID], [PAR_INDEX], [PROMULGATE_DATE], [P_INDEX]) " \
                         "VALUES(%f,'%s','%s','%s','%s','%s','%s',%d,'%s','%s','%s')" % \
                         (single_data["AG_PRICE"], single_data["CRAFT_INDEX"], single_data["CRAFT_NAME"],
                          single_data["C_UNIT"], single_data["EUD_NAME"], single_data["EUD_PIC"],
                          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(single_data["GET_P_DATE"] / 1000)),
                          single_data["ID"], single_data["PAR_INDEX"],
                          time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(single_data["PROMULGATE_DATE"] / 1000)),
                          single_data["P_INDEX"])
            ms.exec_non_query(sql_string)
        print("request:%d insert success" % page_no)
        page_no = page_no + 1
