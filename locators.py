from selenium.webdriver.common.by import By


class ToDoPageLocators(object):
    INPUT_FIELD = (By.ID, 'new-todo')
    TODO_LIST = (By.ID, 'todo-list')
    TODO_ELEMENT_MARKER = (By.TAG_NAME, 'li')
    TODO_ELEMENT_TEXT_MARKER = (By.CLASS_NAME, 'label')
    ACTIVE_ELEMENTS = (By.CLASS_NAME, 'active')
    COMPLETED_ELEMENTS = (By.CLASS_NAME, 'completed')
    BUTTON_DELETE_SINGLE = (By.XPATH, "..//button[@class='destroy']")
    BUTTON_MARK_SINGLE = (By.XPATH, "..//input")
    BUTTON_MARK_ALL = (By.ID, "toggle-all")
    BUTTON_DELETE_DONE = (By.ID, "clear-completed")
    FILTER_LIST = (By.ID, 'filters')
    FILTER_ALL = (By.XPATH, "//*[contains(text(), 'All')]")
    FILTER_ACTIVE = (By.XPATH, "//*[contains(text(), 'Active')]")
    FILTER_DONE = (By.XPATH, "//*[contains(text(), 'Completed')]")
    FILTER_SELECTED = (By.CLASS_NAME, "selected")
