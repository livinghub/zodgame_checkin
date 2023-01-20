import re
import time
import io
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

def is_vaild_tid(tid):
    if tid in open('./zodgame/tid.txt', encoding='ASCII').read():
        return False
    else:
        return True

def go_reply(driver, tid):
    view_url = '''https://zodgame.xyz/forum.php?mod=viewthread&tid=''' + str(tid) + '''&extra=page%3D1'''
    
    driver.get(view_url)
    WebDriverWait(driver, 240).until(
        lambda x: x.title != "Just a moment..."
    )
    js = '''
    var comment=["好东西，谢谢大佬分享。", "嘿嘿，碉堡了！", "东西很不错(￣ˇ￣)，谢谢楼猪！","感谢大佬的分享！真不错","感谢大佬，碉堡了",
                "好东西呀，很有感觉。","真不错,谢谢了","太牛了，真不愧是大佬","无敌了，简直，谢谢分享","很棒，很戳我xp"];
    var comment2=["(￣ˇ￣)", "b（￣▽￣）d", "(=￣ω￣=)", "(^ ^)", "／▽▽＼", "!(￣ˇ￣)!", " 弟弟很喜欢", "。。。我好了", " 弟弟哭了", " www.www", "。。。我替弟弟谢谢你", "。。弟弟不行了"];
    var STARTNUMBER = -1;
    var ENDNUMBER = 10;
    var temp_count = Math.floor(Math.random() * comment.length);
    var temp_count2 = Math.floor(Math.random() * comment2.length);
    document.getElementById("fastpostmessage").value = comment[temp_count]+comment2[temp_count2];
    document.getElementById("fastpostsubmit").click();
    ''' # js语句
    driver.execute_script(js) # 执行js的方法
    time.sleep(16)

def get_vaild_tid(driver):
    fid_list = ['10', '100', '102', '75', '68', '132', '13', '12', '111']
    # fid_list = ['10']
    tid_list = []
    forum_url = '''https://zodgame.xyz/forum.php?mod=forumdisplay&fid='''
    for fid in fid_list:
        driver.get(forum_url + fid)
        for element in driver.find_elements(By.XPATH, '//span[contains(text(), "回帖奖励")]/../../..'):
            # print(element.get_attribute('id'))
            flag_tid = element.get_attribute('id').split('_')
            if(flag_tid[0] == 'normalthread'):
                if(is_vaild_tid(flag_tid[1])):
                    tid_list.append(flag_tid[1])
    
    with open('./zodgame/tid.txt', 'a', encoding='ASCII') as f:
        for tid in tid_list:
            f.write(tid+'\n')
    
    return tid_list
    
def zodgame_autoreply(driver):
    tid_list = get_vaild_tid(driver)
    for tid in tid_list:
        go_reply(driver, tid)
        # print(tid)

def get_ptid(driver):
    url = '''https://zodgame.xyz/home.php?mod=space&uid=646395&do=thread&view=me&type=reply&order=dateline&from=space&page='''
    ptid_list = []
    for i in range(1, 6):
        driver.get(url + str(i))
        for element in driver.find_elements(By.XPATH, '//table/tbody/tr/th/a'):
            href = element.get_attribute('href')
            # print(href)
            ptid = re.search('[0-9]{6}', href).group()
            ptid_list.append(ptid)
            print(ptid)
    with open('./zodgame/tid2.txt', 'a', encoding='ASCII') as f:
        for ptid in ptid_list:
            f.write(ptid+'\n')
