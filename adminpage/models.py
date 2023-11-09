from django.db import models
from userFolder.models import Account
from recruiter.models import JobPost

from github import Github
import os


class GetDocuments(models.Model):
    fk_account = models.ForeignKey(Account, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='images/', blank=True, null=True)
    tor = models.FileField(upload_to='images/', blank=True, null=True)
    nbi = models.FileField(upload_to='images/', blank=True, null=True)
    psa = models.FileField(upload_to='images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # List of fields to process
        fields_to_process = ['resume', 'tor', 'nbi', 'psa']

        # Iterate through the fields and process the files
        for field_name in fields_to_process:
            file_field = getattr(self, field_name)
            if file_field:
                g = Github("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")
                repo = g.get_user().get_repo("github-as-static-assets-repository")
                file_path = file_field.path
                file_name = os.path.basename(file_path)

                with open(file_path, 'rb') as file:
                    content = file.read()

                repo.create_file("images/" + file_name,
                                 "uploading an image", content)


class RecordProcessToGetReco(models.Model):
    process_to = models.CharField(max_length=255)
    char_count = models.CharField(max_length=255)


class TimeToGetCompatibilityScore(models.Model):
    process_to = models.CharField(max_length=255)
    char_count = models.CharField(max_length=255)


class LogUserEngagement(models.Model):
    jobpost = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
