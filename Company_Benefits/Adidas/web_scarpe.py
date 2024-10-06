from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# 启动浏览器
driver = webdriver.Chrome()
url = "https://careers.adidas-group.com/jobs?brand=&team=&type=&keywords=&location=%5B%7B%22country%22%3A%22Germany%22%7D%5D&sort=&locale=de&offset=0"
driver.get(url)

# 循环点击“加载更多”按钮，直到按钮不再出现
while True:
    try:
        # 使用显式等待，等待“加载更多”按钮可点击
        wait = WebDriverWait(driver, 10)
        load_more_button = wait.until(EC.element_to_be_clickable((By.ID, "search-result__load-more")))
        
        # 滚动到按钮位置
        driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)

        # 使用 JavaScript 点击按钮
        driver.execute_script("arguments[0].click();", load_more_button)

        print("one click")

        time.sleep(2)  # 等待岗位加载

    except:
        # 如果没有更多的“加载更多”按钮，退出循环
        print("No more jobs to load.")
        break

# 在所有岗位加载完毕后，使用 BeautifulSoup 解析页面中的岗位链接
soup = BeautifulSoup(driver.page_source, 'html.parser')

# 找到所有岗位链接
job_links = soup.find_all('a', class_='job-list__inner')

# 创建一个空的 DataFrame 来存储抓取的数据
job_data_full = pd.DataFrame(columns=['Job Title', 'Job Description'])
i=0
# 遍历所有岗位链接并抓取详细信息
for link in job_links:
    print(i)
    i += 1
    job_url = link['href']
    driver.get(job_url)  # 进入二级页面
    
    try:
        # 抓取二级页面内容
        job_soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 抓取岗位标题，处理可能出现的异常
        job_title = job_soup.find('h1').find('span', {'itemprop': 'title'}).text if job_soup.find('h1') else 'No Title'

        # 抓取岗位描述，处理可能出现的异常
        job_description = job_soup.find('span', {'class': 'jobdescription'}).text if job_soup.find('span', {'class': 'jobdescription'}) else 'No Description'

        # 将数据存入 DataFrame
        job_data_full = job_data_full.append({
            'Job Title': job_title,
            'Job Description': job_description
        }, ignore_index=True)
    
    except Exception as e:
        # 捕获任何错误并打印错误信息，继续下一个循环
        print(f"Error while processing job {job_url}: {e}")
        continue  # 继续下一个岗位
    
    driver.back()  # 回到所有岗位的页面

# 关闭浏览器
driver.quit()

# 保存所有抓取的数据到 CSV 文件
job_data_full.to_csv('adidas_jobs_complete.csv', index=False)
