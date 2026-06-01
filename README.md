# Departments Tree Web App

A web application designed to manage company structures, department hierarchies, and employees. This project was developed as a test case for **hitalent**.

The application implements a tree structure for departments (with built-in validation against cyclic dependencies) and covers full CRUD operations for departments and employees.

## Features & Business Logic
- **Department Hierarchy**: Every department can have multiple nested sub-departments.
- **Cycle Prevention**: Includes validation that prevents a department from becoming part of its own hierarchy (a department cannot be its own parent or a child of its own sub-departments).
- **RESTful API**: Full CRUD management for organizational entities.

## Tech Stack
- **Backend Framework:** FastAPI (Python)
- **Data Validation:** Pydantic v2
- **ORM:** SQLAlchemy (Async)
- **Database Migrations:** Alembic
- **Database:** PostgreSQL
- **Containerization:** Docker & Docker Compose

##  Quick Start (Local Run)

### Steps to Run:

1. **Clone the repository:**
   ```bash
   git clone git@github.com:Elias-Wide/fastapi_departments_tree.git
   cd fastapi_departments_tree
   ```

2. **Configure environment variables:**
   Create a `.env` file based on the provided example:
   ```bash
   cp .env.example .env
   ```
3. **Start the application using Docker Compose:**
   ```bash
   docker compose up --build
   ```

The application will automatically run Alembic migrations and start the server.

* **Swagger UI (API Interactive Docs):** http://localhost:8000/docs
* **ReDoc:** http://localhost:8000/redoc

---

## API Specification (Endpoints)

### Departments

| Method | Endpoint | Query Parameters | Description |
| :--- | :--- | :--- | :--- |
| **POST** | `/departments` | _None_ | Create a new department |
| **GET** | `/departments/` | _None__| Get all departments hierarchy |
| **GET** | `/departments/{department_id}` |  `depth` *(int, required)*<br>`include_employees` *(bool, default: true)* | Get department by ID |
| **PATCH** | `/departments/{department_id}` | _None_ | Partially update a department by ID (e.g., change parent) |
| **DELETE** | `/departments/{department_id}` | `mode` *(str("cascade | reassign"), default: "cascade, reassign")*<br>`reassign_to_department_id` *(int, optional)* | Delete department by ID |
| **POST** | `/departments/{department_id}/employees` | _None_ | Add an employee to the specified department |

### Employees

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/employees/` | Get all employees |
| **GET** | `/employees/{employee_id}` | Get employee by ID |

---

##  Project Structure

```text
├── app/                  # Root project directory
│   ├── api/              # API Routing layer
│   │   └── endpoints/
│   │       └─v1/
│   │          ├── departments.py
│   │          ├── employees.py
│   │          └── routers.py
│   ├── core/                    # App configuration & logging
│   │   ├── exceptions/          # Centralized exception handling
│   │   │   ├── api/             # API layer exceptions (4xx, validation)
│   │   │   ├── database/        # DB layer errors (Not Found, Integrity)
│   │   │   ├── services/        # Business logic exceptions (cycling, etc.)
│   │   │   ├── handler.py       # FastAPI exception handlers (global catch)
│   │   │   └── mapper.py
│   │   ├── constants/    # Business logic constants
│   │   ├── logging.py 
│   ├── db/               # Database connection and session management
│   │   ├── database.py
│   │   └── manager.py
│   ├── dependencies/     # FastAPI Dependency Injection (DI)
│   │   ├── db_manager.py
│   │   └── departments.py
│   ├── migrations/       # Alembic database migrations
│   │   └── versions/     # Migration history files
│   ├── models/           # SQLAlchemy database models
│   │   ├── departments.py
│   │   └── employees.py
│   ├── repositories/     # Data Access Layer (SQLAlchemy CRUD operations)
│   │   ├── base.py
│   │   ├── departments.py
│   │   └── employees.py
│   ├── schemas/          # Pydantic data validation schemas
│   │   ├── departments.py
│   │   └── employees.py
│   ├── services/         # Core business logic
│   │   ├── base.py
│   │   ├── departments.py
│   │   └── employees.py
│   ├── tests/            # Pytest test suite
│   │   ├── fixtures/     # Test database fixtures
│   │   └── conftest.py
│   ├── config.py         # Environment variables configuration
│   ├── conftest.py       # Global pytest configurations
│   ├── Dockerfile        # Docker container configuration
│   └── main.py           # FastAPI application entrypoint

```
