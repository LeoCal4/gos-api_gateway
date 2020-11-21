from unittest.mock import Mock, patch
from .rao_test import RaoTest
import requests
from werkzeug.exceptions import HTTPException

class TestRaoTest(RaoTest):

    def setUp(self):
        super(TestRaoTest, self).setUp()
        from gooutsafe.rao.restaurant_manager import RestaurantManager
        self.restaurant_manager = RestaurantManager

    # test using unittest.mock
    @patch('gooutsafe.rao.restaurant_manager.requests.get')
    def test_get_rating_bounds(self, mock_get):
        mock_get.return_value = Mock(status_code=200, json=lambda : {'bounds': {'min_value': 4, 'max_value': 5}})
        response = self.restaurant_manager.get_rating_bounds()
        assert response is not None
        assert response['min_value'] == 4

    # test using unittest.mock
    def test_get_rating_bounds2(self):
        with self.assertRaises(HTTPException) as http_error:
            self.restaurant_manager.get_rating_bounds()
            self.assertEqual(http_error.exception.code, 500)
