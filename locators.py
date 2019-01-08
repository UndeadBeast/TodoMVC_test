from selenium.webdriver.common.by import By


class ToDoPageLocators(object):
    ACTIVE_ELEMENTS = (By.CLASS_NAME, 'active')
    BUTTON_DELETE_DONE = (By.ID, "clear-completed")
    BUTTON_DELETE_SINGLE = (By.XPATH, "..//button[@class='destroy']")
    BUTTON_MARK_SINGLE = (By.XPATH, "..//input")
    BUTTON_MARK_ALL = (By.ID, "toggle-all")
    COMPLETED_ELEMENTS = (By.CLASS_NAME, 'completed')
    FILTER_ACTIVE = (By.XPATH, "//*[contains(text(), 'Active')]")
    FILTER_ALL = (By.XPATH, "//*[contains(text(), 'All')]")
    FILTER_DONE = (By.XPATH, "//*[contains(text(), 'Completed')]")
    FILTER_LIST = (By.ID, 'filters')
    FILTER_SELECTED = (By.CLASS_NAME, "selected")
    INPUT_FIELD = (By.ID, 'new-todo')
    TODO_ELEMENT_MARKER = (By.TAG_NAME, 'li')
    TODO_ELEMENT_TEXT_MARKER = (By.CLASS_NAME, 'label')
    TODO_LIST = (By.ID, 'todo-list')
