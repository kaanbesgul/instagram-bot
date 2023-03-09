from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pytesseract
from PIL import Image
import requests
from math import *

# Sayfadaki öğelerin seçici stratejileri

ilanlar={
    'tevkil1':{
        'https://www.instagram.com/tevkil/':4
    },
    'tevkil2':{
        'https://www.instagram.com/tevkil_/':2
    },
    'tevkil3':{
        'https://www.instagram.com/tevkiliniz/':3
    },
    'tevkil4':{
        'https://www.instagram.com/tevkilbirligi/':1
    }
}


username_input_selector = (By.NAME, 'username')
password_input_selector = (By.NAME, 'password')
login_button_selector = (By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')
not_now=(By.XPATH, "//button[contains(text(),'Şimdi Değil')]")
comment_input_selector = (By.CSS_SELECTOR, 'textarea[aria-label="Yorum ekle..."]')
post_comment_button_selector = (By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[3]/div/form/div/div[2]')

# Ana işlev
def instagram_comment_on_last_post(username, password,keyword):
    driver = webdriver.Chrome(executable_path="C:\\Users\\kaanb\\OneDrive\\Masaüstü\\Veyso\\chromedriver.exe")  
    wait = WebDriverWait(driver, 10)

    def login():

        # Instagram sayfasını aç
        driver.get("https://www.instagram.com")

        # Kullanıcı adı ve parola alanlarını doldur
        wait.until(EC.presence_of_element_located(username_input_selector)).send_keys(username)
        wait.until(EC.presence_of_element_located(password_input_selector)).send_keys(password)
        wait.until(EC.element_to_be_clickable(login_button_selector)).click()
        wait.until(EC.element_to_be_clickable(not_now)).click()
        wait.until(EC.element_to_be_clickable(not_now)).click()

        global linkler

        linkler=[]

    def gezin(keyvalue):

        
    
        for i in ilanlar:
            for y in ilanlar[i]:
                url=y
                ceil_1=ceil((ilanlar[i][y]/3))
                kalan2=ilanlar[i][y]%3

                if kalan2 == 0:
                    kalan2=3

                last_post_selector = (By.XPATH, '/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[3]/article/div[1]/div/div['+str(ceil_1)+']/div['+str(kalan2)+']/a/div[1]/div[1]/img')
                click_last_post=(By.XPATH,'/html/body/div[2]/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[3]/article/div[1]/div/div['+str(ceil_1)+']/div['+str(kalan2)+']/a')


            driver.get(y)
            

            last_post = wait.until(EC.presence_of_element_located(last_post_selector))
            click_last_post_2=wait.until(EC.presence_of_element_located(click_last_post))
            image = Image.open(requests.get(last_post.get_attribute("src"), stream=True).raw)
            text = pytesseract.image_to_string(image)
            

            if (keyvalue in text.lower() and click_last_post.get_attribute("href") not in linkler):
                wait.until(EC.presence_of_element_located(click_last_post)).click()
                wait.until(EC.presence_of_element_located(comment_input_selector)).click()
                wait.until(EC.presence_of_element_located(comment_input_selector)).send_keys('hi')
                wait.until(EC.presence_of_element_located(post_comment_button_selector)).click()
                linkler.append(click_last_post_2.get_attribute("href"))
                print(click_last_post_2.get_attribute("href"))
                print(text.lower())
            else:
                print('hi')
    login()

    while True:
        gezin(keyword)
            

instagram_comment_on_last_post("uslandeli8","3*hdpj9Gh`#_Hx?","yalova")
