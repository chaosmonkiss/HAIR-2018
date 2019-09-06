from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np
import csv
import pandas as pd


def login(driver,ID,PW):
    driver.get('https://sso2.ntis.go.kr/3rdParty/loginFormPageID.jsp')
    driver.find_element_by_name('userid').send_keys(ID)
    driver.find_element_by_name('password').send_keys(PW)
    driver.find_element_by_xpath('/html/body/div/form/input').click()
        
def format_string(string):
    string = string.replace('  ',' ')
    string = string.replace('\n',' ')
    string = string.replace('\t',' ')
    string = string.replace('\xa0',' ')
    return string 

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    if iteration == total: 
        print()
        
def get_content(driver,url,data,YEAR):
    
    if YEAR == '2013':
        page_index = np.flipud(np.arange(0,50110,10))
    elif YEAR == '2014':
        page_index = np.flipud(np.arange(0,52850,10))
    elif YEAR == '2015':
        page_index = np.flipud(np.arange(0,53390,10))
    else:
        page_index = np.flipud(np.arange(0,20,10)) #example
    
    j = 0
    for p in page_index: 

        page_url = url + '&pager.offset={}'.format(str(p))
        driver.get(page_url)
    
        try:
            for i in np.arange(1,11):
                
                data[j]={}
                
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                select = soup.select('body > div.LY-subWrapper > div.LY-pageBox > form > table > tbody > tr > td')
                data[j]['pubyear'] = select[8*(i-1)].text.strip() #연도 
                data[j]['author'] = select[-2+8*i].text.strip() #책임자명
                data[j]['budget'] = select[-1+8*i].text.strip() #정부연구비(백만)

                driver.find_element_by_xpath(
                    '/html/body/div[3]/div[2]/form/table/tbody/tr[{}]/td[6]/a'.format(str(i))
                ).click()
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                select = soup.select('div > table > tbody > tr > td')
                data[j]['identino'] = select[3].text.strip() #과제고유번호 
                data[j]['identicode'] = select[5].text.strip() #세부과제번호 
                data[j]['projname'] = select[6].text.strip() #내역사업명 
                data[j]['title'] = select[7].text.strip() #과제명 
                data[j]['affili'] = select[8].text.strip() #연구책임자소속기관 
                data[j]['puborg'] = select[9].text.strip() #과제수행기관
                data[j]['department'] = select[10].text.strip() #주관부처(연구관리전문기관)
                data[j]['progstate'] = select[12].text.strip()#과제진행상태
                data[j]['devstage'] = select[13].text.strip() #연구개발단계
                data[j]['projtype'] = select[14].text.strip() #세부과제성격 
                data[j]['unit'] = select[15].text.strip() #연구수행주체
                data[j]['lifecycle'] = select[16].text.strip() #기술수명주기
                data[j]['region'] = select[17].text.strip() #지역
                data[j]['techcateg'] = format_string(select[18].text.strip()) #과학기술표준분류
                data[j]['applic'] = format_string(select[19].text.strip()) #적용분야 
                data[j]['tech6T'] = select[20].text.strip() #6T관련기술 
                data[j]['techstrat'] = select[21].text.strip() #국가전략기술 

                select = soup.select('div > table')
                data[j]['abstract'] = select[6].text #요약서
                
                
                j += 1
                driver.back()
        except:
            print(data[-1])
            
        printProgressBar(j + 1, 20, prefix = 'Progress:', suffix = 'Complete', length = 100)

def main():
    # path to chromedriver 
    PATH_TO_CD = '/Users/bokyung/workspace/chromedriver'
    # id and password for NTIS  
    ID = ''
    PW = ''
    # year to crawl 
    YEAR = '2012'

    driver = webdriver.Chrome(PATH_TO_CD)
    driver.implicitly_wait(3)
    login(driver,ID,PW)
    url = 'http://rndgate.ntis.go.kr/switch.do?prefix=/ia/info&page=/ProjectGroup.do?method=iaProjectSubjectList&searchVO.yrFrom={}&searchVO.yrTo={}'.format(YEAR,YEAR)
    driver.get(url)
    printProgressBar(0, 20, prefix = 'Progress:', suffix = 'Complete', length = 50)
    data= {}
    get_content(driver,url,data,YEAR)

    print('crawling complete') #crawling to dic
    len(data)

    df = pd.DataFrame(data)
    df = df.transpose()
    df.to_csv("NTIS_{}".format(YEAR), sep="\t")
    print('tsv complete') #export to tsv
     
if __name__ == "__main__":
    main()

