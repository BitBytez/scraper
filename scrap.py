from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from Mailer import Mailer
from ExcelWriter import ExcelWriter
from GSheetWriter import GSheetWriter

class Browser:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    def __del__(self):
        self.driver.close()
        pass

    def launchBrowser(self, url):
        self.driver.get(url)
        return self.driver

def readTable(table):
    tableHead = table.find_element(By.CLASS_NAME, "rt-thead")
    headerCols = tableHead.find_elements(By.CLASS_NAME, "rt-th")
    headData = []
    for hc in headerCols[:-1]:
        headData.append(hc.text) 
    tableBody = table.find_element(By.CLASS_NAME, "rt-tbody")
    rows = tableBody.find_elements(By.CLASS_NAME, "rt-tr-group")
    rowData = [headData]
    for row in rows:
        cols = row.find_elements(By.CLASS_NAME, "rt-td")
        colData = []
        for col in cols[:-1]:
            colData.append(col.text)
        rowData.append(colData)
    return rowData


def getData():
    browser = Browser()
    driver = browser.launchBrowser("https://demoqa.com/webtables")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "rt-table")))
    table = driver.find_element(By.CLASS_NAME, "rt-table")
    data = readTable(table)
    return data

def writeIntoExcel(data):
    excel = ExcelWriter()
    excel.writeRows(data)
    excel.saveExcel()

def writeIntoGSheets(data):
    gsWriter = GSheetWriter()
    sheetID = gsWriter.createSheet("this is sample title")
    gsWriter.insertIntoSheet(sheetID, data)
    link = "https://docs.google.com/spreadsheets/d/{}".format(sheetID)
    return link

def sendMail(link):
    mail = Mailer()
    body = "This the required GSheets link : {}".format(link)
    mail.send_mail(body=body)

def main():
    data = getData()
    writeIntoExcel(data)
    link = writeIntoGSheets(data)
    sendMail(link)
main()