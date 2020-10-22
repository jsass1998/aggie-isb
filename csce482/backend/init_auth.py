from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers import registry

localhost, created = Site.objects.get_or_create(
    domain = "localhost:8000",
    name = "localhost:8000"
)
localhost.save()

with open('google_client_id.txt', 'r') as client_id_file:
    google_client_id = client_id_file.read().replace('\n', '')

with open('google_client_secret.txt', 'r') as client_secret_file:
    google_client_secret = client_secret_file.read().replace('\n', '')

google_auth_api, created = SocialApp.objects.get_or_create(
    provider = "google",
    name = "Google API",
    client_id = google_client_id,
    secret = google_client_secret
)
google_auth_api.sites.set([localhost])
google_auth_api.save()