from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from bs4 import BeautifulSoup
import requests


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
