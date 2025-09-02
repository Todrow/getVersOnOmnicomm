from django import forms
from .models import SoftwareVersion, Component
from django.core.exceptions import ValidationError


class SoftwareVersionForm(forms.ModelForm):
    # Заменяем чекбокс на выпадающий список
    is_critical = forms.ChoiceField(
        choices=[(False, 'Minor'), (True, 'Major (Критическое обновление)')],
        label="Критическое обновление",
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial='Minor'
    )

    class Meta:
        model = SoftwareVersion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.initial['is_critical'] = self.instance.is_critical
        self.fields['is_broken'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        version = cleaned_data.get('version')

        if version:
            parts = version.split('.')
            if len(parts) == 5:
                try:
                    cleaned_data['tractor_model'] = parts[0]
                    cleaned_data['engine_comp'] = parts[1]
                    cleaned_data['first_number'] = int(parts[2])
                    cleaned_data['second_number'] = int(parts[3])
                    cleaned_data['third_number'] = int(parts[4])
                except:
                    pass
        elif cleaned_data.get('tractor_model') and cleaned_data.get('engine_comp') and cleaned_data.get('first_number') and cleaned_data.get('second_number') and cleaned_data.get('third_number'):
            cleaned_data['version'] = f"{cleaned_data.get('tractor_model')}.{cleaned_data.get('engine_comp')}.{cleaned_data.get('first_number')}.{cleaned_data.get('second_number')}.{cleaned_data.get('third_number')}"
        else:
            raise ValidationError(
                f'Должно быть заполнено либо поле "Обозначение ПО", либо все остальные поля, кроме даты выпуска')
        return cleaned_data


class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = '__all__'


class StatusForm(forms.Form):
    status = forms.ChoiceField(
        choices=[(0, 'Все'), (2, 'Критически устаревшие трактора (major)'),
                 (3, 'Не критически устаревшие трактора(minor)')],
        label='Статус трактора',
        initial='Все'
    )
