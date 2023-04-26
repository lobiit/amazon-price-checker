# Price Tracker

This is a Python program that tracks the price of a product on Amazon and sends an email notification if the price drops below a certain threshold. It uses the BeautifulSoup library to scrape the webpage for the current price and compares it to the desired price.

## Installation

To use this program, you will need to have Python 3.x installed on your system. You can download the latest version of Python from the official website: https://www.python.org/downloads/

You will also need to install the following third-party libraries:

- requests
- BeautifulSoup
- smtplib

You can install these libraries using the following command:

```bash
pip install requests beautifulsoup4 secure-smtplib
```

## Usage

To use this program, you will need to provide the URL of the product page on Amazon and the desired price threshold. You can do this by editing the `URL` and `DESIRED_PRICE` variables in the `price_tracker.py` file.

Once you have set the URL and desired price, you can run the program using the following command:

```bash
python price_tracker.py
```

The program will check the price of the product and send an email notification if the price drops below the desired threshold.

You can also set up a cron job to run the program automatically on a daily basis. To do this, open your crontab file by running the following command:

```bash
crontab -e
```

Then add the following line to the file:

```bash
0 0 * * * /usr/bin/python /path/to/price_tracker.py
```

This will run the program at midnight (0:00) every day.

## License

This program is licensed under the MIT License.