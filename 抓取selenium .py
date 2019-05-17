from selenium import webdriver#等待页面加载某些元素
from selenium.webdriver.common.by import By #按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.support.ui import WebDriverWait#键盘按键操作
from selenium.webdriver.support import expected_conditions as EC
import time
from pyquery import PyQuery as pq
import pymongo
from Selenium爬取.mongo_config import *
client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]


'''
浏览器的初始化
'''
browser=webdriver.Firefox() #调用火狐浏览器
wait=WebDriverWait(browser, 10)

'''
目标页面
'''
def search():
    try:
        browser.get("https://www.jd.com/")
        input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#key'))) #等到id为key的元素加载完毕,最多等10秒
        submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.button')))
        input.send_keys('美食')
        submit.click()
        total=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.p-skip > em:nth-child(1) > b:nth-child(1)')))
        page_get()
        return total.text
    except TimeoutError:
        return search()
'''
翻页
'''
def page_next(pn):
    try:
        # input = browser.find_element_by_css_selector('input.input-txt:nth-child(2)')  # 找到搜索框的id为q
        input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'input.input-txt:nth-child(2)')))
        submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'a.btn:nth-child(4)')))
        input.clear()
        input.send_keys(pn)
        submit.click()
        page_get()
        print(pn)
    except TimeoutError:
        page_next(pn)

'''
商品信息抓取
'''
def page_get():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#J_goodsList .gl-warp .gl-item .gl-i-wrap')))  # 等待所有信息加载完毕
    html=browser.page_source
    doc=pq(html)
    items=doc('#J_goodsList .gl-warp .gl-item').items()  # 得到所有选择内容
    for item in items:
        product = {
            # 'x': item.find('.p-img img').attr('src'),
            # 'a': item.find('.p-name.p-name-type-2 a').attr('href'),
            'b': item.find('.p-name.p-name-type-2 a').text(),
        }
        print(product)
        # mongodb_save(product)
'''
数据的存储
'''
# def mongodb_save(result):
#     try:
#         if db[MONGO_TABLE].insert(result):
#             print("mongodb存储成功")
#     except:
#         print("something wrong")





def main():
    try:
        t = int(search())
        print(type(t))
        for i in range(2,4):
            page_next(i)
    except:
        print('chucuo')
    # finally:
        # browser.close()
main()