import scrapy
import requests
import re
import time
import pymongo

class PpblogSpider(scrapy.Spider):
    name = 'ppblog'
    # allowed_domains = ['www.people.com.cn']
    start_urls = ['http://blog.sina.com.cn/s/articlelist_1197161814_0_1.html']
    i = -1
    j = -1
    total = 0

    # myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    # # 创建数据库
    # mydb = myclient["spiderdb"]
    #
    # # 创建集合
    # mycol = mydb["likaifu"]


    def parse(self, response):
        self.i = -1
        self.j = self.j + 1
        # 获取每页的所有(50个)url
        global  url_list
        url_list = response.xpath(
            '//*[@id="module_928"]/div[@class="SG_connBody"]/div[@class="article_blk"]/div[@class="articleList"]/div[@class="articleCell SG_j_linedot1"]/p[1]/span[2]/a/@href').extract()

        for i in range(len(url_list)):
            yield scrapy.Request(url=url_list[i],callback=self.pp)
            time.sleep(1)
        # for url in url_list:
        #     print(url)
        #     yield scrapy.Request(url=url,callback=self.pp)
        #     time.sleep(1)

        # 获取下一页的url
        url_next = response.xpath(
            '//*[@id="module_928"]/div[@class="SG_connBody"]/div[@class="article_blk"]/div[@class="SG_page"]/ul[@class="SG_pages"]/li[@class="SG_pgnext"]/a/@href').extract()

        if url_next:
            start_urls = url_next[0]
            # yield scrapy.Request(url=start_urls, callback=self.parse)

        pass

    def pp(self,response):
        self.i = self.i + 1
        self.total = self.total+1
        # 获取每篇文章的标题
        title_0 = response.xpath('//*[@id="articlebody"]/div[@class="articalTitle"]/h2/text()').extract()
        if title_0:
            title = title_0[0]
        else:
            title = response.xpath('//*[@id="articlebody"]/div[@class="BNE_title"]/h1/text()').extract()[0]

        # 获取每篇文章的发表时间
        time_0 = response.xpath('//*[@id="articlebody"]/div[@class="articalTitle"]/span[@class="time SG_txtc"]/text()').extract()
        if time_0:
            time_1 = time_0[0]
            time_2 = time_1.replace('(', '')
            time = time_2.replace(')', '')
        else:
            time_1 = response.xpath('//*[@id="pub_time"]/text()').extract()[0]
            time_2 = time_1.replace('(','')
            time = time_2.replace(')','')

        # 获取每篇文章的标签
        label_0 = response.xpath('//*[@id="sina_keyword_ad_area"]/table/tr/td[@class="blog_tag"]/h3/text()').extract()
        if label_0:
            label = label_0[0]
        else:
            label = '无'
        # 获取每篇文章的正文内容
        article_0 = response.xpath('//*[@id="sina_keyword_ad_area2"][descendant-or-self::*]')
        article_1 = article_0.xpath('string(.)').extract()[0]
        article_2 = article_1.replace("\n",'')
        article_3 = article_2.replace(' ','')
        article = article_3.replace('\t', '')

        comments_url_1 = url_list[self.i]
        comments_url_3 = ''
        for i in range(0, 24):
            comments_url_3 += comments_url_1[i]
        comments_url_2 = list(comments_url_3)
        comments_url_2.insert(7, "comet.")
        if(self.j == 0):
            comments_url_2.insert(25, "&requestId=aritlces_number_5945&fetch=c,r,f,z")
        if(self.j == 1):
            comments_url_2.insert(25, "&requestId=aritlces_number_9895&fetch=c,r,f,z")
        if(self.j == 2):
            comments_url_2.insert(25, "&requestId=aritlces_number_3473&fetch=c,r,f,z")
        if(self.j == 3):
            comments_url_2.insert(25, "&requestId=aritlces_number_355&fetch=c,r,f,z")
        if(self.j == 4):
            comments_url_2.insert(25, "&requestId=aritlces_number_1136&fetch=c,r,f,z")
        if(self.j == 5):
            comments_url_2.insert(25, "&requestId=aritlces_number_865&fetch=c,r,f,z")
        comments_url_2.insert(25, comments_url_1[41]+comments_url_1[42]+comments_url_1[43] + comments_url_1[44] + comments_url_1[45] + comments_url_1[46])
        comments_url_2.insert(25, "api?maintype=num&uid=475b3d56&aids=")
        comments_url = ''
        for i in range(len(comments_url_2)):
            comments_url += comments_url_2[i]
        # try:
        cc = requests.post(url=comments_url,timeout =(7,7))
        str = re.findall(r':\d+', cc.text)
        # 获取每篇文章的阅读数
        read_count = str[0][1:]
        # 获取每篇文章的评论数
        comments = str[2][1:]
        # 获取每篇文章的收藏数
        collect_count = str[1][1:]
        # 获取每篇文章的转载数
        reproduce_count = str[3][1:]
        # print("正文：", article)
        print(url_list[self.i],self.i)
        print(comments_url)
        print("j=",self.j,"i=",self.i)
        print("总数：",self.total)
        # 插入数据
        # mydict = {"url":url_list[self.i],"title":title,"time":time,"标签":label,"正文":article,"阅读数": read_count,"评论数": comments,"收藏数": collect_count,"转载数": reproduce_count}
        # self.mycol.insert_one(mydict)
        print("标题:", title,"阅读数:", read_count,"评论数:", comments,"收藏数:", collect_count,"转载数:", reproduce_count,"发表时间：",time,"标签:",label,"正文:",article)

        pass
