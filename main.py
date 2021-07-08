import requests
import json


def spider(page_no):
    hasNext = True
    totalData = []
    while hasNext:
        url = "https://nc.mofcom.gov.cn/jghq/priceList"
        payload = {'pageNo': page_no,
                   'queryDateType': '4',
                   'sortColumns': '[{"column":"GET_P_DATE","ordername":"asc"}]',
                   'timeRange': '2021-07-07 ~ 2021-07-08'}
        headers = {
            'Cookie': 'insert_cookie=28314071'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        jsonResult = json.loads(response.text)
        data = jsonResult['result']
        totalData.extend(data)
        hasNext = jsonResult['hasNext']
        page_no = page_no + 1
        print("request:%d,count:%d,total:%d" % (page_no, len(data), len(totalData)))
    print(totalData)


if __name__ == '__main__':
    spider(1)
