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
        assert self.is_title_exists(), "Unable to load page"
        time.sleep(2)

    #   -------------------------------------------------------------------

    def is_element_in_list(self, element_text):
        element = self.driver.find_element_by_xpath("//label[text()='{0}']".format(element_text))
        if element.is_displayed():
            return True
        else:
            return False

    def is_title_exists(self):
        return "TroopJS • TodoMVC" in self.driver.title

    def verify_elements_in_list(self, all_tasks, active_tasks, done_tasks):
        theoretical_elements = (all_tasks, active_tasks, done_tasks)
        factual_elements = self.count_element_in_list()
        assert theoretical_elements == factual_elements \
            , "Factual # elements != actual: \n Fact: {0}\n Theory: {1}" \
            .format(factual_elements, theoretical_elements)

    @timeit
    def count_element_in_list(self):
        list_of_elements = self.driver.find_element(*ToDoPageLocators.TODO_LIST)
        all_elements = list_of_elements.find_elements(*ToDoPageLocators.TODO_ELEMENT_MARKER)
        self.driver.implicitly_wait(0)
        active_elements = list_of_elements.find_elements(*ToDoPageLocators.ACTIVE_ELEMENTS)
        completed_elements = list_of_elements.find_elements(*ToDoPageLocators.COMPLETED_ELEMENTS)
        self.driver.implicitly_wait(self.default_wait_timeout)
        elements = (len(all_elements), len(active_elements), len(completed_elements))
        return elements

    def check_active_filter(self):
        active_filter_link = self.driver.find_element(*ToDoPageLocators.FILTER_SELECTED)
        return active_filter_link.text

    def is_element_visible(self, element_name, should_be_visisble="True"):
        self.driver.implicitly_wait(0)
        element = self.driver.find_element_by_xpath("//label[text()='{0}']".format(element_name))
        self.driver.implicitly_wait(self.default_wait_timeout)

        if element:
            assert element.is_displayed() == should_be_visisble\
                , "False vision state of element {0} ".format(element_name)

    #   --------------------------------------------------------------------
    @timeit
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

        assert self.is_element_in_list(element_text), "Unable to load element {0}".format(element_text)

    @timeit
    def edit_element(self, find_what, replace_with):
        editable_element = self.driver.find_element_by_xpath("//label[text()='{0}']".format(find_what))
        ActionChains(self.driver).double_click(editable_element).perform()
        input_field = editable_element.find_element_by_xpath("..//..//input[@class='edit']")
        input_field.send_keys(Keys.CONTROL + "a")
        input_field.send_keys(Keys.DELETE)
        input_field.send_keys(replace_with)
        input_field.send_keys(Keys.ENTER)
        #   TODO: Add some verification before return

    def delete_single_element(self, element_text):
        count_of_elements_before = self.count_element_in_list()
        element_to_delete = self.driver.find_element_by_xpath("//label[text()='{0}']".format(element_text))
        hover = ActionChains(self.driver).move_to_element(element_to_delete)
        hover.perform()
        delete_button = element_to_delete.find_element(*ToDoPageLocators.BUTTON_DELETE_SINGLE)
        ActionChains(self.driver).click(delete_button).perform()
        count_of_elements_after = self.count_element_in_list()
        assert count_of_elements_after[0] == count_of_elements_before[0] - 1 \
            , "Same amount of elements after deletion attempt. Probably element {0} wasn't deleted".format(element_text)

    def delete_all_completed_elements(self):
        delete_button = self.driver.find_element(*ToDoPageLocators.BUTTON_DELETE_DONE)
        delete_button.click()
        assert not delete_button.is_displayed(), "Deleted elements are still present or button visible"

    def mark_single_element(self, element_text):
        count_of_elements_before = self.count_element_in_list()
        element_to_mark = self.driver.find_element_by_xpath("//label[text()='{0}']".format(element_text))
        element_to_mark.find_element(*ToDoPageLocators.BUTTON_MARK_SINGLE).click()
        count_of_elements_after = self.count_element_in_list()
        assert count_of_elements_after[2] == count_of_elements_before[2] + 1, \
            "Same amount of done elements before and after marking. Probably element {0} wasn't marked" \
            .format(element_text)

    def mark_all(self):
        self.driver.find_element(*ToDoPageLocators.BUTTON_MARK_ALL).click()
        #   TODO: Add some verification before return

    def switch_to_all(self):
        filter_panel = self.driver.find_element(*ToDoPageLocators.FILTER_LIST)
        filter_panel.find_element(*ToDoPageLocators.FILTER_ALL).click()
        assert self.check_active_filter() == "All", "Not All elements page active now"

    def switch_to_active(self):
        filter_panel = self.driver.find_element(*ToDoPageLocators.FILTER_LIST)
        filter_panel.find_element(*ToDoPageLocators.FILTER_ACTIVE).click()
        assert self.check_active_filter() == "Active", "Not Active elements page active now"

    def switch_to_done(self):
        filter_panel = self.driver.find_element(*ToDoPageLocators.FILTER_LIST)
        filter_panel.find_element(*ToDoPageLocators.FILTER_DONE).click()
        assert self.check_active_filter() == "Completed", "Non Completed elements page active now"

    def destroy(self):
        self.driver.quit()
