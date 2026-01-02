import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from tests.contact_page import ContactPage

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

def test_positive_submission(driver):
    """Позитивный сценарий: все поля заполнены."""
    page = ContactPage(driver)
    page.open()
    page.fill_form("Мила", "sirmanovamilana@mail.ru", "Привет!")
    page.submit()
    assert page.is_success(), "Ожидалось сообщение об успешной отправке"

def test_negative_empty_name(driver):
    """Негативный сценарий: не введено имя."""
    page = ContactPage(driver)
    page.open()
    page.fill_form("", "sirmanovamilana@mail.ru", "Привет!")
    page.submit()
    assert page.is_error(), "Ожидалось сообщение об ошибке при пустом имени"