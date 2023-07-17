
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage




urlpatterns = [
    path('', include("app.urls")),
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon/favicon.ico'))),

]
