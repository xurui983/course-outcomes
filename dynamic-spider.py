from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pymongo
from selenium.common.exceptions import NoSuchElementException

# # 创建chrome参数对象
# opt = webdriver.ChromeOptions()
# # 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
# opt.set_headless()
# # 创建chrome无界面对象
# browser = webdriver.Chrome(options=opt)
browser = webdriver.Chrome()
# 等待10s WebDriverWait默认每500毫秒调用一下
wait = WebDriverWait(browser,10)

# 记录总共爬取多少
k = 0
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# 创建数据库
mydb = myclient["dynamicdb"]

# 创建集合
myco = mydb["jd"]

def search():
    try:
        browser.get('https://www.jd.com')
        # 判断是否加载成功
        input = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="key"]')))
        submit = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="search"]/div[@class="search-m"]/div[@class="form"]/button')))
        input.send_keys('美食')
        submit.click()
        total = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="J_bottomPage"]/span[@class="p-skip"]/em/b'))).text
        return total
    except TimeoutException:
        return search()

def geturl(i):
    try:
        url = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="J_goodsList"]/ul/li[' + str(i + 1) + ']/div/div[@class="p-img"]/a')))
        return url
    except TimeoutException:
        geturl(i)

def getname(i):
    try:
        name = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="J_goodsList"]/ul/li[' + str(
            i + 1) + ']/div/div[@class="p-name p-name-type-2"]/a/em'))).text.replace('\r', '').replace('\n', '')
        if name == '':
            return '无'
        return name
    except TimeoutException:
        getname(i)

def getprice(i):
    try:
        price = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="J_goodsList"]/ul/li[' + str(i + 1) + ']/div/div[@class="p-price"]/strong/i')))
        if price == '':
            return '无'
        return price.text
    except TimeoutException:
        getprice(i)

def getshop(i):
    try:
        shop = browser.find_element_by_xpath(
            ('//*[@id="J_goodsList"]/ul/li[' + str(i + 1) + ']/div/div[@class="p-shop"]/span/a'))
        return shop.text
    except NoSuchElementException:
        return '无'

def getcomment(i):
    try:
        comment = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="J_goodsList"]/ul/li[' + str(i + 1) + ']/div/div[@class="p-commit"]/strong/a'))).text
        if comment == '':
            return '无'
        return comment
    except TimeoutException:
        getcomment(i)

# 翻页方法
def next_page(page_number):
    global k
    global myclient
    global mydb
    global mycol
    try:
        # 滑动到底部，加载出后三十个货物信息
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="J_bottomPage"]/span[2]/input')))
        # 等到确定按钮出现
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > a')))
        # input清空
        input.clear()
        input.send_keys(page_number)
        submit.click()
        # 判断翻页是否成功
        wait.until(EC.text_to_be_present_in_element(
            (By.XPATH, '//*[@id="J_bottomPage"]/span[@class="p-num"]/a[@class="curr"]'), str(page_number)))
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        for i in range(0, 60):
            k = k + 1
            url = geturl(i)
            name = getname(i)
            price = getprice(i)
            shop = getshop(i)
            comment = getcomment(i)
            print('第', page_number,'页','第', i+1,'个','总共', k,'个')
            print('url:', url.get_attribute('href'))
            print('名称：', name, '价格：', price,'店铺',shop,'评论数',comment)
            # 插入数据
            mydict = {"url":url.get_attribute('href'),"名称":name,"价格":price,"店铺":shop,"评论数":comment}
            myco.insert_one(mydict)
    except TimeoutException:
        next_page(page_number)

def main():
    total = search()
    print(total)
    for i in range(1,int(total)+1):
        next_page(i)

if __name__ == '__main__':
    main()
