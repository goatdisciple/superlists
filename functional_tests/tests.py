from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    # I don't know why, but this prevents send_keys() from sending crazy
    # nonsense strings on my machine
    def do_send_keys(self, textbox, term):
        while True:
            textbox.clear()  # for when we loop and search more than once
            i = 0
            while i < len(term):
                textbox.send_keys(term[i:i+10])
                i += 10
            actual_text = textbox.get_attribute('value')
            if actual_text == term:
                break
            else:
                pass  # retry because of rare send_keys() problem

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])


    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
            )

        # She types "Buy peacock feathers" into a text box (Edith's
        # hobby is tying fly-fishing lures)
        self.do_send_keys(inputbox, 'Buy peacock feathers')

        # When she hits enter, the page updates, and now the page
        # lists "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another
        # item. She enters "Use peacock feathers to make a fly" (Edith
        # is very methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.do_send_keys(inputbox, 'Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table(
            '2: Use peacock feathers to make a fly')

        # Edith wonders whether the site will remember her list. Then
        # she sees that the site has generated a unique URL for her --
        # there is some explanatory text to that effect.
        self.fail('Finish the test!')

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep
