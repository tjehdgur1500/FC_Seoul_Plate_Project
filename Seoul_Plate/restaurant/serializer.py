from rest_framework import serializers
from restaurant.models import Restaurant
from review.serializers import ReviewSerializer


class RestSerializer(serializers.ModelSerializer):
    """ 식당 정보, 북마크 수 Serializer """
    # read-only-fields: https://www.django-rest-framework.org/api-guide/serializers/#specifying-read-only-fields

    class Meta:
        model = Restaurant
        fields = (
            'id',
            'rest_name',
            'rest_star',
            'rest_address',
            'rest_phone_number',
            'rest_food',
            'rest_sale',
            'rest_time',
            'rest_break_time',
            'rest_count',
        )
        read_only_fields = ['rest_count']


class RestDetailSerializer(serializers.ModelSerializer):
    """ restaurant detail show review Serializer """
    owner_rest = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = (
            'id',
            'rest_name',
            'rest_star',
            'rest_address',
            'rest_phone_number',
            'rest_food',
            'rest_sale',
            'rest_time',
            'rest_break_time',
            'rest_count',
            'owner_rest',
        )
        read_only_fields = ['rest_count']
