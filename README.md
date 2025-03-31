
HRMS - Restaurant & Bar Management System

HRMS (Hospitality Resource Management System) is a web-based POS and management tool designed for restaurants and bars. It helps streamline order processing, inventory tracking, staff management, and shift scheduling.
Features

-Order Management – Handle dine-in, takeout, and online orders seamlessly.
-Inventory Tracking – Monitor stock levels and manage ingredient usage.
=Staff & Shift Management – Assign roles, track attendance, and manage payroll.
=POS System – Process payments and generate invoices in real time.
=HTMX-Powered UI – Dynamic updates without page reloads for a smooth user experience.

Tech Stack

    Backend: Django (Python)

    Frontend: HTML, HTMX (for AJAX-based dynamic updates)

    Authentication: Django’s built-in auth system

Installation

    Clone the repository:

git clone https://github.com/gentitrim/hrms.git
cd hrms

Create a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run migrations and start the server:

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

Access the system at http://127.0.0.1:8000/
