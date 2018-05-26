


# coding:utf-8
import re
import time # 使用time模设置时间
import datetime 
import requests
import sqlite3
import json
import random
from bs4 import BeautifulSoup


def buliding_find(page_num):
    
    global page_now,page_all,page_next,page_cha,buliding_sum,build_info,check_done

    
    conn = sqlite3.connect("TZ_FangChan.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS taizhou
           (
           id             integer PRIMARY KEY autoincrement, 
           name           TEXT,
           info           TEXT,
           mi2            NUMERIC,
           tel            TEXT,
           avg            NUMERIC,
           howsell        TEXT,
           getdate        TEXT,
           GPS_lat        TEXT,
           GPS_lng        TEXT);''')
    conn.commit()
    
    
    link = 'http://tz.tmsf.com/newhouse/property_searchall.htm'

    headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '136',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'tz.tmsf.com',
        'Origin': 'http://tz.tmsf.com',
        'Referer': 'http://tz.tmsf.com/newhouse/property_searchall.htm',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    }

    postdata={
        'keytype':' 1',
        'keyword':'' ,
        'sid':'331000',
        'districtid': '',
        'areaid':'' ,
        'dealprice':'' ,
        'propertystate':'',
        'propertytype':'' ,
        'ordertype': '',
        'priceorder': '',
        'openorder': '',
        'page': page_num
        }

    cookie_str = r'JSESSIONID=8A16C08E75765B848E460F642109709B; Hm_lvt_a1aa04488030878537d6d809bdd46a64=1525344891; Hm_lpvt_a1aa04488030878537d6d809bdd46a64=1525345832'
    cookies = {}
    for line in cookie_str.split(';'):
        key, value = line.split('=', 1)
        cookies[key] = value
    

    res= requests.post(link,headers=headers,data=postdata,cookies = cookies)
    res = res.content.decode('utf-8')

    soup = BeautifulSoup(res,"lxml")
    
    #批量替换图片型数字
    soup = re.sub(r'<span class="numbbone"></span>', "1", str(soup))
    soup = re.sub(r'<span class="numbbtwo"></span>', "2", soup)
    soup = re.sub(r'<span class="numbbthree"></span>', "3", soup)
    soup = re.sub(r'<span class="numbbfour"></span>', "4", soup)
    soup = re.sub(r'<span class="numbbfive"></span>', "5", soup)
    soup = re.sub(r'<span class="numbbsix"></span>', "6", soup)
    soup = re.sub(r'<span class="numbbseven"></span>', "7", soup)
    soup = re.sub(r'<span class="numbbeight"></span>', "8", soup)
    soup = re.sub(r'<span class="numbbnine"></span>', "9", soup)
    soup = re.sub(r'<span class="numbbzero"></span>', "0", soup)
    soup = re.sub(r'<span class="numbone"></span>', "1", (soup))
    soup = re.sub(r'<span class="numbtwo"></span>', "2", soup)
    soup = re.sub(r'<span class="numbthree"></span>', "3", soup)
    soup = re.sub(r'<span class="numbfour"></span>', "4", soup)
    soup = re.sub(r'<span class="numbfive"></span>', "5", soup)
    soup = re.sub(r'<span class="numbsix"></span>', "6", soup)
    soup = re.sub(r'<span class="numbseven"></span>', "7", soup)
    soup = re.sub(r'<span class="numbeight"></span>', "8", soup)
    soup = re.sub(r'<span class="numbnine"></span>', "9", soup)
    soup = re.sub(r'<span class="numbzero"></span>', "0", soup)
    soup = re.sub(r'<span class="numbdor"></span>', ".", soup)
#    soup = re.sub(r' ', "", soup) #替换空格
    soup = re.sub(r'	', "", soup)  #替换乱七八糟的字符
    soup = BeautifulSoup(soup,"lxml") #重新整理，lxml方式格式化
#    print(soup.prettify())
#=====分析网页字段=================================================================

    #取得当前页，总页码，
    for num_info in soup.find_all("font",class_='green1'):
        num_allinfo = re.findall(r'\d+',num_info.text)

    page_now = int(num_allinfo[0])
    page_all = int(num_allinfo[1])
    page_cha = int(num_allinfo[1])-int(num_allinfo[0])

    
    #取得检索命中数
    for bulidingnuml in soup.find_all("span",class_='s_how01'):
        buliding_sumlist = re.findall(r'\d+',bulidingnuml.text)
   #列表转换成字符串 buliding_sum = int(buliding_sum)   
    buliding_sum = int(buliding_sumlist[0])

#    print("buliding_sum",buliding_sum) 
    

#==================================================================
    build_name_info = []
    build_info_info = []
    build_sell_mi2_info = []
    build_sell_tel_info = []
    build_sell_avg_info = []
    build_howsell_info = []
    
    for i in soup.find_all("li",class_=None):
        soup2=BeautifulSoup(i.prettify(),'lxml')
#        print(soup2)
        
        build_name = soup2.find_all("div","a",class_= 'build_txt')
        for b_name in build_name:
            name = b_name.a.text.strip(' ').replace('\r','').replace('\n','').replace('\t','').replace(' ','')
            build_name_info.append(name)
                
        build_info = soup2.find_all("p",class_= 'build_txt04')
        for b_info in build_info:
            info = b_info.text.strip(' ').replace('\r','').replace('\n','').replace('\t','').replace(' ','')
            build_info_info.append(info)
                
        build_sell_mi2 = soup2.find_all("div","p",class_= 'build_txt06')
        for b_mi2 in build_sell_mi2:
            mi2 = b_mi2.p.text.replace('\r','').replace('\n','').replace('\t','').replace('元/㎡','').strip(' ')
            build_sell_mi2_info.append(mi2)
                
        build_sell_tel = soup2.find_all("div",class_= 'build_txt05')
        for b_tel in build_sell_tel:
            tel = b_tel.text.replace('\r','').replace('\n','').replace('\t','').replace('售楼电话：','').strip(' ')
            build_sell_tel_info.append(tel)

        build_sell_avg = soup2.find_all(text=re.compile("累计均价"))
        for b_avg in build_sell_avg:
            avg = b_avg.replace('\r','').replace('\n','').replace('\t','').replace('累计均价','').replace('元/㎡','').strip(' ')
            build_sell_avg_info.append(avg)
                
        build_howsell = soup2.find_all("div",class_= 'howsell')
        for b_howsell in build_howsell:
            howsell = b_howsell.text.replace('\r','').replace('\n','').replace('\t','').replace('可售','').replace('套数','').replace('总','').strip(' ').replace(' ','')
            build_howsell_info.append(howsell)
        
    get_date_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        
    n = 0
    length=len(build_name_info)
    while n < length:
        build_name_info1 = build_name_info[n]
        build_info_info1 = build_info_info[n]
        build_sell_mi2_info1 = build_sell_mi2_info[n]
        build_sell_tel_info1 =build_sell_tel_info[n]
        build_sell_avg_info1 = build_sell_avg_info[n]
        build_howsell_info1 = build_howsell_info[n]
        insert_sql = """INSERT INTO taizhou (id,name,info,mi2,tel,avg,howsell,getdate) VALUES (null,?,?,?,?,?,?,?);"""
        c.execute(insert_sql,(build_name_info1,build_info_info1,build_sell_mi2_info1,build_sell_tel_info1,build_sell_avg_info1,build_howsell_info1,get_date_time))
#        print(u'正在存储第%d页第%d条数据' %(page_now,n))
        conn.commit()
#        time.sleep(1)
#        print(u'第%d条数据存储完毕' %n)
        n=n+1
#    print('第%d页数据存储完毕' %page_now)
    print(u'从刚才提取的情况看，你需要的数据共有%d条，共%d页，目前你已提取到了第%d页' %(buliding_sum,page_all,page_now))
    
    
#============================================================        
    
#============================================================
    
    if page_now < page_all:
        check_done = False
        page_next = page_now+1
    else:
        check_done = True
        
    print(page_now,page_all,page_next,page_cha,buliding_sum,check_done)
    c.close()
    conn.close()
    return(page_now,page_all,page_next,page_cha,buliding_sum,check_done) 


#================================================
#加入时间概念，随机时间爬取
def main(run_num):
    h = 2 #random.randint(1,11)
    m = 4 #random.randint(1,59)
    print(u'这是第%d次运行',%rum_num)
    print (u'下次运行时间',h,m)
    while True:  
        now = datetime.datetime.now()
        print(now.hour, now.minute)
        if now.hour == h and now.minute == m:
            break  
# 每隔60秒检测一次
        time.sleep(60)
    letsgo()
    get_gps()
    print('今天的任务完成，等待明天继续重启运行')
    waitToTomorrow()
    
#================================================
def letsgo():
    global page_now,page_all,page_next,page_cha,buliding_sum,build_info,check_done
    page_num = 1
    print('当前提取第1页数据')
    buliding_find(page_num)
    print('第1页数据提取完毕')

    while check_done is False:
        buliding_find(page_next)
    else:
        print('你需要的全部数据均已提取完毕！')
        
def get_gps():
    conn = sqlite3.connect("TZ_FangChan.db")
    d = conn.cursor()
    cursor = d.execute('select id,name,GPS_lat,GPS_lng from taizhou where GPS_lat is null')
    alllist = cursor.fetchall()
    print(alllist)
    for row in alllist:
        FC_id = row[0]
        FC_name = row[1]
        FC_lat = row[2]
        FC_lng = row[3]
        FC_name = FC_name.replace("·", "")
        decodejson = getjson(FC_name)
        time.sleep(1)
        print(decodejson)
        if decodejson['result']:
            try:
                for each_zhongdian in decodejson['result']:
                    try:
                        name = each_zhongdian['name']
                    except:
                        name = None
                    try:
                        navi_lat = each_zhongdian['location']['lat']
                    except:
                        navi_lat = None
                    try:
                        navi_lng = each_zhongdian['location']['lng']
                    except:
                        navi_lng = None

                    neirong = {
                        'id':FC_id,
                        'name':FC_name,
                        'navi_lat':navi_lat,
                        'navi_lng':navi_lng,
                    }
                    print(neirong)
                    time.sleep(1)
                    break
                update_sql = "UPDATE taizhou SET GPS_lat = ? , GPS_lng = ? " + "WHERE ID = ?"
                d.execute(update_sql,(navi_lat,navi_lng,FC_id))
                conn.commit()
            except: 
                print('无法查询到信息！')
                continue
                
        print(u'正在更新第%d条积累的GPS地址' % (FC_id))
        
    conn.close()
    print('所有地址关联GPS完毕')
    
def getjson(QUERY_MESSAGE):
     
    headers ={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4882.400 QQBrowser/9.7.13059.400'
    }

    PLACE_MESSAGE={
        'ak':'EGCf8va5kBw2iFybsuEOyzDC9c3VfaKD',
        'query':QUERY_MESSAGE,
        'output':'json',
        'region':244,
        'city_limit':'true'
    }
    
    r=requests.get("http://api.map.baidu.com/place/v2/suggestion",params=PLACE_MESSAGE,headers= headers)
    decodejson =json.loads(r.text)
    return decodejson     
    
def waitToTomorrow():
#Wait to tommorow 00:00 am
    tomorrow = datetime.datetime.replace(datetime.datetime.now() + datetime.timedelta(days=1), 
    hour=0, minute=0, second=0)
    delta = tomorrow - datetime.datetime.now()
    time.sleep(delta.seconds)
    rum_number = run_number + 1
    main(run_number)
    
#================================================
if __name__ == "__main__": 
    main(1)


