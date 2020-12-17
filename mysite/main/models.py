from django.db import models
from django.utils import timezone

# Create your models here.
class Tutorial(models.Model):
    tutorial_title = models.CharField(max_length=200)
    tutorial_content = models.TextField()
    tutorial_published = models.DateTimeField('date published', default= timezone.now())

    def __str__(self):
        return self.tutorial_title

class EmailSender(models.Model):
    contact_name = models.CharField(max_length=200)
    contact_email = models.CharField(max_length=200)
    email_body = models.TextField()

    def __str__(self):
        return self.contact_email

    def is_valid(self):
        if self.contact_email and self.contact_email.strip():
            if self.contact_name and self.contact_name.strip():
                if self.email_body and self.email_body.strip():
                    return True