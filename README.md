# APSI-Diploma

Moduł do dyplomowania w ramach uczelni

## Instalacja zależności

```bash
pip3 install -r requirements.txt
```

## Uruchamianie

Aplikację uruchamia się poprzez:

```bash
python3 apsi_diploma/manage.py runserver
```

Do poprawnego wypełnienia bazy danych potrzebne może być jeszcze uruchomienie migracji:

```bash
python3 apsi_diploma/manage.py migrate
```

Aby zainicjalizować użytkowników, grupy oraz uprawnienia należy uruchomić:

```bash
cp ./apsi_diploma/diploma_app/migrations/permission_migration/0002_create_groups.py  ./apsi_diploma/diploma_app/migrations
python3 apsi_diploma/manage.py migrate
rm ./apsi_diploma/diploma_app/migrations/0002_create_groups.py
```
