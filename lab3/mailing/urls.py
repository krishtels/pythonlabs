from django.urls import path

from .views import MailingListView, MailingDetailView, MailingCreate


urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('<int:pk>', MailingDetailView.as_view(), name='mailing_detail'),
    path('create/', MailingCreate.as_view(), name='mailing_create'),
]