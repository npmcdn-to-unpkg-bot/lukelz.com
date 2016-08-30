from django.test import TestCase
from .models import NonMediaItem

# Create your tests here.

class NonMediaItemTestCase(TestCase):
    def test_item(self):
        i = NonMediaItem()
        i.name = "Dog"
        i.price = 50
        i.weight = 20
        i.length = 14
        i.width = 18
        i.height = 8
        i.is_fulfilled=True
        i.item_category = "Beauty"
        i.get_size()
        i.shipping_weight()
        self.assertEqual(i.get_size(), 'large standard')
        self.assertEqual(i.fulfillment_cost(), '3.03')