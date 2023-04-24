# Import the required modules
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from bs4 import BeautifulSoup
import requests
# Import the email modules
from django.core.mail import send_mail
from django.conf import settings


# Define a function to scrape the price from the amazon URL
def get_price(url):
    # Send a request to the URL and get the HTML content
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    # Find the element that contains the price
    price_element = soup.find(id="priceblock_ourprice")
    # Extract the price as a string and remove the currency symbol
    price_string = price_element.text.strip()[1:]
    # Convert the price to a float and return it
    price_float = float(price_string)
    return price_float


# Define a view function for the API endpoint
@api_view(["POST"])
def notify_price(request):
    # Get the data from the request body as a JSON object
    data = request.data
    # Get the amazon URL, the desired price and the user email from the data
    url = data["url"]
    desired_price = data["desired_price"]
    user_email = data["user_email"]
    # Get the current price from the amazon URL using the scraping function
    current_price = get_price(url)
    # Compare the current price and the desired price
    if current_price <= desired_price:
        # If the current price is lower or equal to the desired price, send an email notification to the user
        subject = f"Price Alert: {url}"
        message = f"The price of {url} has dropped to {current_price}. Buy it now!"
        from_email = settings.EMAIL_HOST_USER  # The email address of the sender (configured in settings.py)
        recipient_list = [user_email]  # The email address of the receiver (passed in the request data)
        send_mail(subject, message, from_email, recipient_list)  # Send the email using Django's built-in function
        # Also send a notification message as a JSON response
        message = f"An email notification has been sent to {user_email}."
    else:
        # If the current price is higher than the desired price, send a waiting message as a JSON response
        message = f"The price of {url} is still {current_price}. Wait for it to drop below {desired_price}."
    # Return a JSON response with the message
    return Response({"message": message})
