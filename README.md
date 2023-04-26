# Django Price Tracker

A web application that allows users to track the price of an item on a website and receive an email notification if the price drops to or below a desired price.

## Installation

1. Clone the repository:

```
git clone https://github.com/lobiit/amazon-price-checker
```

2. Install the requirements:

```
cd amazon-price-tracker
pip install -r requirements.txt
```

3. Migrate the database:

```
python manage.py migrate
```
# To run this command daily using a cron job, you need to add a new entry to your system's crontab file. Here are the steps to do this:

Open your system's crontab file in your text editor.
````
$ crontab -e
````
Add the following line to the end of the file, replacing path/to/python with the path to your Python interpreter, and path/to/project with the path to your Django project's root directory:
````
0 0 * * * path/to/python path/to/project/manage.py check_price_daily
````

Save and close the file.
## Usage

1. Start the development server:

```
python manage.py runserver
```

2. Navigate to the URL http://localhost:8000/ in your web browser.

3. Enter the URL of the item you want to track and the desired price.

4. Click the "POST" button.

5. The application will check the price of the item daily and send you an email if the price drops to or below the desired price.

## License

This project is licensed under the MIT License