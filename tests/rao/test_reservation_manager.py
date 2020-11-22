from random import randint
from unittest.mock import Mock, patch

import requests
from werkzeug.exceptions import HTTPException

from .rao_test import RaoTest


class TestReservationManager(RaoTest):

    @classmethod
    def setUpClass(cls):
        super(TestReservationManager, cls).setUpClass()
        from gooutsafe.rao.reservation_manager import ReservationManager
        cls.reservation_manager = ReservationManager

    @patch('gooutsafe.rao.reservation_manager.requests.post')
    @patch('gooutsafe.rao.reservation_manager.requests.get')
    def test_create_reservation_success(self, mock_get, mock_post):
        mock_get.return_value = Mock(status_code=200, 
                                    json = lambda:{
                                        'restaurant_sheet':{
                                            'restaurant':{
                                                'tables':{},
                                                'availabilities': {},
                                            },
                                        },
                                    })
        mock_post.return_value = Mock(status_code=200)
        restaurant_id = 1
        user_id = 1
        start_time = '2020-11-29 20:00:00'
        people_number = 1
        response = self.reservation_manager.create_reservation(restaurant_id,
                                                                user_id,
                                                                start_time,
                                                                people_number)
        assert response.status_code == 200

    @patch('gooutsafe.rao.reservation_manager.requests.post')
    def test_create_reservation_error(self, mock):
        mock.side_effect = requests.exceptions.ConnectionError()
        mock.return_value = Mock(status_code=200)
        restaurant_id = 1
        user_id = 1
        start_time = '2020-11-29 20:00:00'
        people_number = 1
        with self.assertRaises(HTTPException) as http_error:
            self.reservation_manager.create_reservation(restaurant_id,
                                                                user_id,
                                                                start_time,
                                                                people_number)
            self.assertEqual(http_error.exception.code, 500)
        #TIMEOUT ERROR
        mock.side_effect = requests.exceptions.ConnectTimeout()
        mock.return_value = Mock(status_code=200)
        restaurant_id = 1
        user_id = 1
        start_time = '2020-11-29 20:00:00'
        people_number = 1
        with self.assertRaises(HTTPException) as http_error:
            self.reservation_manager.create_reservation(restaurant_id,
                                                                user_id,
                                                                start_time,
                                                                people_number)
            self.assertEqual(http_error.exception.code, 500)


    @patch('gooutsafe.rao.reservation_manager.requests.get')
    def test_get_all_reservation_restaurant_success(self, mock):
        mock.return_value = Mock(status_code=200)
        restaurant_id = 1
        response = self.reservation_manager.get_all_reservation_restaurant(restaurant_id)
        assert response.status_code == 200
        
    
    @patch('gooutsafe.rao.reservation_manager.requests.get')
    def test_get_all_reservation_restaurant_error(self, mock):
        mock.side_effect = requests.exceptions.ConnectionError()
        mock.return_value = Mock(status_code=200)
        restaurant_id = 1
        with self.assertRaises(HTTPException) as http_error:
            self.reservation_manager.get_all_reservation_restaurant(restaurant_id)
            self.assertEqual(http_error.exception.code, 500)
        

    @patch('gooutsafe.rao.reservation_manager.requests.get')
    def tast_get_all_reservation_customer_success(self, mock):
        mock.return_value = Mock(status_code=200)
        customer_id = 1
        response = self.reservation_manager.get_all_reservation_customer(customer_id)
        assert response.status_code == 200

    @patch('gooutsafe.rao.reservation_manager.requests.get')
    def test_get_all_reservation_customer_error(self, mock):
        mock.side_effect = requests.exceptions.ConnectionError()
        mock.return_value = Mock(status_code=200)
        customer_id = 1
        with self.assertRaises(HTTPException) as http_error:
            self.reservation_manager.get_all_reservation_customer(customer_id)
            self.assertEqual(http_error.exception.code, 500)

    @patch('gooutsafe.rao.reservation_manager.requests.get')
    def tast_get_reservation_success(self, mock):
        mock.return_value = Mock(status_code=200)
        reservation_id = 1
        response = self.reservation_manager.get_reservation(reservation_id)
        assert response.status_code == 200

    @patch('gooutsafe.rao.reservation_manager.requests.get')
    def test_get_reservation_error(self, mock):
        mock.side_effect = requests.exceptions.ConnectionError()
        mock.return_value = Mock(status_code=200)
        reservation_id = 1
        with self.assertRaises(HTTPException) as http_error:
            self.reservation_manager.get_reservation(reservation_id)
            self.assertEqual(http_error.exception.code, 500)

    @patch('gooutsafe.rao.reservation_manager.requests.put')
    @patch('gooutsafe.rao.reservation_manager.requests.get')
    def test_edit_reservation_success(self, mock_get, mock_put):
        mock_get.return_value = Mock(status_code=200, 
                                    json = lambda:{
                                        'restaurant_sheet':{
                                            'restaurant':{
                                                'tables':{},
                                                'availabilities': {},
                                            },
                                        },
                                    })
        mock_put.return_value = Mock(status_code=200)
        reservation_id = 1
        restaurant_id = 1
        start_time = '2020-11-29 20:00:00'
        people_number = 1
        response = self.reservation_manager.edit_reservation(reservation_id,
                                                                restaurant_id,
                                                                start_time,
                                                                people_number)
        assert response.status_code == 200

    @patch('gooutsafe.rao.reservation_manager.requests.get')
    def test_edit_reservation_error(self, mock):
        mock.side_effect = requests.exceptions.ConnectionError()
        mock.return_value = Mock(status_code=200)
        reservation_id = 1
        restaurant_id = 1
        start_time = '2020-11-29 20:00:00'
        people_number = 1
        with self.assertRaises(HTTPException) as http_error:
            self.reservation_manager.edit_reservation(reservation_id,
                                                                restaurant_id,
                                                                start_time,
                                                                people_number)
            self.assertEqual(http_error.exception.code, 500)


    @patch('gooutsafe.rao.reservation_manager.requests.put')
    def test_confirm_reservation_success(self, mock):
        mock.return_value = Mock(status_code=200)
        reservation_id = 1
        response = self.reservation_manager.confirm_reservation(reservation_id)
        assert response.status_code == 200

    @patch('gooutsafe.rao.reservation_manager.requests.put')
    def test_confirm_reservation_error(self, mock):
        mock.side_effect = requests.exceptions.ConnectionError()
        mock.return_value = Mock(status_code=200)
        reservation_id = 1
        with self.assertRaises(HTTPException) as http_error:
            self.reservation_manager.confirm_reservation(reservation_id)
            self.assertEqual(http_error.exception.code, 500)
    
    @patch('gooutsafe.rao.reservation_manager.requests.post')
    def test_filtered_reservations_success(self, mock):
        mock.return_value = Mock(status_code=200)
        restaurant_id = 1
        start_time = '2020-11-29 1:00:00'
        end_time = '2020-11-29 23:00:00'
        response = self.reservation_manager.filtered_reservations(restaurant_id, start_time, end_time)
        assert response.status_code == 200

    @patch('gooutsafe.rao.reservation_manager.requests.post')
    def test_filtered_reservations_error(self, mock):
        mock.side_effect = requests.exceptions.ConnectionError()
        mock.return_value = Mock(status_code=200)
        restaurant_id = 1
        start_time = '2020-11-29 1:00:00'
        end_time = '2020-11-29 23:00:00'
        with self.assertRaises(HTTPException) as http_error:
            self.reservation_manager.filtered_reservations(restaurant_id, start_time, end_time)
            self.assertEqual(http_error.exception.code, 500)

    @patch('gooutsafe.rao.reservation_manager.requests.delete')
    def test_delete_reservation(self, mock):
        mock.return_value = Mock(status_code=200)
        reservation_id = 1
        response = self.reservation_manager.delete_reservation(reservation_id)
        assert response.status_code == 200

    @patch('gooutsafe.rao.reservation_manager.requests.delete')
    def test_confirm_reservation_error(self, mock):
        mock.side_effect = requests.exceptions.ConnectionError()
        mock.return_value = Mock(status_code=200)
        reservation_id = 1
        with self.assertRaises(HTTPException) as http_error:
            self.reservation_manager.delete_reservation(reservation_id)
            self.assertEqual(http_error.exception.code, 500)
    
    @patch('gooutsafe.rao.reservation_manager.requests.get')
    def test_get_restaurant_details(self, mock):
        mock.side_effect = requests.exceptions.ConnectionError()
        mock.return_value = Mock(status_code=200)
        mock.return_value = Mock(status_code=200)
        restaurant_id = 1
        with self.assertRaises(HTTPException) as http_error:
            self.reservation_manager.get_restaurant_detatils(restaurant_id)
            self.assertEqual(http_error.exception.code, 500)