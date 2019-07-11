from rest_framework import serializers
from persons.models import Person
from authorization.serializers import AuthTokensSerializer


class PersonSerializer(serializers.ModelSerializer):
    tokens = AuthTokensSerializer(many=False)

    class Meta:
        model = Person
        fields = ('tokens', 'firstName', 'secondName', 'thirdName', 'phoneNumber')
