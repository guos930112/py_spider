# 用来分析的脚本
# 某个省份 哪个运营商 总的微博条数 关于网络的问题反馈 信息有多少

import os
import json

# 所有省份
sf_list = ["北京", "天津", "上海", "重庆", "内蒙古", "广西", "西藏", "宁夏", "新疆",
           "河北", "山西", "辽宁", "吉林", "黑龙江", "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南",
           "湖北", "湖南", "广东", "海南", "四川", "贵州", "云南", "陕西", "甘肃", "青海", "台湾", "香港", "澳门",
           ]
# 三大运营商
yys_list = ["移动", "联通", "电信"]


# 打开文件 分析
def net_word_analyse():
    for sf in sf_list:
        for yys in yys_list:
            path = './json/'
            file_name = path + sf + "_" + yys + ".json"
            if os.path.exists(file_name):
                with open(file_name, 'r', encoding='utf-8') as file:
                    json_data_list = json.load(file)
                    # print(json_data_list, type(json_data_list))
                    if len(json_data_list) > 0:
                        all_mount = len(json_data_list)
                        net_word_list = []
                        for item in json_data_list:
                            content = item['content']
                            if "网络" in content or "网络崩溃" in content or "网络瘫痪" in content:
                                net_word_list.append(item)
                        # 包含 网络
                        net_word_mount = len(net_word_list)
                        # 网络崩溃
                        # 网络瘫痪
                        # 网络有问题
                        account_rate = net_word_mount / all_mount
                        print("%s - %s 基数:%d 包含网络关键字的数量:%d 当前网络关键词占比:%.2f" % (
                        sf, yys, all_mount, net_word_mount, account_rate))
                    else:
                        print("%s - %s 数据有问题:" % (sf, yys))
                        continue


if __name__ == '__main__':
    net_word_analyse()
