"""
Base_Url:https://www.17173.com/
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
import requests


class Login(object):

    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd
        self.base_url = "https://www.17173.com/"
        # 获取chrome浏览器的驱动，并启动Chrome浏览器
        self.driver = webdriver.Chrome(executable_path=r"E:\webdriver_\chrome_85.0.4183.83\chromedriver.exe")

    def get_random_float(self, min, max, digits=4):

        return round(random.uniform(min, max), digits)

    # 保存滑动验证的图片
    def recognition(self):
        # 到 滑动验证的页面
        """
        1.网站上滑动验证的逻辑为 每个图滑动三次 自动换图  后期可以设置点击画图，因为同样的图此一次出错，后面也会出错
        2.目前没有添加换图， 并且后期的比例与初始位置需要根据实际情况设置，目前设置的值 偶尔可以成功 但几率不高
        3. 并且部分图滑动成功之后 出现智能检测  可以自己设计滑动轨迹 或者修改滑动轨迹，看能否绕过检测，本程序滑动时很大几率被检测到，滑动轨迹还需要设计
        :return:
        """

        img_src = self.driver.find_element_by_xpath("//div[@class='tc-bg']/img").get_attribute("src")
        img_src_res = requests.get(img_src)
        with open("captcha1.png", "wb") as f:
            f.write(img_src_res.content)
        tc_jpp = self.driver.find_element_by_xpath("//div[@class='tc-jpp']/img").get_attribute("src")
        tc_jpp_res = requests.get(tc_jpp)
        with open("captcha2.png", "wb") as f:
            f.write(tc_jpp_res.content)

        cv2.imwrite('r3.jpg', cv2.imread('captcha1.png', 0))
        cv2.imwrite('r4.jpg', cv2.imread('captcha2.png', 0))
        cv2.imwrite('r4.jpg', abs(255 - cv2.cvtColor(cv2.imread('r4.jpg'), cv2.COLOR_BGR2GRAY)))
        result = cv2.matchTemplate(cv2.imread('r4.jpg'), cv2.imread('r3.jpg'), cv2.TM_CCOEFF_NORMED)
        x, y = np.unravel_index(result.argmax(), result.shape)

        cv2.rectangle(cv2.imread('r3.jpg'), (y + 20, x + 20), (y + 136 - 25, x + 136 - 25), (7, 249, 151), 2)
        print('识别坐标为:', y)
        return y
        # 滑动轨迹

    def _get_tracks(self, distance):

        track = []
        mid1 = round(distance * random.uniform(0.1, 0.2))
        mid2 = round(distance * random.uniform(0.65, 0.76))
        mid3 = round(distance * random.uniform(0.84, 0.88))
        # 设置初始位置、初始速度、时间间隔
        current, v, t = 0, 0, 0.2
        distance = round(distance)

        while current < distance:
            # 四段加速度
            if current < mid1:
                a = random.randint(10, 15)
            elif current < mid2:
                a = random.randint(30, 40)
            elif current < mid3:
                a = -70
            else:
                a = random.randint(-25, -18)

            # 初速度 v0
            v0 = v
            # 当前速度 v = v0 + at
            v = v0 + a * t
            v = v if v >= 0 else 0
            move = v0 * t + 1 / 2 * a * (t ** 2)
            move = round(move if move >= 0 else 1)
            # 当前位移
            current += move
            # 加入轨迹
            track.append(move)

        print("current={}, distance={}".format(current, distance))

        # 超出范围
        back_tracks = []
        out_range = distance - current
        if out_range < -8:
            sub = int(out_range + 8)
            back_tracks = [-1, sub, -3, -1, -1, -1, -1]
        elif out_range < -2:
            sub = int(out_range + 3)
            back_tracks = [-1, -1, sub]

        print("forward_tracks={}, back_tracks={}".format(track, back_tracks))
        return {'forward_tracks': track, 'back_tracks': back_tracks}

        # 开始滑动

    def _slider_action(self, tracks):

        # 点击滑块
        huakuai = self.driver.find_element_by_xpath("//div[@class='tc-drag-thumb']")
        ActionChains(self.driver).click_and_hold(on_element=huakuai).perform()

        # 正向滑动
        for track in tracks['forward_tracks']:
            yoffset_random = random.uniform(-2, 4)
            ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=yoffset_random).perform()

        time.sleep(random.uniform(0.06, 0.5))

        # 反向滑动
        for back_tracks in tracks['back_tracks']:
            yoffset_random = random.uniform(-2, 2)
            ActionChains(self.driver).move_by_offset(xoffset=back_tracks, yoffset=yoffset_random).perform()

        # 抖动
        ActionChains(self.driver).move_by_offset(
            xoffset=self.get_random_float(0, -1.67),
            yoffset=self.get_random_float(-1, 1)
        ).perform()
        ActionChains(self.driver).move_by_offset(
            xoffset=self.get_random_float(0, 1.67),
            yoffset=self.get_random_float(-1, 1)
        ).perform()

        time.sleep(self.get_random_float(0.6, 1))

        ActionChains(self.driver).release().perform()
        time.sleep(0.5)

    def move(self):
        xx = self.recognition()
        distance = int(xx / 4.15) + 90  # 此处应该是计算真实的比例以及初始位置

        # 轨迹
        tracks = self._get_tracks(distance)

        # 移动滑块
        self._slider_action(tracks)
        time.sleep(1.2)

    def login_(self):
        self.driver.get(self.base_url)
        time.sleep(self.get_random_float(0.6, 1))

        self.driver.find_element_by_xpath("//a[@data-ui-mark='loginBtn']").click()
        time.sleep(self.get_random_float(0.6, 1))

        self.driver.switch_to.frame("nut")
        self.driver.find_element_by_xpath("//input[@name='email']").send_keys(self.user)
        time.sleep(self.get_random_float(0.6, 1))
        self.driver.find_element_by_xpath("//input[@name='password']").send_keys(self.pwd)

        self.driver.find_element_by_xpath("//div[@class='gpp-form-bt']/button[text()='登录']").click()
        time.sleep(self.get_random_float(2, 5))
        self.driver.switch_to.frame("tcaptcha_iframe")
        while 1:
            self.move()

        time.sleep(20)
        self.driver.close()


if __name__ == '__main__':
    user = ""
    pwd = "222222"

    login = Login(user, pwd)  # TODO: 输入账号&密码
    login.login_()


