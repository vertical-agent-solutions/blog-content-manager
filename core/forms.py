from django import forms
from .models import Topic, Category

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