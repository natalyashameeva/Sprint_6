import pytest
from page_objects.faq_page import FAQPage


class TestFAQ:

    @pytest.mark.parametrize("question_index", range(8))
    def test_question_answer(self, driver, question_index):
        faq_page = FAQPage(driver)

        faq_page.scroll_to_bottom()
        faq_page.click_question_and_check_answer(question_index)