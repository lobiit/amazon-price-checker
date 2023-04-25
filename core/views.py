# Import the required modules
import requests
from bs4 import BeautifulSoup

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import PriceAlert
from .serializers import NotifyPriceSerializer
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(subject, message, from_email, recipient_list):
    message = Mail(
        from_email=from_email,
        to_emails=recipient_list,
        subject=subject,
        html_content=message)
    try:
        sg = SendGridAPIClient('SENDGRID_API_KEY')
        response = sg.send(message)
    except Exception as e:
        print(e.message)


def get_price(url):
    try:
        # Send a request to the URL and get the HTML content
        headers = {"accept-language": "en-GB,en;q=0.9",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")

        # Find the element that contains the price
        price_element = soup.select_one('span.a-offscreen')
        print(price_element)

        if price_element is not None:
            # Extract the price as a string and remove the currency symbol
            price_string = price_element.text.strip()[1:]

            # Convert the price to a float and return it
            price_float = float(price_string)
            print("found price")
            return price_float
        else:
            # Handle the case where price_element is None
            # For example, raise an exception or return a default value
            print("could not find price element")
            raise ValueError("Could not find price element")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
    except requests.exceptions.Timeout as err:
        print(f"Timeout Error: {err}")
    except requests.exceptions.ConnectionError as err:
        print(f"Connection Error: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Something went wrong: {err}")


# Define a view class for the API endpoint that inherits from GenericAPIView
class NotifyPriceView(GenericAPIView):
    # Specify the serializer class for the view
    serializer_class = NotifyPriceSerializer

    # Override the post method to handle post requests
    def post(self, request):
        # Get the data from the request body as a JSON object
        data = request.data
        # Create an instance of the serializer with the data and pass in the context with the request object
        serializer = self.get_serializer(data=data, context={"request": request})
        # Validate the data using the serializer
        if serializer.is_valid():
            # Get the amazon URL, the desired price, the user email and the content from the validated data
            url = serializer.validated_data["url"]
            desired_price = serializer.validated_data["desired_price"]
            user_email = serializer.validated_data["user_email"]
            # Try to get the current price from the amazon URL using the scraping function
            try:
                current_price = get_price(url)
                # print(current_price)
                # Compare the current price and the desired price
                if current_price <= desired_price:
                    # If the current price is lower or equal to the desired price, send an email notification to the
                    # user using django mail
                    subject = f"Price Alert: {url}"
                    message = f"The price of {url} has dropped to {current_price}. Buy it now!"

                    # The email address of the sender (configured in settings.py)
                    from_email = "darchiki80@gmail.com"

                    # The email address of the receiver (passed in the request data)
                    recipient_list = [user_email]

                    # Send the email using SendGrid
                    send_email(subject, message, from_email, recipient_list)

                    # Also send a notification message as a JSON response
                    message = f"An email notification has been sent to {user_email}."
                else:
                    # If the current price is higher than the desired price, send a waiting message as a JSON response
                    message = f"The price of {url} is still {current_price}. Wait for it to drop below {desired_price}."
                # Create or update a PriceAlert object with the validated data and save it to the database
                price_alert, created = PriceAlert.objects.update_or_create(
                    url=url,
                    user_email=user_email,
                    defaults={"desired_price": desired_price}
                )
                price_alert.save()
            except ValueError:
                # If there was a ValueError exception raised by get_price, send an error message as a JSON response
                message = f"Could not find price element for {url}. Please make sure it is a valid amazon product page."
            # Return a JSON response with the message
            return Response({"message": message})
        else:
            # If the data is not valid, return a JSON response with the errors from the serializer
            return Response(serializer.errors)
