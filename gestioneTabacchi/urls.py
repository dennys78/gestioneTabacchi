from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('incassi.urls', namespace="incassi")),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include("django.contrib.auth.urls"))
]

