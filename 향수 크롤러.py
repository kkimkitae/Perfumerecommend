from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import time
import csv
import os
import urllib.request

subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')

option = Options()
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=option)

driver.get("https://www.fragrantica.com/country/France.html")
driver.implicitly_wait(10)
driver.maximize_window()

f = open(r"C:\Users\WIN10\MJU_Study\capstone\fra_data_1.csv", 'w', encoding='UTF-8', newline='')
csvWriter = csv.writer(f)
cnt = 3 #브랜드 당 향수 개수 count, 시작 idx는 항상 3
brand_num = 2 #프랑스 브랜드 한정 첫 시작 idx 2
while brand_num <= 872: #등록된 프랑스 향수 브랜드가 872개
    elem = driver.find_element_by_css_selector("#main-content > div.grid-x.grid-margin-x > div.small-12.medium-8.large-9.cell > div.grid-x.grid-margin-x.grid-margin-y > div:nth-child({}) > a".format(brand_num))
    driver.execute_script("arguments[0].click();", elem)
    time.sleep(10)
    while True:
        try:
            try:
                perfume_name = driver.find_element_by_css_selector("#brands > div:nth-child({}) > div:nth-child(1) > div.flex-child-auto > h3 > a".format(cnt)).text
                time.sleep(3)
            except:
                try:
                    cnt += 1
                    perfume_name = driver.find_element_by_css_selector("#brands > div:nth-child({}) > div:nth-child(1) > div.flex-child-auto > h3 > a".format(cnt)).text
                except:
                    driver.back()
                    time.sleep(10)
                    brand_num += 1
                    cnt = 3
                    break

            elem = driver.find_element_by_css_selector("#brands > div:nth-child({}) > div:nth-child(1) > div.flex-child-auto > h3 > a".format(cnt))
            driver.execute_script("arguments[0].click();", elem)
            time.sleep(3)
            
            rating = driver.find_element_by_css_selector("#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(4) > div.small-12.medium-6.text-center > div > p.info-note > span:nth-child(1)").text
            rating = float(rating)
            time.sleep(3)

            voters_num = driver.find_element_by_css_selector("#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(4) > div.small-12.medium-6.text-center > div > p.info-note > span:nth-child(3)").get_attribute("content")
            voters_num = int(voters_num)
            time.sleep(3)

            # if(rating < 3.5 or voters_num < 10): #평균 평점이 3.5 미만이거나 평가자 수가 10명 미만이라면 필요 없는 data로 간주하여 crawling하지 않음
            #     cnt += 1
            #     driver.back()
            #     time.sleep(10)
            #     continue
            # 일단 이 부분은 고려하지 않는 것으로 생각, 나중에라도 데이터 전처리 과정을 통해 날릴 수 있음
            
            gender = driver.find_element_by_css_selector("#toptop > h1 > small").text
            time.sleep(3)
            if(len(gender) == 9): #여성용
                gender = "여성용"
            elif(len(gender) == 17): #공용
                gender = "남녀공용"
            else: #남성용
                gender = "남성용"

            main_accord1 = driver.find_element_by_css_selector("#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(1)").text
            time.sleep(3)
            main_accord2 = driver.find_element_by_css_selector("#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(2)").text
            time.sleep(3)

            spring = driver.find_element_by_css_selector("#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div > div:nth-child(2) > div.voting-small-chart-size > div > div").get_attribute("style")
            time.sleep(3)
            start = spring.find("width") + 7
            end = spring.find("%")
            spring = [float(spring[start:end]), "spring"]

            summer = driver.find_element_by_css_selector("#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div > div:nth-child(3) > div.voting-small-chart-size > div > div").get_attribute("style")
            time.sleep(3)
            start = summer.find("width") + 7
            end = summer.find("%")
            summer = [float(summer[start:end]), "summer"]

            fall = driver.find_element_by_css_selector("#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div > div:nth-child(4) > div.voting-small-chart-size > div > div").get_attribute("style")
            time.sleep(3)
            start = fall.find("width") + 7
            end = fall.find("%")
            fall = [float(fall[start:end]), "fall"]

            winter = driver.find_element_by_css_selector("#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div > div:nth-child(1) > div.voting-small-chart-size > div > div").get_attribute("style")
            time.sleep(3)
            start = winter.find("width") + 7
            end = winter.find("%")
            winter = [float(winter[start:end]), "winter"]

            season = sorted([spring, summer, fall, winter])[3][1]

            day = driver.find_element_by_css_selector("#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div > div:nth-child(5) > div.voting-small-chart-size > div > div").get_attribute("style")
            time.sleep(3)
            start = day.find("width") + 7
            end = day.find("%")
            day = [float(day[start:end]), "day"]

            night = driver.find_element_by_css_selector("#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div > div:nth-child(6) > div.voting-small-chart-size > div > div").get_attribute("style")
            time.sleep(3)
            start = night.find("width") + 7
            end = night.find("%")
            night = [float(night[start:end]), "night"]

            day_or_night = sorted([day, night])[1][1]

            longevity = []
            sillage = []

            elem = driver.find_elements_by_class_name("vote-button-legend")
            for i in range(11, len(elem)):
                if(i >= 11 and i <= 15):
                    longevity.append(int(elem[i].text))
                elif(i >= 16 and i <= 19):
                    sillage.append(int(elem[i].text))

            very_weak = [longevity[0], "very_weak"]

            weak = [longevity[1], "weak"]

            moderate = [longevity[2], "moderate"]

            long_lasting = [longevity[3], "long_lasting"]

            eternal = [longevity[4], "eternal"]

            longevity = sorted([very_weak, weak, moderate, long_lasting, eternal])[4][1]

            intimate = [sillage[0], "intimate"]

            moderate = [sillage[1], "moderate"]

            strong = [sillage[2], "strong"]

            enormous = [sillage[3], "enormous"]

            sillage = sorted([intimate, moderate, strong, enormous])[3][1]
            
            print("=====", perfume_name, gender, main_accord1, main_accord2, season, day_or_night, longevity, sillage, rating, voters_num, "=====")
            csvWriter.writerow([perfume_name, gender, main_accord1, main_accord2, season, day_or_night, longevity, sillage, rating, voters_num])

            image = driver.find_element_by_css_selector("#main-content > div.grid-x.grid-margin-x > div.small-12.medium-12.large-9.cell > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div > div > img").get_attribute("src")
            img_folder = './france_perfume_img' #폴더 이름 국가에 맞게 바꿔주세요!! 이미지 폴더는 현재 비쥬얼 스튜디오 작업 공간 안에 생깁니다
 
            if not os.path.isdir(img_folder): #이미지 저장
                os.mkdir(img_folder)
            urllib.request.urlretrieve(image, "./france_perfume_img/{}.jpg".format(perfume_name))#여기 경로 명도 본인이 만든 폴더명으로 해주세요!!

            cnt += 1
            driver.back()
            time.sleep(10)
        except:
            try:
                driver.back()
                time.sleep(10)
                cnt += 1
                driver.find_element_by_css_selector("#brands > div:nth-child({}) > div:nth-child(1) > div.flex-child-auto > h3 > a".format(cnt)).text
                time.sleep(10)
            except:
                driver.back()
                time.sleep(10)
                brand_num += 1
                break
            continue

f.close()