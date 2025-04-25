from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from decimal import Decimal, InvalidOperation


def to_decimal(value):
    try:
        if value is None or value.strip() == '' or value.strip() == '-':
            return Decimal('0.0')
        return Decimal(value.replace(',', '').replace(' ', ''))
    except (InvalidOperation, AttributeError):
        return Decimal('0.0')


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

    url = 'https://finance.yahoo.com/quote/IUSQ.DE/'
    driver.get(url)

    try:
        agree_btn = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'accept-all') and text()='Accept all']")
            )
        )
        agree_btn.click()
    except Exception as e:
        print("Błąd podczas klikania przycisku 'Accept all':", e)

    bid_text = WebDriverWait(driver, 4).until(
        EC.presence_of_element_located(
            (By.XPATH, "//span[@title='Bid']/following-sibling::span")
        )
    ).text

    ask_text = WebDriverWait(driver, 4).until(
        EC.presence_of_element_located(
            (By.XPATH, "//span[@title='Ask']/following-sibling::span")
        )
    ).text

    if ask_text == "" or bid_text == "":
        open_value = WebDriverWait(driver, 4).until(
            EC.presence_of_element_located(
                (By.XPATH, "//span[@title='Open']/following-sibling::span//fin-streamer")
            )
        ).text
        return (
            to_decimal(open_value),
            to_decimal(open_value)
        )

    driver.quit()

    return (
        to_decimal(bid_text[:6]),
        to_decimal(ask_text[:6]),
    )
