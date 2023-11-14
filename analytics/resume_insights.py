from seekerFolder import models
from userFolder import models as ufm

from . import generate_charts
from django.db.models import Count
from collections import Counter


def extract_resume_obj():
    resume_obj = models.Resume.objects.values_list(
        'resume_objective', flat=True)
    resume_data = ' '.join(resume_obj)

    img = generate_charts.generate_word_cloud(
        resume_data, "resume_obj_insight")
    return img


def extract_skills():
    skills_text = models.Resume.objects.values_list(
        'skill', flat=True
    )
    skills_data = ' '.join(skills_text)
    img = generate_charts.generate_word_cloud(
        skills_data, "seeker_skills_insight")

    return img


def extract_references():
    ref_rel_text = models.Resume.objects.values(
        'relationship_to_you', 'institution')
    ref_ins_text = models.Resume.objects.values(
        'institution').annotate(count=Count('institution'))

    split_institutions = [item['institution'].split(
        '_+_')[0] for item in ref_ins_text]
    institution_counts = Counter(split_institutions)
    ibh_label = list(institution_counts.keys())
    ibh_value = list(institution_counts.values())
    img1 = generate_charts.generate_barh_template(
        ibh_label, ibh_value, "ibh-instit", "Institutions of Commonly Used Reference Contact")

    split_rel_to_you = [item['relationship_to_you'].split(
        '_+_')[0] for item in ref_rel_text]
    rel_to_you_counts = Counter(split_rel_to_you)
    ibh_label = list(rel_to_you_counts.keys())
    ibh_value = list(rel_to_you_counts.values())
    img2 = generate_charts.generate_barh_template(
        ibh_label, ibh_value, "ibh-reltoyou", "Relation of Commonly Used Reference Contact to the Job Seeker")

    return {"img1": img1, "img2": img2}

    # institution_counts = Counter(split_institutions)
    # print(institution_counts)


def extract_compatibility():
    compatibility = models.Resume.objects.values(
        "compatibility")
    print(compatibility)


def extract_spoken_language():
    pass


def extract_hobbies_interest():
    hni = models.Resume.objects.values('hobbies_interest')
    split_hni = [item['hobbies_interest'].split(
        '_+_')[0] for item in hni]
    split_hni_again = [value.split(', ') for value in split_hni]

    flat_list = [item for sublist in split_hni_again for item in sublist]

    hni_counts = Counter(flat_list)

    bar_labels = list(hni_counts.keys())
    bar_values = list(hni_counts.values())

    img = generate_charts.generate_column_template(
        bar_labels, bar_values, "hni-cg")
    return img


def extract_basic_count():
    with_resume = models.Resume.objects.all().count()
    without_resume = ufm.Account.objects.filter(role__role="seeker").count()

    pie_values = [with_resume, without_resume - with_resume]
    pie_labels = ["With Resume", "Without Resume"]

    img = generate_charts.generate_pie_template(
        pie_labels, pie_values, "ribs-pie")
    return img
