from django.contrib import admin
from .models import Tutorial
from tinymce import TinyMCE
from django.db import models

# Register your models here.
class TutorialsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title/Date",{"fields":["tutorial_title","tutorial_published"]}),
        ("Content",{"fields":["tutorial_content"]})
    ]

    formfield_overrides = {
        models.TextField : {'widget':TinyMCE()}
    }

admin.site.register(Tutorial, TutorialsAdmin)
