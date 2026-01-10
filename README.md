# BackEndProjectFastAPI

1-  cd ./backend/

<!-- Active virtual Enviroment if not created create uisng"python -m venv  . venv"  -->

2-  source ./.venv/bin/activate

3-  pip install -r requirements.txt

4-  uvicorn app:app --reload

This particular Project is designed to understand the fundamentals, constraints, and strengths of using FastAPI as a significant part of a developement project simulating real-world developement. 

Technologies Used ======================================================

FastAPI – A modern, high-performance web framework used to build RESTful APIs and handle communication between the backend and frontend. The project implements a Supplier and Product management system with full CRUD functionality.

FastAPI-Mail – Used to send automated emails to suppliers, providing product details and supplier information.

Jinja2 – Used for server-side HTML rendering and CSS templating, enabling dynamic pages within FastAPI routes.

Uvicorn – An ASGI server used to run the FastAPI application, providing high performance, async concurrency, and hot-reloading during development.

Tortoise ORM – An asynchronous ORM that enables database interactions using Python models instead of raw SQL, fully leveraging async/await for non-blocking request handling

Technologies Used ======================================================
