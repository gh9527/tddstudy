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
        self.client.post('/',data={'item_text':'a new list item'})
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'a new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/',data={'item_text':'a new list item'})

        self.assertEqual(response.status_code,302)
        self.assertEqual(response['location'],'/list/the-only-list-in-the-world/')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(),0)

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

class ListViewTest(TestCase):
    def test_users_list_template(self):
        response = self.client.get('/list/the-only-list-in-the-world/')
        self.assertTemplateUsed(response,'list.html')

    def test_display_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/list/the-only-list-in-the-world/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
