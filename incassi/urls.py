from django.urls import path
from . import views
from .views import (
    IncassoList, IncassoCreate, IncassoUpdate,
    delete_image, delete_dettaglio, delete_incasso, HomeView
)

app_name = 'incassi'

urlpatterns = [
    #path("", views.HomeView.as_view(), name="homepage"),
    path("", views.HomeView, name="homepage"),
    path('incassi/lista/', IncassoList.as_view(), name='list_incassi'),
    path('incassi/crea/', IncassoCreate.as_view(), name='crea_incasso'),
    path('incassi/update/<int:pk>/', IncassoUpdate.as_view(), name='update_incasso'),
    path('delete-image/<int:pk>/', delete_image, name='delete_image'),
    path('delete-dettaglio/<int:pk>/', delete_dettaglio, name='delete_dettaglio'),
    path('delete-incasso/<int:pk>/', delete_incasso, name='delete_incasso'),
]