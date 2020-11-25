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
        assert rv.status_code == 200

    def test_put_toggle_like_error(self):
        owner = self.login_test_operator()
        restaurant = self.create_random_restaurant(owner['id'])
        rv = self.client.get(self.BASE_URL + '/restaurants/like/' + str(0), json=restaurant)
        assert rv.status_code == 302

    def test_post_details(self):
        owner = self.login_test_operator()
        restaurant = self.create_random_restaurant(owner['id'])
        rv = self.client.get(self.BASE_URL + '/restaurants/details/' + str(owner['id']), json=restaurant)
        assert rv.status_code == 200

    def test_post_save_details(self):
        owner = self.login_test_operator()
        restaurant = self.create_random_restaurant(owner['id'])
        tables = {'number': 10, 'max_capacity': 10}
        rv = self.client.post(self.BASE_URL + '/restaurants/save/' + str(owner['id']) + '/' + str(restaurant['id']),
            json=tables, follow_redirects=False)
        assert rv.status_code == 302
        
    def test_post_save_time(self):
        owner = self.login_test_operator()
        restaurant = self.create_random_restaurant(owner['id'])
        time = {'day': 'Monday', 'start_time': '10:00', 'end_time': '15:00'}
        rv = self.client.post(self.BASE_URL + '/restaurants/savetime/' + str(owner['id']) + '/' + str(restaurant['id']),
            json=time, follow_redirects=False)
        assert rv.status_code == 302

    def test_post_save_measure(self):
        owner = self.login_test_operator()
        restaurant = self.create_random_restaurant(owner['id'])
        measure = {'measure': 'Monday'}
        rv = self.client.post(self.BASE_URL + '/restaurants/savemeasure/' + str(owner['id']) + '/' + str(restaurant['id']),
            json=measure, follow_redirects=False)
        assert rv.status_code == 302

    def test_post_avg_stay(self):
        owner = self.login_test_operator()
        restaurant = self.create_random_restaurant(owner['id'])
        stay = {'hours': 1, 'minutes': 30}
        rv = self.client.post(self.BASE_URL + '/restaurants/avgstay/' + str(owner['id']) + '/' + str(restaurant['id']),
            json=stay, follow_redirects=False)
        assert rv.status_code == 302
    
    def test_post_edit_restaurant(self):
        owner = self.login_test_operator()
        restaurant = self.create_random_restaurant(owner['id'])
        rv = self.client.post(self.BASE_URL + '/edit_restaurant/' + str(owner['id']) + '/' + str(restaurant['id']),
            json=restaurant, follow_redirects=False)
        assert rv.status_code == 302

    def test_get_edit_restaurant(self):
        owner = self.login_test_operator()
        # restaurant = self.create_random_restaurant(owner['id'])
        rv = self.client.get(self.BASE_URL + '/edit_restaurant/' + str(owner['id']) + '/' + str(0),
            follow_redirects=False)
        assert rv.status_code == 200

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
