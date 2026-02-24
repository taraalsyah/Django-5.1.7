from django import forms
from .models import Ticket, TicketHistory, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter category description'}),
        }

class TicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.is_create = kwargs.pop('is_create', False)
        user = kwargs.pop('user', None)  # ambil user dari view
        super().__init__(*args, **kwargs)
        if user:
            self.fields['requested_by'].initial = user.email  # set default
            self.fields['requested_by'].widget.attrs['readonly'] = True # buat readonly
        
        # Populate category choices from Category model
        category_choices = [('', 'Select Category')] + [(c.name, c.name) for c in Category.objects.all()]
        self.fields['category'] = forms.ChoiceField(
            choices=category_choices,
            widget=forms.Select(attrs={'class': 'form-select'}),
            required=False
        )

        if self.is_create:
            # Saat create → status fix 'Open' dan disembunyikan
            self.fields['status'].widget=forms.HiddenInput()

    class Meta:
        model = Ticket
        fields = [
            'title',
            'description',
            'category',
            'status',
            'assigned_to',
            'requested_by',
            'attachments'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ticket title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the issue'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category name'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Assignee (optional)'}),
            'requested_by': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Requested by'}),
            'attachments': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Upload attachments (optional)'}),
        }
    def clean_status(self):
        # Saat create, kunci nilai status = 'Open'
        if self.is_create:
            return 1  # 'Open'
        return int(self.cleaned_data['status'])
    

class TicketHistoryForm(forms.ModelForm):
    class Meta:
        model = TicketHistory
        fields = ['ticket', 'updated_by', 'comment', 'status', 'attachment']
        widgets = {
            'ticket': forms.HiddenInput(),       # biasanya dipilih otomatis
            'updated_by': forms.HiddenInput(),   # auto diisi user login
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the issue'}),
            'status': forms.HiddenInput(),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Upload attachments (optional)'}),
        }