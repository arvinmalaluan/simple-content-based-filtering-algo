from django.db import models

from seekerFolder.models import AllProfile


class Conversation(models.Model):
    involve_one = models.ForeignKey(
        AllProfile, on_delete=models.CASCADE, related_name='conversations_one', null=True, blank=True)
    involve_two = models.ForeignKey(
        AllProfile, on_delete=models.CASCADE, related_name='conversations_two', null=True, blank=True)
    custom_key = models.CharField(
        max_length=20, primary_key=True, blank=True, unique=True)
    involve_one_name = models.CharField(max_length=200, null=True, blank=True)
    involve_two_name = models.CharField(max_length=200, null=True, blank=True)
    profile_one = models.ImageField(null=True, blank=True, upload_to='images/')
    profile_two = models.ImageField(null=True, blank=True, upload_to='images/')
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        val = ''

        if (self.involve_one.account > self.involve_two.account):
            val = f"{self.involve_one.account}{self.involve_two.account}"
        else:
            val = f"{self.involve_two.account}{self.involve_one.account}"

        self.custom_key = val
        self.involve_one_name = self.involve_one.name
        self.involve_two_name = self.involve_two.name
        self.profile_one = self.involve_one.photo
        self.profile_two = self.involve_two.photo
        super().save(*args, **kwargs)


class Messages(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    receiver = models.CharField(max_length=20)
    message = models.TextField()
    message_created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def last_20_messages(cls, filter_by):
        return cls.objects.filter(conversation__custom_key=filter_by).order_by('message_created')
