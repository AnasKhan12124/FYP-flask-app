
import pandas as pd

# Load FAQ data from CSV
def load_faq_data():
    faq_df = pd.read_csv('faq_data.csv')
    return dict(zip(faq_df['Question'].str.lower(), faq_df['Answer']))

# Check if the query exists in the FAQ data
def is_in_faq_data(query, faq_data):
    query = query.lower().strip()  # Strip spaces and lower case
    return query in faq_data

# Fetch the answer for a query
def get_answer_from_faq(query, faq_data):
    return faq_data.get(query.lower(), "Sorry, I couldn't find an answer for that.")
