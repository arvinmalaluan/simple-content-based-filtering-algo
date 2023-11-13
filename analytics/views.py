from .ml_model import provide_recommendation, provide_compatibility
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count

from django.utils import timezone
from datetime import timedelta
from datetime import datetime, timezone

from django.http import FileResponse
import io
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

import matplotlib.pyplot as plt
from PIL import Image as PilImage

# Models
from userFolder import models as uFModel
from seekerFolder import models as sFModel
from recruiter import models as rFModel
from chat.models import Messages

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


@api_view(['POST'])
def count_my_posts(request):
    user_id = request.data['id']
    day_counts = []

    for i in range(7):
        date = datetime.now() - timedelta(days=i)
        count = rFModel.JobPost.objects.filter(
            allprofile=user_id, created__date=(date)).count()
        day_counts.append({
            "date": date.strftime("%Y-%m-%d"),
            "count": count
        })

    # Sort the list by date
    day_counts = sorted(day_counts, key=lambda x: x['date'])

    return Response({"data": day_counts})


@api_view(['POST'])
def count_my_applicants(request):
    user_id = request.data['id']
    job_ids = rFModel.JobPost.objects.filter(
        allprofile=user_id).values_list('id', flat=True)
    day_counts = []

    for i in range(7):
        date = datetime.now() - timedelta(days=i)
        count = rFModel.Applicants.objects.filter(
            job__id__in=job_ids, applied__date=date,).count()
        day_counts.append({
            "date": date.strftime("%Y-%m-%d"),
            "count": count
        })

    # Sort the list by date
    day_counts = sorted(day_counts, key=lambda x: x['date'])

    return Response({"data": day_counts})


@api_view(['POST'])
def count_my_messages(request):
    user_id = request.data['id']
    end_date = datetime.now()
    start_date = end_date - timedelta(days=6)

    messages_counts = Messages.objects.filter(
        message_created__range=(start_date, end_date),
        receiver=user_id
    ).values('message_created__date').annotate(count=Count('message_created__date')).order_by()

    # Create a dictionary to store dates and their respective counts
    day_counts = [{"date": item['message_created__date'].strftime(
        '%Y-%m-%d'), "count": item['count']} for item in messages_counts]

    # Create a set of existing dates
    existing_dates = {item['date'] for item in day_counts}

    # Fill in missing dates with count 0
    for i in range(7):
        date = (end_date - timedelta(days=i)).date()
        formatted_date = date.strftime('%Y-%m-%d')
        if formatted_date not in existing_dates:
            day_counts.append({"date": formatted_date, "count": 0})

    # Sort the list by date
    day_counts = sorted(day_counts, key=lambda x: x['date'])

    return Response({"data": day_counts})


@api_view(['POST'])
def stat_for_seekers(request):
    user_id = request.data['id']
    today = datetime.now(timezone.utc).date()
    unique_message_count = Messages.objects.filter(
        receiver=user_id, message_created__date=today).values('conversation').distinct().count()

    unique_applied_count = rFModel.Applicants.objects.filter(
        applicant=user_id, status="applied").count()

    unique_rejected_count = rFModel.Applicants.objects.filter(
        applicant=user_id, status="rejected").count()

    pending_interview_count = rFModel.Applicants.objects.filter(
        applicant=user_id, status="applied", interview__date__gt=today
    ).count()

    return Response({"count_message": unique_message_count, "count_applied": unique_applied_count, "count_rejected": unique_rejected_count, "count_pending_interviews": pending_interview_count})


@api_view(['GET'])
def get_resume_insights(request):
    pass


@api_view(['GET'])
def get_jobpost_insights(request):
    report_type = request.GET.get('type')

    # Job Posting Summary Report
    all_jobs_count = rFModel.JobPost.objects.all().count()
    status_distribution = rFModel.JobPost.objects.values(
        'status').annotate(count=Count('status'))
    jobtitle_distribution = rFModel.JobPost.objects.values(
        'job_title').annotate(count=Count('job_title'))
    location_distribution = rFModel.JobPost.objects.values(
        'location').annotate(count=Count('location'))
    emp_type_distribution = rFModel.JobPost.objects.values(
        'emp_type').annotate(count=Count('emp_type'))

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

    title = Paragraph(
        "<font size=14><b>Job Posting Summary Report</b></font>")
    flowables.append(title)
    flowables.append(Spacer(1, 0.15 * inch))

    body = Paragraph(
        f"<font size=14>All Jobs: <b>{all_jobs_count}</b></font>")
    flowables.append(body)
    flowables.append(Spacer(1, 0.05 * inch))

    label = [item['emp_type'] for item in emp_type_distribution]
    value = [item['count'] for item in emp_type_distribution]

    img = generate_charts.generate_pie_template(
        label, value, "emp_type_chart")
    flowables.append(img)
    flowables.append(Spacer(1, 0.25 * inch))

    label = [item['status'] for item in status_distribution]
    value = [item['count'] for item in status_distribution]

    img = generate_charts.generate_pie_template(
        label, value, "status_chart")
    flowables.append(img)
    flowables.append(Spacer(1, 0.25 * inch))

    body = Paragraph(
        f"<font size=14><b>Job Positions and Their Counts</b></font>")
    flowables.append(PageBreak())
    flowables.append(body)
    flowables.append(Spacer(1, 0.1 * inch))

    label = [item['job_title'] for item in jobtitle_distribution]
    value = [item['count'] for item in jobtitle_distribution]

    img = generate_charts.generate_barh_template(
        label, value, "jobtitle_dis", "Job Positions and Their Counts")
    flowables.append(img)
    flowables.append(Spacer(1, 0.25 * inch))

    body = Paragraph(
        f"<font size=14><b>Geographical Distribution of Job Openings</b></font>")
    flowables.append(PageBreak())
    flowables.append(body)
    flowables.append(Spacer(1, 0.1 * inch))

    label = [item['location'] for item in location_distribution]
    value = [item['count'] for item in location_distribution]

    img = generate_charts.generate_column_template(
        label, value, "location_dis")
    flowables.append(img)
    flowables.append(Spacer(1, 0.25 * inch))

    title = Paragraph(
        "<font size=14><b>Skill and Qualification Analysis</b></font>")
    flowables.append(PageBreak())
    flowables.append(title)
    flowables.append(Spacer(1, 0.2 * inch))

    title = Paragraph(
        "<font size=12><b>Unveiling the Top Keywords for In-Demand Skills in a Job Post</b></font>")
    flowables.append(title)
    flowables.append(Spacer(1, 0.15 * inch))

    skills_data = rFModel.JobPost.objects.values_list('skills', flat=True)
    skills_text = ' '.join(skills_data)

    img = generate_charts.generate_word_cloud(skills_text, "skills-wc")
    flowables.append(img)
    flowables.append(Spacer(1, 0.2 * inch))

    title = Paragraph(
        "<font size=12><b>Unveiling the Top Keywords for Common Qualifications in a Job Post</b></font>")
    flowables.append(title)
    flowables.append(Spacer(1, 0.15 * inch))

    qualif_data = rFModel.JobPost.objects.values_list(
        'qualifications', flat=True)
    qualif_text = ' '.join(qualif_data)

    img = generate_charts.generate_word_cloud(qualif_text, "qualif-wc")
    flowables.append(img)

    title = Paragraph(
        "<font size=14><b>Responsibilities and Benefits Analysis</b></font>")
    flowables.append(PageBreak())
    flowables.append(title)
    flowables.append(Spacer(1, 0.2 * inch))

    title = Paragraph(
        "<font size=12><b>Unveiling the Top Keywords for Responsibilities in a Job Post</b></font>")
    flowables.append(title)
    flowables.append(Spacer(1, 0.15 * inch))

    respon_data = rFModel.JobPost.objects.values_list(
        'responsibilities', flat=True)
    beneft_data = rFModel.JobPost.objects.values_list('benefits', flat=True)

    respon_text = ' '.join(respon_data)
    beneft_text = ' '.join(beneft_data)

    img = generate_charts.generate_word_cloud(
        respon_text, "responsibilities-wc")
    flowables.append(img)
    flowables.append(Spacer(1, 0.2 * inch))

    title = Paragraph(
        "<font size=12><b>Unveiling the Top Keywords for Benefits in a Job Post</b></font>")
    flowables.append(title)
    flowables.append(Spacer(1, 0.15 * inch))

    img = generate_charts.generate_word_cloud(beneft_text, "benefits-wc")
    flowables.append(img)

    # Build the PDF
    doc.build(flowables)

    buf.seek(0)

    # Return file
    return FileResponse(buf, as_attachment=True, filename='job-insigths-report.pdf')


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

    recruiter_location_distribution = sFModel.AllProfile.objects.filter(
        fk__role__role='recruiter').values('location').annotate(count=Count('location'))
    seeker_location_distribution = sFModel.AllProfile.objects.filter(
        fk__role__role='seeker').values('location').annotate(count=Count('location'))

    img = generate_charts.generate_column(
        recruiter_location_distribution, seeker_location_distribution)
    flowables.append(img)
    flowables.append(Spacer(1, 0.4 * inch))

    flowables.append(PageBreak())
    no_profile_header = Paragraph(
        "<font size=14><b>Comprehensive Overview of Job Recruiters' Profiles</b></font>")
    flowables.append(no_profile_header)
    flowables.append(Spacer(1, 0.2 * inch))

    rld = sFModel.AllProfile.objects.filter(
        fk__role__role='recruiter').values('emp_count')
    emp_counts = [int(item['emp_count']) for item in rld]
    average_emp_count = sum(emp_counts) / \
        len(emp_counts) if len(emp_counts) > 0 else 0

    rsc = sFModel.AllProfile.objects.filter(
        fk__role__role='recruiter').values('subsidiaries_count')
    rsc_counts = [int(item['subsidiaries_count']) for item in rsc]
    average_rsc_count = sum(rsc_counts) / \
        len(rsc_counts) if len(rsc_counts) > 0 else 0

    formatted_rld = round(average_emp_count, 2)
    formatted_rsc = round(average_rsc_count, 2)

    img = generate_charts.generate_column_avg_count(
        formatted_rld, formatted_rsc)
    flowables.append(img)

    no_profile_header = Paragraph(
        "<font size=14><b>Comprehensive Overview of Job Seekers' Profiles</b></font>")
    flowables.append(Spacer(1, 0.5 * inch))
    flowables.append(no_profile_header)
    flowables.append(Spacer(1, 0.2 * inch))

    gender_count = sFModel.AllProfile.objects.filter(
        fk__role__role='seeker').values('educational_attainment').annotate(count=Count('educational_attainment'))

    img = generate_charts.generate_column_educational_attainment(gender_count)
    flowables.append(Spacer(1, 0.2 * inch))
    flowables.append(img)

    # Build the PDF
    doc.build(flowables)

    buf.seek(0)

    # Return file
    return FileResponse(buf, as_attachment=True, filename='user-overview-report.pdf')
