import requests
from lxml import etree
import json
import os
import time

# 所有省份
sf_list = ["北京", "天津", "上海", "重庆", "内蒙古", "广西", "西藏", "宁夏", "新疆",
           "河北", "山西", "辽宁", "吉林", "黑龙江", "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南",
           "湖北", "湖南", "广东", "海南", "四川", "贵州", "云南", "陕西", "甘肃", "青海", "台湾", "香港", "澳门",
           ]
# 三大运营商
yys_list = ["移动", "联通", "电信"]

# 需要请求的url
ss_url = "https://s.weibo.com/weibo?q="
ym_url = "&wvr=6&b=1&display=0&retcode=6102&page="
# end_url = "&display=0&retcode=6102"
# "&wvr=6&b=1&display=0&retcode=6102&page=3"
# "&wvr=6&b=1&display=0&retcode=6102&page=1"

# 需要增加请求头 和 cookie 
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51"
cookie = "_s_tentry=-; Apache=6743092465208.416.1600232123735; SINAGLOBAL=6743092465208.416.1600232123735; ULV=1600232123821:1:1:1:6743092465208.416.1600232123735:; login_sid_t=15350aee6c8cb42f693728cbcf4980b4; cross_origin_proto=SSL; appkey=; WBStorage=70753a84f86f85ff|undefined; UOR=,,login.sina.com.cn; SCF=AoNBY6NYF_rOvA9HDQ3WjJBVC7E8CJZ1ZhEP62eTCpvarqsC714U9HIIfvGvLiV4QqjKHOti3VnXr-mnscPoFlo.; SUB=_2A25yYFlRDeRhGeBH7FAX8CfFzTiIHXVRFM2ZrDV8PUNbmtAKLXPjkW9NQaHJk4pwrmfXiS4Ehf65RptggBJGkjJ9; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5I2EaIIPBgKGEXPwPoxpVz5JpX5o275NHD95Qc1KMESo541KqXWs4Dqcjri--Xi-iFi-2fi--4i-24i-8hi--fiKnciKnfi--fiKnRi-24TgU0; SUHB=0xnCE-nz1vpWJQ; ALF=1601004417; SSOLoginState=1600399617; wvr=6; webim_unReadCount=%7B%22time%22%3A1600399622972%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A20%2C%22msgbox%22%3A0%7D"
headers = {"User-Agent": user_agent,
           "Cookie": cookie
           }

# 页面分析 xpath语法 公共部分
pub_div = '//div[@class="card-feed"]'
# 微博内容部分
content_div = '//div[@class="card-feed"]/div[2]/p[1]/text()'


def spider_instance(sf, yys):
    """
        具体处理爬取的逻辑
    :param sf: 省份
    :param yys: 运营商
    :return:
    """
    # 数据存储 列表
    data_list = []
    for i in range(10):  # 爬取的页数
        con_url = ss_url + sf + yys + ym_url + str(i + 1)
        print("请求的url=======", con_url)
        response = requests.get(url=con_url, headers=headers)
        con_text = response.content
        node_list = etree.HTML(con_text).xpath(pub_div)
        for node in node_list:
            # 只获取 微博内容
            content = node.xpath('.//div[2]/p[1]/text()')
            item = dict()
            if content:  # 防止有空值
                n_content = " ".join(content)  # 把列表里的元素 连接成一个字符串
                n_content.replace("\n", "").strip()
                item["content"] = n_content
                data_list.append(item)
            print(len(data_list))
        time.sleep(0.5)  # 延迟一些时间 防止反爬
    # 保存文本
    path = "./json/"
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = path + sf + "_" + yys + ".json"
    f = open(file_name, "w", encoding="utf-8")
    # ensure_ascii=True ascii 编码 为 False unicode编码 utf-8
    json.dump(data_list, f, ensure_ascii=False)


def net_spider():
    for sf in sf_list:  # 各个省份
        for yys in yys_list:  # 各个运营商
            path = './json/'
            file_name = path + sf + "_" + yys + ".json"
            if os.path.exists(file_name):
                with open(file_name, 'r', encoding='utf-8') as file:
                    json_data_list = json.load(file)
                if len(json_data_list) > 0 and len(json_data_list) > 30:
                    continue
                else:
                    spider_instance(sf, yys)
            else:
                spider_instance(sf, yys)


if __name__ == '__main__':
    net_spider()
