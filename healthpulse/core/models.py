from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patientprofile')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Patient: {self.user.username}"

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctorprofile')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Doctor: {self.user.username}"