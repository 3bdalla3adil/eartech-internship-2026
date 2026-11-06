from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RoleRegistrationForm
from .models import PatientProfile, DoctorProfile


def register_view(request):
    if request.method == 'POST':
        form = RoleRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')
            user.save()

            if role == 'patient':
                PatientProfile.objects.create(user=user)
            elif role == 'doctor':
                DoctorProfile.objects.create(user=user)

            login(request, user)
            return redirect('login')
    else:
        form = RoleRegistrationForm()

    return render(request, 'register.html', {'form': form})