from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import requests
import time
import uuid
import os

from image_generate import openai_image_gen
from text_generate import openai_text_gen


options = Options()
options.add_argument("user-data-dir=./chrome_data")

driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()), options=options
)

driver.get("https://web.whatsapp.com/")

time.sleep(20)

chats = driver.find_elements(By.CSS_SELECTOR, "div._3OvU8")


def return_chat_gpt_response(text: str = None) -> str:
    response_text_data = openai_text_gen(text)
    return response_text_data


def return_stable_diffusion_response(text: str = None) -> str:
    response_image_data = openai_image_gen(text)
    print('[INFO]: Image Generated.')
    content = requests.get(
        response_image_data
    ).content
    if 'data' not in os.listdir(os.getcwd()):
        os.mkdir(os.path.join(os.getcwd(), 'data'))
    file_path = os.path.abspath(f"./data/{uuid.uuid4().__str__()}.jpeg")
    with open(file_path, "wb") as file:
        file.write(content)
    return file_path


while True:
    for chat in chats:

        try:
            unread = chat.find_element(
                By.CSS_SELECTOR,
                "span.l7jjieqr.cfzgl7ar.ei5e7seu.h0viaqh7.tpmajp1w.c0uhu3dl."
                "riy2oczp.dsh4tgtl.sy6s5v3r.gz7w46tb.lyutrhe2.qfejxiq4.fewfhwl7."
                "ovhn1urg.ap18qm3b.ikwl5qvt.j90th5db.aumms1qt",
            ).text

            print(unread)
            if int(unread) >= 1:
                chat.click()
                message = driver.find_elements(By.CSS_SELECTOR, "div._1Gy50")[-1].text

                print(message)

                input_box = driver.find_element(
                    By.CSS_SELECTOR,
                    "div.fd365im1.to2l77zo.bbv8nyr4.mwp4sxku.gfz4du6o.ag5g9lrv",
                )
                input_box.click()

                if "!chatgpt " in message:

                    # TODO do some chatgpt shit

                    message = message.split("!chatgpt ")[1]

                    response = return_chat_gpt_response(message)

                    input_box.send_keys(response)
                    input_box.send_keys(Keys.ENTER)
                    input_box.send_keys(Keys.ESCAPE)

                elif "!chatgpt-image " in message:

                    message = message.split("!chatgpt-image ")[1]

                    response = return_chat_gpt_response(f"generate a promt for {message}")
                    image_path = return_stable_diffusion_response(response) 

                    attachment_box = driver.find_element(
                        By.XPATH, '//div[@title = "Attach"]'
                    )
                    attachment_box.click()

                    image_box = driver.find_element(
                        By.XPATH,
                        '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]',
                    )
                    image_box.send_keys(image_path)

                    time.sleep(3)
                    send_button = driver.find_element(
                        By.XPATH,
                        '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span'
                        "/div/div/div[2]/div/div[2]/div[2]/div/div",
                    )
                    send_button.click()

                    time.sleep(4)

                    input_box = driver.find_element(
                        By.CSS_SELECTOR,
                        "div.fd365im1.to2l77zo.bbv8nyr4.mwp4sxku.gfz4du6o.ag5g9lrv",
                    )
                    input_box.send_keys(Keys.ESCAPE)

                else:
                    time.sleep(4)

                    input_box = driver.find_element(
                        By.CSS_SELECTOR,
                        "div.fd365im1.to2l77zo.bbv8nyr4.mwp4sxku.gfz4du6o.ag5g9lrv",
                    )
                    input_box.send_keys(Keys.ESCAPE)

        except (NoSuchElementException, StaleElementReferenceException):
            pass

    time.sleep(2)
