from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time as t

name = '하승준'            #이름
PW = '0302'                #비번
YYMMDD = '041215'          #생년월일
location = "인천광역시"    #지역
s_type = "고등학교"        #학교종류
s_name = "가림고등학교"    #학교 이름

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome('C:/python/another/chromedriver')

driver.get('https://hcs.eduro.go.kr/#/relogin')

driver.find_element_by_id("btnConfirm2").click()
driver.find_element_by_id("schul_name_input").click()
loc = driver.find_element_by_xpath('//*[@id="sidolabel"]')
loc.send_keys(location)
bb = driver.find_element_by_xpath('//*[@id="crseScCode"]')
bb.send_keys(s_type)

driver.find_element_by_id("orgname").send_keys(s_name)
driver.find_element_by_class_name("searchBtn").click()

radio=WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="softBoardListLayer"]/div[2]/div[1]/ul/li/a')))
driver.execute_script("arguments[0].click();", radio)
driver.find_element_by_class_name("layerFullBtn").click()

driver.find_element_by_id("user_name_input").send_keys(name)
driver.find_element_by_id("birthday_input").send_keys(YYMMDD)
driver.find_element_by_id("btnConfirm").click()

t.sleep(2)
driver.find_element_by_class_name("input_text_common").click()

t.sleep(2)
for i in PW:
    aa = driver.find_element_by_xpath('//*[@id="password_mainDiv"]')
    a = aa.find_elements_by_tag_name('a')
    for j in a:
        if i in j.get_attribute('aria-label'):
            j.click()
            break

driver.find_element_by_xpath('//*[@id="btnConfirm"]').click()
t.sleep(1)
driver.find_element_by_xpath('//*[@id="container"]/div/section[2]/div[2]/ul/li/a/em').click()
t.sleep(1)
radio=WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="survey_q1a1"]')))
driver.execute_script("arguments[0].click();", radio)
radio=WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="survey_q2a1"]')))
driver.execute_script("arguments[0].click();", radio)
radio=WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="survey_q3a1"]')))
driver.execute_script("arguments[0].click();", radio)
driver.find_element_by_xpath('//*[@id="btnConfirm"]').click()

t.sleep(3)

driver.quit()
tm = t.localtime(t.time())
n_time = t.strftime('%Y-%m-%d %I:%M:%S %p', tm)
print("==========================================================\n")
print(f"{n_time}    {name}님의 자가진단이 완료되었습니다.")
print("==========================================================\n")
