from random import choice, randint
from unittest import skip
from unittest.mock import Mock, patch

from faker import Faker
from flask import url_for
from werkzeug.exceptions import HTTPException

from .view_test import ViewTest


class TestRestaurantViews(ViewTest):

    @classmethod
    def setUpClass(cls):
        super(TestRestaurantViews, cls).setUpClass()
        from gooutsafe.rao.restaurant_manager import RestaurantManager 
        cls.restaurant_manager = RestaurantManager
    
    def test_restaurants_sheet(self):
        operator = self.login_test_operator()
        restaurant = self.create_random_restaurant(operator['id'])
        rv = self.client.get(self.BASE_URL + '/restaurants/' + str(restaurant['id']))
        assert rv.status_code == 200

    def test_restaurants_sheet_error(self):
        operator = self.login_test_operator()
        _ = self.create_random_restaurant(operator['id'])
        rv = self.client.get(self.BASE_URL + '/restaurants/' + str(0))
        assert rv.status_code == 302

    def test_add_get(self):
        _ = self.login_test_operator()
        rv = self.client.get(self.BASE_URL + '/restaurants/add/' + str(0))
        assert rv.status_code == 200

    def test_add_post(self):
        owner = self.login_test_operator()
        restaurant = self.generate_random_restaurant_data(owner['id'])
        rv = self.client.post(self.BASE_URL + '/restaurants/add/' + str(owner['id']), json=restaurant)
        assert rv.status_code == 302

    def test_put_toggle_like(self):
        owner = self.login_test_operator()
        restaurant = self.create_random_restaurant(owner['id'])
        rv = self.client.get(self.BASE_URL + '/restaurants/like/' + str(restaurant['id']), json=restaurant,
            follow_redirects=False)
        assert rv.status_code == 302

    def test_put_toggle_like_error(self):
        owner = self.login_test_operator()
        restaurant = self.create_random_restaurant(owner['id'])
        rv = self.client.get(self.BASE_URL + '/restaurants/like/' + str(0), json=restaurant)
        assert rv.status_code == 302


    """
    # needs the whole resturant dict since it actually renders the page
    @skip('It fails')
    @patch('gooutsafe.rao.restaurant_manager.requests.get')
    def test_restaurant_sheet(self, mock):
        with self.captured_templates(self.app) as templates:
            data = {'restaurant_sheet': {'restaurant': {}, 'average_rate': 0, 'max_rate': 0, 'is_open': False}}
            mock.return_value = Mock(status_code=200, json=lambda : data)
            rv = self.client.get('/restaurants/' + str(randint(0, 999)))
            assert rv.status_code == 200
            assert len(templates) == 1
            template, _ = templates[0]
            assert template.name == 'restaurantsheet.html'

    # uses current_user.id :(
    @skip('It fails too')
    @patch('gooutsafe.rao.restaurant_manager.requests.put')
    def test_like(self, mock):
        with self.captured_templates(self.app) as templates:
            mock.return_value = Mock(status_code=200)
            rv = self.client.get('/restaurants/like/' + str(randint(0, 999)))
            assert rv.status_code == 302
            assert len(templates) == 1
            template, _ = templates[0]
            assert template.name == 'restaurantsheet.html'

    def test_add_restaurant_get(self):
        with self.captured_templates(self.app) as templates:
            rv = self.client.get('/restaurants/add/' + str(randint(0, 999)))
            assert rv.status_code == 200
            assert len(templates) == 1
            template, _ = templates[0]
            assert template.name == 'create_restaurant.html'

    @patch('gooutsafe.rao.restaurant_manager.requests.post')
    def test_add_restaurant_post(self, mock):
        with self.captured_templates(self.app) as templates:
            mock.return_value = Mock(status_code=200)
            restaurant = self.create_random_restaurant()
            del restaurant['lon']
            del restaurant['lat']
            del restaurant['menu_type']
            restaurant['phone'] = str(restaurant['phone'])
            rv = self.client.post('/restaurants/add/' + str(randint(0, 999)), data=restaurant)
            assert rv.status_code == 200
            assert len(templates) == 1
            template, _ = templates[0]
            assert template.name == 'create_restaurant.html'
    """
    ### Helper methods ###

    def create_random_restaurant(self, op_id):
        restaurant = self.generate_random_restaurant_data(op_id)
        restaurant_id = self.restaurant_manager.post_add(restaurant)
        if restaurant_id is not None:
            restaurant['id'] = restaurant_id
            return restaurant
        else:
            raise ValueError('Restaurant creation error')

    def generate_random_restaurant_data(self, op_id):
        name = self.faker.company()
        address = self.faker.street_address()
        city = self.faker.city()
        phone = self.faker.phone_number()
        menu_type = choice(['Italian', 'Japanese'])
        restaurant = {
            'name': name,
            'address': address,
            'city': city,
            'phone': phone,
            'menu_type': menu_type,
            'op_id': op_id
        }
        return restaurant