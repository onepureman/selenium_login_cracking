"""
Base_Url: https://www.tianyancha.com/vipintro/?jsid=SEM-SOUGOU-PP-VIS-212505
Author: jing
Modify: 2020/12/4
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
        self.base_url = "https://www.tianyancha.com/vipintro/?jsid=SEM-SOUGOU-PP-VIS-212505"

        self.driver = webdriver.Chrome(executable_path=r"E:\webdriver_\chrome_85.0.4183.83\chromedriver.exe")  # 获取chrome浏览器的驱动，并启动Chrome浏览器

    def get_random_float(self, min, max, digits=4):

        return round(random.uniform(min, max), digits)

    def login_(self):
        self.driver.get(self.base_url)
        time.sleep(self.get_random_float(0.6, 1))
        self.driver.find_element_by_xpath("//a[text()='登录/注册']").click()
        time.sleep(self.get_random_float(1, 2))

        self.driver.find_element_by_xpath("//div[@tyc-event-ch='LoginPage.PasswordLogin']").click()
        time.sleep(self.get_random_float(0.6, 1))

        self.driver.find_element_by_xpath("//*[@id='mobile']").send_keys("18513606785")
        time.sleep(self.get_random_float(0.06, 0.6))
        self.driver.find_element_by_xpath("//*[@id='password']").send_keys("12365478")
        time.sleep(self.get_random_float(0.06, 0.6))
        self.driver.find_element_by_xpath("//div[@class='modulein modulein1 mobile_box  f-base collapse in']/div[text()='登录']").click()
        time.sleep(self.get_random_float(1, 2))

        # TODO: 下面开始处理滑动验证码


        # time.sleep(20)

        # self.driver.close()


if __name__ == '__main__':
    user = ""
    pwd = "222222"

    login = Login(user, pwd)  # TODO: 输入账号&密码
    login.login_()