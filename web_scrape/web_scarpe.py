from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

# 启动浏览器
driver = webdriver.Chrome()
url = "https://careers.adidas-group.com/jobs?brand=&team=&type=&keywords=&location=%5B%7B%22country%22%3A%22Germany%22%7D%5D&sort=&locale=de&offset=0"
driver.get(url)

# 创建一个空的 DataFrame 来存储抓取的数据
columns = ['Job Title', 'Job Description']
job_data = pd.DataFrame(columns=columns)

# 翻页并进入每个岗位的详细页面
while True:
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # 找到所有岗位链接并逐个点击进入详细页面
    job_links = soup.find_all('a', class_='job-list__inner')  # 提取包含岗位链接的 a 标签

    for link in job_links:
        job_url = link['href']  # 获取岗位链接
        driver.get(job_url)  # 进入二级页面
        
        # 抓取二级页面内容
        job_soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # 抓取岗位标题
        job_title = job_soup.find('h1').find('span', {'itemprop': 'title'}).text
        
        # 抓取岗位描述
        job_description = job_soup.find('span', {'class': 'jobdescription'}).text
        
        # 将数据存入 DataFrame
        job_data = job_data.append({
            'Job Title': job_title,
            'Job Description': job_description
        }, ignore_index=True)

        driver.back()  # 回到一级页面
    
    # 检查是否有“weiter laden”（加载更多）按钮，继续加载
    try:
        next_button = driver.find_element_by_id('search-result__load-more')  # 根据按钮的 ID 查找
        next_button.click()  # 点击“加载更多”按钮
        time.sleep(2)  # 等待页面加载
    except:
        break  # 没有下一页时结束循环

driver.quit()

# 将数据保存到 CSV 文件
job_data.to_csv('adidas_jobs.csv', index=False)
