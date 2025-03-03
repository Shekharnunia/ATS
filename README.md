# Candidate Tracking System (ATS)

This project implements a Candidate Tracking System (ATS) using Django REST Framework (DRF). It provides API endpoints for managing candidate information and performing search operations.


### Directory structure
``` 
.
├── ./ats
│   ├── ./ats/__init__.py
│   ├── ./ats/asgi.py
│   ├── ./ats/settings.py
│   ├── ./ats/urls.py
│   └── ./ats/wsgi.py
├── ./candidates
│   ├── ./candidates/__init__.py
│   ├── ./candidates/admin.py
│   ├── ./candidates/api
│   │   ├── ./candidates/api/v1
│   │   │   ├── ./candidates/api/v1/serializers.py
│   │   │   ├── ./candidates/api/v1/urls.py
│   │   │   └── ./candidates/api/v1/views.py
│   │   └── ./candidates/api/v2
│   │       ├── ./candidates/api/v2/filters.py
│   │       ├── ./candidates/api/v2/serializers.py
│   │       ├── ./candidates/api/v2/services.py
│   │       ├── ./candidates/api/v2/urls.py
│   │       └── ./candidates/api/v2/views.py
│   ├── ./candidates/apps.py
│   ├── ./candidates/migrations
│   │   ├── ./candidates/migrations/0001_initial.py
│   │   ├── ./candidates/migrations/0002_alter_candidate_gender.py
│   │   ├── ./candidates/migrations/0003_auto_20250303_1307.py
│   │   ├── ./candidates/migrations/0004_auto_20250303_1336.py
│   │   ├── ./candidates/migrations/0005_candidate_candidates__name_1a7d0c_gin.py
│   │   └── ./candidates/migrations/__init__.py
│   ├── ./candidates/models.py
│   ├── ./candidates/tests.py
│   └── ./candidates/urls.py
└── ./manage.py
```


## Features

* **Candidate Management:**
    * Create, retrieve, update, and delete candidate records.
    * Stores candidate information: Name, Age (calculated), Gender, Email, and Phone Number.
* **Search Functionality:**
    * Search candidates by name.
    * Results are sorted by relevancy, defined as the number of matching words between the search query and the candidate's name.
    * ORM based search, for improved efficiency.
* **API Versioning:**
    * Implemented API versioning (v1 and v2) for future extensibility.
* **Age Calculation:**
    * Age is automatically calculated from the candidate's date of birth.
* **Database Indexing:**
    * A GinIndex is used on the candidate's name field for efficient relevancy ordering.
* **DRF Utilization:**
    * Extensive use of DRF's generics, serializers, and filtering.

## Getting Started

### Prerequisites

* Python 3.x
* pip
* PostgreSQL

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <your_repository_url>
    cd <your_repository_directory>
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure the database:**

    * Create a PostgreSQL database.
    * Update the `ats/settings.py` file with your database credentials.

5.  **Run migrations:**

    ```bash
    python manage.py migrate
    ```

6.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

### Usage

The API endpoints are available at:

* `candidates/v1/`: Version 1 API
* `candidates/v2/`: Version 2 API

**API Endpoints:**

* **List/Create Candidates:**
    * `GET /candidates/v1/` or `GET /candidates/v2/`
    * `POST /candidates/v1/` or `POST /candidates/v2/`
* **Retrieve/Update/Delete Candidate:**
    * `GET /candidates/v1/<id>/` or `GET /candidates/v2/<id>/`
    * `PUT /candidates/v1/<id>/` or `PUT /candidates/v2/<id>/`
    * `PATCH /candidates/v1/<id>/` or `PATCH /candidates/v2/<id>/`
    * `DELETE /candidates/v1/<id>/` or `DELETE /candidates/v2/<id>/`
* **Search Candidates:**
    * `GET /candidates/v1/search/?q=<search_query>` or `GET /candidates/v2/search/?q=<search_query>`

**Example Search Query:**

* `GET /candidates/v1/search/?q=Ajay Kumar Yadav`
