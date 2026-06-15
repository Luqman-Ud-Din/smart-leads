# smart-leads

A Python and Django application for collecting Upwork job listings, storing them in a database, and exposing reporting APIs for skill and search-term trends.

## Overview

`smart-leads` ingests Upwork job data from RSS feeds, stores job, skill, and search-term relationships, and provides API endpoints for reporting on publishing activity over time.

The project includes:

- a Django 4.2 application structure
- scheduled job ingestion from Upwork RSS feeds
- models for jobs, skills, and search terms
- budget parsing and job budget update commands
- reporting endpoints built with Django REST Framework
- Swagger and ReDoc API documentation via `drf-yasg`

## Features

- Fetch Upwork job listings using configured search terms
- Store jobs with associated skills and search terms
- Parse and persist budget information from job descriptions
- Generate hourly job publication reports
- Report by overall jobs, skills, and search terms
- Browse and test APIs through Swagger and ReDoc

## Repository structure

```text
.
├── configurations/        # Django project configuration
├── job_reports/           # Reporting API and reporting utilities
├── jobs/                  # Job models, admin, and management commands
├── search_terms/          # Search term models and admin
├── services/              # Supporting service modules
├── skills/                # Skill models and admin
├── fetch_upwork_jobs.bat  # Windows helper script for scheduled execution
├── manage.py
├── requirements.txt
├── LICENSE
└── README.md
```

## Tech stack

- Python
- Django 4.2.13
- Django REST Framework
- drf-yasg
- Microsoft SQL Server via `mssql-django`
- `django-crontab`
- `feedparser`

## Requirements

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

Primary runtime dependencies include:

- Django 4.2.13
- djangorestframework 3.15.2
- drf-yasg 1.21.7
- mssql-django 1.5
- django-crontab 0.7.1
- feedparser 6.0.11

## Getting started

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Configure the database and application settings.
5. Apply migrations.
6. Create any required search terms in the admin or database.
7. Run the development server.

Example setup:

```bash
git clone <your-fork-or-repo-url>
cd smart-leads
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Configuration

Project settings live in `configurations/settings.py`.

### Database

The repository is currently configured to use Microsoft SQL Server through `mssql-django`.

Important: the committed settings file currently contains development database values and other sensitive configuration. Before deploying or sharing this project, move secrets and environment-specific settings to environment variables or a local, untracked settings file.

Typical configuration areas to review:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `DATABASES`
- `UPWORK_RSS_FEED_URL_T`
- timezone and reporting configuration

### Scheduled jobs

A cron configuration is defined to run the Upwork fetch command every 5 minutes:

```python
CRONJOBS = [
    ('*/5 * * * *', 'django.core.management.call_command', ['fetch_upwork_jobs'])
]
```

A Windows batch helper script, `fetch_upwork_jobs.bat`, is also included for local or Task Scheduler-based execution.

## Data model summary

The core entities include:

- `Job`
  - stores job ID, URL, published date, description, and budget information
- `Skill`
  - stores normalized skill names
- `SearchTerm`
  - stores configured search phrases used to query Upwork feeds
- `JobSkill`
  - join model between jobs and skills
- `JobSearchTerm`
  - join model between jobs and search terms

## Management commands

### Fetch Upwork jobs

Fetches job listings from Upwork RSS feeds for all configured search terms:

```bash
python manage.py fetch_upwork_jobs
```

### Update job budgets

Parses stored job descriptions and updates missing or outdated budget fields:

```bash
python manage.py update_jobs_budget
```

## API documentation

The project exposes reporting APIs and provides interactive documentation.

Available documentation routes:

- `/swagger/`
- `/redoc/`
- `/swagger.json`

The configured API prefix is:

```text
/api/v1
```

## Reporting endpoints

Based on the current URL configuration, reporting endpoints are exposed under:

```text
/api/v1/job_reports/
```

The `job_reports/api/v1` module currently includes endpoints for:

- jobs published per hour
- jobs published by skills per hour
- jobs published by search terms per hour

Most report endpoints support `start_date` and `end_date` query parameters in `YYYY-MM-DD` format.

## Running the project locally

Start the development server:

```bash
python manage.py runserver
```

Create a superuser if you want admin access:

```bash
python manage.py createsuperuser
```

Then visit:

- `/admin/`
- `/swagger/`
- `/redoc/`

## Notes

- The project appears to be designed for analytics around Upwork demand and skill trends.
- Reporting logic converts database timestamps from UTC to configured reporting time zones.
- The repository includes a GPL-3.0 license.
- The current README was minimal; this version expands it to better match common community expectations.

## Security considerations

Before using this project in production, consider addressing the following:

- move secrets out of source control
- rotate any exposed tokens or credentials
- set `DEBUG = False`
- review host restrictions and deployment settings
- verify that third-party feed access complies with platform terms of use

## Contributing

Contributions are welcome. A typical contribution flow is:

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Run checks and test locally.
5. Open a pull request with a clear description.

## License

This project is licensed under the **GNU General Public License v3.0**. See the `LICENSE` file for details.
