import pytest
from page_objects.order_page import OrderPage
from constants import YANDEX_DZEN_URL


class TestOrder:

    @pytest.mark.parametrize("name, surname, address, metro_station, phone, scooter_color", [
        ("Анна", "Иванова", "Москва, Проспект Мира, 3", "Сухаревская", "89991234567", "black"),
        ("Василий", "Иванов", "Москва, Песчаная, 1", "Сокол", "89999999991", "grey")
    ])
    def test_order(self, driver, name, surname, address, metro_station, phone, scooter_color):
        order_page = OrderPage(driver)

        order_page.accept_cookies()

        # Оформление заказа, первая часть формы
        order_page.click_order_button(top_button=True)
        order_page.fill_order_form(name, surname, address, phone, metro_station)

        # Вторая часть формы
        order_page.select_date_and_rent_duration(comment="Позвонить за час до доставки")
        order_page.select_scooter_color(scooter_color)

        # Оформление заказа и проверка
        order_page.submit_order()
        order_page.confirmation_order()
        order_page.verify_success_modal()

        order_page.order_status()
        order_page.verify_cancel_button()

        # Проверяем переход на главную страницу при клике на логотип Самоката
        order_page.click_scooter_logo()
        order_page.verify_home_header()

    def test_yandex_logo(self, driver):
        order_page = OrderPage(driver)
        order_page.accept_cookies()
        # Проверяем открытие нового окна при клике на логотип Яндекса
        new_window_url = order_page.click_yandex_logo()
        assert new_window_url == YANDEX_DZEN_URL




