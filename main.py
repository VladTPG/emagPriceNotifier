
import helperfunc as hf
import tkinter as tk
from tkinter import simpledialog
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def main():
    ROOT = tk.Tk()
    ROOT.withdraw()

    url = simpledialog.askstring(
        title="URL OF PRODUCT", prompt="What's the url of the product?:")
    targetPrice = float(simpledialog.askstring(
        title="PRICE", prompt="What's the desired price for the product?:"))
    sendermail = simpledialog.askstring(
        title="E-MAIL", prompt="What's your e-mail address:")
    password = simpledialog.askstring(
        title="PASSWORD", prompt="What's your password?:")
    destinationmail = simpledialog.askstring(
        title="DESTINATION", prompt="Where do you want to receive the notification?:")

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)

    hf.price_checker(targetPrice, url, sendermail, password, destinationmail)

if __name__ =='__main__':
    main()