from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from list.views import home_page

# Create your tests here.
class HomePageTest(TestCase):
    def test_home_page_return_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response,'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/',data={'item_text':'a new list item'})
        self.assertIn('a new list item',response.content.decode())
        self.assertTemplateUsed(response,'home.html')