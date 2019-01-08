# -*- coding: utf-8 -*-
import time
import unittest

from selenium import webdriver

import configparser
import page

# TODO: divide test to several


class LonelyTestCase(unittest.TestCase):
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

    def test_add(self):
        main_page = self.main_page
        assert main_page.is_title_exists(), "Unable to load page"
        time.sleep(3)
        self.assertTrue(main_page.add_element(u"1st element"), "Troubles adding 1st element")
        self.assertTrue(main_page.add_element(u"2nd element (1234567890.,;:’”\\/*-+)"), "Troubles adding 2st element")
        self.assertTrue(main_page.add_element(u"3rd element (!@#$%^&()_+=~`<>{}:|)"), "Troubles adding 3st element")
        self.assertTrue(main_page.add_element(u"4th element (☺☻♥♦♀♂)"), "Troubles adding 4st element")
        self.assertEqual(main_page.count_element_in_list()
                         , (4, 4, 0)
                         , "Amount of elements not as expected: (All, Active, Done)")

        self.assertTrue(main_page.delete_single_element("4th element (☺☻♥♦♀♂)"), "Element #4 wasn't deleted")
        self.assertTrue(main_page.mark_single_element("3rd element (!@#$%^&()_+=~`<>{}:|)"), "Element #3 wasn't marked")
        self.assertEqual(main_page.count_element_in_list()
                         , (3, 2, 1)
                         , "Amount of elements not as expected: (All, Active, Done)")

        self.assertTrue(main_page.switch_to_active())
        self.assertFalse(main_page.is_element_visible("3rd element (!@#$%^&()_+=~`<>{}:|)")
                         , "Completed element visible in Active list")

        self.assertTrue(main_page.delete_all_completed_elements(), "Elements are still present or button visible")
        self.assertEqual(main_page.count_element_in_list()
                         , (2, 2, 0)
                         , "Amount of elements not as expected: (All, Active, Done)")

        self.assertTrue(main_page.add_element(u"5th element (1234567890.,;:’”\\/*-+)"))
        self.assertTrue(main_page.add_element(u"!@#$%^&()_+=~`<>{}:|)"))
        self.assertTrue(main_page.add_element(u"7th element (Хєллоу ВорлдЪ ☺☻♥♦♀♂)"))
        self.assertEqual(main_page.count_element_in_list()
                         , (5, 5, 0)
                         , "Amount of elements not as expected: (All, Active, Done)")

        self.assertTrue(main_page.switch_to_all())
        self.assertTrue(main_page.edit_element("7th element (Хєллоу ВорлдЪ ☺☻♥♦♀♂)"
                                               , "7th element (Хєллоу ВорлдЪ ☺☻♥♦♀♂) edited")
                        , "Edition unsuccessfully")

        self.assertTrue(main_page.mark_all(), "All elements were not marked")
        self.assertTrue(main_page.switch_to_done())
        self.assertEqual(main_page.count_element_in_list()
                         , (5, 0, 5)
                         , "Amount of elements not as expected: (All, Active, Done)")

        self.assertTrue(main_page.edit_element("7th element (Хєллоу ВорлдЪ ☺☻♥♦♀♂) edited"
                                               , "7th element edited%2 (Хєллоу ВорлдЪ ☺☻♥♦♀♂)")
                        , "Edition unsuccessfully")
        self.assertTrue(main_page.mark_all(), "All elements were not marked")
        self.assertTrue(main_page.switch_to_all())
        self.assertEqual(main_page.count_element_in_list()
                         , (5, 5, 0)
                         , "Amount of elements not as expected: (All, Active, Done)")

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
