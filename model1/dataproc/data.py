# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import os
import threading


def get_contents():
    url = 'http://fenix.univ.rzeszow.pl/~mkepski/ds/uf.html'
    return requests.get(url)


def parse_xml(contents, base_dir):
    soup = BeautifulSoup(contents.text, 'lxml')
    data = soup.find_all('tr')
    process_data(base_dir, data)


def download(file_path, fall_seq_cam0_d_name, fall_seq_cam0_d_href):
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    r = requests.get(fall_seq_cam0_d_href, stream=True)
    with open(file_path + '/' + fall_seq_cam0_d_name, "wb") as file:
        for chunk in r.iter_content(chunk_size=1024*1024):
            if chunk:
                file.write(chunk)
                print(fall_seq_cam0_d_href + "---》download end")


def process_data(base_dir, datas):
    nums =0 
    dir ='adl'
    for data in datas:
        nums +=1
        try:
            seq = data.contents[1].text
           

            if len(seq) == 2 :
                # print(seq)
                cam0_name = "cam0 "+str(nums) + '.mp4'
                cam0_href = "http://fenix.univ.rzeszow.pl/~mkepski/ds/data/adl-"+seq+"-cam0.mp4"
                cam1_name = "cam1 "+str(nums) + '.mp4'
                cam1_href = "http://fenix.univ.rzeszow.pl/~mkepski/ds/data/adl-"+seq+"-cam1.mp4"
                download(base_dir +dir, cam0_name, cam0_href)
                download(base_dir +dir, cam1_name, cam1_href)
            else: 
                dir +=seq

        except Exception as e:
            # print(e)
            pass


if __name__ == "__main__":
    base_dir = 'D:\\workspace\\openpose\\data\\'
    parse_xml(get_contents(), base_dir)