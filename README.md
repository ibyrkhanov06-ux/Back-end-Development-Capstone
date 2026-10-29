# Back-end-Development-Capstone

Djirection is a Django band website built from the IBM Skills Network
sfvih-Back-end-Development-Capstone starter template, integrated with Flask Songs
and Pictures services. Implementation assistance: OpenAI Codex.

## Environment setup and run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SONGS_URL=http://127.0.0.1:5001
export PICTURES_URL=http://127.0.0.1:5000
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

Choose your own administrator username and password when prompted; credentials
are never committed. Visit `/admin/` and log in with that superuser. Under
Concerts, select Add and enter the concert name, duration in hours, city and date,
then Save. The demonstration deployment contains Djirection Live in Astana.

## Application usage

- Home `/` shows the band description and navigation.
- Songs `/songs/` retrieves song titles from the Songs API. Click a title to open
  its Lyrics modal, then close the modal to return to the list.
- Photos `/photos/` retrieves photo cards with event dates and locations.
- Sign up `/signup/` creates a website user; `/login/` signs in and `/logout/` signs out.
- Concerts `/concerts/` requires login. Open a concert using the edit icon to
  inspect its details and record attendance.
- Django Admin `/admin/login/` provides the administration login form.

## Deployment and verification

Python 3.12 and Django 5.2.7 are used for the main application. Migrations completed
successfully and all three application-flow tests passed. The Docker image was
built and pushed to IBM Container Registry, then deployed as `djangoserver` on
OpenShift using `kubectl apply -f deployment.yml`. Gunicorn serves port 8000 and
WhiteNoise serves collected static assets. Songs uses the internal service URL
`http://songs:8080`; Pictures runs on IBM Code Engine.

Configure DJANGO_SECRET_KEY, DJANGO_DEBUG=0, DJANGO_ALLOWED_HOSTS and the two
service URLs before deploying. The lab uses an ephemeral SQLite volume: a rollout
recreates its database, so create the administrator and demonstration concert
after rollout. For durable deployments replace this with persistent storage.
