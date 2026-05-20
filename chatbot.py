import pickle
from database import get_faqs

# Load saved vectorizer
with open("model/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# Load saved trained model
with open("model/chatbot_model.pkl", "rb") as f:
    model = pickle.load(f)


def get_response(user_input):
    try:
        faqs = get_faqs()

        if not faqs:
            return "No FAQs available in database."

        answers = [answer for question, answer in faqs]

        # Convert user input into vector
        X = vectorizer.transform([user_input])

        # Find nearest FAQ
        distance, index = model.kneighbors(X)

        score = 1 - distance[0][0]

        # Threshold for confidence
        if score > 0.35:
            return answers[index[0][0]]

        return "Sorry, I couldn't understand that. Please ask differently."

    except Exception as e:
        print("Chatbot Error:", e)
        return "Sorry, something went wrong."
