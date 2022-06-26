release: sh -c 'python manage.py makemigrations && python manage.py migrate'
web: gunicorn --chdir apsi_diploma apsi_diploma.wsgi
