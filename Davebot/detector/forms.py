from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# class TextInputForm(forms.Form):
#     text_input = forms.CharField(label= "", widget=forms.Textarea(attrs={'rows': 12, 'cols': 50, 'class': 'custom-field', 'placeholder': 'Enter the text you want to test for AI/Chatbot plagiarism (minimum 20 words).', 'style': 'background-color: #FFF8DB; color: black; font-family: Source Code Pro;'} ))



from django.forms import formset_factory

class TupleForm(forms.Form):
    element_1 = forms.CharField(label="Element 1")
    element_2 = forms.CharField(label="Element 2")
    def clean(self):
        # Override clean method to return cleaned data without validation
        return self.cleaned_data

TupleFormSet = formset_factory(TupleForm, extra=0)  # Assuming you've created the formset class already

class TextInputForm(forms.Form):
    text_input = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 10,
            'cols': 35,
            'class': 'custom-field border-black',
            'placeholder': 'Enter the text you want to test for AI/Chatbot text (minimum 20 words)',
            'style': 'background-color: #201A31; color: white; font-family: Poppins, sans-serif; font-size: 14px; border-color: white;',
        }),
        label='Text Input:',  # Set the label for the field
    )

    rubric_input = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 5,
            'cols': 25,
            'class': 'custom-field border-black',
            'placeholder': 'Enter the rubric for your assignment.',
            'style': 'background-color: #201A31; color: white; font-family: Poppins, sans-serif; font-size: 14px; border-color: white;',
        }),
        label='Rubric Input:',  # Set the label for the field
    )
    
    subject_input = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 1.5,
            'cols': 10,
            'class': 'custom-field border-black',
            'placeholder': 'Enter the subject this is for.',
            'style': 'background-color: #201A31; color: white; font-family: Poppins, sans-serif; font-size: 14px; border-color: white;',
        }),
        label='Subject Input:',  # Set the label for the field
    )

    file_input = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'custom-file-input',
            'id': 'customFile',
            'style': 'background-color: #201A31; color: white; font-family: Poppins, sans-serif; font-size: 14px;',
            'multiple': True,
        }),
        label='File Input:',  # Set the label for the field
    )
   

    def clean(self):
        cleaned_data = super().clean()
        text_input = cleaned_data.get('text_input')
        file_input = cleaned_data.get('file_input')
        if not text_input and not file_input:
            raise forms.ValidationError('Either a text input or a file input is required')
        elif text_input and file_input:
            raise forms.ValidationError('Only one of text input or file input can be submitted')
        if text_input: 
            word_count = len(text_input.split())
            if word_count < 20:
                raise ValidationError(_('The text input must be at least 20 words.'), code='invalid')
        return cleaned_data

