from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from accounts.models import Profile

# Create your models here.

class Job(models.Model):
    role = models.CharField(max_length=255)
    applied_on = models.CharField(max_length=255)
    notes = models.TextField()
    date = models.DateField(auto_now=True)
    profile = models.ForeignKey(Profile, related_name='jobs', on_delete=models.CASCADE)
    APPLIED = 'Applied'
    INTERVIEW = 'Interview'
    TECHTEST = 'Tech Test'
    OFFER = 'Offer'
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'
    STATUS_CHOICES = [
        (APPLIED, 'Applied'),
        (INTERVIEW, 'Interview'),
        (TECHTEST, 'Tech Test'),
        (OFFER, 'Offer'),
        (ACCEPTED, 'Accepted'),
        (REJECTED,'Rejected'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=APPLIED,
    )
    
    def __str__(self):
        return self.role
