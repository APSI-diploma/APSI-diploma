release: sh -c 'python apsi_diploma/manage.py migrate && python apsi_diploma/manage.py migrate apsi_diploma/diploma_app/migrations/permission_migration/0002_create_groups.py'
web: gunicorn --chdir apsi_diploma apsi_diploma.wsgi
