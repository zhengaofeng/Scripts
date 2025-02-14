import re
import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime


db_config = {
    'host': '192.168.33.100',
    'user': 'root',
    'password': '1925@Zgf',
    'database': 'cmdb',
    'charset': 'utf8mb4'
}
# 创建 ChromeDriver 服务
service = Service(ChromeDriverManager().install())  # 自动下载并管理 ChromeDriver
# 使用 ChromeDriver 服务启动浏览器
driver = webdriver.Chrome(service=service)

def connect_to_database():
    try:
        conn = pymysql.connect(**db_config)
        return conn
    except pymysql.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

# 插入数据到 MySQL
def insert_data_to_db(data):
    try:
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            insert_query = """
                            INSERT INTO alert_record_test (alert_id, alert_content, alert_ip, alert_group, alert_level, 
                                                           alert_assign_state, alert_dispose_state, alert_count, alert_time, install_time)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
            cursor.executemany(insert_query, data)
            conn.commit()
            cursor.close()
            conn.close()
            print("Data inserted successfully.")

    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def getting_data():

    driver.get("http://******")	# 替换为实际的网址
    time.sleep(7)

    try:

        input_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@formcontrolname='username']"))
        )
        # 填写账号和密码
        username = ""  # 替换为实际的用户名
        password = ""  # 替换为实际的密码
        captcha_value = input("请输入验证码: ")  

        username_input = driver.find_element(By.XPATH, "//input[@formcontrolname='username']")
        username_input.send_keys(username)

        password_input = driver.find_element(By.XPATH, "//input[@formcontrolname='password']")
        password_input.send_keys(password)

        captcha_input = driver.find_element(By.XPATH, "//input[@formcontrolname='captcha_value']")
        captcha_input.send_keys(captcha_value)

        # 等待并点击登录按钮
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@nztype='primary']"))
        )
        login_button.click()

        # 等待登录过程完成，可以根据实际情况修改等待时间
        time.sleep(5)
        for i in range(1, 51):
            url = f"http://******__icontains=%E7%8A%B6%E6%80%81%E5%8F%98%E4%B8%BA&page={i}&page_size=10&__t=1739426069143"  # 替换为实际的网址
            driver.get(url)
            time.sleep(5)

            # 获取页面内容
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            tbody = soup.find('tbody', class_='ant-table-tbody')
            data = []
            if tbody:
                rows = tbody.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    alert_id = cols[0].text.strip()
                    alert_content = cols[1].text.strip()
                    alert_ip_after = cols[2].text.strip()
                    alert_ip_after = re.match(r"(\d+\.+\d+\.+\d+\.+\d)", alert_ip_after)
                    alert_ip = alert_ip_after.group(1) if alert_ip_after else ""
                    alert_group = cols[3].text.strip()
                    alert_level = cols[4].text.strip()
                    alert_assign_state = cols[5].text.strip()
                    alert_dispose_state = cols[6].text.strip()
                    alert_count = cols[7].text.strip()
                    alert_time = cols[8].text.strip()
                    install_time = datetime.now()
                    data.append((alert_id, alert_content, alert_ip, alert_group, alert_level, alert_assign_state,
                                 alert_dispose_state, alert_count, alert_time, install_time))
                insert_data_to_db(data)


            else:
                print("没有找到表格内容")

    except Exception as e:
        print(f"Error: {e}")

    driver.quit()





if __name__ == '__main__':
    getting_data()
