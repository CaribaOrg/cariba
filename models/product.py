#!/usr/bin/python3
''' This is a module for Product '''

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Float, Integer, JSON
from sqlalchemy.orm import relationship
import random


class Product(BaseModel, Base):
    '''
    Product class represents a product in the inventory.

    Attributes:
        name (str): The name of the product.
        price (float): The price of the product (default=0).
        description (str): The description of the product.
        quantity (int): The quantity available in the inventory (default=1).
        oem_number (str): The Original Equipment Manufacturer (OEM)
            number of the product.
        category_id (str): The foreign key referencing the associated category.
        category (relationship): The relationship with the associated category.

    Relationships:
        - 'category': Represents the linked category, back-ref to 'products'.
    '''
    __tablename__ = 'products'
    name = Column(String(1024))
    price = Column(Float, default=0)
    description = Column(String(1024))
    quantity = Column(Integer, default=1)
    rating = Column(Float)
    icon = Column(String(1024))
    category_id = Column(String(60), ForeignKey('categories.id'))
    category = relationship('Category',
                            back_populates='products',
                            uselist=False)
    support = Column(JSON)

    def __init__(self, **kwargs):
        '''
        Initialize a new instance of the Product class.

        Args:
            **kwargs: Arbitrary keyword arguments for attribute assignment.
        '''
        super().__init__(**kwargs)
        self.rating = round(random.uniform(3.0, 5.0), 1)
        self.quantity = round(random.uniform(0, 500))
        make_names = ['abarth', 'ac', 'acura', 'alfa romeo', 'allard', 'allstate', 'alpine', 'alvis', 'am general', 'american austin', 'american bantam', 'american motors', 'amphicar', 'apollo', 'armstrong-siddeley', 'arnolt-bristol', 'arnolt-mg', 'aston martin', 'asuna', 'auburn', 'audi', 'austin', 'austin-healey', 'avanti', 'baic', 'bentley', 'berkeley', 'bizzarrini', 'bmw', 'bond', 'borgward', 'bricklin', 'bristol', 'bugatti', 'buick', 'cadillac', 'case', 'changan', 'checker', 'chevrolet', 'chirey', 'chrysler', 'cisitalia', 'citroen', 'cole', 'continental', 'cord', 'crosley', 'cunningham', 'cupra', 'daewoo', 'daf', 'daihatsu', 'daimler', 'datsun', 'delage', 'delahaye', 'dellow', 'delorean', 'denzel', 'desoto', 'detomaso', 'deutsch-bonnet', 'diana', 'dkw', 'dodge', 'doretti', 'du pont', 'dual-ghia', 'duesenberg', 'durant', 'eagle', 'edsel', 'elcar', 'elva', 'erskine', 'essex', 'excalibur', 'facel vega', 'fairthorpe', 'falcon knight', 'fargo', 'faw', 'ferrari', 'fiat', 'fisker', 'flint', 'ford', 'foton', 'franklin', 'frazer nash', 'freightliner', 'gardner', 'genesis', 'geo', 'giant motors', 'glas', 'gmc', 'goliath', 'gordon-keeble', 'graham', 'graham-paige', 'griffith', 'healey', 'henry j', 'hillman', 'hino', 'hispano-suiza', 'honda', 'hotchkiss', 'hrg', 'hudson', 'humber', 'hummer', 'hupmobile', 'hyundai', 'infiniti', 'international', 'iso', 'isuzu', 'iveco', 'jac', 'jaguar', 'jeep', 'jensen', 'jewett', 'jmc', 'jordan', 'jowett', 'kaiser-frazer', 'karma', 'kenworth', 'kia', 'kissel', 'kurtis', 'lada', 'laforza', 'lagonda', 'lamborghini', 'lanchester', 'lancia', 'land rover', 'lasalle', 'lea-francis', 'lexington', 'lexus', 'lincoln', 'lotus', 'lucid', 'mack', 'maico', 'marathon', 'marauder', 'marcos', 'marmon', 'maserati', 'mastretta', 'matra', 'maxwell', 'maybach', 'mazda', 'mclaren', 'mercedes-benz', 'mercury', 'merkur', 'messerschmitt', 'mg', 'mini', 'mitsubishi', 'mitsubishi fuso', 'mobility ventures', 'monteverdi', 'moon', 'moretti', 'morgan', 'morris', 'moskvich', 'nardi', 'nash', 'nissan', 'nsu', 'oakland', 'oldsmobile', 'omega', 'opel', 'osca', 'packard', 'paige', 'panhard', 'panoz', 'panther', 'passport', 'peerless', 'pegaso', 'peterbilt', 'peugeot', 'pierce-arrow', 'plymouth', 'polestar', 'pontiac', 'porsche', 'qvale', 'ram', 'reliant', 'renault', 'reo', 'rickenbacker', 'riley', 'rivian', 'roamer', 'rockne', 'rolls-royce', 'rover', 'saab', 'sabra', 'saleen', 'salmson', 'saturn', 'scion', 'seat', 'shelby', 'siata', 'simca', 'singer', 'skoda', 'smart', 'spyker', 'srt', 'ssangyong', 'standard', 'star', 'stearns knight', 'sterling', 'stevens-duryea', 'studebaker', 'stutz', 'subaru', 'sunbeam', 'suzuki', 'swallow', 'talbot-lago', 'tatra', 'tesla', 'think', 'toyota', 'triumph', 'turner', 'tvr', 'uaz', 'ud', 'utilimaster', 'vam', 'vauxhall', 'vespa', 'volkswagen', 'volvo', 'vpg', 'wartburg', 'westcott', 'whippet', 'willys', 'windsor', 'wolseley', 'workhorse', 'yellow cab', 'yugo', 'zacua', 'zundapp']
        self.support = random.sample(make_names, random.randint(50, 250))
        
    def is_supported(self, car):
        return car.make.lower() in self.support

    def add_to_cart(self, user, quantity=1):
        '''
        Add the product to the user's shopping cart.

        Args:
            user (User): The user for whom the product is added to the cart.
            quantity (int): The quantity of product to be added (default=1).
        '''
        from models.cart_item import CartItem
        for item in user.cart.cart_items:
            if self.id == item.product.id:
                if quantity <= 0 or quantity + item.quantity > self.quantity:
                    quantity = self.quantity - item.quantity
                item.quantity += quantity
                item.cart.total_price += round(quantity * self.price, 2)
                item.cart.total_items += quantity
                item.cart.shipping = 3 + round((0.1 * user.cart.total_price), 2)
                return
        if quantity <= 0 or quantity > self.quantity:
            quantity = self.quantity
        ci_dict = {
                'cart_id': user.cart.id,
                'product_id': self.id,
                'quantity': quantity
                }
        ci = CartItem(**ci_dict)
        ci.save()
        user.cart.cart_items.append(ci)
        user.cart.total_price += round(quantity * self.price, 2)
        user.cart.total_items += quantity
        user.cart.shipping = 3 + round((0.1 * user.cart.total_price), 2)
        user.save()

    def remove_from_cart(self, user, quantity=1):
        '''
        Remove a specified quantity of the product from user's shopping cart.

        Args:
            user (User): The user whose cart needs to be updated.
            quantity (int, optional): The quantity of the product to be removed
                (default=1).
        '''
        from models.cart_item import CartItem
        for item in user.cart.cart_items:
            if self.id == item.product.id:
                if item.quantity <= quantity:
                    item.delete()
                    user.cart.cart_items.remove(item)
                    user.cart.total_price -= round(item.quantity * self.price, 2)
                    user.cart.total_items -= item.quantity
                    user.save()
                    return
                user.cart.total_price -= round(quantity * self.price, 2)
                item.quantity -= quantity
                item.cart.total_items -= quantity
                user.cart.shipping = 3 + round((0.1 * user.cart.total_price), 2) if item.cart.total_items else 0
                item.save()
                user.save()
                return
