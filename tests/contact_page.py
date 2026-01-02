from selenium.webdriver.common.by import By
from tests.base_page import BasePage, Locator

class ContactPage(BasePage):
    NAME_FIELD: Locator = (By.NAME, "name")
    EMAIL_FIELD: Locator = (By.NAME, "email")
    MESSAGE_FIELD: Locator = (By.NAME, "message")
    SUBMIT_BUTTON: Locator = (By.CSS_SELECTOR, "button[type='submit']")
    SUCCESS_FLASH: Locator = (By.CSS_SELECTOR, "p.flash-success")
    ERROR_FLASH: Locator = (By.CSS_SELECTOR, "p.flash-error")

    def __init__(self, driver, base_url: str = "http://127.0.0.1:5000/"):
        super().__init__(driver, base_url=base_url)

    def open(self):
        super().open("/")

    def fill_form(self, name: str, email: str, message: str):
        self.type(self.NAME_FIELD, name)
        self.type(self.EMAIL_FIELD, email)
        self.type(self.MESSAGE_FIELD, message)

    def submit(self):
        try:
            self.scroll_into_view(self.SUBMIT_BUTTON)
        except Exception:
            pass
        self.click(self.SUBMIT_BUTTON)

    def is_success(self) -> bool:
        return self.is_visible(self.SUCCESS_FLASH)

    def is_error(self) -> bool:
        return self.is_visible(self.ERROR_FLASH)