"""
Base_Url: https://passport.jd.com/uc/login
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
        self.pwd =pwd
        self.driver = webdriver.Chrome(executable_path=r"E:\webdriver_\chrome_85.0.4183.83\chromedriver.exe")  # 获取chrome浏览器的驱动，并启动Chrome浏览器

    def recognition(self):

        # 设置等待 使用WebDriverWait方法
        # div = WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located((By.XPATH, "//div[@class='JDJRV-bigimg']/img"))).get_attribute("src")
        # print(div)

        r1 = self.driver.find_element_by_xpath("//div[@class='JDJRV-bigimg']/img").get_attribute("src")
        r1de = base64.b64decode(re.findall(";base64,(.*)", r1)[0])
        r2 = self.driver.find_element_by_xpath("//div[@class='JDJRV-smallimg']/img").get_attribute("src")
        r2de = base64.b64decode(re.findall(";base64,(.*)", r2)[0])

        with open("./captcha1.png", "wb") as f:
            f.write(r1de)
        with open("./captcha2.png", "wb") as f:
            f.write(r2de)
        time.sleep(1)

        cv2.imwrite('r3.jpg', cv2.imread('captcha1.png', 0))
        cv2.imwrite('r4.jpg', cv2.imread('captcha2.png', 0))
        cv2.imwrite('r4.jpg', abs(255 - cv2.cvtColor(cv2.imread('r4.jpg'), cv2.COLOR_BGR2GRAY)))
        result = cv2.matchTemplate(cv2.imread('r4.jpg'), cv2.imread('r3.jpg'), cv2.TM_CCOEFF_NORMED)
        x, y = np.unravel_index(result.argmax(), result.shape)

        cv2.rectangle(cv2.imread('r3.jpg'), (y + 20, x + 20), (y + 136 - 25, x + 136 - 25), (7, 249, 151), 2)
        print('识别坐标为:', y)
        return y

    def get_random_float(self,min, max, digits=4):
        """
        :param min:
        :param max:
        :param digits:
        :return:
        """
        return round(random.uniform(min, max), digits)

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
        huakuai = self.driver.find_element_by_xpath("//div[@class='JDJRV-slide-inner JDJRV-slide-btn']")
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
        distance = int(xx / 1.285)

        # 轨迹
        tracks = self._get_tracks(distance)

        # 移动滑块
        self._slider_action(tracks)

        time.sleep(1)

        if self.driver.current_url == "https://passport.jd.com/uc/login":
            return False
        else:
            return True

    def login_(self):
        self.driver.get("https://passport.jd.com/uc/login")
        time.sleep(1)
        self.driver.find_element_by_xpath("//a[text()='账户登录']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//*[@id="loginname"]').send_keys(self.user)  # 账号

        self.driver.find_element_by_id("nloginpwd").send_keys(self.pwd)  # 密码
        time.sleep(1)
        self.driver.find_element_by_xpath("//div[@class='login-btn']/a[@class='btn-img btn-entry']").click()

        # 开始反复滑动直到成功验证
        huadong_num = 1
        while 1:
            time.sleep(1)
            if self.move():
                break

            huadong_num += 1

        print("登陆成功, 成功率为：", 1/huadong_num * 100, "%")

        self.driver.get("https://item.jd.com/100012043978.html")

        # 2020-12-09 09:59:59 == 1607479199 TODO: 设置定时任务

        click_qiang = self.driver.find_element_by_xpath("//a[@id='btn-reservation']")
        click_qiang.click()
        print("请求地址：", click_qiang.get_attribute("href"))
        time.sleep(0.6)
        self.driver.find_element_by_xpath("//button[@class='checkout-submit']").click()
        time.sleep(10)
        # self.driver.close()


if __name__ == '__main__':
    user = ""
    pwd = ""

    login = Login(user, pwd)  # 请输入账号密码
    login.login_()

