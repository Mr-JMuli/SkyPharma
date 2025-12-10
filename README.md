# Skypharma - Online Pharmacy

A full-featured online pharmacy web application built with Django and Bootstrap 5.

## Features

- **User Authentication**: Registration, login, password reset
- **Medicine Catalog**: Browse medicines by category, search functionality
- **Shopping Cart**: Add/remove items, update quantities
- **Checkout & Orders**: Place orders, view order history
- **Order Tracking**: Track delivery status with progress visualization
- **Prescription Refill Reminders**: Set and manage medication reminders
- **Admin Dashboard**: Manage medicines, orders, and users

## Tech Stack

- **Backend**: Django 5.x
- **Frontend**: Bootstrap 5, Bootstrap Icons
- **Database**: SQLite
- **Image Handling**: Pillow

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install django pillow
   ```

2. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Seed the database** (creates admin user and sample data):
   ```bash
   python manage.py seed_data
   ```

4. **Run the development server**:
   ```bash
   python manage.py runserver 0.0.0.0:5000
   ```

5. **Access the application**:
   - Main site: http://localhost:5000
   - Admin login: username=`admin`, password=`admin123`

## Admin Features

- Dashboard with statistics (users, orders, sales)
- Manage medicines (add, edit, delete)
- Update order status (Pending → Confirmed → Shipped → Delivered)
- View all users

## Project Structure

```
skypharma_project/     # Django project settings
pharmacy/              # Main application
  models.py            # Database models
  views.py             # View functions
  forms.py             # Form definitions
  urls.py              # URL routing
  admin.py             # Django admin config
  management/commands/ # Custom management commands
templates/             # HTML templates
  base.html            # Base template
  pharmacy/            # App templates
  registration/        # Auth templates
static/css/            # Custom CSS styles
media/                 # Uploaded files
```

## Default Admin Credentials

- **Username**: admin
- **Password**: admin123

*Remember to change these in production!*
