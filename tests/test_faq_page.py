import pytest
from page_objects.faq_page import FAQPage

class TestFAQ:

    @pytest.mark.parametrize("question_index", range(8))
    def test_question_answer(self, driver, question_index):
        faq_page = FAQPage(driver)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        faq_page.click_question_and_check_answer(question_index)