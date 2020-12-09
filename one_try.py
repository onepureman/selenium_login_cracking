from selenium import webdriver

driver = webdriver.Chrome(executable_path=r'E:\webdriver_\chrome_85.0.4183.83\chromedriver.exe')  #获取chrome浏览器的驱动，并启动Chrome浏览器
driver.get("https://www.17173.com/")

sub = driver.find_element_by_xpath("//div[@class='topbar-user-loginout']/a[text()='登录']")
# driver.implicitly_wait(10)
# driver.set_window_rect(100,200,32,50)    #设置窗口的大小和坐标

# print(driver.current_url)  # 获取本页面URL
# print(driver.get_window_size())  # 获取窗口的大小
# print(driver.get_window_position())  # 获取窗口的坐标
# print(driver.window_handles)         #返回当前会话中的所有窗口的句柄

# print(driver.page_source)

# driver.execute_script("alert('hello')")  # 执行JS代码
# print(driver.get_cookies())  # Cookies操作

print(driver.name)  # 获取当前浏览器名

# driver.quit()
