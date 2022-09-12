from django import forms
from managing.models import CustomUser

class RegisterForm(forms.ModelForm) :
    password = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput(attrs={"class" : "form-control"}))
    
    class Meta :
        model = CustomUser 
        fields = ("username", "email", "national_code")
        
    def clean_password2(self) :
        cd = self.cleaned_data
        if cd["password"] != cd["password2"] :
            raise forms.validationError("your password and repeated one must be exactly match")
        return cd["password2"]
        
    #def save(self, *args, **kwargs) :
    

class UpdateUser(forms.ModelForm) :
    class Meta :
        model = CustomUser
        fields = ("username",)