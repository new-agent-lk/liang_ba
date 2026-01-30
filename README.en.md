# liang_ba

## Introduction
liang_ba is a comprehensive enterprise content management system built with Django and Wagtail CMS. It combines corporate information display, stock market data analysis, and rich content management capabilities. The platform is designed for enterprises that need both professional content management and financial data visualization.

## Software Architecture
The system adopts a modern layered architecture based on the Django framework with the following core components:
- **Frontend**: HTML/CSS, JavaScript (jQuery, Bootstrap, ECharts)
- **Backend**: Django 4.2.7 with Wagtail 5.2.1 CMS
- **Database**: MySQL with Redis caching
- **API Layer**: Django REST Framework for RESTful APIs
- **Content Management**: Wagtail CMS with custom content pages
- **Security**: JWT authentication and authorization

## Features
- **Corporate Information Display**: Product center, news updates, case studies, recruitment information
- **Stock Market Data Analysis**: Real-time financial data visualization and analytics
- **Dynamic Page Generation**: Powered by Wagtail CMS with content stream functionality
- **Rich Text Editing**: Integrated django-ckeditor for advanced content creation
- **Scheduled Tasks**: Cron job support for automated daily report generation
- **Responsive Design**: Mobile-friendly interface with Bootstrap
- **RESTful API**: Comprehensive API endpoints for frontend applications
- **Admin Panel**: Advanced administration interface with role-based access control

## Installation

### Prerequisites
- Python 3.8+
- MySQL Server
- Redis Server
- Node.js (optional, for screenshot utilities)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/liang_ba.git
   cd liang_ba
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database connection in [base_settings.py](file:///home/kang/workspace/liang_ba/base_settings.py) (database name, username, password)
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'liang_ba',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': '127.0.0.1',
           'PORT': '3306',
       }
   }
   ```

5. Run database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create a superuser account:
   ```bash
   python manage.py createsuperuser
   ```

7. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

8. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage Instructions

1. **Admin Panel**: Access the admin panel at `/admin/` to manage users and content
2. **Wagtail CMS**: Use the Wagtail interface at `/manage/` to create and manage content pages
3. **API Endpoints**: Access REST APIs at `/api/admin/` for programmatic data operations
4. **Public Site**: Visit the main site at `/` to view published content

## Key Components

- **Company Info Module**: Manages company profile, products, news, and recruitment
- **Wagtail Apps**: Custom content pages with dynamic content streams
- **User Management**: Custom user models with extended profiles
- **Job Scheduling**: Automated tasks for daily content generation
- **Media Management**: Rich media handling with CKEditor integration

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## Tech Stack

- **Backend**: Django 4.2.7, Django REST Framework 3.14.0
- **CMS**: Wagtail 5.2.1
- **Database**: MySQL with PyMySQL connector
- **Cache**: Redis with django-redis
- **Frontend**: Bootstrap 5, jQuery, ECharts
- **Authentication**: JWT tokens
- **CORS**: Cross-origin resource sharing support
- **Scheduled Tasks**: django-crontab

## License

This project is licensed under the MIT License - see the LICENSE file for details.