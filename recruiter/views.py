from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse

from . import models
from . import serializer
from seekerFolder import serializers
from seekerFolder.models import AllProfile, Post, Resume
from analytics import ml_model


class GP_JobPost(generics.ListCreateAPIView):
    queryset = models.JobPost.objects.prefetch_related('allprofile')
    serializer_class = serializer.JPSerializer

    def get(self, request, *args, **kwargs):
        profile_id = request.query_params.get('allprofile')
        self.queryset = self.queryset.filter(allprofile=profile_id)
        response = super().get(request, *args, **kwargs)

        for job_post in response.data:
            profile_id = job_post['allprofile']
            profile = AllProfile.objects.get(account=profile_id)
            job_post['recruiter_profile'] = serializers.ProfileSerializer(
                profile).data

        return response


class POST_JobPost(generics.ListCreateAPIView):
    queryset = models.JobPost.objects.all()
    serializer_class = serializer.JobPostSerializer


class GP_RecruiterProfile(generics.ListCreateAPIView):
    queryset = models.RecruiterProfile.objects.all()
    serializer_class = serializer.RecruiterProfileSerializer


class U_RecruiterProfile(generics.RetrieveUpdateAPIView):
    queryset = models.RecruiterProfile.objects.all()
    serializer_class = serializer.RecruiterProfileSerializer


class UD_JobPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.JobPost.objects.all()
    serializer_class = serializer.JobPostSerializer

    # def get(self, request, *args, **kwargs):
    #     response = super().get(request, *args, **kwargs)
    #     job_post = self.get_object()

    #     response.data['recruiter_profile'] = serializers.ProfileSerializer(
    #         job_post.allprofile).data

    #     return response


class GA_JobPost(generics.ListCreateAPIView):
    queryset = models.JobPost.objects.all()
    serializer_class = serializer.JobPostSerializer


class C_Apply(generics.ListCreateAPIView):
    queryset = models.Applicants.objects.all()
    serializer_class = serializer.ApplicantSerializer


class UD_Apply(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Applicants.objects.all()
    serializer_class = serializer.ApplicantSerializer

    def get_object(self):
        custom_key = self.kwargs['custom_key']
        return get_object_or_404(models.Applicants, custom_key=custom_key)


class GA_JobPostWApplicants(generics.ListCreateAPIView):
    serializer_class = serializer.JPSerializer

    def get_queryset(self):
        return models.JobPost.objects.select_related('allprofile').prefetch_related(
            'applicants').order_by('created')


class GA_MyJobPosts(generics.ListCreateAPIView):
    serializer_class = serializer.JPSerializer

    def get_queryset(self):
        my_id = self.kwargs.get('id')

        return models.JobPost.objects.filter(allprofile=my_id).select_related('allprofile').prefetch_related(
            'applicants').order_by('created')


@api_view(['GET'])
def job_posts(request):
    posts = Post.objects.select_related('profile').prefetch_related(
        'comments', 'engagements').order_by('-created')
    serializer = serializers.PostSerializer(posts, many=True)
    print(serializer.data)

    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def get_my_application(request):
    application = "hello"


@api_view(['POST'])
def handle_application(request):
    job = request.data['job']
    applicant = request.data['applicant']
    key = request.data['key']
    skills = ''
    job_instance = models.JobPost.objects.get(id=job)
    allprofile_i = AllProfile.objects.get(account=applicant)

    try:
        instance = Resume.objects.get(account=applicant)
        skills = instance.skill
    except Resume.DoesNotExist:
        print("No record found with id=24")

    param_job_title = job_instance.job_title
    param_skills = skills.split('_+_')
    compatibility = ml_model.provide_compatibility(
        param_job_title, param_skills)

    try:
        application = models.Applicants.objects.create(
            job=job_instance,
            applicant=allprofile_i,
            custom_key=key,
            status='applied',
            compatibility=compatibility
        )

        print(application)
    except Exception as e:
        print('no skills detected: ', e)

    context = {"success": 1}

    return JsonResponse(context)
