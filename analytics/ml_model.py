import pickle
import os
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Get the directory of the script you're running:
dir_path = os.path.dirname(os.path.realpath(__file__))

# Combine this with your relative path
csv_path = os.path.join(dir_path, 'utils', 'jobs.pkl')
rsm_path = os.path.join(dir_path, 'utils', 'resume_list.pkl')

jobs = pickle.load(open(csv_path, 'rb'))
resume = pickle.load(open(rsm_path, 'rb'))


def provide_recommendation(input_skills):
    tfidf_vectorizer = TfidfVectorizer()
    resume_matrix = tfidf_vectorizer.fit_transform(resume['Resume_str'])

    input_skills_text = ' '.join(input_skills)
    input_tfidf = tfidf_vectorizer.transform([input_skills_text])

    similarity = cosine_similarity(input_tfidf, resume_matrix)
    sim_scores = list(enumerate(similarity[0]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:]

    job_indices = [i[0] for i in sim_scores]
    recommended_jobs = resume.iloc[job_indices]

    compatibility_percentages = []
    for index, row in recommended_jobs.iterrows():
        compatibility_percentage = cosine_similarity(tfidf_vectorizer.transform(
            [input_skills_text]), resume_matrix[index])[0][0] * 100
        compatibility_percentages.append(compatibility_percentage)

    print("Recommended Jobs:")
    recommended_jobs_info = []
    tracker = []

    for i in range(10):
        job_title = recommended_jobs['Category'].iloc[i]
        compatibility_percentage = compatibility_percentages[i]

        if compatibility_percentage != 0:
            compatibility_percentage += 50

        if job_title not in tracker:
            job_info = {
                "Job Title": job_title,
                "Compatibility Percentage": f"{compatibility_percentage:.2f}%"
            }
            recommended_jobs_info.append(job_info)

        tracker.append(job_title)

    return recommended_jobs_info


def provide_compatibility(job_title, input_skills):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(jobs['combined'])

    try:
        # Find the index of the specified job title
        job_index = jobs[jobs['Title'] == job_title].index[0]

        input_skills_text = ' '.join(input_skills)
        input_tfidf = tfidf_vectorizer.transform([input_skills_text])

        compatibility_percentage = cosine_similarity(
            input_tfidf, tfidf_matrix[job_index])[0][0] * 100

        if compatibility_percentage != 0:
            compatibility_percentage += 50

        return f"{compatibility_percentage:.2f}"

    except Exception as e:
        return "Unsuccessful"
