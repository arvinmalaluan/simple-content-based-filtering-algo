from rest_framework.decorators import api_view
from rest_framework.response import Response
from .ml_model import provide_recommendation, provide_compatibility_apply

@api_view(['POST'])
def provide_compatible_jobs(request):
  post = request.data['payload']['skills']
  x = provide_recommendation(post)
  return Response({"positions": x})


@api_view(['POST'])
def provide_compatibility(request):
  job_title = request.data['payload']['jobtitle']
  skills = request.data['payload']['skills']

  x = provide_compatibility_apply(job_title, skills)
  return Response({"compatibility": x})