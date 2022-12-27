from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from tkinter import *
from functools import partial

import config


class Browser:
    def __init__(self):
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()))

    def __del__(self):
        self.driver.close()
        pass

    def launchBrowser(self, url):
        self.driver.get(url)
        return self.driver


def login(driver):
    username = config.LOGIN_USERNAME
    password = config.LOGIN_PASSWORD
    userBox = driver.find_element("name", "username")
    userBox.send_keys(username)
    passBox = driver.find_element("name", "password")
    passBox.send_keys(password)
    passBox.submit()


def OpenWindow():
    def validateLogin(username, password):
        print("username entered :", username.get())
        print("password entered :", password.get())
        print("Language Entered :", clicked.get(), clicked)
        X = username.get()
        Y = password.get()
        tkWindow.destroy()
        main(X, Y)

    tkWindow = Tk()
    tkWindow.geometry('700x350')
    tkWindow.title('Login Form - Python GUI')
    usernameLabel = Label(tkWindow, text="User Name").grid(row=0, column=0)
    username = StringVar()
    usernameEntry = Entry(
        tkWindow, textvariable=username).grid(row=0, column=1)
    passwordLabel = Label(tkWindow, text="Password").grid(row=1, column=0)
    password = StringVar()
    passwordEntry = Entry(tkWindow, textvariable=password,
                          show='*').grid(row=1, column=1)
    validateLogin = partial(validateLogin, username, password)

    loginButton = Button(tkWindow, text="Login",
                         command=validateLogin).grid(row=4, column=0)
    clickedLabel = Label(tkWindow, text="Select any One Language!", font=(
        "", 10)).grid(row=2, column=0)
    clicked = StringVar()
    main_menu = OptionMenu(tkWindow, clicked, "C++", "Java", "Python",
                           "Rust", "Go", "Ruby", "Enter details").grid(row=2, column=2)
    clickedEntry = Entry(tkWindow, textvariable=clicked).grid(row=3, column=2)
    print(password.get(), username.get())
    tkWindow.mainloop()


def main(username, password):
    browser = Browser()
    amazon_url = "https://www.amazon.in/ap/signin?openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&"
    driver = browser.launchBrowser(amazon_url)
    email_box = driver.find_element(By.NAME, 'email')
    email_box.send_keys(username)
    email_box.send_keys(Keys.ENTER)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, "password")))
    pass_box = driver.find_element(By.NAME, 'password')
    pass_box.send_keys(password)
    pass_box.send_keys(Keys.ENTER)
    sleep(20)

    pass


OpenWindow()
