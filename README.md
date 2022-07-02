# DATA BASE
1. In MySQL: Create database "demo_django"
2. Command: cd demo_django -> create "local_settings.py" file, copy content from local_settings.example.py. Fill your user and password MySQL.

# Django
1. Migrate database and create user: python3 manage.py migrate
2. Create superadmin CMS django: python3 manage.py createsuperuser
Fill your infor superuser
3. Go: localhost:8000/admin and pass admin user have just create to manage content.

# API Docs: https://web.postman.co/documentation/19896346-d4a74868-5db2-4f83-b6e5-1b415fedd480/publish?workspaceId=06ec86c2-3f7e-4b98-8a72-99cba10d6599


# User to login by api:
username: employee
password: DemoDjango123@

username: client
password: DemoDjango123@

username: manager
password: DemoDjango123@