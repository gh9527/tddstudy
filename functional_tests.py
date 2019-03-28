from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVistorTest(unittest.TestCase):

    def setUp(self):
        self.brower = webdriver.Chrome()

    def tearDown(self):
        self.brower.quit()

    def check_for_row_in_list_table(self,row_text):
        table = self.brower.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text,[row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
                
        #访问网站首页
        self.brower.get('http://127.0.0.1:8000/')
        #网站标题和头部包含'To-Do'这个词
        self.assertIn('To-Do',self.brower.title)
        header_text = self.brower.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)
        
        #应用邀请她输入一个代办事项
        inputbox = self.brower.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'enter a to-do item'
        )
        #她在一个文本框中输入了’buy peacock feather‘
        #她按回车键后，页面更新了
        #代办事向表显示了’1：buy peacock feather‘
        inputbox.send_keys('1：buy peacock feather')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(3)
        self.check_for_row_in_list_table('1：buy peacock feather')
        #页面有显示了一个文本框，可以输入其他代办事项
        #她输入了’use peacock feathers to make a fly
        inputbox = self.brower.find_element_by_id('id_new_item')
        inputbox.send_keys('use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1：buy peacock feather')
        self.check_for_row_in_list_table('use peacock feathers to make a fly')
        self.fail('finish test')
        #页面再次更新
        #网站为她生成唯一url

if __name__ == "__main__":
    unittest.main(warnings='ignore')