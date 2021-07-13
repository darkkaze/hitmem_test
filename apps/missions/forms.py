from django.forms import ModelForm

from .models import Hit


class HitCreateForm(ModelForm):
    class Meta:
        model = Hit
        fields = ('target', 'description',  'hitmen_by')


class HitUpdateForm(ModelForm):
    class Meta:
        model = Hit
        fields = ('status',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = [
            ('failed', 'Failed'),
            ('completed', 'Completed')]
