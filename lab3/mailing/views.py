from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView

from lab3.settings import STUDENT
from mailing.forms import MailingCreateForm
from mailing.models import Mailing
from people.models import User
from .tasks import send_notification


class MailingListView(LoginRequiredMixin, ListView):
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'

    def get_queryset(self):
        queryset = Mailing.objects.filter(from_user=self.request.user)
        return queryset


class MailingDetailView(LoginRequiredMixin, DetailView):
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'
    queryset = Mailing.objects.all()


class MailingCreate(LoginRequiredMixin, CreateView):
    queryset = Mailing.objects.all()
    template_name = 'mailing/mailing_create.html'
    form_class = MailingCreateForm
    success_url = reverse_lazy('mailing_list')
    success_message = 'Рассылка успешно создана.'

    def form_valid(self, form):
        form.instance.from_user = self.request.user
        user_sender_email = self.request.user.email
        form.save()
        message = form.cleaned_data['message']
        subject = form.cleaned_data['subject']
        to_users = User.objects.filter(id__in=form.cleaned_data['to_users'])
        users_getting_email = []
        for user in to_users:
            users_getting_email.append(user.email)
        send_notification.delay(subject, message, user_sender_email, users_getting_email)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(MailingCreate, self).get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context['students'] = User.objects.filter(user_status=STUDENT)
        else:
            context['students'] = User.objects.select_related('student') \
                .filter(student__group=self.request.user.teacher.group_manager_id)
        return context
