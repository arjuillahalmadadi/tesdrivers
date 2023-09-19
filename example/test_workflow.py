# coding: utf-8

import time
import logging
import random
logging.basicConfig(level=10)

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC  # noqa
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
import undetected_chromedriver as uc

# Fungsi untuk mengklik elemen secara acak di dalam area elemen yang ditentukan
def random_click(driver, element):
    # Mendapatkan koordinat x dan y elemen
    x = element.location['x']
    y = element.location['y']

    # Menggulir halaman web ke elemen tersebut
    driver.execute_script("window.scrollTo(0, arguments[0]);", y)

    # Menggunakan ActionChains untuk menggerakkan kursor dan melakukan klik
    actions = ActionChains(driver)
    actions.move_to_element_with_offset(element, x, y).click().perform()

while True:
    def main(args=None):
        TAKE_IT_EASY = True

        if args:
            TAKE_IT_EASY = args.no_sleeps

        if TAKE_IT_EASY:
            sleep = time.sleep
        else:
            sleep = lambda n: print("we could be sleeping %d seconds here, but we don't" % n)

        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("--headless")  # Menjalankan Chrome dalam mode headless
        driver = uc.Chrome(options=chrome_options)
        driver.maximize_window()  # Maksimalkan jendela
        random_click(driver, driver.find_element(By.TAG_NAME, "body"))
        driver.get("https://www.google.com")
        
        inp_search = driver.find_element(By.XPATH, '//*[@id="APjFqb"]')
        inp_search.send_keys("linkmovie.online linkmovie online\n")

        results_container = WebDriverWait(driver, timeout=3).until(
            presence_of_element_located((By.ID, "rso"))
        )

        driver.execute_script(
            """
            let container = document.querySelector('#rso');
            let el = document.createElement('div');
            el.style = 'width:500px;display:block;background:red;color:white;z-index:999;transition:all 2s ease;padding:1em;font-size:1.5em';
            el.textContent = "Excluded from support...!";
            container.insertAdjacentElement('afterBegin', el);
            setTimeout(() => {
                el.textContent = "<<<  OH , CHECK YOUR CONSOLE! >>>"}, 2500)
            
        """
        )

        sleep(3)

        for item in results_container.find_elements(By.TAG_NAME, "a"):
            print(item.text)

        driver._web_element_cls = uc.UCWebElement

        print("switched to use uc.WebElement. which is more descriptive")
        results_container = driver.find_element(By.ID, "rso")

        for item in results_container.children():
            print(item.tag_name)
            for grandchild in item.children(recursive=True):
                print("\t\t", grandchild.tag_name, "\n\t\t\t", grandchild.text)

        print("lets go to image search")
        inp_search = driver.find_element(By.XPATH, '//*[@id="APjFqb"]')
        inp_search.clear()
        inp_search.send_keys("linkmovie online\n")

        body = driver.find_element(By.TAG_NAME, "body")
        image_search_button = body.find_elements(By.XPATH, '//*[@id="rso"]/div[1]/div/div/div[1]/div/div/span/a/h3')[0]
        image_search_button.click()

        image_search_body = WebDriverWait(driver, 5).until(
            presence_of_element_located((By.TAG_NAME, "body"))
        )

        print("getting image sources data, hold on...")

        # for item in image_search_body.find_elements(By.TAG_NAME, "img"):
        #     src = item.get_attribute("src") or item.get_attribute("data-src")
        #     print(src, "\n")

        USELESS_SITES = [
            "https://mov.linkmovie.online",
            "https://mov.linkmovie.online",
            "https://mov.linkmovie.online",
            "https://mov.linkmovie.online",
            "https://mov.linkmovie.online",
            "https://mov.linkmovie.online",
            "https://mov.linkmovie.online",
            "https://mov.linkmovie.online",
            "https://mov.linkmovie.online",
            "https://mov.linkmovie.online",
        ]

        print("opening 9 additional windows and controlling them")
        sleep(2)

        for i in range(9):
            driver.window_new()
            # Menyimpan tangkapan layar setiap window tambahan
            driver.save_screenshot(f'driver_{i+1}_screenshot.png')

        print("now we have 10 windows")
        sleep(3)
        print("using the new windows to open 9 other useless sites")
        sleep(4)

        for idx in range(1, 10):
            print("opening ", USELESS_SITES[idx])
            driver.switch_to.window(driver.window_handles[idx])

            try:
                driver.get(USELESS_SITES[idx])
                sleep(3)
                # Menggulir ke bawah
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2)

                # Menggulir ke atas
                driver.execute_script("window.scrollTo(0, 0);")
                sleep(2)

                # Auto klik dua kali pada halaman web
                random_click(driver, driver.find_element(By.TAG_NAME, "body"))
                
                sleep_time = random.randint(3, 9)
                print(f'Menunggu {sleep_time} detik sebelum iterasi berikutnya...')
                sleep(sleep_time)

            except WebDriverException as e:
                print(
                    "webdriver exception. This is not an issue in chromedriver, but rather an issue specific to your current connection. message:",
                    e.args,
                )
                continue

        for handle in driver.window_handles[1:]:
            driver.switch_to.window(handle)
            # print("look. %s is working" % driver.current_url)
            sleep(3)

        print("closing windows (including the initial one), but keeping the last new opened window")
        sleep(4)

        for handle in driver.window_handles[:-1]:
            driver.switch_to.window(handle)
            # print("look. %s is closing" % driver.current_url)
            sleep(2)
            driver.close()

        driver.switch_to.window(driver.window_handles[0])
        # print("now we only have ", driver.current_url, "left")

        sleep(2)

        driver.get("https://mov.linkmovie.online")

        sleep(5)

        # print("let's go to the UC project page")
        driver.get("https://linkmovie.online")

        sleep(7)
        driver.quit()

    if __name__ == "__main__":
        import argparse

        p = argparse.ArgumentParser()
        p.add_argument("--no-sleeps", "-ns", action="store_false")
        a = p.parse_args()
        main(a)
