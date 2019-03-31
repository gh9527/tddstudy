from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

MAX_WAIT = 3
class NewVistorTest(StaticLiveServerTestCase):

	def setUp(self):
		self.brower = webdriver.Firefox()

	def tearDown(self):
		self.brower.quit()

	def wait_for_row_in_list_table(self,row_text):
		start_time = time.time()
		while True:
			try:
				table = self.brower.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(row_text,[row.text for row in rows])
				return
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)

	def test_can_start_a_list_for_one_user(self):
				
		#访问网站首页
		self.brower.get(self.live_server_url)
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

		self.wait_for_row_in_list_table('1：buy peacock feather')
		#页面有显示了一个文本框，可以输入其他代办事项
		#她输入了’use peacock feathers to make a fly
		inputbox = self.brower.find_element_by_id('id_new_item')
		inputbox.send_keys('2:use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1：buy peacock feather')
		self.wait_for_row_in_list_table('2:use peacock feathers to make a fly')


	def test_multiple_users_can_start_lists_at_different_urls(self):

		#edith新建一个代办清单
		self.brower.get(self.live_server_url)
		inputbox = self.brower.find_element_by_id('id_new_item')
		inputbox.send_keys('buy peacock feather')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('buy peacock feather')

		#他注意到清单有唯一的url
		edith_list_url = self.brower.current_url
		self.assertRegex(edith_list_url,'/list/.+')

		#Francis访问了网站
		##使用一个新的浏览器会话，确保edith的信息不会从cookie中泄露
		self.brower.quit()
		self.brower = webdriver.Firefox()
		#francis访问首页，页面中看不到edith的清单
		self.brower.get(self.live_server_url)
		page_text = self.brower.find_element_by_tag_name('body').text
		self.assertNotIn('buy peacock feather',page_text)
		self.assertNotIn('make a fly', page_text)

		#francis 输入一个新代办事项，新建一个清单
		inputbox = self.brower.find_element_by_id('id_new_item')
		inputbox.send_keys('buy milk')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('buy milk')

		#francis获得了她的唯一url
		francis_list_url = self.brower.current_url
		self.assertRegex(francis_list_url,'/list/.+')
		self.assertNotEqual(francis_list_url,edith_list_url)


	def test_layout_and_stying(self):
		#伊利斯访问首页
		self.brower.get(self.live_server_url)
		self.brower.set_window_size(1024,768)
		#她看到输入框完美居中显示 
		inputbox = self.brower.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=10
		)

		self.fail('finish test')
	#页面再次更新
	#网站为她生成唯一url
