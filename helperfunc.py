import smtplib
import time
import requests
import pyautogui
import pywinauto
import pygetwindow as gw
from bs4 import BeautifulSoup

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}


def focus_to_window(window_title=None):
    window = gw.getWindowsWithTitle(window_title)[0]
    if window.isActive == False:
        pywinauto.application.Application().connect(
            handle=window._hWnd).top_window().set_focus()


def send_mail(sendermail, destinationmail, password, url):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sendermail, password)
    subject = 'The product is in stock'
    body = 'Link: ' + url
    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        sendermail,
        destinationmail,
        msg
    )
    server.quit()
    print('E-mail sent!')


def price_checker(targetPrice, url, sendermail, password, destinationmail):
    while True:
        stock = False
        pretBun = False
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        text = soup.find(class_="label label-out_of_stock")
        pret = soup.find(class_="product-new-price")
        if pret != None:
            pret = soup.find(class_="product-new-price").get_text()
            pret = pret.replace(" ", " ")
            pret = pret.replace("Lei", " ")
            try:
                pret = pret.replace(".", "")
            except:
                pass
            print(pret)
            try:
                pret = float(pret)/100.0
            except:
                pass
            if type(pret) is not None:
                pret = pret.replace(",",".")
                pret = float(pret)
            if type(pret) == float:
                if pret < targetPrice:
                    pretBun = True
        if text != None:
            text = soup.find(class_="label label-out_of_stock").get_text()
        print("Checking stock...")
        time.sleep(1)
        if text == None:
            stock = True
        print(pret)
        print(text)
        print("In stock:", stock)
        print("Wanted price:", pretBun)
        if stock == True and pretBun == True:
            nr_notificari = 5
            focus_to_window("eMAG")
            time.sleep(1)
            pyautogui.press('f5')
            while(nr_notificari):
                print("In stock")
                send_mail(sendermail, destinationmail, password, url)
                time.sleep(30)
                nr_notificari -= 1
        else:
            print("\n")
            print("Not in stock or price too high\nChecking again in 5 seconds!\n")
        if text == None and pret == None:
            active = gw.getActiveWindow().title
            try:
                focus_to_window("eMAG")
                time.sleep(2)
                pyautogui.press('f5')
                time.sleep(1)
                focus_to_window(active)
            except:
                print("Eroare la eMAG")
                pass
        time.sleep(4)