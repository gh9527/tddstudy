from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest


from list.models import Item, List
from list.views import home_page

# Create your tests here.
class HomePageTest(TestCase):
    def test_home_page_return_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response,'home.html')

class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'the first list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.all()
        self.assertEqual(saved_list.first(), list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.list,list_)
        self.assertEqual(first_saved_item.text, 'the first list item')
        self.assertEqual(second_saved_item.text,'item the second')
        self.assertEqual(second_saved_item.list,list_)

class ListViewTest(TestCase):



    def test_users_list_template(self):
        response = self.client.get('/list/the-only-list-in-the-world/')
        self.assertTemplateUsed(response,'list.html')

    def test_display_all_list_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)

        response = self.client.get('/list/the-only-list-in-the-world/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post('/list/new',data={'item_text':'a new list item'})
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'a new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/list/new',data={'item_text':'a new list item'})
        self.assertRedirects(response,'/list/the-only-list-in-the-world/')