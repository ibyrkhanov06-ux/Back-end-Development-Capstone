# Back-end-Development-Capstone

Django band website with signup/login/logout, concerts and attendance, Songs and Photos pages integrated with the Flask APIs.

Run python manage.py migrate and python manage.py runserver. Configure SONGS_URL and PICTURES_URL (defaults localhost ports 5001 and 5000).

Local verification: migrations succeeded; three application-flow tests passed. Dockerfile is supplied but Docker build and cloud deployment have not yet been verified. For deployment set DJANGO_SECRET_KEY, DJANGO_DEBUG=0 and DJANGO_ALLOWED_HOSTS, and run migrations before starting gunicorn.

Based on the IBM Skills Network starter template. Implementation assistance: OpenAI Codex. Cloud deployment evidence is not yet available.
