# -*- coding: utf-8 -*-
import time
import unittest

from selenium import webdriver

import configparser
import page

# TODO: divide test to several


class UseCaseScenario(unittest.TestCase):
    def setUp(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.wait_timeout = float(config['DEFAULT']['default_wait_timeout'])
        self.input_delay = float(config['TEST']['break_after_input_text'])
        self.driver = webdriver.Chrome(config['ENVIRONMENT']['chromedriver_path'])
        self.driver.set_page_load_timeout(config['DEFAULT']['page_load_timeout'])
        self.driver.get(config['DEFAULT']['site_URL'])

        self.driver.implicitly_wait(self.wait_timeout)
        self.verificationErrors = []
        self.accept_next_alert = True

        self.main_page = page.ToDoPage(self.driver, self.wait_timeout, self.input_delay)

    def test_scenario(self):
        main_page = self.main_page
        main_page.add_element(u"1st element")
        main_page.add_element(u"2nd element (1234567890.,;:’”\\/*-+)")
        main_page.add_element(u"3rd element (!@#$%^&()_+=~`<>{}:|)")
        main_page.add_element(u"4th element (☺☻♥♦♀♂)")
        main_page.verify_elements_in_list(4, 4, 0)
        main_page.delete_single_element("4th element (☺☻♥♦♀♂)")
        main_page.mark_single_element("3rd element (!@#$%^&()_+=~`<>{}:|)")
        main_page.verify_elements_in_list(3, 2, 1)
        main_page.switch_to_active()
        main_page.is_element_visible("3rd element (!@#$%^&()_+=~`<>{}:|)", should_be_visisble=False)
        main_page.delete_all_completed_elements()
        main_page.verify_elements_in_list(2, 2, 0)
        main_page.add_element(u"5th element (1234567890.,;:’”\\/*-+)")
        main_page.add_element(u"6th element (!@#$%^&()_+=~`<>{}:|)")
        main_page.add_element(u"7th element (Хєллоу ВорлдЪ ☺☻♥♦♀♂)")
        main_page.verify_elements_in_list(5, 5, 0)
        main_page.switch_to_all()
        main_page.edit_element("7th element (Хєллоу ВорлдЪ ☺☻♥♦♀♂)"
                               , "7th element (Хєллоу ВорлдЪ ☺☻♥♦♀♂) edited")
        main_page.mark_all()
        main_page.switch_to_done()
        main_page.verify_elements_in_list(5, 0, 5)
        main_page.edit_element("7th element (Хєллоу ВорлдЪ ☺☻♥♦♀♂) edited"
                               , "7th element edited%2 (Хєллоу ВорлдЪ ☺☻♥♦♀♂)")
        main_page.mark_all()
        main_page.switch_to_all()
        main_page.verify_elements_in_list(5, 5, 0)

    def tearDown(self):
        self.main_page.destroy()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
