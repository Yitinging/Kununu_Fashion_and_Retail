import requests

# 目标网站的URL
url = "https://careers.adidas-group.com/jobs?brand=&team=&type=&keywords=&location=%5B%7B%22country%22%3A%22Germany%22%7D%5D&sort=&locale=de&offset=0"
url1 = "https://jobs.adidas-group.com/adidas/job/Herzogenaurach-INTERNSHIP-DATA-DOMAIN-PLATFORMS-&-GOVERNANCE-%28MFD%29/1125959101/?feedId=301201&utm_source=j2w"
# 添加User-Agent头信息，模拟浏览器请求
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# 发送HTTP GET请求
response = requests.get(url1, headers=headers)

# 检查请求是否成功
if response.status_code == 200:
    # 打印网站的HTML代码
    print(response.text)
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
