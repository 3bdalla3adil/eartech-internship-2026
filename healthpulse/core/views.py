from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RoleRegistrationForm
from .models import PatientProfile, DoctorProfile
from django.urls import reverse
from django.http import HttpResponseForbidden

def register_view(request):
    if request.method == 'POST':
        form = RoleRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')

            if role == 'doctor':
                DoctorProfile.objects.create(user=user)
                login(request, user)
                return redirect('doctor_dashboard')
            else:
                PatientProfile.objects.create(user=user)
                login(request, user)
                return redirect('patient_dashboard')
    else:
        form = RoleRegistrationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def home_redirect(request):
    if hasattr(request.user, 'doctorprofile'):
        return redirect('doctor_dashboard')
    return redirect('patient_dashboard')

@login_required
def doctor_dashboard(request):
    if not hasattr(request.user, 'doctorprofile'):
        if hasattr(request.user, 'patientprofile'):
            return redirect('patient_dashboard')
        return HttpResponseForbidden("Access Denied")

    return render(request, 'doctor_dashboard.html')


@login_required
def patient_dashboard(request):
    if not hasattr(request.user, 'patientprofile'):
        if hasattr(request.user, 'doctorprofile'):
            return redirect('doctor_dashboard')
        return HttpResponseForbidden("Access Denied")

    return render(request, 'patient_dashboard.html')


class RoleLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse('home_redirect')
class RoleLogoutView(LogoutView):
    next_page = 'login'