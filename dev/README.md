# Lanify Backend Documentation

## Environment Setup

### Requirements

- Python 3.9+
- Virtual environment (optional but recommended)

### Installation

1. Ensure you are in the codebase directory (`dev/`).

1. Create and activate a virtual environment:

   #### Using venv

   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

   #### Using conda

    ```bash
    conda create --name lanify python=3.9
    conda activate lanify
    ```

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

1. Apply database migrations:

   ```bash
   flask db upgrade
   ```

---

## Running the Application

```bash
python app.py
```

By default, the application runs at [http://localhost:8080/](http://localhost:8080/).

To access the API documentation, visit [http://localhost:8080/swagger-ui](http://localhost:8080/swagger-ui).

---

## Project Structure

```
dev/
│── app.py                 # Entry point of the application
│── config.py              # Configuration settings
│── extensions.py          # Flask extensions (DB, API, etc.)
│── data/                  # Initial data for the database
│── migrations/            # Database migration files
│── models/                # Database models
│── service/               # Business logic layer
```

---

## Database Management with Flask-Migrate

Before running any commands below, make sure you are in the root directory of the codebase (`dev/`).

### Create a Migration File

Whenever you add, delete or update a model:

```bash
flask db migrate -m "Describe changes"
```

### Apply Migrations (Upgrade Database Schema)

Run the following command to apply all migrations:

```bash
flask db upgrade
```

> **Note:** It is important to run `flask db upgrade` after pulling changes from the repository to ensure that the
> database schema is up-to-date.

### Rollback to Previous State

If needed, revert to the previous migration:

```bash
flask db downgrade
```

### Check Current Migration Status

```bash
flask db current
```

### View All Migration History

```bash
flask db history
```

---

## Updating or Adding a Model

1. Modify or add a new model in `models/`
2. Run:
   ```bash
   flask db migrate -m "Added new model or updated fields"
   flask db upgrade
   ```
