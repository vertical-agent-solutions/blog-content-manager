from django import forms
from .models import Topic, Category, ArticleParameters

class TopicForm(forms.ModelForm):
    # Make category field not required
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'data-existing-category': 'true'
        })
    )
    
    # Add a field for new category
    new_category = forms.CharField(
        max_length=200, 
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Or enter a new category name'
        })
    )
    new_category_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Description for the new category (optional)',
            'rows': 3
        }),
        required=False
    )
    
    class Meta:
        model = Topic
        fields = ['title', 'description', 'category', 'new_category', 'new_category_description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        new_category = cleaned_data.get('new_category')

        # Check if neither or both are provided
        if not category and not new_category:
            raise forms.ValidationError({
                'category': 'Please either select an existing category or create a new one.',
                'new_category': 'Please either select an existing category or create a new one.'
            })
        if category and new_category:
            raise forms.ValidationError({
                'category': 'Please choose only one: either select an existing category or create a new one.',
                'new_category': 'Please choose only one: either select an existing category or create a new one.'
            })

        # Check if new category name already exists
        if new_category and Category.objects.filter(name__iexact=new_category).exists():
            raise forms.ValidationError({
                'new_category': f'A category with the name "{new_category}" already exists. Please select it from the dropdown instead.'
            })

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        new_category = self.cleaned_data.get('new_category')
        
        if new_category:
            # Create new category
            category = Category.objects.create(
                name=new_category,
                description=self.cleaned_data.get('new_category_description', '')
            )
            instance.category = category
        
        if commit:
            instance.save()
        return instance 

class ArticleGenerationForm(forms.Form):
    parameters = forms.ModelChoiceField(
        queryset=ArticleParameters.objects.all(),
        required=False,
        empty_label="Custom parameters",
        widget=forms.Select(attrs={'class': 'form-select', 'data-parameters-select': True})
    )
    
    purpose = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False,
        help_text="What is the main purpose of this article?"
    )
    
    target_audience = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False,
        help_text="Who is the target audience for this article?"
    )
    
    tone_of_voice = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False,
        help_text="What tone of voice should be used? (e.g., professional, casual, academic)"
    )
    
    word_count = forms.IntegerField(
        initial=500,
        min_value=100,
        max_value=5000,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        help_text="How many words should the article be?"
    )
    
    save_as_default = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'data-save-toggle': True})
    )
    
    parameter_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Give these parameters a name to save them for future use"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        parameters = cleaned_data.get('parameters')
        save_as_default = cleaned_data.get('save_as_default')
        
        if not parameters:
            # If not using saved parameters, require the custom fields
            required_fields = ['purpose', 'target_audience', 'tone_of_voice', 'word_count']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, 'This field is required when not using saved parameters.')
        
        if save_as_default and not cleaned_data.get('parameter_name'):
            self.add_error('parameter_name', 'Parameter name is required when saving as default.')
        
        return cleaned_data 