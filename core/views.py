import requests
from bs4 import BeautifulSoup
import datetime
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .models import PriceAlert
from .serializers import NotifyPriceSerializer


def send_email(subject, messages, from_email, recipient_list):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ', '.join(recipient_list)
    msg['Subject'] = subject
    msg.attach(MIMEText(messages, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, 'YOUR_EMAIL_PASSWORD')
            server.sendmail(from_email, recipient_list, msg.as_string())
            print("Email sent successfully")
    except Exception as e:
        print(str(e))


def get_price(url):
    try:
        headers = {"accept-language": "en-GB,en;q=0.9",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")

        price_element = soup.select_one('span.a-offscreen')

        if price_element is not None:
            price_string = price_element.text.strip()[1:]
            price_float = float(price_string)
            return price_float
        else:
            raise ValueError("Could not find price element")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: {err}")
    except requests.exceptions.Timeout as err:
        print(f"Timeout Error: {err}")
    except requests.exceptions.ConnectionError as err:
        print(f"Connection Error: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Something went wrong: {err}")


def check_price_hourly(url, desired_price, user_email):
    while True:
        current_price = get_price(url)

        if current_price <= desired_price:
            subject = f"Price Alert: {url}"
            message = f"The price of {url} has dropped to {current_price}. Buy it now!"

            from_email = "darchiki80@gmail.com"
            recipient_list = [user_email]

            send_email(subject, message, from_email, recipient_list)

            return f"An email notification has been sent to {user_email}."
        else:
            print(f"The price of {url} is still {current_price}. Wait for it to drop below {desired_price}.")

        time.sleep(3600)


class NotifyPriceView(GenericAPIView):
    serializer_class = NotifyPriceSerializer

    def post(self, request):
        data = request.data
        serializer = self.get_serializer(data=data, context={"request": request})

        if serializer.is_valid():
            url = serializer.validated_data["url"]
            desired_price = serializer.validated_data["desired_price"]
            user_email = serializer.validated_data["user_email"]
            message = check_price_hourly(url, desired_price, user_email)

            price_alert, created = PriceAlert.objects.update_or_create(
                url=url,
                user_email=user_email,
                defaults={"desired_price": desired_price}
            )
            price_alert.save()

            return Response({"message": message})
        else:
            return Response(serializer.errors)
