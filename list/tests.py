from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from list.models import Item
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

class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'the first list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'the first list item')
        self.assertEqual(second_saved_item.text,'item the second')