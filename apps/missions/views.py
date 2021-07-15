from apps.permissions.mixins import PermissionMixin
from apps.permissions.permissions import (IsAuthenticated, IsManager, IsMyHit,
                                          IsMyTarget)
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import HitCreateForm, HitUpdateForm
from .models import Hit


class HitListView(PermissionMixin, ListView):
    model = Hit
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        elif self.request.user.is_staff:
            return super().get_queryset().filter(managed_by=self.request.user)
        else:
            return super().get_queryset().filter(hitmen_by=self.request.user)


class HitDetailView(PermissionMixin, UpdateView):
    model = Hit
    permission_classes = [IsAuthenticated, IsMyTarget | IsMyHit]
    success_url = reverse_lazy('hit_list')

    def get_form_class(self):
        """
        return diferent form depending from the user

        notes: 
            this method is part of the generic flow and 
        """

        if self.request.user.is_staff:
            return HitCreateForm
        else:
            return HitUpdateForm

    def get_form(self, form_class=None):
        """
        Return an instance of the form to be used in this view

        notes: 
            this method is part of the generic flow and 
        """
        if form_class is None:
            form_class = self.get_form_class()
        if self.request.user.is_superuser or not self.request.user.is_staff:
            return form_class(**self.get_form_kwargs())
        else:
            return form_class(
                manager=self.request.user, **self.get_form_kwargs())

    def get_template_names(self):
        """
        return diferent template depending from the user

        notes: 
            this method is part of the generic flow and 
        """
        if self.request.user.is_staff:
            return super().get_template_names()
        else:
            return ['missions/hit_detail.html']

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.

        notes: this method is part of the generic flow and 
            we can override here extra save data and send messages
        """

        self.object = form.save()
        messages.success(self.request, f'Hit {self.object} actualizado')
        return super().form_valid(form)


class HitCreateView(PermissionMixin, CreateView):
    model = Hit
    permission_classes = [IsAuthenticated, IsManager]
    fields = ('target', 'description', 'hitmen_by')
    success_url = reverse_lazy('hit_list')

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.

        notes: this method is part of the generic flow and 
            we can override here extra save data and send messages
        """
        self.object = form.save(commit=False)
        self.object.managed_by = self.request.user
        messages.success(self.request, f'Hit {self.object} creado')
        return super().form_valid(form)
