# IO_Organizer
Project_on_IO_lessons

# Hot to run project

1. Install docker on your desktop 
2. Run command:  docker run --name postgres_ts -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=1458 -p 5432:5432 -d postgres 
(if postgres install on your computer, your should stop postgres before run this command)
3. Download lasted project version from GitHub
4. Go to the directory ~/IO_Oganizer (next all commands run in this directory)
5. Activate python environment ts_agh : ts_agh/bin/activate
6. Create django migrations: python task_manager/manage.py makemigrations
7. Run migrations: python task_manager/manage.py migrate
8. Start django project: python task_manager/manage.py runserver
9. Enjoy

# Helpful links:
https://docs.docker.com/engine/install/
https://www.baeldung.com/ops/postgresql-docker-setup
https://techvidvan.com/tutorials/django-project-structure-layout/
https://dev.to/kachiic/how-to-clone-a-django-project-from-github-and-run-it-locally-mac-ios-2o4k

