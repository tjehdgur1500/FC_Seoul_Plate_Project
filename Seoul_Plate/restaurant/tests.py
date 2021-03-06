from django.test import TestCase
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APITestCase

from restaurant.models import Restaurant


class RestaurantTestCase(APITestCase):
    def setUp(self) -> None:
        # Restaurant.objects.create(rest_name='test_title', rest_star=4.5, rest_address='address')
        # self.query_set = Restaurant.objects.all()
        self.restaurant_size = 3
        self.test_restaurant = baker.make('restaurant.Restaurant', _quantity=self.restaurant_size, rest_name='test',
                                          rest_star=4.5, rest_address='address')

    def test_should_list_restaurant(self):
        """
        Request : GET - /api/restaurant/
        """
        response = self.client.get('/api/restaurants')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), self.restaurant_size)

        for test_rest, response_rest in zip(self.test_restaurant, response.data['results']):
            self.assertEqual(test_rest.id, response_rest['id'])
            self.assertEqual(test_rest.rest_name, response_rest['rest_name'])
            # serializer 에서 선언한 필드가 정확히 response 되는지 확인 필요

    def test_should_detail_restaurant(self):
        """
        Request : GET - /api/restaurants/{restaurant_id}
        """
        test_restaurant = self.query_set[0]
        response = self.client.get(f'/api/restaurants/{test_restaurant.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(test_restaurant.id, response.data['id'])
        # serializer 에서 선언한 필드가 정확히 response 되는지 확인 필요
