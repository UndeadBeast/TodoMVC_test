# -*- coding: utf-8 -*-
import unittest

from selenium import webdriver

import configparser
import page


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
        mp = self.main_page
        # add elements
        mp.add_element(u"1st element")
        mp.add_element(u"2nd element (1234567890.,;:’”\\/*-+)")
        mp.add_element(u"3rd element (!@#$%^&()_+=~`<>{}:|)")
        mp.add_element(u"4th element (☺☻♥♦♀♂)")
        mp.verify_elements_in_list(4, 4, 0)
        # delete one element
        mp.delete_single_element("4th element (☺☻♥♦♀♂)")
        # mark one element
        mp.mark_single_element("3rd element (!@#$%^&()_+=~`<>{}:|)")
        mp.verify_elements_in_list(3, 2, 1)
        mp.switch_to_active()
        mp.is_element_visible("3rd element (!@#$%^&()_+=~`<>{}:|)", should_be_visisble=False)
        # unmark single element
        mp.switch_to_done()
        mp.mark_single_element("3rd element (!@#$%^&()_+=~`<>{}:|)")
        mp.is_element_visible("3rd element (!@#$%^&()_+=~`<>{}:|)", should_be_visisble=False)
        mp.switch_to_active()
        # mark one element again
        mp.mark_single_element("3rd element (!@#$%^&()_+=~`<>{}:|)")
        # delete all done elements
        mp.delete_all_completed_elements()
        mp.verify_elements_in_list(2, 2, 0)
        #add elements again
        mp.add_element(u"5th element (1234567890.,;:’”\\/*-+)")
        mp.add_element(u"6th element (!@#$%^&()_+=~`<>{}:|)")
        mp.add_element(u"7th element (Хєллоу ВорлдЪ ☺☻♥♦♀♂)")
        mp.verify_elements_in_list(5, 5, 0)
        # edit elements
        mp.switch_to_all()
        mp.edit_element("7th element (Хєллоу ВорлдЪ ☺☻♥♦♀♂)"
                        , "7th element (Хєллоу ВорлдЪ ☺☻♥♦♀♂) edited")
        #mark all elements
        mp.mark_all()
        mp.switch_to_done()
        mp.verify_elements_in_list(5, 0, 5)
        # edit done element
        mp.edit_element("7th element (Хєллоу ВорлдЪ ☺☻♥♦♀♂) edited"
                        , "7th element edited%2 (Хєллоу ВорлдЪ ☺☻♥♦♀♂)")
        # unmark all elements
        mp.mark_all()
        mp.switch_to_all()
        mp.verify_elements_in_list(5, 5, 0)

    def tearDown(self):
        self.main_page.destroy()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
