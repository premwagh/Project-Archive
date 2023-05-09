
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def data_similarity(new_data, existing_data):
    v = TfidfVectorizer().fit_transform([existing_data, new_data]).toarray()
    return cosine_similarity([v[0], v[1]])[0][1]


def uniqueness_percentile(new_data, existing_data):
    return 100-data_similarity(new_data, existing_data)*100


def uniqueness_percentile_against_data_list(new_data, existing_data_set):
    max_similarity = 0
    for existing_data in existing_data_set:
        max_similarity = max(
            max_similarity, data_similarity(new_data, existing_data))

    return 100-max_similarity*100
