import requests
import json
import re
import os
import time
import csv

file_path = "/Users/xiangchao/Desktop/Tarena/eastmoney"
if not os.path.exists(file_path):
    os.mkdir(file_path)
os.chdir(file_path)

def set_table():
    print("欢迎下载东方财富报表")
    year = int(input('请输入要查询的年份（四位数2007-2018）：\n'))
    while (year < 2007 or year > 2018):
        year = int(input('年份输入错误，请重新输入:\n'))
    quarter = int(input('请输入小写数字季度(1:1季报，2-年中报，3：3季报，4-年报)：\n'))
    while (quarter < 1 or quarter > 4):
        quarter = int(input('季度数值输入错误，请重新输入:\n'))
    quarter = '{:02d}'.format(quarter * 3)
    if (quarter == '06') or (quarter == '09'):
        day = 30
    else:
        day = 31
    date = '{}-{}-{}'.format(year,quarter,day)

    tables = int(input('请输入查询的报表种类对应的数字(1-业绩报表；2-业绩快报表：3-业绩预告表；4-预约披露时间表；5-资产负债表；6-利润表；7-现金流量表): \n'))
    dict_tables = {1: '业绩报表', 2: '业绩快报表', 3: '业绩预告表',
                   4: '预约披露时间表', 5: '资产负债表', 6: '利润表', 7: '现金流量表'}

    dict = {1: 'YJBB', 2: 'YJKB', 3: 'YJYG',
            4: 'YYPL', 5: 'ZCFZB', 6: 'LRB', 7: 'XJLLB'}
    category = dict[tables]

    # js请求参数里的type，第1-4个表的前缀是'YJBB20_'，后3个表是'CWBB_'
    # 设置set_table()中的type、st、sr、filter参数
    if tables == 1:
        category_type = 'YJBB20_'
        st = 'latestnoticedate'
        sr = -1
        filter =  "(securitytypecode in ('058001001','058001002'))(reportdate=^%s^)" %(date)
    elif tables == 2:
        category_type = 'YJBB20_'
        st = 'ldate'
        sr = -1
        filter = "(securitytypecode in ('058001001','058001002'))(rdate=^%s^)" %(date)
    elif tables == 3:
        category_type = 'YJBB20_'
        st = 'ndate'
        sr = -1
        filter=" (IsLatest='T')(enddate=^2018-06-30^)"
    elif tables == 4:
        category_type = 'YJBB20_'
        st = 'frdate'
        sr = 1
        filter =  "(securitytypecode ='058001001')(reportdate=^%s^)" %(date)
    else:
        category_type = 'CWBB_'
        st = 'noticedate'
        sr = -1
        filter = '(reportdate=^%s^)' % (date)

    category_type = category_type + category
    # print(category_type)
    # 设置set_table()中的filter参数

    yield{
    'date':date,
    'category':dict_tables[tables],
    'category_type':category_type,
    'st':st,
    'sr':sr,
    'filter':filter
    }

def page_choose(page_all):
    start_page = int(input("请输入下载起始页数：\n"))
    nums = input("请输入要下载的页数：\n")
    print('*'*80)

    if nums.isdigit():
        end_page = start_page + int(nums)
    elif nums == '':
        end_page = int(page_all.group(1))
    else:
        print("页数输入错误")
    yield{
        'start_page':start_page,
        'end_page':end_page
    }
    

def get_table(date, category_type,st,sr,filter,page):
    url = 'http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?'
    params = {
        'type':category_type,
        'token':'70f12f2f4f091e459a279469fe49eca5',
        'st':st,
        'sr':sr,
        'p':page,
        'ps':50,
        'js':'var SEwPKMXD={pages:(tp),data: (x),font:(font)}',
        'filter':filter,
    }
    response = requests.get(url,params=params).text
    print(response)
    pat = re.compile('var.*?{pages:(\d+),data:.*?')
    page_all = re.search(pat, response)

    pattern = re.compile('var.*?data:(.*),font:(.*)}',re.S)
    items = re.search(pattern, response)
    data = items.group(1)
    code = items.group(2)
    code = json.loads(code)
    
    # 抓取数据时，发现数字文本都用字体文件代替，只能抓到对应的数字编码，然后需要作转换
    new_code = {}
    if code['FontMapping']:
        code = json.loads(code)
        code = code['FontMapping']
        for c in code:
            new_code[c['code']] = str(c['value'])
        for c in new_code:
            data = data.replace(c,new_code[c])
    data = json.loads(data)
    return page_all, data, page

def write_header(data,category):
    with open('{}.csv'.format(category),'a',encoding='utf_8_sig',newline='') as f:
        headers = list(data[0].keys())
        writer = csv.writer(f)
        writer.writerow(headers)

def write_table(data,page,category):
    print('\n正在下载第 %s 页表格' % page)
    for d in data:
        with open('{}.csv'.format(category),'a',encoding='utf_8_sig',newline='') as f:
            w = csv.writer(f)
            w.writerow(d.values())

def main(date, category_type, st, sr, filter, page):
    func = get_table(date, category_type, st, sr, filter, page)
    data = func[1]
    page = func[2]
    write_table(data,page,category)

if __name__ == '__main__':
    for i in set_table():
        date = i.get('date')
        category = i.get('category')
        category_type = i.get('category_type')
        st = i.get('st')
        sr = i.get('sr')
        filter = i.get('filter')
    constant = get_table(date,category_type,st,sr,filter,1)
    page_all = constant[0]

    for i in page_choose(page_all):
        start_page = i.get('start_page')
        end_page = i.get('end_page')

    write_header(constant[1],category)
    start_time = time.time()

    for page in range(start_page, end_page):
        main(date, category_type, st, sr, filter, page)

    end_time = time.time() - start_time
    print('下载完成')
    print('下载用时：{:.1f}s' .format(end_time))

    
        
                 
