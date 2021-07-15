from apps.users.models import EmailUser
from django.forms import ModelForm

from .models import Hit


class HitCreateForm(ModelForm):
    class Meta:
        model = Hit
        fields = ('target', 'description',  'hitmen_by')

    def __init__(self, *args, manager=None, **kwargs):
        super().__init__(*args, **kwargs)
        if manager:
            self.fields['hitmen_by'].choices = [
               (x.id, x) for x in EmailUser.objects.filter(managed_by=manager)]


class HitUpdateForm(ModelForm):
    class Meta:
        model = Hit
        fields = ('status',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = [
            ('failed', 'Failed'),
            ('completed', 'Completed')]
