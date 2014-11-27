from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from unittest import skip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys

class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    # I don't know why, but this prevents send_keys() from sending crazy
    # nonsense strings on my machine
    def do_send_keys(self, textbox, term):
        # while True:
            textbox.clear()  # for when we loop and search more than once
            i = 0
            while i < len(term):
                textbox.send_keys(term[i:i+10])
                i += 10
            # actual_text = textbox.get_attribute('value')
            # if actual_text == term:
            #     break
            # else:
            #     pass  # retry

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')
