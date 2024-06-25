## Django Job Finder
Django Job Finder is a web application designed to aggregate job listings from various RSS feeds and allow users to search and filter these jobs based on specific criteria.

## Features
- Job Search: Users can search for jobs using keywords, company names, locations, and date ranges.
- RSS Feed Integration: Users can add RSS feeds of job listings, which are then parsed and stored in the database.
- Job Listings: Display a list of job listings fetched from RSS feeds with details like title, company, location, description, and publication date.
- Responsive Design: The application is designed to be responsive and work seamlessly on both desktop and mobile devices.
## Installation
To run this project locally, follow these steps:

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

Open your web browser and go to http://localhost:8000 to view the application.

Usage
Job Search:

## Navigate to the job search page (/job-search/).
Enter search criteria such as keywords, company names, locations, and date ranges to find matching job listings.
Add New RSS Feed:

## Navigate to the new feed page (/new-feed/).
Enter the title, site name, and URL of the RSS feed you want to add.
Submit the form to add the RSS feed. Jobs from this feed will be parsed and displayed in the application.
Contributing
Contributions are welcome! Here's how you can contribute to the project:

## Fork the repository on GitHub.
Clone your forked repository locally.
Create a new branch for your feature or bug fix.
Make your changes and commit them with descriptive commit messages.
Push your changes to your fork on GitHub.
Submit a pull request to the master branch of the original repository.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Adjust the sections and content as per your project's specific features and requirements. Make sure to replace placeholders like https://github.com/criscandia/DjangoJobfinder.git with the actual URL of your GitHub repository and provide accurate instructions for installation and usage.
