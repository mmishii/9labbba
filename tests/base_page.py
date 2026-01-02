from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from typing import Tuple, List, Optional
import os
import time

Locator = Tuple[By, str]

class BasePage:
    DEFAULT_TIMEOUT = 10

    def __init__(self, driver: WebDriver, base_url: Optional[str] = None, timeout: int = None):
        self.driver = driver
        self.base_url = base_url or ""
        self.timeout = timeout or self.DEFAULT_TIMEOUT
        self.wait = WebDriverWait(self.driver, self.timeout)

    # --- Навигация ---
    def open(self, path: str = "/"):
        """Открыть страницу (относительный путь или полный URL)."""
        url = path if path.startswith("http") else self.base_url.rstrip("/") + "/" + path.lstrip("/")
        self.driver.get(url)

    # --- Поиск элементов ---
    def find(self, locator: Locator):
        """Ждёт, пока элемент появится в DOM (presence)."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_visible(self, locator: Locator):
        """Ждёт, пока элемент станет видимым."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator: Locator) -> List:
        """Возвращает список найденных элементов (может быть пустым)."""
        return self.driver.find_elements(*locator)

    def click(self, locator: Locator):
        """Клик по элементу с ожиданием кликабельности."""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except StaleElementReferenceException:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()

    def type(self, locator: Locator, text: str, clear_first: bool = True):
        """Ввод текста в поле."""
        element = self.find_visible(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: Locator) -> str:
        """Возвращает текст видимого элемента."""
        element = self.find_visible(locator)
        return element.text.strip()

    def is_visible(self, locator: Locator) -> bool:
        """Проверяет, виден ли элемент."""
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_condition(self, condition, timeout: Optional[int] = None):
        """Ожидает произвольное условие Selenium ExpectedCondition."""
        wait = WebDriverWait(self.driver, timeout or self.timeout)
        return wait.until(condition)