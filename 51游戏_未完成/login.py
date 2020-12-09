"""
Base_Url:http://www.51.com/
Author: jing
Modify:
"""


from selenium import webdriver
import time
from PIL import Image as Im
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import re
import base64
import cv2
import numpy as np
import random


class Login(object):

    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd
        self.base_url = "http://www.51.com/"
        # 获取chrome浏览器的驱动，并启动Chrome浏览器
        self.driver = webdriver.Chrome(executable_path=r"E:\webdriver_\chrome_85.0.4183.83\chromedriver.exe")

    def get_random_float(self, min, max, digits=4):
        return round(random.uniform(min, max), digits)

    def login_(self):
        self.driver.get(self.base_url)
        time.sleep(self.get_random_float(0.6, 1))

        # 输入账号
        self.driver.find_element_by_xpath('//*[@id="frame_login_user"]').send_keys("545454")
        time.sleep(self.get_random_float(0.6, 1))

        # 输入密码
        self.driver.find_element_by_xpath("//span[@class='t_c passw']/input[@id='frame_login_pass']").send_keys(
            "12365478")
        time.sleep(self.get_random_float(0.6, 1))

        self.driver.find_element_by_xpath('//*[@id="frame_login_button"]').click()

        time.sleep(10)
        self.driver.close()


if __name__ == '__main__':
    user = ""
    pwd = "222222"

    login = Login(user, pwd)  # TODO: 输入账号&密码
    login.login_()