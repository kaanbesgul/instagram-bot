from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import InvalidSessionIdException
from selenium.common.exceptions import ElementNotInteractableException
import pytesseract
from PIL import Image
import requests
from math import *
import musteri
import time

# Sayfadaki öğelerin seçici stratejileri

global linkler

linkler=[]

ilanlar={
    'tevkil1':{
        'https://www.instagram.com/tevkil/':None
    },
    'tevkil2':{
        'https://www.instagram.com/tevkil_/':None
    },
    'tevkil3':{
        'https://www.instagram.com/tevkiliniz/':None
    },
    'tevkil4':{
        'https://www.instagram.com/tevkilbirligi/':None
    },
    'tevkil5':{
        'https://www.instagram.com/tevkilavukatt/':None
    },
    'tevkil6':{
        'https://www.instagram.com/tevkiltrr/':None
    },
    'tevkil7':{
        'https://www.instagram.com/tevkil.jet/':None
    },
    'tevkil8':{
        'https://www.instagram.com/tevkilavukat/':None
    },
    'tevkil9':{
        'https://www.instagram.com/tevkil.avukat.platformu/':None
    },
    'tevkil10':{
        'https://www.instagram.com/tevkilat/':None
    }
}


username_input_selector = (By.NAME, 'username')
password_input_selector = (By.NAME, 'password')
login_button_selector = (By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')
not_now=(By.XPATH, "//div[contains(text(),'Şimdi Değil')]")
not_now2=(By.XPATH, "//button[contains(text(),'Şimdi Değil')]")
comment_input_selector = (By.XPATH, '//textarea[@placeholder="Yorum ekle..."]')
post_comment_button_selector = (By.XPATH, '/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[3]/div/form/div/div[2]/div')



# Ana işlev
def instagram_comment_on_last_post(username, password,keyword):

    global driver

    driver = webdriver.Chrome(executable_path="C:\\Users\\kaanb\\OneDrive\\Masaüstü\\Veyso\\chromedriver.exe")  
    wait = WebDriverWait(driver, 10)
    driver.maximize_window()

    def login():

        # Instagram sayfasını aç
        driver.get("https://www.instagram.com")

        # Kullanıcı adı ve parola alanlarını doldur
        wait.until(EC.presence_of_element_located(username_input_selector)).send_keys(username)
        wait.until(EC.presence_of_element_located(password_input_selector)).send_keys(password)
        wait.until(EC.element_to_be_clickable(login_button_selector)).click()
        wait.until(EC.element_to_be_clickable(not_now)).click()
        wait.until(EC.element_to_be_clickable(not_now2)).click()



    def gezin(my_dict):

        for i in ilanlar:
            for y in ilanlar[i]:

                url=y
                driver.get(y)

                for z in range(1,10):

                    ceil_1=ceil((z/3))
                    kalan2=z%3

                    if kalan2 == 0:
                        kalan2=3

                    #Sabitlenmiş hikaye var mı kontrolü

                    try:
                        element1=wait.until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/div[2]")))
                        driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/div[3]")
                        mydiv=3
                    except NoSuchElementException:

                        mydiv=2

                    try:
                        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/div["+str(mydiv)+"]/article/div[1]/div/div[1]/div[1]/a/div[1]/div[1]")))
                        driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/div['+str(mydiv)+']/article/div[1]/div/div['+str(ceil_1)+']/div['+str(kalan2)+']/a/div[2]')
                    except NoSuchElementException:
                        ilanlar[i][y]=z
                        break

                last_post_selector = (By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/div['+str(mydiv)+']/article/div[1]/div/div['+str(ceil_1)+']/div['+str(kalan2)+']/a/div[1]/div[1]/img')
                click_last_post=(By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/div['+str(mydiv)+']/article/div[1]/div/div['+str(ceil_1)+']/div['+str(kalan2)+']/a')

            last_post = wait.until(EC.presence_of_element_located(last_post_selector))
            click_last_post_2=wait.until(EC.presence_of_element_located(click_last_post))
            image = Image.open(requests.get(last_post.get_attribute("src"), stream=True).raw)
            text = pytesseract.image_to_string(image)

            for musteri_aday in my_dict:

                if (musteri_aday in text.lower() and click_last_post_2.get_attribute("href") not in linkler):
                    wait.until(EC.presence_of_element_located(click_last_post)).click()
                    time.sleep(1)
                    wait.until(EC.presence_of_element_located(comment_input_selector)).click()
                    wait.until(EC.presence_of_element_located(comment_input_selector)).send_keys('Merhaba,meslektaşım {} size yardımcı olabilir.Telefon:{}'.format(musteri.musteriler[musteri_aday][0],musteri.musteriler[musteri_aday][1]))
                    time.sleep(1)
                    wait.until(EC.presence_of_element_located(post_comment_button_selector)).click()
                    time.sleep(1)
                    linkler.append(click_last_post_2.get_attribute("href"))
                    print(click_last_post_2.get_attribute("href"))
                    print(text.lower())
                else:
                    continue

    login()

    while True:
        gezin(keyword)

while True:

    try:

        instagram_comment_on_last_post("username","password",musteri.musteriler)

    except NoSuchElementException:

        print("Element bulunamadı hatası aldı.")
        driver.quit()

    except TimeoutException:

        print("Zaman hatası aldı.")
        driver.quit()

    except InvalidSessionIdException:

        print("Invalid Session hatası aldı.")
        driver.quit()

    except ElementNotInteractableException:

        print("Element not interactable hatasi aldi.")
        driver.quit()
