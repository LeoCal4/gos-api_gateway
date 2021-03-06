from random import randint
from unittest.mock import Mock, patch

import requests
from werkzeug.exceptions import HTTPException

from .rao_test import RaoTest


class TestRestaurantManager(RaoTest):

    @classmethod
    def setUpClass(cls):
        super(TestRestaurantManager, cls).setUpClass()
        from gooutsafe.rao.restaurant_manager import RestaurantManager
        cls.restaurant_manager = RestaurantManager
    
    @patch('gooutsafe.rao.restaurant_manager.requests.get')
    def test_get_restaurant_sheet_success(self, mock):
        mock.return_value = Mock(status_code=200, json=lambda : {'restaurant_sheet': {'value': randint(0, 999)}})
        response = self.restaurant_manager.get_restaurant_sheet(randint(0, 999))
        assert 'value' in response

    @patch('gooutsafe.rao.restaurant_manager.requests.get')
    def test_get_restaurant_sheet_fail(self, mock):
        mock.return_value = Mock(status_code=400, json=lambda : {'message': 0})
        response = self.restaurant_manager.get_restaurant_sheet(randint(0, 999))
        assert response is None

    @patch('gooutsafe.rao.restaurant_manager.requests.get')
    def test_get_restaurant_sheet_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400, json=lambda : {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.restaurant_manager.get_restaurant_sheet(randint(0, 999))
            self.assertEqual(http_error.exception.code, 500)

    @patch('gooutsafe.rao.restaurant_manager.requests.put')
    def test_put_toggle_like_success(self, mock):
        mock.return_value = Mock(status_code=200)
        response = self.restaurant_manager.put_toggle_like(randint(0, 999), randint(0, 999))
        assert response == True

    @patch('gooutsafe.rao.restaurant_manager.requests.put')
    def test_put_toggle_like_fail(self, mock):
        mock.return_value = Mock(status_code=404, json=lambda : {'message': 0})
        response = self.restaurant_manager.put_toggle_like(randint(0, 999), randint(0, 999))
        assert response == False

    @patch('gooutsafe.rao.restaurant_manager.requests.put')
    def test_put_toggle_like_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=404, json=lambda : {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.restaurant_manager.put_toggle_like(randint(0, 999), randint(0, 999))
            self.assertEqual(http_error.exception.code, 500)

    @patch('gooutsafe.rao.restaurant_manager.requests.post')
    def test_post_add_success(self, mock):
        name = 'Pizza da Musca'
        address = 'Via Pippa'
        city = 'Pisa'
        phone = '1234567890'
        menu_type = 'Italian'
        data = {
                'name': name,
                'address': address,
                'city': city,
                'phone': phone,
                'menu_type': menu_type,
                'op_id': randint(0, 999)
            }
        mock.return_value = Mock(status_code=200,
            json = lambda :{
                'restaurant_id':1
            })
        response = self.restaurant_manager.post_add(data)
        assert response == True

    @patch('gooutsafe.rao.restaurant_manager.requests.post')
    def test_post_add_fail(self, mock):
        mock.return_value = Mock(status_code=400, json=lambda : {'message': 0})
        response = self.restaurant_manager.post_add({})
        print(response)
        assert response == None

    @patch('gooutsafe.rao.restaurant_manager.requests.post')
    def test_post_add_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400, json=lambda : {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.restaurant_manager.post_add({})
            self.assertEqual(http_error.exception.code, 500)

    @patch('gooutsafe.rao.restaurant_manager.requests.get')
    def test_get_restaurant_by_op_id_success(self, mock):
        mock.return_value = Mock(status_code=200, json=lambda : {'restaurant_sheet': {'restaurant': 0}})
        response = self.restaurant_manager.get_restaurant_by_op_id(randint(0, 999))
        assert 'restaurant' in response

    @patch('gooutsafe.rao.restaurant_manager.requests.get')
    def test_get_restaurant_by_op_id_fail(self, mock):
        mock.return_value = Mock(status_code=404, json=lambda : {'message': 0})
        response = self.restaurant_manager.get_restaurant_by_op_id(randint(0, 999))
        assert response is None

    @patch('gooutsafe.rao.restaurant_manager.requests.get')
    def test_get_restaurant_by_op_id_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=404)
        with self.assertRaises(HTTPException) as http_error:
            self.restaurant_manager.get_restaurant_by_op_id(randint(0, 999))
            self.assertEqual(http_error.exception.code, 500)

    @patch('gooutsafe.rao.restaurant_manager.requests.post')
    def test_post_add_tables_success(self, mock):
        mock.return_value = Mock(status_code=200)
        response = self.restaurant_manager.post_add_tables(randint(0, 999), {})
        assert response == True

    @patch('gooutsafe.rao.restaurant_manager.requests.post')
    def test_post_add_tables_fail(self, mock):
        mock.return_value = Mock(status_code=400, json=lambda : {'message': 0})
        response = self.restaurant_manager.post_add_tables(randint(0, 999), {})
        assert response == False

    @patch('gooutsafe.rao.restaurant_manager.requests.post')
    def test_post_add_tables_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=404)
        with self.assertRaises(HTTPException) as http_error:
            self.restaurant_manager.post_add_tables(randint(0, 999), {})
            self.assertEqual(http_error.exception.code, 500)

    @patch('gooutsafe.rao.restaurant_manager.requests.post')
    def test_post_add_time_success(self, mock):
        mock.return_value = Mock(status_code=200)
        response = self.restaurant_manager.post_add_time(randint(0, 999), {})
        assert response == True

    @patch('gooutsafe.rao.restaurant_manager.requests.post')
    def test_post_add_time_fail(self, mock):
        mock.return_value = Mock(status_code=400, json=lambda : {'message': 0})
        response = self.restaurant_manager.post_add_time(randint(0, 999), {})
        assert response == False

    @patch('gooutsafe.rao.restaurant_manager.requests.post')
    def test_post_add_time_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=404)
        with self.assertRaises(HTTPException) as http_error:
            self.restaurant_manager.post_add_time(randint(0, 999), {})
            self.assertEqual(http_error.exception.code, 500)

    @patch('gooutsafe.rao.restaurant_manager.requests.put')
    def test_put_add_measure_success(self, mock):
        mock.return_value = Mock(status_code=200)
        response = self.restaurant_manager.put_add_measure(randint(0, 999), {})
        assert response == True

    @patch('gooutsafe.rao.restaurant_manager.requests.put')
    def test_put_add_measure_fail(self, mock):
        mock.return_value = Mock(status_code=400, json=lambda : {'message': 0})
        response = self.restaurant_manager.put_add_measure(randint(0, 999), {})
        assert response == False

    @patch('gooutsafe.rao.restaurant_manager.requests.put')
    def test_put_add_measure_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=404)
        with self.assertRaises(HTTPException) as http_error:
            self.restaurant_manager.put_add_measure(randint(0, 999), {})
            self.assertEqual(http_error.exception.code, 500)

    @patch('gooutsafe.rao.restaurant_manager.requests.put')
    def test_put_add_avg_stay_success(self, mock):
        mock.return_value = Mock(status_code=200)
        response = self.restaurant_manager.put_add_avg_stay(randint(0, 999), {})
        assert response == True

    @patch('gooutsafe.rao.restaurant_manager.requests.put')
    def test_put_add_avg_stay_fail(self, mock):
        mock.return_value = Mock(status_code=400, json=lambda : {'message': 0})
        response = self.restaurant_manager.put_add_avg_stay(randint(0, 999), {})
        assert response == False

    @patch('gooutsafe.rao.restaurant_manager.requests.put')
    def test_put_add_avg_stay_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=404)
        with self.assertRaises(HTTPException) as http_error:
            self.restaurant_manager.put_add_avg_stay(randint(0, 999), {})
            self.assertEqual(http_error.exception.code, 500)

    @patch('gooutsafe.rao.restaurant_manager.requests.put')
    def test_put_edit_restaurant_success(self, mock):
        mock.return_value = Mock(status_code=200)
        response = self.restaurant_manager.put_edit_restaurant(randint(0, 999), {})
        assert response == True

    @patch('gooutsafe.rao.restaurant_manager.requests.put')
    def test_put_edit_restaurant_fail(self, mock):
        mock.return_value = Mock(status_code=400, json=lambda : {'message': 0})
        response = self.restaurant_manager.put_edit_restaurant(randint(0, 999), {})
        assert response == False

    @patch('gooutsafe.rao.restaurant_manager.requests.put')
    def test_put_edit_restaurant_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400, json=lambda : {'message': 0})
        with self.assertRaises(HTTPException) as http_error:
            self.restaurant_manager.put_edit_restaurant(randint(0, 999), {})
            self.assertEqual(http_error.exception.code, 500)

    @patch('gooutsafe.rao.restaurant_manager.requests.get')
    def test_get_get_all_success(self, mock):
        mock.return_value = Mock(status_code=200, json=lambda : {'message': 0, 'restaurants': {'restaurant': 0}})
        response = self.restaurant_manager.get_get_all()
        assert 'restaurant' in response

    @patch('gooutsafe.rao.restaurant_manager.requests.get')
    def test_get_get_all_fail(self, mock):
        mock.return_value = Mock(status_code=400, json=lambda : {'message': 0, 'restaurants': {'restaurant': 0}})
        response = self.restaurant_manager.get_get_all()
        assert response is None

    @patch('gooutsafe.rao.restaurant_manager.requests.get')
    def test_get_get_all_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400)
        with self.assertRaises(HTTPException) as http_error:
            self.restaurant_manager.get_get_all()
            self.assertEqual(http_error.exception.code, 500)

    @patch('gooutsafe.rao.restaurant_manager.requests.get')
    def test_get_search_by_success(self, mock):
        mock.return_value = Mock(status_code=200, json=lambda : {'message': 0, 'restaurants': {'restaurant': 0}})
        response = self.restaurant_manager.get_search_by('', '')
        assert 'restaurant' in response

    @patch('gooutsafe.rao.restaurant_manager.requests.get')
    def test_get_search_by_fail(self, mock):
        mock.return_value = Mock(status_code=400, json=lambda : {'message': 0, 'restaurants': {'restaurant': 0}})
        response = self.restaurant_manager.get_search_by('', '')
        assert response is None

    @patch('gooutsafe.rao.restaurant_manager.requests.get')
    def test_get_search_by_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400)
        with self.assertRaises(HTTPException) as http_error:
            self.restaurant_manager.get_search_by('', '')
            self.assertEqual(http_error.exception.code, 500)

    @patch('gooutsafe.rao.restaurant_manager.requests.get')
    def test_get_rating_bounds_success(self, mock):
        mock.return_value = Mock(status_code=200, json=lambda : {'bounds': {'min_value': 0, 'max_value': 0}})
        response = self.restaurant_manager.get_rating_bounds()
        assert 'min_value' in response

    @patch('gooutsafe.rao.restaurant_manager.requests.get')
    def test_get_rating_bounds_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400)
        with self.assertRaises(HTTPException) as http_error:
            self.restaurant_manager.get_rating_bounds()
            self.assertEqual(http_error.exception.code, 500)

    @patch('gooutsafe.rao.restaurant_manager.requests.post')
    def test_post_review_success(self, mock):
        mock.return_value = Mock(status_code=200, json=lambda : {'already_written': True})
        response = self.restaurant_manager.post_review({})
        assert response == (True, True)

    @patch('gooutsafe.rao.restaurant_manager.requests.post')
    def test_post_review_fail(self, mock):
        mock.return_value = Mock(status_code=400, json=lambda : {'message': 0})
        response = self.restaurant_manager.post_review({})
        assert response == (False, None)

    @patch('gooutsafe.rao.restaurant_manager.requests.post')
    def test_post_review_error(self, mock):
        mock.side_effect = requests.exceptions.Timeout()
        mock.return_value = Mock(status_code=400)
        with self.assertRaises(HTTPException) as http_error:
            self.restaurant_manager.post_review({})
            self.assertEqual(http_error.exception.code, 500)
