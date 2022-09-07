import time as t
from dataclasses import dataclass
from selenium import webdriver


driver_path = './chromedriver'
# 옵션 생성
options = webdriver.ChromeOptions()
# 창 숨기는 옵션 추가
options.add_argument("headless")

@dataclass
class return_lunch:
    menu: list
    error: str

def check_school(school_name,driver = None,quit = True):
    if driver == None:
         driver = webdriver.Chrome(driver_path,options = options)
         #driver = webdriver.Chrome(driver_path)
    driver.get(f'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query={school_name}')
    try:
        a = driver.find_element_by_xpath('//*[@id="main_pack"]/div[2]/div[1]/div[1]/h2/a/strong').text
        if quit == False:
            return a
        else:
            driver.quit()
            return a
    except:
        if quit == False:
            return False
        else:
            driver.quit()
            return False


class lunch():
    def __init__(self):
        self.driver = webdriver.Chrome(driver_path)
        #self.driver = webdriver.Chrome(driver_path)


    def get_lunch(self, school_name):
        l_list = []
        cs = check_school(school_name,self.driver,False)
        if cs != False:
            self.driver.get(f'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query={school_name}')
            #학교 검색 후 급식식단 선택
            t.sleep(1)

            if self.driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[2]/div[1]/div[3]/div/div/ul/li[3]/a').text != '급식식단':
                a = return_lunch(None,f'{school_name}의 급식 식단이 없습니다.')
                self.driver.quit()
                del l_list
                return a

            self.driver.find_element_by_xpath('//*[@id="main_pack"]/div[2]/div[1]/div[3]/div/div/ul/li[3]/a').click()


            for i in self.driver.find_elements_by_css_selector('#main_pack > div.sc_new.cs_common_module.case_normal.color_23._school.cs_kindergarten._edu_list > div.cm_content_wrap > div > div.timeline_list.open > ul > li'):
                l_list.append(i.find_element_by_class_name('cm_date').text)
                l_list.append(i.find_element_by_class_name('item_list').text)
            a = return_lunch(l_list,None)
            self.driver.quit()
            del l_list
            return a

        else:
            a = return_lunch(None,f'{school_name} 학교를 찾을 수 없습니다.')
            self.driver.quit()
            del l_list
            return a
