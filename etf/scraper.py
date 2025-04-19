from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def get_element_text(driver, by, value, wait_time=4):
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((by, value))
        )
        return element.text.strip()
    except Exception as e:
        print(f"Błąd podczas pobierania elementu ({value}):", e)
        return None


def get_iusq_de():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    url = 'https://stooq.pl/q/?s=iusq.de'
    driver.get(url)

    try:
        agree_btn = WebDriverWait(driver, 4).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'fc-cta-consent') and contains(@aria-label, 'Zgadzam się')]"))
        )
        agree_btn.click()
    except Exception as e:
        print("Błąd podczas klikania przycisku zgody:", e)

    exchange = get_element_text(driver, By.ID, "aq_iusq.de_c3")
    date = get_element_text(driver, By.ID, "aq_iusq.de_d2")
    time = get_element_text(driver, By.ID, "aq_iusq.de_t1")
    daily_change_value = get_element_text(driver, By.ID, "aq_iusq.de_m2")
    daily_change_percent = get_element_text(driver, By.ID, "aq_iusq.de_m3")[1:-2]
    bid = get_element_text(driver, By.ID, "aq_iusq.de_b3")
    ask = get_element_text(driver, By.ID, "aq_iusq.de_a3")
    driver.quit()

    return float(exchange), date, time, daily_change_value, daily_change_percent, bid, ask

get_iusq_de()