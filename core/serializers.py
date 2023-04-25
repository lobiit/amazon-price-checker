# Import the serializers module from rest_framework
from django.db.migrations import serializer
from rest_framework import serializers


# Define a serializer class for the notify price api
class NotifyPriceSerializer(serializers.Serializer):
    # Define a field for the amazon URL as a URLField with a label
    url = serializers.URLField(max_length=500, required=True, label="Amazon URL")
    # Define a field for the desired price as a DecimalField with a label
    desired_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True, label="Desired Price")
    # Define a field for the user email as an EmailField with a label
    user_email = serializers.EmailField(max_length=100, required=True, label="User Email")


