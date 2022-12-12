from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import time

options = Options()
options.add_argument("user-data-dir=/chrome_data")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

driver.get("https://web.whatsapp.com/")

time.sleep(20)

chats = driver.find_elements(By.CSS_SELECTOR, "div._3OvU8")

for chat in chats:

    try:
        unread = chat.find_element(By.CSS_SELECTOR, "span.l7jjieqr.cfzgl7ar.ei5e7seu.h0viaqh7.tpmajp1w.c0uhu3dl."
                                                    "riy2oczp.dsh4tgtl.sy6s5v3r.gz7w46tb.lyutrhe2.qfejxiq4.fewfhwl7."
                                                    "ovhn1urg.ap18qm3b.ikwl5qvt.j90th5db.aumms1qt").text

        print(unread)
        if int(unread) >= 1:
            chat.click()
            message = driver.find_element(By.CSS_SELECTOR, "div._1Gy50").text

            if "!chatgpt" in message:
                # TODO do some chatgpt shit
                print(message)
                message = message.split("!chatgpt ")[1]
            elif "!chatgpt-image" in message:
                # TODO do some chatgpt + stablediff shit
                print(message)
                message = message.split("!chatgpt-image ")[1]
            else:
                pass

    except NoSuchElementException:
        pass
