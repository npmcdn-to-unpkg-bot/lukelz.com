from time import strftime, gmtime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class NonMediaItem(models.Model):
    item_name = models.CharField(max_length=150)
    price = models.FloatField() # in dollars

    weight = models.FloatField() # in pounds
    unit_volume = models.FloatField(null=True, blank=True) # cubic feet
    length = models.FloatField(null=True, blank=True) # order does not matter inches
    width = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)

    item_size = models.CharField(max_length=30, blank=True,
        choices= [('small standard', 'small standard'), ('large standard', 'large standard'), ('small oversize', 'small oversize'),
        ('medium oversize', 'medium oversize'), ('large oversize', 'large oversize'), ('special oversize', 'special oversize')])

    #For referral cost calc
    item_category = models.CharField(
        max_length=150,
        choices=[('3D Printed Products', '3D Printed Products'), ('Amazon Device Accessories', 'Amazon Device Accessories'), ('Amazon Kindle', 'Amazon Kindle'), ('Automotive & Powersports', 'Automotive & Powersports'), ('Baby Products (excluding Baby Apparel)', 'Baby Products (excluding Baby Apparel)'), ('Beauty', 'Beauty'), ('Books', 'Books'), ('Everything Else', 'Everything Else'), ('Cell Phone Devices*', 'Cell Phone Devices*'), ('Clothing & Accessories', 'Clothing & Accessories'), ('Collectible Coins', 'Collectible Coins'), ('Consumer Electronics', 'Consumer Electronics'), ('Electronics Accessories', 'Electronics Accessories'), ('Everything Else', 'Everything Else'), ('Furniture & Decor', 'Furniture & Decor'), ('Health & Personal Care (including Personal Care Appliances)', 'Health & Personal Care (including Personal Care Appliances)'), ('Home & Garden (including Pet Supplies)', 'Home & Garden (including Pet Supplies)'), ('Independent Design', 'Independent Design'), ('Industrial & Scientific (including Food Service and Janitorial & Sanitation)', 'Industrial & Scientific (including Food Service and Janitorial & Sanitation)'), ('Jewelry', 'Jewelry'), ('Kitchen', 'Kitchen'), ('Luggage & Travel Accessories', 'Luggage & Travel Accessories'), ('Major Appliances', 'Major Appliances'), ('Music', 'Music'), ('Musical Instruments', 'Musical Instruments'), ('Office Products', 'Office Products'), ('Outdoors', 'Outdoors'), ('Personal Computers', 'Personal Computers'), ('Shoes, Handbags and Sunglasses', 'Shoes, Handbags and Sunglasses'), ('Software & Computer/Video Games', 'Software & Computer/Video Games'), ('Sports', 'Sports'), ('Sports Collectibles', 'Sports Collectibles'), ('Tools & Home Improvement', 'Tools & Home Improvement'), ('Toys & Games', 'Toys & Games'), ('Video & DVD', 'Video & DVD'), ('Video Games', 'Video Games'), ('Video Game Consoles', 'Video Game Consoles'), ('Watches', 'Watches'), ('Everything Else', 'Everything Else')])

    # For variable cost calc
    shipping_type = models.CharField(max_length=50, choices=[('FBA', 'FBA'), ('domestic standard', 'domestic standard'), ('domestic expedited', 'domestic expedited')])

    # For fulfillment calc
    is_fulfilled = models.BooleanField(default=False)
    item_fulfillment_cost = models.FloatField(null=True, blank=True)
    zero_fulfillment_item = models.BooleanField(default=False)
    average_order_size = models.IntegerField()
    average_time_stored = models.IntegerField()

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, blank=True, null=True)

    def __str__(self):
        return self.item_name

    @property
    def profit(self):
      return "{0:.2f}".format(self.price - self.total_amazon_cost())

    @property
    def format_amazon_cost(self):
        return self.total_amazon_cost()
    
    def total_amazon_cost(self):
        return round(self.referral_cost() + self.variable_cost() + self.fulfillment_cost() + self.storage_cost(), 2)

    @property
    def format_referral_cost(self):
        return round(self.referral_cost(), 4)

    def referral_cost(self):
        categories = {
            "3D Printed Products": [
                "12%",
                "--"
            ],
            "Amazon Device Accessories": [
                "45%",
                "$1.00"
            ],
            "Amazon Kindle": [
                "15%",
                "--"
            ],
            "Automotive & Powersports": [
                "12%", # 10% for tires and wheels
                "$1.00"
            ],
            "Baby Products (excluding Baby Apparel)": [
                "15%",
                "$1.00"
            ],
            "Beauty": [
                "15%",
                "$1.00"
            ],
            "Books": [
                "15%",
                "--"
            ],
            "Cell Phone Devices*": [
                "8%",
                "--"
            ],
            "Clothing & Accessories": [
                "15%",
                "$1.00"
            ],
            "Collectible Coins": [
                "--",
                "$1.00"
            ],
            "Consumer Electronics": [
                "8%",
                "$1.00"
            ],
            "Electronics Accessories": [
                "--",
                "$1.00"
            ],
            "Furniture & Decor": [
                "15%",
                "$1.00"
            ],
            "Health & Personal Care (including Personal Care Appliances)": [
                "15%",
                "$1.00"
            ],
            "Home & Garden (including Pet Supplies)": [
                "15%",
                "$1.00"
            ],
            "Independent Design": [
                "--",
                "$1.00"
            ],
            "Industrial & Scientific (including Food Service and Janitorial & Sanitation)": [
                "12%",
                "$1.00"
            ],
            "Jewelry": [
                "20%",
                "$2.00"
            ],
            "Kitchen": [
                "15%",
                "$1.00"
            ],
            "Luggage & Travel Accessories": [
                "15%",
                "$1.00"
            ],
            "Major Appliances": [
                "--",
                "$1.00"
            ],
            "Music": [
                "15%",
                "--"
            ],
            "Musical Instruments": [
                "15%",
                "$1.00"
            ],
            "Everything Else": [
                "15%",
                "--"
            ],
            "Office Products": [
                "15%",
                "$1.00"
            ],
            "Outdoors": [
                "15%",
                "$1.00"
            ],
            "Personal Computers": [
                "6%",
                "$1.00"
            ],
            "Shoes, Handbags and Sunglasses": [
                "15%",
                "$1.00"
            ],
            "Software & Computer/Video Games": [
                "15%",
                "--"
            ],
            "Sports": [
                "15%",
                "$1.00"
            ],
            "Sports Collectibles": [
                "--",
                "--"
            ],
            "Tools & Home Improvement": [
                "--",
                "$1.00"
            ],
            "Toys & Games": [
                "15%",
                "--"
            ],
            "Video & DVD": [
                "15%",
                "--"
            ],
            "Video Game Consoles": [
                "8%",
                "--"
            ],
            "Video Games": [
                "15%",
                "--"
            ],
            "Watches": [
                "--",
                "$2.00"
            ]
        }
        if categories[self.item_category][0] == "--":
            return float(categories[self.item_category][1][1:])
        elif categories[self.item_category][1] == "--":
            return self.price * .01 * float(categories[self.item_category][0][:-1])
        else:
            return max(
                self.price * .01 * float(categories[self.item_category][0][:-1]),
                float(categories[self.item_category][1][1:])
            )

    @property
    def format_variable_cost(self):
        return round(self.variable_cost(), 4)

    def variable_cost(self):
        if self.shipping_type == 'FBA':
            return 0
        elif self.shipping_type == 'domestic standard':
            return 0.45 + .05 * self.weight
        else:
            return 0.65 + .1 * self.weight

    # Fulfillment vs own inventory
    # Store items with highest fulfillment_cost(FBA fees + storage * months)/Price in warehouse
    # Store items that do not benefit much from (buy box, Prime subscribers) how to quantify??
    # Per item Amazon fulfillment (w/o shipping speed)
    
    @property
    def format_fulfillment_cost(self):
        return round(self.fulfillment_cost(), 4)

    def fulfillment_cost(self):
        pack_cost = {
            'small oversize': 4.09,
            'medium oversize': 5.20,
            'large oversize': 8.40,
            'special oversize': 10.53,
        }
        if not self.is_fulfilled:
            return 0
        elif self.item_fulfillment_cost:
            return self.item_fulfillment_cost
        elif self.get_size() == 'small standard' or self.get_size() == 'large standard':
            return 1.0 / self.average_order_size + 1.06 + self.weight_handling_cost()
        else:
            return pack_cost[self.get_size()] + self.weight_handling_cost()

    def weight_handling_cost(self):
        size = self.get_size()
        if size == 'small standard':
            if strftime("%m", gmtime()) <= '10':
                return 0.5
            else:
                return 0.47
        elif size == 'large standard':
            if strftime("%m", gmtime()) <= '10':
                if self.weight <= 1:
                    return 0.96
                elif self.weight <= 2:
                    return 1.95
                else:
                    return 1.95 + 0.39 * (self.shipping_weight() - 2)
            else:
                if self.weight <= 1:
                    return 0.82
                elif self.shipping_weight() <= 2:
                    return 1.66
                else:
                    return 1.66 + 0.35 * (self.shipping_weight() - 2)
        elif size == 'small oversize':
            if strftime("%m", gmtime()) > '10':
                return 1.85 + .35 * max(self.shipping_weight() - 2, 0)
            else:
                return 2.06 + .39 * max(self.shipping_weight() - 2, 0)
        elif size == 'medium oversize':
            if strftime("%m", gmtime()) > '10':
                return 2.1 + .35 * max(self.shipping_weight() - 2, 0)
            else:
                return 2.73 + .39 * max(self.shipping_weight() - 2, 0)
        elif size == 'large oversize':
            if strftime("%m", gmtime()) > '10':
                return 56.57 + .76 * max(self.shipping_weight() - 90, 0)
            else:
                return 63.98 + .80 * max(self.shipping_weight() - 90, 0)
        else:
            if strftime("%m", gmtime()) > '10':
                return 115.73 + .88 * max(self.shipping_weight() - 90, 0)
            else:
                return 124.58 + .92 * max(self.shipping_weight() - 90, 0)

    def shipping_weight(self):
        if self.unit_volume:
            unit_volume = self.unit_volume * 1728
        else:
            unit_volume = self.length * self.width * self.height

        return max(self.weight, unit_volume / 166)

    def get_size(self):
        if self.item_size:
            return self.item_size
        dimensions = [self.length, self.width, self.height]
        dimensions.sort(reverse=True)
        length_girth = dimensions[0] + 2 * (dimensions[1] + dimensions[2])
        if self.shipping_weight() <= 12 and dimensions[0] <= 15 and dimensions[1] <= 12 and dimensions[2] <= 0.75:
            return 'small standard'
        elif self.shipping_weight() <= 20 and dimensions[0] <= 18 and dimensions[1] <= 14 and dimensions[2] <= 8:
            return 'large standard'
        elif self.shipping_weight()<= 70 and dimensions[0] <= 60 and dimensions[1] <= 30 and length_girth <= 130:
            return 'small oversize'
        elif self.shipping_weight() <= 150 and dimensions[0] <= 108 and length_girth <= 130:
            return 'medium oversize'
        elif self.shipping_weight() <= 150 and dimensions[0] <= 108 and length_girth <= 165:
            return 'large oversize'
        else:
            return 'special oversize'

    @property
    def format_storage_cost(self):
        return round(self.storage_cost(), 4)

    def storage_cost(self):
        if self.unit_volume:
            unit_volume = self.unit_volume
        else:
            unit_volume = self.length * self.width * self.height / 1728
        if self.get_size() == 'small standard' or self.get_size() == 'large standard':
            if strftime("%m", gmtime()) <= '10':
                return 0.54 * unit_volume * self.average_time_stored
            return 2.25 * unit_volume * self.average_time_stored
        else:
            if strftime("%m", gmtime()) <= '10':
                return 0.43 * unit_volume * self.average_time_stored
            return 1.15 * unit_volume * self.average_time_stored


