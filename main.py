import random
from time import time, localtime
import cityinfo
from requests import get, post
from datetime import datetime, date
import sys
import os
import http.client, urllib
import json
from zhdate import ZhDate


def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)

def get_access_token():
    # appId
    app_id = config["app_id"]
    # appSecret
    app_secret = config["app_secret"]
    post_url = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                .format(app_id, app_secret))
    try:
        access_token = get(post_url).json()['access_token']
    except KeyError:
        print("获取access_token失败，请检查app_id和app_secret是否正确")
        os.system("pause")
        sys.exit(1)
    # print(access_token)
    return access_token

def get_birthday(birthday, year, today):
    birthday_year = birthday.split("-")[0]
    # 判断是否为农历生日
    if birthday_year[0] == "r":
        r_mouth = int(birthday.split("-")[1])
        r_day = int(birthday.split("-")[2])
        # 今年生日
        birthday = ZhDate(year, r_mouth, r_day).to_datetime().date()
        year_date = birthday


    else:
        # 获取国历生日的今年对应月和日
        birthday_month = int(birthday.split("-")[1])
        birthday_day = int(birthday.split("-")[2])
        # 今年生日
        year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        if birthday_year[0] == "r":
            # 获取农历明年生日的月和日
            r_last_birthday = ZhDate((year + 1), r_mouth, r_day).to_datetime().date()
            birth_date = date((year + 1), r_last_birthday.month, r_last_birthday.day)
        else:
            birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    return birth_day

def get_weather(province, city):
    # 城市id
    try:
        city_id = cityinfo.cityInfo[province][city]["AREAID"]
    except KeyError:
        print("推送消息失败，请检查省份或城市是否正确")
        os.system("pause")
        sys.exit(1)
    # city_id = 101280101
    # 毫秒级时间戳
    t = (int(round(time() * 1000)))
    headers = {
        "Referer": "http://www.weather.com.cn/weather1d/{}.shtml".format(city_id),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    url = "http://d1.weather.com.cn/dingzhi/{}.html?_={}".format(city_id, t)
    response = get(url, headers=headers)
    response.encoding = "utf-8"
    response_data = response.text.split(";")[0].split("=")[-1]
    response_json = eval(response_data)
    # print(response_json)
    weatherinfo = response_json["weatherinfo"]
    # 天气
    weather = weatherinfo["weather"]
    # 最高气温
    temp = weatherinfo["temp"]
    # 最低气温
    tempn = weatherinfo["tempn"]
    return weather, temp, tempn

#词霸每日一句
def get_ciba():
    if (Whether_Eng!="否"):
        url = "http://open.iciba.com/dsapi/"
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        r = get(url, headers=headers)
        note_en = r.json()["content"]
        note_ch1 = r.json()["note"][:20]
        note_ch2 = r.json()["note"][20:40] if len(r.json()["note"]) >= 40 else ""
        note_ch3 = r.json()["note"][40:60] if len(r.json()["note"]) >= 60 else ""
        note_ch4 = r.json()["note"][60:80] if len(r.json()["note"]) >= 80 else ""
        note_ch5 = r.json()["note"][80:100] if len(r.json()["note"]) >= 100 else ""
        return note_ch1,note_ch2,note_ch3,note_ch4,note_ch5, note_en
    else:
        return "",""

#彩虹屁
def caihongpi():
    if (caihongpi_API!="替换掉我"):
        conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
        params = urllib.parse.urlencode({'key':caihongpi_API})
        headers = {'Content-type':'application/x-www-form-urlencoded'}
        conn.request('POST','/caihongpi/index',params,headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        data = data["newslist"][0]["content"]
        if("XXX" in data):
            data.replace("XXX","东东")
        data1 = data[:20]
        data2 = data[20:40] if len(data) >= 40 else ""
        data3 = data[40:60] if len(data) >= 60 else ""
        data4 = data[60:80] if len(data) >= 80 else ""
        data5 = data[80:100] if len(data) >= 100 else ""
        return data1,data2,data3,data4,data5
    else:
        return ""


#朋友圈
def pyq():
    if (pyq_api!="替换掉我"):
        conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
        params = urllib.parse.urlencode({'key':pyq_api})
        headers = {'Content-type':'application/x-www-form-urlencoded'}
        conn.request('POST','/pyqwenan/index',params,headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        data = data["newslist"][0]["content"]
        data1 = data[:20]
        data2 = data[20:40] if len(data) >= 20 else ""
        data3 = data[40:60] if len(data) >= 40 else ""
        data4 = data[60:80] if len(data) >= 60 else ""
        data5 = data[80:100] if len(data) >= 80 else ""
        return data1,data2,data3,data4,data5
    else:
        return ""

#健康小提示API
def health():
    if (health_API!="替换掉我"):
        conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
        params = urllib.parse.urlencode({'key':health_API})
        headers = {'Content-type':'application/x-www-form-urlencoded'}
        conn.request('POST','/healthtip/index',params,headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        data = data["newslist"][0]["content"]
        data1 = data[:20]
        data2 = data[20:40] if len(data) >= 40 else ""
        data3 = data[40:60] if len(data) >= 60 else ""
        data4 = data[60:80] if len(data) >= 80 else ""
        data5 = data[80:100] if len(data) >= 100 else ""
        return data1,data2,data3,data4,data5
    else:
        return ""

#星座运势
def lucky():
    if (lucky_API!="替换掉我"):
        conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
        params = urllib.parse.urlencode({'key':lucky_API,'astro':astro})
        headers = {'Content-type':'application/x-www-form-urlencoded'}
        conn.request('POST','/star/index',params,headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        data = "工作指数："+str(data["newslist"][2]["content"])+"   今日概述："+str(data["newslist"][8]["content"])
        data1 = data[:20]
        data2 = data[20:40] if len(data) >= 40 else ""
        data3 = data[40:60] if len(data) >= 60 else ""
        data4 = data[60:80] if len(data) >= 80 else ""
        data5 = data[80:100] if 80<=len(data) else ""
        data6 = data[100:120] if len(data)>=100 else ""
        data7 = data[120:140] if len(data)>=120 else ""
        return data1,data2,data3,data4,data5,data6,data7
    else:
        return ""

#励志名言
def lizhi():
    if (lizhi_API!="替换掉我"):
        conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
        params = urllib.parse.urlencode({'key':lizhi_API})
        headers = {'Content-type':'application/x-www-form-urlencoded'}
        conn.request('POST','/lzmy/index',params,headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        data=data["newslist"][0]["saying"]
        data1 = data[:20]
        data2 = data[20:40] if len(data) >= 40 else ""
        data3 = data[40:60] if len(data) >= 60 else ""
        data4 = data[60:80] if len(data) >= 80 else ""
        data5 = data[80:100] if len(data) >= 100 else ""
        return data1,data2,data3,data4,data5
    else:
        return ""
        
#下雨概率和建议
def tip():
    if (tianqi_API!="替换掉我"):
        conn = http.client.HTTPSConnection('api.tianapi.com')  #接口域名
        params = urllib.parse.urlencode({'key':tianqi_API,'city':city})
        headers = {'Content-type':'application/x-www-form-urlencoded'}
        conn.request('POST','/tianqi/index',params,headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data)
        tips = data["newslist"][0]["tips"]
        tips_1 = tips[:20]
        tips_2 = tips[20:40] if len(tips) >= 40 else ""
        tips_3 = tips[40:60] if len(tips) >= 60 else ""
        tips_4 = data[60:80] if len(data) >= 80 else ""
        tips_5 = data[80:100] if len(data) >= 100 else ""
        return tips_1,tips_2,tips_3,tips_4,tips_5
    else:
        return "",""

#推送信息
def send_message(to_user, access_token, city_name, weather, max_temperature, min_temperature, pipi1,pipi2,pipi3,pipi4,pipi5, pyq1,pyq2,pyq3,pyq4,pyq5,lizhi1,lizhi2,lizhi3,lizhi4,lizhi5,tips1,tips2,tips3,tips4,tips5, note_ch1,note_ch2,note_ch3,note_ch4,note_ch5, note_en, health_tip1,health_tip2,health_tip3,health_tip4,health_tip5, lucky_1,lucky_2,lucky_3,lucky_4,lucky_5,lucky_6,lucky_7):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]
    # 获取在一起的日子的日期格式
    love_year = int(config["love_date"].split("-")[0])
    love_month = int(config["love_date"].split("-")[1])
    love_day = int(config["love_date"].split("-")[2])
    love_date = date(love_year, love_month, love_day)
    # 获取在一起的日期差
    love_days = str(today.__sub__(love_date)).split(" ")[0]
    # 获取所有生日数据
    birthdays = {}
    for k, v in config.items():
        if k[0:5] == "birth":
            birthdays[k] = v
    data = {
        "touser": to_user,
        "template_id": config["template_id"],
        "url": "http://weixin.qq.com/download",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{} {}".format(today, week),
                "color": get_color()
            },
            "city": {
                "value": city_name,
                "color": get_color()
            },
            "weather": {
                "value": weather,
                "color": get_color()
            },
            "min_temperature": {
                "value": min_temperature,
                "color": get_color()
            },
            "max_temperature": {
                "value": max_temperature,
                "color": get_color()
            },
            "love_day": {
                "value": love_days,
                "color": get_color()
            },


            "note_en": {
                "value": note_en,
                "color": get_color()
            },
            "note_ch1": {
                "value": note_ch1,
                "color": get_color()
            },
             "note_ch2": {
                "value": note_ch2,
                "color": get_color()
            },
            "note_ch3": {
                "value": note_ch3,
                "color": get_color()
            },
             "note_ch4": {
                "value": note_ch4,
                "color": get_color()
            },
            "note_ch5": {
                "value": note_ch5,
                "color": get_color()
            },
            
            
            "pipi1": {
                "value": pipi1,
                "color": get_color()
            },
            "pipi2": {
                "value": pipi2,
                "color": get_color()
            },
            "pipi3": {
                "value": pipi3,
                "color": get_color()
            },
            "pipi4": {
                "value": pipi4,
                "color": get_color()
            },
            "pipi5": {
                "value": pipi5,
                "color": get_color()

            },
                        
            "pyq1": {
                "value": pyq1,
                "color": get_color()
            },
            "pyq2": {
                "value": pyq2,
                "color": get_color()
            },
            "pyq3": {
                "value": pyq3,
                "color": get_color()
            },
            "pyq4": {
                "value": pyq4,
                "color": get_color()
            },
            "pyq5": {
                "value": pyq5,
                "color": get_color()

            },
            

            "lucky1": {
                "value": lucky_1,
                "color": get_color()
            },
            "lucky2": {
                "value": lucky_2,
                "color": get_color()
            },
            "lucky3": {
                "value": lucky_3,
                "color": get_color()
            },
            "lucky4": {
                "value": lucky_4,
                "color": get_color()
            },
            "lucky5": {
                "value": lucky_5,
                "color": get_color()
            },
            "lucky6": {
                "value": lucky_6,
                "color": get_color()
            },
            "lucky7": {
                "value": lucky_7,
                "color": get_color()
            },
            "lizhi1": {
                "value": lizhi1,
                "color": get_color()
            },
            "lizhi2": {
                "value": lizhi2,
                "color": get_color()
            },
            "lizhi3": {
                "value": lizhi3,
                "color": get_color()
            },
            "lizhi4": {
                "value": lizhi4,
                "color": get_color()
            },
            "lizhi5": {
                "value": lizhi5,
                "color": get_color()
            },


            "health1": {
                "value": health_tip1,
                "color": get_color()
            },
            "health2": {
                "value": health_tip2,
                "color": get_color()
            },
            "health3": {
                "value": health_tip3,
                "color": get_color()
            },
            "health4": {
                "value": health_tip4,
                "color": get_color()
            },
            "health5": {
                "value": health_tip5,
                "color": get_color()
            },

            "tips1": {
                "value": tips1,
                "color": get_color()
            },
            "tips2": {
                "value": tips2,
                "color": get_color()
            },
            "tips3": {
                "value": tips3,
                "color": get_color()
            },
            "tips4": {
                "value": tips4,
                "color": get_color()
            },
            "tips5": {
                "value": tips5,
                "color": get_color()
            }
        }
    }
    for key, value in birthdays.items():
        # 获取距离下次生日的时间
        birth_day = get_birthday(value, year, today)
        # 将生日数据插入data
        data["data"][key] = {"value": birth_day, "color": get_color()}
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)


if __name__ == "__main__":
    try:
        with open("config.txt", encoding="utf-8") as f:
            config = eval(f.read())
    except FileNotFoundError:
        print("推送消息失败，请检查config.txt文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("推送消息失败，请检查配置文件格式是否正确")
        os.system("pause")
        sys.exit(1)

    # 获取accessToken
    accessToken = get_access_token()
    # 接收的用户
    users = config["user"]
    # 传入省份和市获取天气信息
    province, city = config["province"], config["city"]
    weather, max_temperature, min_temperature = get_weather(province, city)
    #获取彩虹屁API
    caihongpi_API=config["caihongpi_API"]
    #获取朋友圈API
    pyq_api=config["pyq_api"]
    #获取励志古言API
    lizhi_API=config["lizhi_API"]
    #获取天气预报API
    tianqi_API=config["tianqi_API"]
    #是否启用词霸每日金句
    Whether_Eng=config["Whether_Eng"]
    #获取健康小提示API
    health_API=config["health_API"]
    #获取星座运势API
    lucky_API=config["lucky_API"]
    #获取星座
    astro = config["astro"]
    # 获取词霸每日金句
    note_ch1,note_ch2,note_ch3,note_ch4,note_ch5, note_en= get_ciba()
    #彩虹屁
    pipi1,pipi2,pipi3,pipi4,pipi5 = caihongpi()
    #彩虹屁
    pyq1,pyq2,pyq3,pyq4,pyq5 = pyq()
    #健康小提示
    health_tip1,health_tip2,health_tip3,health_tip4,health_tip5 = health()
    #下雨建议
    tips1,tips2,tips3,tips4,tips5 = tip()
    #励志名言
    lizhi1,lizhi2,lizhi3,lizhi4,lizhi5 = lizhi()
    #星座运势
    lucky_1,lucky_2,lucky_3,lucky_4,lucky_5,lucky_6,lucky_7 = lucky()
    # 公众号推送消息
    for user in users:
        send_message(user, accessToken, city, weather, max_temperature, min_temperature, pipi1,pipi2,pipi3,pipi4,pipi5, pyq1,pyq2,pyq3,pyq4,pyq5, lizhi1,lizhi2,lizhi3,lizhi4,lizhi5,tips1,tips2,tips3,tips4,tips5, note_ch1,note_ch2,note_ch3,note_ch4,note_ch5, note_en, health_tip1,health_tip2,health_tip3,health_tip4,health_tip5, lucky_1,lucky_2,lucky_3,lucky_4,lucky_5,lucky_6,lucky_7)
    import time
    time_duration = 3.5
    time.sleep(time_duration)
