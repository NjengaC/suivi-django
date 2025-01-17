from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib import messages

class CustomPasswordResetView(PasswordResetView):
    template_name = 'forgot_password.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_url = reverse_lazy('entry:login')
    form_class = PasswordResetForm

    def form_valid(self, form):
        messages.success(self.request, "Instructions to reset your password have been sent to your email.")
        return super().form_valid(form)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'reset_password.html'
    success_url = reverse_lazy('entry:login')
    form_class = SetPasswordForm

    def form_valid(self, form):
        messages.success(self.request, "Your password has been successfully reset. You can now log in with your new password.")
        return super().form_valid(form)

