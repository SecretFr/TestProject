from selenium import webdriver
import time

browser = webdriver.Chrome("C:\\Users\\ajou\\Downloads\\chromedriver_win32\\chromedriver.exe")
browser.get("https://nid.naver.com/nidlogin.login")

id=browser.find_element_by_css_selector("#id").send_keys("naver_id")
pw=browser.find_element_by_css_selector("#pw").send_keys("naver_pw")

browser.find_element_by_css_selector("#frmNIDLogin > fieldset > input").click()

time.sleep(10)
browser.quit()
