# BackEndProjectFastAPI

1-  cd ./backend/

<!-- Active virtual Enviroment if not created create uisng"python -m venv  . venv"  -->
2-  source ./.venv/bin/activate

3-  pip install -r requirements.txt

4-  uvicorn app:app --reload

This particular Project is designed to understand the fundamentals, constraints, and strengths of using FastAPI as a significant part of a developement project simulating real-world developement . 

Technologies Used ---------------------------------------------------------
FastAPI -- Web Framework for building web server and API. We use FastApi in order to communicate with responses and requests from the frontend/routes. We create a Supplier and Product system that focuses on CRUD operations.

FastApi-Email -- We use FastAPI email to send example emails to supliers and let them get the product and know who it is supplied by

Jinja2 -- To add css templating to routes, I use Jinja2 which will render dynamic HTML content in our fast api routes.

Uvicorn -- With uvicorn in combination with FastApi we are able to run FastApi on a server and take in requests. Allows for high performance, instant code changes, better concurrency, and less resource usage

Tortoise ORM -- Allows for asycnhrononus object relational mapping which will allow us to use python code rather than SQL code to interact with our database. Tortoise works well with asynch/wait allowing for many requests without blocking

---------------------------------------------------------------------------


