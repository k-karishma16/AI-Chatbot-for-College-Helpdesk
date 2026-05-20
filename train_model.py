import sqlite3
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# Connect to database
conn = sqlite3.connect("chatbot.db")
cursor = conn.cursor()

# Get FAQ questions
cursor.execute("SELECT question FROM faq")
questions = [row[0] for row in cursor.fetchall()]
conn.close()

# Check if questions exist
if not questions:
    print("No FAQs found in database. Run app.py first.")
    exit()

# Create model folder if not exists
os.makedirs("model", exist_ok=True)

# Vectorize questions
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

# Train nearest neighbor model
model = NearestNeighbors(n_neighbors=1, metric="cosine")
model.fit(X)

# Save vectorizer
with open("model/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

# Save model
with open("model/chatbot_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained successfully.")
