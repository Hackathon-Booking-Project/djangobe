from django.urls import path
from . import views


urlpatterns = [
    path(
        'planing',
        views.TerminAPI.as_view(),
        name='visitorsTerminAPI'
    ),
]
