from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.forms import ModelForm 
from django.contrib.auth.models import User
from django.core.validators import ValidationError
from .models import Profile, Adress
from crispy_forms.helper import FormHelper
from crispy_forms import bootstrap, layout
from crispy_forms.layout import Layout, Row
from crispy_forms.bootstrap import InlineField, FormActions, StrictButton, Div
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(label='Email:',widget=forms.TextInput())
    password = forms.CharField(label='Palavra-chave:' ,widget=forms.PasswordInput())


class ChandPasswordForm(PasswordChangeForm):
   
    def __init__(self, *args, **kwargs):
        
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        

        self.error_messages['password_mismatch']="As duas palavras-chave não correspondem"
        self.error_messages['password_incorrect']="A Password antiga não está correcta"
       
        for fieldname in ['new_password1', 'new_password2']:
            self.fields[fieldname].help_text = None

        print(self.error_messages)
        print(self.has_error)
        for field in self.fields.items():
            print(field)
            # if 'required' in field.error_messages:
            #     field.error_messages['required'] = 'You have to field this.'

   
class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.error_messages['password_mismatch']="As duas palavras-chave não correspondem"
        self.error_messages['password_incorrect']="A Password antiga não está correcta"
        for fieldname in ['username']:
            print(self.fields[fieldname])
        
        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None
       # self.errors['username'] = None

    email=forms.CharField(required=True, label="Endereço de Email")
    first_name=forms.CharField(required=True, label="Primeiro Nome")
    last_name=forms.CharField(required=True, label="Ultimo Nome")
    username=forms.EmailField(widget=forms.HiddenInput())
    check=forms.BooleanField(required=True, label="Li e concordo com as Politicas de Privacidade e com os Termos e condições deste Website")


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("O Email já existe")
        return email
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email","first_name","last_name")



class UserNameForm(ModelForm):
    first_name=forms.CharField(required=True, label="Primeiro Nome")
    last_name=forms.CharField(required=True, label="Ultimo Nome")

    class Meta:
        model = User
        fields = ['first_name',"last_name"]



class CheckAdress(ModelForm):
    receiver=forms.CharField(label="Destinatário:")
    street=forms.CharField(label="Morada:")
    city=forms.CharField(label="Cidade:")
    postal_code=forms.CharField(label="Código Postal:")
    district=forms.CharField(label="Distrito:")
    contact=forms.IntegerField(label="Contacto:")
    nif=forms.IntegerField(label="NIF:", required=False)


    def clean_postal_code(self):
        data = self.cleaned_data['postal_code']
        print("from adress clean data validation form")

        data_clean=data.replace("-","")
        if not data_clean.isnumeric() or len(data_clean)!=7:
            
            self.add_error('postal_code', "Código Postal Inválido")
            
        #print(f"clean postal code data: {data}")
        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data
    def __init__(self, *args, **kwargs):
        print("From form adress!!!!!!!!!!")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
        'receiver',
        'street',
        Row(
            Div('postal_code',css_class="col-md-12 col-lg-2"),
            Div('city',css_class="col-md-12 col-lg-5"),
            Div('district',css_class="col-md-12 col-lg-5")
        ),
        'contact',
        'nif',
        )
    class Meta:
        model = Adress
        fields = ['receiver', 'street','postal_code','city','district','contact','nif']
    