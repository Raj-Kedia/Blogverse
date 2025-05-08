# Blogverse

Blogverse is a modern blog management website built with Django that allows users to create, read, update, and delete blog posts. The platform features a clean and intuitive user interface with support for markdown content.

## Features

- User authentication and authorization
- Create, read, update, and delete blog posts
- Markdown support for rich text formatting
- Comment system for blog posts
- Responsive design for all devices
- Admin dashboard for content management
- Search functionality
- Category-based post organization

## Tech Stack

- **Backend**: Django 4.2.5
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **Markdown Processing**: markdown2
- **Static Files**: WhiteNoise
- **Production Server**: Gunicorn

## Prerequisites

- Python 3.11.11 or higher
- pip (Python package manager)
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/bidur0123/Blogverse.git
cd Blogverse
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Deployment

This project is configured for deployment on Render. The deployment process is automated through the `render.yaml` configuration file.

### Environment Variables

The following environment variables need to be set in your deployment environment:

- `SECRET_KEY`: Django secret key
- `DEBUG`: Set to 'False' in production
- `PYTHON_VERSION`: 3.11.11

## Project Structure

```
Blogverse/
├── blog/                 # Blog application
│   ├── migrations/      # Database migrations
│   ├── templates/       # Blog templates
│   ├── models.py        # Database models
│   ├── views.py         # View logic
│   └── urls.py          # URL routing
├── home/                # Home application
├── static/              # Static files (CSS, JS, images)
├── templates/           # Base templates
├── blogverse/          # Project settings
├── manage.py           # Django management script
├── requirements.txt    # Project dependencies
└── render.yaml         # Render deployment configuration
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

- Raj Kedia
## Acknowledgments

- Django Documentation
- Markdown2 Documentation
- Render Documentation
