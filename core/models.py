# Import the models module from django.db
from django.db import models


# Define a model class for the price alert
class PriceAlert(models.Model):
    # Define a field for the amazon URL as a URLField
    url = models.URLField(max_length=200)
    # Define a field for the desired price as a DecimalField
    desired_price = models.DecimalField(max_digits=10, decimal_places=2)
    # Define a field for the user email as an EmailField
    user_email = models.EmailField(max_length=100)
    # Define a field for the date and time of creation as a DateTimeField
    created_at = models.DateTimeField(auto_now_add=True)

    # Define a string representation of the model object
    def __str__(self):
        return f"{self.url} - {self.desired_price} - {self.user_email}"
