# -*- coding:utf-8 -*-

import os
import time
import datetime
import codecs
from lxml import etree
import multiprocessing as mp
from os import makedirs
from os.path import exists
from selenium import webdriver
from selenium.webdriver.common.proxy import *
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# # date格式转为string格式
today = datetime.date.today()
today_string = today.strftime('%Y-%m-%d')


def html_getter(site,file_name):
    driver = webdriver.Firefox()
    # chromedriver = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
    # os.environ['webdriver.chrome.driver'] = chromedriver
    # driver = webdriver.Chrome(chromedriver)
    driver.get(site)
    driver.maximize_window() # 将浏览器最大化显示
    time.sleep(5) # 控制间隔时间，等待浏览器反映
    # 保存页面
    source_code = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
    f = codecs.open(file_name, 'w+', 'utf8')
    f.write(source_code)
    f.close()

#open page
def file_html(file_name):
    f = open(file_name,'r')
    html = f.read()
    f.close()
    return html

def data_get(html):
    selector = etree.HTML(html)
    tbody=selector.xpath('/html/body/main/table/tbody/tr')
    for each in tbody:
        # #1.'drug'
        drug_name=each.xpath('td[1]/strong/text()')[0]
        drug_sn=each.xpath('td[1]/a/text()')[0]
        drug=drug_name+'   '+drug_sn
        # #print(drug)
        # #2.'Interacting Gene/Enzyme'
        int=each.xpath('td[2]')[0]
        inter=int.xpath('string(.)')
        # print(inter)
        # #3.'SNP RS ID'
        snp=each.xpath('td[3]/a/text()')
        if snp:
            snp_rs_id=snp[0]
        else:
            snp_rs_id='Not Available	'
        #print snp_rs_id
        #4.Allele name
        Allele=each.xpath('td[4]/text()')
        if Allele:
            Allele_name=Allele[0]
        else:
            Allele_name='Not Available	'
        # #print Allele_name
        # #5.'Defining change'
        Defining=each.xpath('td[5]/text()')
        if Defining:
            Defining_change=Defining[0]
        else:
            Defining_change='Not Available	'
        # print Defining_change
        # 6.'Adverse Reaction'
        Adverse=each.xpath('td[6]/text()')
        if Adverse:
            Adverse_Reaction=Adverse[0]
        else:
            Adverse_Reaction='Not Available	'
        # print Adverse_Reaction
        #7.'Reference(s)'
        ref=each.xpath('td[7]/span/a/text()')[0]
        href=each.xpath('td[7]/span/a/@href')[0]
        original_title=each.xpath('td[7]/span/a/@data-original-title')[0]
        # print ref
        # print(href)
        # print(original_title)

        tt=(drug,inter,snp_rs_id,Allele_name,Defining_change,Adverse_Reaction,ref,href,original_title)
        ll.append(tt)
        return ll
#print ll

def csv_writer(ll):
    headers = ['drug','inter','snp_rs_id','Allele_name','Defining_change','Adverse_Reaction','ref','href','original_title']
    with open('drugbank.csv','a') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(ll)

if __name__ == '__main__':
    ll=[]
    for i in range(1,5):
        page_num=i
        site='http://www.drugbank.ca/genobrowse/snp-adr?page='+str(page_num)
        #get the html through webdriver
        file_name=unicode(today_string)+u'drugbank_'+unicode(str(page_num))+u'.html'

        html_getter(site,file_name)
        html=file_html(file_name)
        data_get(html)
        csv_writer(ll)




















