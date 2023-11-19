from django.db import models
from userFolder.models import Account

from github import Github
import base64
from datetime import datetime


class AllProfile(models.Model):
    account = models.IntegerField(primary_key=True, blank=True)
    fk = models.ForeignKey(
        Account, on_delete=models.CASCADE, blank=True, null=True, related_name='allprofile')
    name = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(null=True, blank=True, upload_to='images/')
    bio = models.CharField(max_length=255, null=True, blank=True)
    social_links = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    portfolio_link = models.CharField(max_length=255, null=True, blank=True)
    educational_attainment = models.CharField(
        max_length=255, null=True, blank=True)

    emp_count = models.IntegerField(
        null=True, blank=True, default=0)
    subsidiaries_count = models.IntegerField(
        null=True, blank=True, default=0)
    comp_overview = models.CharField(max_length=255, null=True, blank=True)
    site_link = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = str(self.photo)

        if not image.startswith('images'):
            g = Github("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")
            repo = g.get_user().get_repo("github-as-static-assets-repository")

            # Create a new file name
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            new_file_name = f"{self.fk.email.split('@')[0]}_photo_{timestamp}"

            with open(self.photo.path, 'rb') as file:
                content = file.read()

            # Upload the file with the new name
            repo.create_file("images/" + new_file_name,
                             "uploading an image", base64.b64encode(content))

            # Save the new file name to the model
            self.photo.name = new_file_name
        else:
            print('hello')

        super().save(*args, **kwargs)

    @classmethod
    def get_profiles_with_role(cls, role):
        return cls.objects.filter(fk__role__in=role)


class Post(models.Model):
    profile = models.ForeignKey(
        AllProfile, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    poster_name = models.CharField(max_length=100, blank=True)
    poster_profile = models.ImageField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.poster_name = self.profile.name
        self.poster_profile = self.profile.photo
        super().save(*args, **kwargs)


class Resume(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    resume_objective = models.TextField()

    education_level = models.CharField(max_length=255)
    name_of_institution = models.CharField(max_length=255)
    year_graduated = models.CharField(max_length=255)
    achievements = models.CharField(max_length=255)

    languages = models.CharField(max_length=255)
    hobbies_interest = models.CharField(max_length=255)

    skill = models.TextField()
    proficiency = models.CharField(max_length=255)

    reward_name = models.CharField(max_length=255)
    year_received = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255)
    reward_description = models.CharField(max_length=255)

    project_name = models.CharField(max_length=255)
    published_year = models.CharField(max_length=255)
    project_description = models.CharField(max_length=255)

    reference_full_name = models.CharField(max_length=255)
    relationship_to_you = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    contact_information = models.CharField(max_length=255)

    compatibility = models.TextField(null=True, blank=True)


class Profile(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    photo = models.ImageField(null=True)
    bio = models.CharField(max_length=255, null=True)
    social_links = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True)
    portfolio_link = models.CharField(max_length=255, null=True)
    educational_attainment = models.CharField(max_length=255, null=True)


class Comments(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    profile = models.ForeignKey(
        AllProfile, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    commentor = models.CharField(max_length=100, blank=True, null=True)
    photo = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.commentor = self.profile.name
        self.photo = self.profile.photo
        super().save(*args, **kwargs)


class Engagement(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='engagements')
    is_liked = models.BooleanField(default=False)
    uni_profile = models.ForeignKey(
        AllProfile, on_delete=models.CASCADE, related_name='profile')
    is_disliked = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    custom_key = models.CharField(max_length=30, blank=True)
    engager = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.custom_key = f'{self.post.id}{self.uni_profile.account}'
        self.engager = self.uni_profile.name
        super().save(*args, **kwargs)
