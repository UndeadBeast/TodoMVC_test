import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from locators import ToDoPageLocators
from utils import timeit


class ToDoPage(object):

    def __init__(self, driver_come, default_wait_timeout=30, input_delay=0.01):
        self.driver = driver_come
        self.default_wait_timeout = default_wait_timeout
        self.input_delay = input_delay

#   -------------------------------------------------------------------

    def is_element_in_list(self, element_text):
        element = self.driver.find_element_by_xpath("//label[text()='{0}']".format(element_text))
        if element.is_displayed():
            return True
        else:
            return False

    def is_title_exists(self):
        return "TroopJS • TodoMVC" in self.driver.title

    @timeit
    def count_element_in_list(self):
        list_of_elements = self.driver.find_element(*ToDoPageLocators.TODO_LIST)
        all_elements = list_of_elements.find_elements(*ToDoPageLocators.TODO_ELEMENT_MARKER)
        # all_elements = list_of_elements.find_elements_by_tag_name("li")
        self.driver.implicitly_wait(0)
        active_elements = list_of_elements.find_elements(*ToDoPageLocators.ACTIVE_ELEMENTS)
        completed_elements = list_of_elements.find_elements(*ToDoPageLocators.COMPLETED_ELEMENTS)
        # completed_elements = list_of_elements.find_elements_by_class_name("completed")
        self.driver.implicitly_wait(self.default_wait_timeout)
        elements = (len(all_elements), len(active_elements), len(completed_elements))
        return elements

#   --------------------------------------------------------------------

    def add_element(self, element_text):
        new_todo_field = self.driver.find_element(*ToDoPageLocators.INPUT_FIELD)
        new_todo_field.click()
        new_todo_field.clear()
        new_todo_field.send_keys(element_text)
        time.sleep(self.input_delay)
        new_todo_field.send_keys(Keys.ENTER)
        if new_todo_field.get_attribute("value"):
            time.sleep(self.input_delay)
            new_todo_field.send_keys(Keys.RETURN)
        if new_todo_field.get_attribute("value"):
            raise ValueError('Error while adding element: ' + element_text)

        return self.is_element_in_list(element_text)

    def edit_element(self, find_what, replace_with):
        editable_element = self.driver.find_element_by_xpath("//label[text()='{0}']".format(find_what))
        ActionChains(self.driver).double_click(editable_element).perform()
        input_field = editable_element.find_element_by_xpath("..//..//input[@class='edit']")
        input_field.send_keys(Keys.CONTROL + "a")
        input_field.send_keys(Keys.DELETE)
        input_field.send_keys(replace_with)
        input_field.send_keys(Keys.ENTER)
        #   TODO: Add some verification before return
        return True

    def delete_single_element(self, element_text):
        count_of_elements_before = self.count_element_in_list()
        element_to_delete = self.driver.find_element_by_xpath("//label[text()='{0}']".format(element_text))
        hover = ActionChains(self.driver).move_to_element(element_to_delete)
        hover.perform()
        delete_button = element_to_delete.find_element(*ToDoPageLocators.BUTTON_DELETE_SINGLE)
        ActionChains(self.driver).click(delete_button).perform()
        count_of_elements_after = self.count_element_in_list()
        return True if count_of_elements_after[0] == count_of_elements_before[0] - 1 else False

    def delete_all_completed_elements(self):
        delete_button = self.driver.find_element(*ToDoPageLocators.BUTTON_DELETE_DONE)
        delete_button.click()
        return not delete_button.is_displayed()

    def mark_single_element(self, element_text):
        count_of_elements_before = self.count_element_in_list()
        element_to_mark = self.driver.find_element_by_xpath("//label[text()='{0}']".format(element_text))
        element_to_mark.find_element(*ToDoPageLocators.BUTTON_MARK_SINGLE).click()
        count_of_elements_after = self.count_element_in_list()
        return True if count_of_elements_after[2] == count_of_elements_before[2] + 1 else False

    def mark_all(self):
        self.driver.find_element(*ToDoPageLocators.BUTTON_MARK_ALL).click()
        #   TODO: Add some verification before return
        return True

    def switch_to_all(self):
        filter_panel = self.driver.find_element(*ToDoPageLocators.FILTER_LIST)
        filter_panel.find_element(*ToDoPageLocators.FILTER_ALL).click()
        return True if self.check_active_filter() == "All" else False

    def switch_to_active(self):
        filter_panel = self.driver.find_element(*ToDoPageLocators.FILTER_LIST)
        filter_panel.find_element(*ToDoPageLocators.FILTER_ACTIVE).click()
        return True if self.check_active_filter() == "Active" else False

    def switch_to_done(self):
        filter_panel = self.driver.find_element(*ToDoPageLocators.FILTER_LIST)
        filter_panel.find_element(*ToDoPageLocators.FILTER_DONE).click()
        return True if self.check_active_filter() == "Completed" else False

    def check_active_filter(self):
        active_filter_link = self.driver.find_element(*ToDoPageLocators.FILTER_SELECTED)
        return active_filter_link.text

    def is_element_visible(self, element_name):
        self.driver.implicitly_wait(0)
        element = self.driver.find_element_by_xpath("//label[text()='{0}']".format(element_name))
        self.driver.implicitly_wait(self.default_wait_timeout)

        if element:
            return element.is_displayed()
        else:
            return False
