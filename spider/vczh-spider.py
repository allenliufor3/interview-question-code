# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import http.cookiejar
import json
import time
import pymysql
import matplotlib.pyplot as plt
# 创建连接
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='spider', use_unicode=True, charset="utf8")
cursor = conn.cursor()
cjar = http.cookiejar.CookieJar()
headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        # 注意浏览器里的encoding 可能是gzip,deflate 而这里需要utf-8 避免不能解码
        'accept-encoding': 'utf-8',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://www.zhihu.com/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
        'Cookie': '这里填写你自己的登录知乎的cookie'
    }
headers_all = []
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
for k, v in headers.items():
    item = (k, v)
    headers_all.append(item)
opener.addheaders = headers_all
urllib.request.install_opener(opener)

def followers(url):
    content = urllib.request.urlopen(url).read().decode('utf-8')
    print(content)
    j = json.loads(content)
    # 如果data数据为空说明已爬取最后一页，结束爬虫
    # 虽然响应数据中有is_end 判断，但是在倒数第二页有is_end为true,所以不好直接用is_end字段判断是否爬取完成，否则会造成最后一页爬取不到
    data = j['data']
    if not data:
        return
    images = {}
    for d in data:
        token = d['url_token']
        name = d['name']
        if d['gender'] == 1:
            gender = '男'
        elif d['gender'] == -1:
            gender = '性别未知'
        else:
            gender = '女'
        follower_count = d['follower_count']
        avatar_url = d['avatar_url_template']
        answer_count = d['answer_count']
        articles_count = d['articles_count']
        headline = d['headline']
        # 将头像url模板中的{size}设置成xll
        avatar_url = avatar_url.replace('{size}', 'xll')
        # 数据存储
        images[name] = avatar_url
        image_name = '/Users/rundouble/Desktop/excited-vczh_followers/' + name + '.jpg'
        urllib.request.urlretrieve(avatar_url, image_name)
        print(name+'\t'+gender+'\t'+str(follower_count))
        kv = [follower_count, name]
        info.append(kv)
        cursor.execute("insert into zhihu_info(token, name, gender, follower_count, answer_count, articles_count, headline, avatar_url) values(%s, %s, %s ,%s, %s ,%s, %s, %s)", (token, name, gender, follower_count, answer_count, articles_count, headline, avatar_url))
        conn.commit()
    url = j['paging']['next']
    if url:
        time.sleep(2)
        followers(url)

def visualize():
    # 性别饼状图
    sizes = []
    cursor.execute('select count(*) from zhihu_info where gender="男";')
    sizes.append(cursor.fetchone()[0])
    cursor.execute('select count(*) from zhihu_info where gender="女";')
    sizes.append(cursor.fetchone()[0])
    cursor.execute('select count(*) from zhihu_info where gender="性别未知";')
    sizes.append(cursor.fetchone()[0])
    labels = 'Male:'+str(sizes[0]), 'Female:'+str(sizes[1]), 'Unknown:'+str(sizes[2])
    explode = [0, 0.1, 0]
    plt.title('Sex Distribution of Followers')
    plt.pie(sizes, explode=explode, labels=labels, autopct='%1.2f%%', startangle=90)
    plt.show()
    # 是否含有简介的饼状图
    sizes = []
    cursor.execute('select count(*) from zhihu_info where headline!=""')
    sizes.append(cursor.fetchone()[0])
    cursor.execute('select count(*) from zhihu_info where headline=""')
    sizes.append(cursor.fetchone()[0])
    labels = 'Contains introduction:'+str(sizes[0]), 'Does not include introduction:'+str(sizes[1])
    explode = [0.1, 0]
    plt.title('Introduction Distribution of Followers')
    plt.pie(sizes, labels=labels, explode=explode, autopct='%1.2f%%', startangle=90)
    plt.show()
    # 关注用户的粉丝数量分布计算
    data = []
    cursor.execute('select COUNT(*) from zhihu_info where follower_count <=100')
    data.append(cursor.fetchone()[0])
    cursor.execute('select COUNT(*) from zhihu_info where follower_count>100 and follower_count <=500')
    data.append(cursor.fetchone()[0])
    cursor.execute('select COUNT(*) from zhihu_info where follower_count>500 and follower_count <=1000')
    data.append(cursor.fetchone()[0])
    cursor.execute('select COUNT(*) from zhihu_info where follower_count>1000 and follower_count<=2000')
    data.append(cursor.fetchone()[0])
    cursor.execute('select COUNT(*) from zhihu_info where follower_count>2000 and follower_count<=5000')
    data.append(cursor.fetchone()[0])
    cursor.execute('select COUNT(*) from zhihu_info where follower_count>5000 and follower_count<=10000')
    data.append(cursor.fetchone()[0])
    cursor.execute('select COUNT(*) from zhihu_info where follower_count>10000 and follower_count<=100000')
    data.append(cursor.fetchone()[0])
    cursor.execute('select COUNT(*) from zhihu_info where follower_count >100000')
    data.append(cursor.fetchone()[0])
    print(data)
    labels = ['0-100', '10-500', '500-1k', '1k-2k', '2k-5k', '5k-1w', '1w-10w', '>10w']
    plt.bar(range(len(data)), data, tick_label=labels, color='rgb')
    plt.title('Follower\'s Fan Distribution')
    plt.show()
    # 关注用户的回答数分布图
    data = []
    cursor.execute('select count(*) from zhihu_info where answer_count=0')
    data.append(cursor.fetchone()[0])
    cursor.execute('select count(*) from zhihu_info where answer_count>0 and answer_count<=5')
    data.append(cursor.fetchone()[0])
    cursor.execute('select count(*) from zhihu_info where answer_count>5 and answer_count<=10')
    data.append(cursor.fetchone()[0])
    cursor.execute('select count(*) from zhihu_info where answer_count>10 and answer_count<=20')
    data.append(cursor.fetchone()[0])
    cursor.execute('select count(*) from zhihu_info where answer_count>20 and answer_count<=30')
    data.append(cursor.fetchone()[0])
    cursor.execute('select count(*) from zhihu_info where answer_count>30 and answer_count<=40')
    data.append(cursor.fetchone()[0])
    cursor.execute('select count(*) from zhihu_info where answer_count>40 and answer_count<=50')
    data.append(cursor.fetchone()[0])
    cursor.execute('select count(*) from zhihu_info where answer_count>50 and answer_count<=100')
    data.append(cursor.fetchone()[0])
    cursor.execute('select count(*) from zhihu_info where answer_count>100 and answer_count<=200')
    data.append(cursor.fetchone()[0])
    cursor.execute('select count(*) from zhihu_info where answer_count>200 and answer_count<=500')
    data.append(cursor.fetchone()[0])
    cursor.execute('select count(*) from zhihu_info where answer_count>500')
    data.append(cursor.fetchone()[0])
    print(data)
    labels = ['0', '1-5', '6-10', '11-20', '21-30', '31-40', '41-50', '51-100', '101-200', '201-500', '>500']
    plt.title('Number of Answers Distribution')
    plt.bar(range(len(data)), data, width=0.5, tick_label=labels, color='rgb')
    plt.show()
    # 用户是否写文章的饼状图
    sizes = []
    cursor.execute('select count(*) from zhihu_info where articles_count=0')
    sizes.append(cursor.fetchone()[0])
    cursor.execute('select count(*) from zhihu_info where articles_count!=0')
    sizes.append(cursor.fetchone()[0])
    labels = 'No Article user:' + str(sizes[0]), 'Article user:' + str(sizes[1])
    explode = [0, 0.1]
    plt.title('Articles Distribution of Followers')
    print(sizes)
    plt.pie(sizes, labels=labels, explode=explode, autopct='%1.2f%%', startangle=90)
    plt.show()
    
url = 'https://www.zhihu.com/api/v4/members/excited-vczh/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=20&limit=20'
followers(url)
visualize()