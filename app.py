
from flask import Flask, render_template, request
from faq_agent import load_faq_data, is_in_faq_data, get_answer_from_faq
from dotenv import load_dotenv
import os
import requests

app = Flask(__name__)

# Load the FAQ data (ensure to load it only once for efficiency)
faq_data = load_faq_data()

# HuggingFace API key (same as before)
load_dotenv()  # Load environment variables from .env file
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# HuggingFace LLM response
def llm_generated_response(query):
    API_URL = "https://api-inference.huggingface.co/models/distilbert-base-cased-distilled-squad"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    # Dynamically build context from faq_data
    context_lines = [f"{question} {answer}" for question, answer in faq_data.items()]
    context = "\n".join(context_lines)

    payload = {
        "inputs": {
            "question": query,
            "context": context
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        answer = result.get('answer', "Sorry, I couldn't find an answer for that.")
        # If the model returns a very short or incomplete answer, return a fallback message
        if len(answer.split()) <= 2:  # Check if the answer is too short
            return "Sorry, I couldn't find a detailed answer for that. Here's what I know: " + answer
        return answer
    else:
        return "Sorry, I'm unable to process your request right now."


# AI agent decision logic
def ai_agent_response(user_query):
    if is_in_faq_data(user_query, faq_data):
        return get_answer_from_faq(user_query, faq_data)  # Get rule-based answer
    else:
        return llm_generated_response(user_query)  # Fallback to LLM model


# Home route
@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    question = None
    if request.method == "POST":
        question = request.form["query"]
        answer = ai_agent_response(question)
    return render_template("index.html", answer=answer, question=question)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
# app.run(host="0.0.0.0", port=port, debug=True)





