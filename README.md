## Django Job Finder
Django Job Finder is a web application designed to aggregate job listings from various RSS feeds and allow users to search and filter these jobs based on specific criteria.

## Features
- Job Search: Users can search for jobs using keywords, company names, locations, and date ranges.
- RSS Feed Integration: Users can add RSS feeds of job listings, which are then parsed and stored in the database.
- Job Listings: Display a list of job listings fetched from RSS feeds with details like title, company, location, description, and publication date.
- Responsive Design: The application is designed to be responsive and work seamlessly on both desktop and mobile devices.
- Automatic RSS Feed Updates: The system fetches and updates RSS feeds from multiple sources periodically.
- Efficient Asynchronous Task Handling: Thanks to Celery, update tasks are performed asynchronously, improving the system's performance and scalability.
- Support for Published Dates: Parses and converts article published dates to a unified format, taking time zones into account.
## Installation
To run this project locally, follow these steps:

## Requirements
Python 3.6+
Django
Celery
RabbitMQ or Redis (as a message broker for Celery)

## Clone the Repository:

bash
Copiar código
git clone https://github.com/criscandia/DjangoJobfinder.git
cd DjangoJobfinder
Set Up Virtual Environment:

bash
Copiar código
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install Dependencies:

bash
Copiar código
pip install -r requirements.txt
Apply Migrations:

bash
Copiar código
python manage.py migrate
Run the Development Server:

bash
Copiar código
python manage.py runserver
Access the Application:
Start the Celery worker:
- celery -A your_project worker --loglevel=info
(Optional) Start Celery Beat for periodic tasks:
- celery -A your_project beat --loglevel=info

Open your web browser and go to http://localhost:8000 to view the application.

Usage
Job Search:
Once set up, the system will begin updating RSS feeds based on the Celery Beat configuration or when the update_rss_feeds task is manually invoked.


## Navigate to the job search page (/job-search/).
Enter search criteria such as keywords, company names, locations, and date ranges to find matching job listings.
Add New RSS Feed:

## Navigate to the new feed page (/new-feed/).
Enter the title, site name, and URL of the RSS feed you want to add.
Submit the form to add the RSS feed. Jobs from this feed will be parsed and displayed in the application.
## Contributing
If you wish to contribute to the project, please follow these steps:

## Fork the repository.
Create a feature branch (git checkout -b feature/myNewFeature).
Make your changes and commit them (git commit -am 'Add some feature').
Push to the branch (git push origin feature/myNewFeature).
Open a Pull Request.

License
This project is licensed under the MIT License - see the LICENSE file for details.


