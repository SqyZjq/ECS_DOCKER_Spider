from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests

# 创建一个函数等待 Selenium Grid 服务变得可用
def wait_for_selenium_grid(url, timeout=0.5, max_retries=10):
    i = 0
    while True:
        try:
            resp = requests.get(url, timeout=timeout)
        except requests.exceptions.RequestException as e:
            i += 1
            print(f"Attempt {i}: Selenium Grid not ready, retrying...")
            if i > max_retries:
                print("Max retries exceeded. Unable to connect to Selenium Grid.")
                raise e
            time.sleep(1)  # 等待一秒钟再重试
        else:
            print("Selenium Grid is ready.")
            print(resp.content)
            break

# 指定ECS服务器地址
ecs_server_url = 'http://chrome:4444/wd/hub'

# 调用函数并传递 Selenium Grid 状态URL
wait_for_selenium_grid(ecs_server_url + "/status")

# 创建ChromeOptions对象
chrome_options = Options()
chrome_options.add_argument('--disable-dev-shm-usage')  # 避免共享内存出现问题
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
# ... 其他浏览器选项 ...

# 设置远程WebDriver
driver = webdriver.Remote(
    command_executor=ecs_server_url,
    options=chrome_options  # 使用options代替之前的desired_capabilities
)

# 下面是您的Selenium测试脚本
driver.get('http://www.baidu.com')
print(driver.title)
print(driver.current_url)
with open('/data/baidu.html', 'w', encoding='utf-8') as f:
    f.write(driver.page_source)
# print(driver.page_source)

# 完成测试后关闭浏览器
driver.quit()
