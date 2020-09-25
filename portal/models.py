from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from accounts.models import Profile

# Create your models here.

class Job(models.Model):
    role = models.CharField(max_length=255)
    applied_on = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
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
    post_link = models.URLField(null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    last_updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.role


class Note(models.Model):
    job = models.ForeignKey(Job, related_name='notes', on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job}'s Note"


class Connection(models.Model):
    profile = models.ForeignKey(Profile, related_name='connects', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], default=1)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} connections on {self.date}"