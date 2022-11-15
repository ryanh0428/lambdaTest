import pytest
from pylenium.driver import Pylenium
from pylenium.element import Element, Elements


class TodoPage:
    def __init__(self, py: Pylenium):
        self.py = py

    def visit_to_do_page(self):
        self.py.visit('https://lambdatest.github.io/sample-todo-app')
        return self

    def get_to_do_by_name(self):
        return self.py.find('//*[@name"li1"]')[0].click()

    def get_all_todos(self) -> Elements:
        return self.py.find("li[ng-repeat*='sampletodo']>input")

    def add_todo(self, name: str) -> 'TodoPage':
        self.py.get('#sampletodotext').type(name)
        self.py.get('#addbutton').click()
        return self


@pytest.fixture
def page(py: Pylenium):
    return TodoPage(py).visit_to_do_page()


def test_check_first_item(page: TodoPage):
    # 2. get the check box
    checkbox = page.get_to_do_by_name()
# 3. click it

# 4. Assert that it's checked
    assert checkbox.should().be_checked()


def test_check_many_items(py: Pylenium, page: TodoPage):
    checkbox = page.get_all_todos()
    checkbox2, checkbox4 = checkbox[1], checkbox[3]
    checkbox2.click()
    checkbox4.click()
    assert py.contains('3 of 5 remaining')


def test_check_all_items(py: Pylenium, page: TodoPage):
    checkboxs = page.get_all_todos()
    for checkbox in checkboxs:
        checkbox.get('input').click()
    assert py.contains('0 of 5 remaining')


def test_add_new_item(py: Pylenium, page: TodoPage):
    page.add_todo('foo')
    assert page.get_all_todos().should().have_length(6)
    assert py.contains("6 of 6 remaining")
