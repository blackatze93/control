## Access control
1. Clone app from github with `git clone https://github.com/blackatze93/control.git`
2. Build Docker image with `docker build  .`
3. Run `docker-compose up`
4. Create superuser with `docker-compose run web python manage.py createsuperuser`
5. Load migrations with `python manage.py migrate`
6. Load site in browser with `http://localhost:8000/admin`