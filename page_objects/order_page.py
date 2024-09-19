from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import BASE_URL, YANDEX_DZEN_URL

class OrderPage:
    def __init__(self, driver):
        self.driver = driver

    # Локаторы для первой части формы
    order_button_top = (By.CLASS_NAME, 'Button_Button__ra12g')
    order_button_bottom = (By.CLASS_NAME, 'Button_Middle__1CSJM')
    name_input = (By.XPATH, '//input[@placeholder="* Имя"]')
    surname_input = (By.XPATH, '//input[@placeholder="* Фамилия"]')
    address_input = (By.XPATH, '//input[@placeholder="* Адрес: куда привезти заказ"]')
    metro_station_input = (By.XPATH, '//input[@placeholder="* Станция метро"]')
    metro_station_dropdown_option = (By.CLASS_NAME, 'select-search__row')
    phone_input = (By.XPATH, '//input[@placeholder="* Телефон: на него позвонит курьер"]')
    next_button = (By.CLASS_NAME, 'Button_Middle__1CSJM')

    # Локаторы для второй части формы
    date_input = (By.XPATH, '//input[@placeholder="* Когда привезти самокат"]')
    calendar_day = (By.XPATH, '//div[contains(@class, "react-datepicker__day--020")]')
    rent_duration_dropdown = (By.CLASS_NAME, 'Dropdown-control')
    rent_duration_option = (By.XPATH, '//div[@class="Dropdown-menu"]/div[1]')
    comment_input = (By.XPATH, '//input[@placeholder="Комментарий для курьера"]')

    # Локаторы выбора цвета самоката
    black_scooter_checkbox = (By.ID, 'black')
    grey_scooter_checkbox = (By.ID, 'grey')

    # Локаторы для оформления и проверки заказа
    submit_button = (By.CSS_SELECTOR, 'button[class*="Button"]:nth-of-type(2)')
    confirmation_order_button = (By.XPATH, '//button[text()="Да"]')
    order_status_button = (By.XPATH, '//button[text()="Посмотреть статус"]')
    cancel_order_button = (By.XPATH, "//button[contains(text(), 'Отменить заказ')]")

    # Локатор для кнопки принятия куки и логотипов
    cookie_accept_button = (By.ID, 'rcc-confirm-button')
    scooter_logo = (By.XPATH, '//img[@alt="Scooter"]')
    yandex_logo = (By.XPATH, '//img[@alt="Yandex"]')
    home_header = (By.XPATH, '//div[@class="Home_Header__iJKdX"]')

    # Локатор для модального окна после успешного оформления
    success_modal = (By.CLASS_NAME, 'Order_Modal__YZ-d3')

    # Метод для проверки видимости модального окна
    def verify_success_modal(self):
        assert self.driver.find_element(*self.success_modal).is_displayed()

    # Проверяем отображение кнопки отмены заказа
    def verify_cancel_button(self):
        assert self.driver.find_element(*self.cancel_order_button).is_displayed()

    # Проверяем заголовок на главной странице
    def verify_home_header(self):
        assert self.driver.find_element(*self.home_header).is_displayed()

    def click_order_button(self, top_button=True):
        if top_button:
            self.driver.find_element(*self.order_button_top).click()
        else:
            self.driver.find_element(*self.order_button_bottom).click()

    def fill_order_form(self, name, surname, address, phone, metro_station):
        self.driver.find_element(*self.name_input).send_keys(name)
        self.driver.find_element(*self.surname_input).send_keys(surname)
        self.driver.find_element(*self.address_input).send_keys(address)

        # Выбор станции метро
        metro_input = self.driver.find_element(*self.metro_station_input)
        metro_input.send_keys(metro_station)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.metro_station_dropdown_option)
        ).click()

        self.driver.find_element(*self.phone_input).send_keys(phone)
        self.driver.find_element(*self.next_button).click()

    def select_date_and_rent_duration(self, comment=""):
        # Ожидание и выбор даты
        date_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.date_input)
        )
        date_field.click()

        calendar_day_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.calendar_day)
        )
        calendar_day_element.click()

        # Ожидание и выбор срока аренды
        rent_dropdown = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.rent_duration_dropdown)
        )
        rent_dropdown.click()
        self.driver.find_element(*self.rent_duration_option).click()

        # Ввод комментария для курьера
        if comment:
            self.driver.find_element(*self.comment_input).send_keys(comment)

    def select_scooter_color(self, color="black"):
        if color == "black":
            self.driver.find_element(*self.black_scooter_checkbox).click()
        elif color == "grey":
            self.driver.find_element(*self.grey_scooter_checkbox).click()

    def submit_order(self):
        self.driver.find_element(*self.submit_button).click()

    def confirmation_order(self):
        self.driver.find_element(*self.confirmation_order_button).click()

    def order_status(self):
        self.driver.find_element(*self.order_status_button).click()


    def accept_cookies(self):
        try:
            self.driver.find_element(*self.cookie_accept_button).click()
        except:
            pass

    def click_scooter_logo(self):
        self.driver.find_element(*self.scooter_logo).click()
        WebDriverWait(self.driver, 10).until(
            EC.url_to_be(BASE_URL)
        )

    def click_yandex_logo(self):
        main_window = self.driver.current_window_handle
        self.driver.find_element(*self.yandex_logo).click()

        WebDriverWait(self.driver, 10).until(
            EC.number_of_windows_to_be(2)
        )

        new_window = [window for window in self.driver.window_handles if window != main_window][0]
        self.driver.switch_to.window(new_window)
        WebDriverWait(self.driver, 10).until(
            EC.url_to_be(YANDEX_DZEN_URL)
        )
        return self.driver.current_url