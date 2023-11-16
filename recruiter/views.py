from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse

from . import models
from . import serializer
from seekerFolder import serializers
from seekerFolder.models import AllProfile, Post, Resume
from analytics import ml_model

from adminpage import for_emailing


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

    def put(self, request, *args, **kwargs):
        # This will print all the data passed in the PUT request

        an = request.data['applicant']
        jt = request.data['job']
        st = request.data['status']

        message = ""
        if st == 'interviewed':
            message = "Congratulations on completing your interview! Your effort and dedication are truly commendable. We appreciate your time and interest in our company. Rest assured, we will keep you updated and notify you promptly if any changes occur in the process. Thank you for your enthusiasm, and we look forward to the possibility of working together."
        elif st == 'rejected':
            message = "We appreciate your interest and effort throughout the interview process. After careful consideration, we regret to inform you that we have chosen not to move forward with your application at this time. We recognize the time and dedication you invested, and we genuinely thank you for your interest in our company. Please do not be disheartened, as opportunities may arise in the future. We wish you the best in your career endeavors, and thank you again for considering us as part of your professional journey."
        elif st == 'hired':
            message = "Congratulations! We are thrilled to inform you that you have been selected for the position. Your skills, experience, and positive attitude have set you apart, and we believe you will be a valuable addition to our team. Welcome aboard! Our HR department will be in touch shortly with the necessary onboarding details. We look forward to your contributions and success within our organization. Once again, congratulations on your well-deserved success!"

        jti = models.JobPost.objects.get(id=jt)
        ani = AllProfile.objects.get(account=an)

        content = {
            "comp_name": jti.allprofile.name,
            "job_title": jti.job_title,
            "name": ani.name,
            "status": message
        }

        try:
            for_emailing.send_email_status_update(content)
        except Exception as e:
            print('error:', e)

        return super().put(request, *args, **kwargs)


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
    applied = request.data['applied']
    compatibility = ml_model.provide_compatibility(
        param_job_title, param_skills)

    try:
        application = models.Applicants.objects.create(
            job=job_instance,
            applicant=allprofile_i,
            custom_key=key,
            status='applied',
            compatibility=compatibility,
            applied=applied
        )

        content = {
            "comp_name": job_instance.allprofile.name,
            "name": allprofile_i.name,
            "position": job_instance.job_title,
            "app_date": applied
        }

        for_emailing.send_email_function(content)

        print(application)
    except Exception as e:
        print('no skills detected: ', e)

    context = {"success": 1}

    return JsonResponse(context)
