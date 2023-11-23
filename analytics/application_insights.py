from recruiter import models as rfm

from . import generate_charts
from datetime import datetime
from django.db.models import Count
from collections import Counter


def extract_applied_insights(start_date):
    if start_date is not None:
        applied = rfm.Applicants.objects.filter(applied__gte=start_date).exclude(
            applied__isnull=True).values('applied')
    else:
        applied = rfm.Applicants.objects.values('applied')

    interview = rfm.Applicants.objects.values('interview')
    hire = rfm.Applicants.objects.values('hire')

    combined_list = list(zip(applied, interview, hire))

    applied_to_interview_diff = []
    applied_to_hire_diff = []

    for applied, interview, hire in combined_list:
        applied_date = applied['applied']

        # Calculate the difference between applied and interview, if interview is not None
        if interview['interview'] is not None:
            interview_date = interview['interview']
            applied_to_interview_diff.append(
                (interview_date - applied_date).days)

        # Calculate the difference between applied and hire, if hire is not None
        if hire['hire'] is not None:
            hire_date = hire['hire']
            applied_to_hire_diff.append((hire_date - applied_date).days)

    ath = sum(applied_to_hire_diff) / len(applied_to_interview_diff)
    ati = sum(applied_to_interview_diff) / len(applied_to_interview_diff)

    col_labels = ["Average Waiting Time Applied to Interview",
                  "Average Waiting Time Applied to Hire"]
    col_values = [ati, ath]

    img = generate_charts.generate_column_template(
        col_labels, col_values, 'ttw-cc')
    return img


def extract_status_insights(start_date):
    if start_date is not None:
        status = rfm.Applicants.objects.filter(applied__gte=start_date).exclude(applied__isnull=True).values(
            'status').annotate(count=Count('status'))
    else:
        status = rfm.Applicants.objects.values(
            'status').annotate(count=Count('status'))

    pie_labels = [item['status'] for item in status]
    pie_values = [item['count'] for item in status]

    img = generate_charts.generate_pie_template(
        pie_labels, pie_values, 'si-pc')

    return img


def extract_average_count():
    apply_count = rfm.Applicants.objects.values(
        'applicant__account').annotate(count=Count('applicant__account'))
    application_count = rfm.Applicants.objects.values(
        'job__allprofile__account').annotate(count=Count('job__allprofile__account'))

    col_labels = ["Application per post", "Sent application per account"]

    ac = [item['count'] for item in apply_count]
    ax = [item['count'] for item in application_count]

    sac = sum(ac) / len(ac)
    sax = sum(ax) / len(ax)

    col_values = [sac, sax]

    img = generate_charts.generate_column_template(
        col_labels, col_values, 'evc-cc')
    return img


def extract_compatibility(start_date):
    if start_date is not None:
        compatibility = rfm.Applicants.objects.filter(
            applied__gte=start_date).values('compatibility')
    else:
        compatibility = rfm.Applicants.objects.values('compatibility')

    # Replace 'Unsuccessful' with 0 and convert to float
    compatibility_values = [float(item['compatibility']) if item['compatibility']
                            != 'Unsuccessful' else 0.0 for item in compatibility]
    avg_val = sum(
        compatibility_values) / len(compatibility_values)
    min_val = min(compatibility_values)
    max_val = max(compatibility_values)

    col_labels = ["Lowest Compatibility Score",
                  "Average Compatibility Score", "Highest Compatibiltiy Score"]
    col_values = [min_val, avg_val, max_val]

    img = generate_charts.generate_column_template(
        col_labels, col_values, "cs-bc")
    return img
