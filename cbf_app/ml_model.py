import pickle
import os
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Get the directory of the script you're running:
dir_path = os.path.dirname(os.path.realpath(__file__))

# Combine this with your relative path
csv_path = os.path.join(dir_path, 'utils', 'jobs.pkl')
rsm_path = os.path.join(dir_path, 'utils', 'resume_list_new.pkl')

jobs = pickle.load(open(csv_path, 'rb'))
resume = pickle.load(open(rsm_path, 'rb'))


def provide_recommendation(input_skills):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    resume_matrix = tfidf_vectorizer.fit_transform(resume['combined'])

    input_skills_text = ' '.join(input_skills)
    input_tfidf = tfidf_vectorizer.transform([input_skills_text])

    weights = {'JobDescription': 0.4,
               'JobRequirment': 0.4, 'RequiredQual': 0.2}
    similarity = cosine_similarity(input_tfidf, resume_matrix.multiply(weights['JobDescription'])) + \
        cosine_similarity(input_tfidf, resume_matrix.multiply(weights['JobRequirment'])) + \
        cosine_similarity(input_tfidf, resume_matrix.multiply(
            weights['RequiredQual']))

    sim_scores = list(enumerate(similarity[0]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:]

    job_indices_scores = [{"Job Title": resume.iloc[i[0]]['Title'],
                           "Compatibility Percentage": min(i[1], 1) * 100}
                          for i in sim_scores]

    # Remove duplicates
    seen = set()
    job_indices_scores_no_duplicates = []

    for job in job_indices_scores:
        job_title = job['Job Title']
        compatibility_score = job.get('Compatibility Score', 0.0)  # Handle missing score gracefully

        if job_title not in seen and compatibility_score != 0.0:
            job_indices_scores_no_duplicates.append(job)
            seen.add(job_title)

    ret_val = job_indices_scores_no_duplicates[:10]

    return ret_val


def provide_compatibility_apply(job_title, input_skills):
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

        value = f"{compatibility_percentage:.2f}%"

        return value

    except Exception as e:
        return "Unsuccessful"
