# encoding=utf8
import io
import re
import sys
import time
import subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def get_driver_version():
   cmd = r'''powershell -command "&{(Get-Item 'C:\Program Files\Google\Chrome\Application\chrome.exe').VersionInfo.ProductVersion}"'''
   try:
       out, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
       out = out.decode('utf-8').split(".")[0]
       return out
   except IndexError as e:
       print('Check chrome version failed:{}'.format(e))
       return 0

def get_ptid(driver):
    url = '''https://zodgame.xyz/home.php?mod=space&uid=646395&do=thread&view=me&type=reply&order=dateline&from=space&page='''
    ptid_list = []
    for i in range(1, 10):
        driver.get(url + str(i))
        for element in driver.find_elements(By.XPATH, '//table/tbody/tr/th/a'):
            href = element.get_attribute('href')
            # print(href)
            ptid = re.search('[0-9]{6}', href).group()
            ptid_list.append(ptid)
            # print(ptid)
    with open('./zodgame/tid.txt', 'a', encoding='ASCII') as f:
        for ptid in ptid_list:
            f.write(ptid+'\n')


def zodgame(cookie_string):
    options = uc.ChromeOptions()
    options.add_argument("--disable-popup-blocking")
      
    version = get_driver_version()
    driver = uc.Chrome(version_main=version, options = options)

    # Load cookie
    driver.get("https://zodgame.xyz/")

    if cookie_string.startswith("cookie:"):
        cookie_string = cookie_string[len("cookie:"):]
    cookie_string = cookie_string.replace("/","%2")
    cookie_dict = [ 
        {"name" : x.split('=')[0].strip(), "value": x.split('=')[1].strip()} 
        for x in cookie_string.split(';')
    ]

    driver.delete_all_cookies()
    for cookie in cookie_dict:
        if cookie["name"] in ["qhMq_2132_saltkey", "qhMq_2132_auth"]:
            driver.add_cookie({
                "domain": "zodgame.xyz",
                "name": cookie["name"],
                "value": cookie["value"],
                "path": "/",
            })
    
    driver.get("https://zodgame.xyz/")
    
    WebDriverWait(driver, 240).until(
        lambda x: x.title != "Just a moment..."
    )
    assert len(driver.find_elements(By.XPATH, '//a[text()="用户名"]')) == 0, "Login fails. Please check your cookie."
        
    # formhash = driver.find_element(By.XPATH, '//input[@name="formhash"]').get_attribute('value')
    # assert zodgame_checkin(driver, formhash) and zodgame_task(driver, formhash), "Checkin failed or task failed."

    #获取已经回复过帖子的tid
    get_ptid(driver)

    driver.close()
    driver.quit()




if __name__ == "__main__":
    cookie_string = sys.argv[1]
    assert cookie_string
    
    zodgame(cookie_string)