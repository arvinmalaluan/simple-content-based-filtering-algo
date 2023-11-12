from django.shortcuts import render
from .ml_model import provide_recommendation, provide_compatibility
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count

from django.http import FileResponse
import io
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet

import matplotlib.pyplot as plt
from PIL import Image as PilImage

# Models
from userFolder import models as uFModel
from seekerFolder import models as sFModel

from . import generate_charts


@api_view(['POST'])
def get_recommendations(request):
    uid = request.data['account']
    skills = request.data['skill']
    education = request.data['education_level']
    achievements = request.data['achievements']

    a = skills.split('_+_')
    b = education.split('_+_')
    c = achievements.split('_+_')

    joined = a + b + c

    var = provide_recommendation(joined)
    return Response({"hello": var})


@api_view(['POST'])
def get_compatibility(request):
    title = request.data['job_title']

    skills = request.data['skills']
    education = request.data['education_level']
    achievements = request.data['achievements']

    a = skills.split('_+_')
    b = education.split('_+_')
    c = achievements.split('_+_')

    print(a, b, c)

    # var = provide_compatibility(title, skills)
    return Response({"return_message": 'hello'})


@api_view(['GET'])
def get_resume_insights(request):
    pass


@api_view(['GET'])
def get_jobpost_insights(request):
    pass


@api_view(['GET'])
def get_useroverview(request):
    report_type = request.GET.get('type')

    # Create Bytestream buffer
    buf = io.BytesIO()

    # Create a SimpleDocTemplate
    doc = SimpleDocTemplate(buf, pagesize=letter, rightMargin=inch,
                            leftMargin=inch, topMargin=inch, bottomMargin=inch)

    # Get a sample style
    styles = getSampleStyleSheet()

    # Create some Flowable objects
    flowables = []

    # Add the header
    header = Paragraph(
        "<font size=20><b>User Overview Report</b></font>")
    subheader = Paragraph(
        "<font size=12>Public Employment Service Office Generated Report</font>")
    address = Paragraph(
        "<font size=12>Lipa City, Batangas, Philippines 4200</font>")
    contact = Paragraph(
        "<font size=12>Tel. no. </font>")

    flowables.append(header)
    flowables.append(Spacer(1, 0.15 * inch))
    flowables.append(subheader)
    flowables.append(address)
    flowables.append(contact)
    flowables.append(Spacer(1, 0.25 * inch))

    newget = uFModel.Account.objects.values(
        'role__role').annotate(count=Count('role'))

    no_profile_header = Paragraph(
        "<font size=14><b>User Distribution by Role</b></font>")
    flowables.append(no_profile_header)
    flowables.append(Spacer(1, 0.4 * inch))

    img = generate_charts.generate_pie(newget)
    flowables.append(img)
    flowables.append(Spacer(1, 0.4 * inch))

    no_profile_header = Paragraph(
        "<font size=14><b>Registered Users with no profiles</b></font>")
    flowables.append(no_profile_header)
    flowables.append(Spacer(1, 0.4 * inch))

    x1_bc = sFModel.AllProfile.objects.all().count()
    x2_bc = uFModel.Account.objects.all().count()

    img = generate_charts.generate_bar(x1_bc, x2_bc)
    flowables.append(img)
    flowables.append(Spacer(1, 0.4 * inch))

    no_profile_header = Paragraph(
        "<font size=14><b>Users Distribution by location</b></font>")
    flowables.append(Spacer(1, 0.2 * inch))
    flowables.append(no_profile_header)
    flowables.append(Spacer(1, 0.4 * inch))

    img = generate_charts.generate_column()
    flowables.append(img)
    flowables.append(Spacer(1, 0.4 * inch))

    # Build the PDF
    doc.build(flowables)

    buf.seek(0)

    # Return file
    return FileResponse(buf, as_attachment=True, filename='user-overview-report.pdf')
