from apps.permissions.mixins import PermissionMixin
from apps.permissions.permissions import IsAuthenticated, IsManager, IsMyHitmen
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import (HitmenBossEditForm, HitmenBossForm, HitmenEditForm,
                    HitmenForm, ManagerUserForm)
from .models import EmailUser


def home_redirect(request):
    if request.user.is_authenticated:
        return redirect(reverse('hit_list'))
    return redirect(reverse('login'))


class SignUpView(CreateView):
    model = EmailUser
    form_class = ManagerUserForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.

        notes: 
            this method is part of the generic flow and 
            we can override here extra save data
        """
        self.object = form.save(commit=False)
        self.object.is_staff = True
        return super().form_valid(form)


class HitmenListView(PermissionMixin, ListView):
    model = EmailUser
    permission_classes = [IsAuthenticated, IsManager]
    paginate_by = None

    def get_queryset(self):
        '''
        notes:
            exclude is_superuser=False, is_staff=False because this view
            only show hitmens.
        '''
        if self.request.user.is_superuser:
            return super().get_queryset().filter(
                is_superuser=False, is_staff=False)
        else:
            return super().get_queryset().filter(
                is_superuser=False,
                is_staff=False,
                is_active=True,
                managed_by=self.request.user)


class HitmenDetailView(PermissionMixin, UpdateView):
    model = EmailUser
    permission_classes = [IsAuthenticated, IsManager, IsMyHitmen]
    success_url = reverse_lazy('hitmen_list')

    def get_form_class(self):
        """
        return diferent form depending from the user

        notes: 
            this method is part of the generic flow and 
        """
        if self.request.user.is_superuser:
            return HitmenBossEditForm
        else:
            return HitmenEditForm

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.

        notes: this method is part of the generic flow and 
            we can override here extra save data and send messages
        """

        self.object = form.save()
        messages.success(self.request, f'Hitmen {self.object} actualizado')
        return super().form_valid(form)


class HitmenCreateView(PermissionMixin, CreateView):
    model = EmailUser
    permission_classes = [IsAuthenticated, IsManager]
    success_url = reverse_lazy('hitmen_list')

    def get_form_class(self):
        """
        return diferent form depending from the user

        notes: 
            this method is part of the generic flow and 
        """
        if self.request.user.is_superuser:
            return HitmenBossForm
        else:
            return HitmenForm

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.

        notes: 
            this method is part of the generic flow and 
            we can override here extra save data
        """
        self.object = form.save(commit=False)
        self.object.managed_by = self.request.user
        messages.success(self.request, f'Hitmen {self.object} creado')
        return super().form_valid(form)
