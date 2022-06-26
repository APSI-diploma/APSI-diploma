release: sh -c 'python apsi_diploma/manage.py makemigrations && python apsi_diploma/manage.py migrate'
web: gunicorn --chdir apsi_diploma apsi_diploma.wsgi
