from django.db import models
from userFolder.models import Account
from recruiter.models import JobPost

from github import Github
from datetime import datetime


class GetDocuments(models.Model):
    fk_account = models.ForeignKey(
        Account, on_delete=models.CASCADE, unique=True)
    resume = models.FileField(upload_to='images/', blank=True, null=True)
    tor = models.FileField(upload_to='images/', blank=True, null=True)
    nbi = models.FileField(upload_to='images/', blank=True, null=True)
    psa = models.FileField(upload_to='images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # List of fields to process
        fields_to_process = ['resume', 'tor', 'nbi', 'psa']

        # Iterate through the fields and process the files
        for field_name in fields_to_process:
            file_field = getattr(self, field_name)
            if file_field:
                g = Github("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")
                repo = g.get_user().get_repo("github-as-static-assets-repository")
                name = self.fk_account.email.split('@')[0]

                # Read the file directly from the FileField
                content = file_field.read()

                
                # Create a new file name
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                new_file_name = f"{name}_{field_name}_{timestamp}.pdf"


                # Upload the file with the new name
                repo.create_file("images/" + new_file_name,
                                 "uploading an image", content)

                # Save the new file name to the model
                setattr(self, field_name, new_file_name)

        # Save the model again to persist the change
        super().save(*args, **kwargs)


class LogBook(models.Model):
    char_count = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)


class LogUserEngagement(models.Model):
    jobpost = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
