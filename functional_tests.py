from selenium import webdriver
import unittest

class NewVistorTest(unittest.TestCase):

    def setUp(self):
        self.brower = webdriver.Chrome()

    def tearDown(self):
        self.brower.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
                
        #访问网站首页
        self.brower.get('http://127.0.0.1:8000/')
        #网站标题包含'To-Do'这个词
        self.assertIn('To-Do',self.brower.title)
        self.fail('Finish the test')
        
        #应用邀请她输入一个代办事项
        #她在一个文本框中输入了’buy peacock feather‘

        #她按回车键后，页面更新了
        #代办事向表显示了’1：buy peacock feather‘
        #页面有显示了一个文本框，可以输入其他代办事项
        #她输入了’use peacock feathers to make a fly
        #页面再次更新
        #网站为她生成唯一url

if __name__ == "__main__":
    unittest.main(warnings='ignore')