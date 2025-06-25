import json
import nltk
import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# 🔽 Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# 🔽 Load spaCy model
    nlp = spacy.load('en_core_web_sm')

# 🔽 Load intents from JSON
with open('intents.json', 'r') as file:
    data = json.load(file)

# 🔄 Convert intents into dictionaries
intents = {}
responses = {}

for item in data['intents']:
    tag = item['tag']
    patterns = item['patterns']
    response = item['response']
    intents[tag] = patterns
    responses[tag] = response

# 🧠 Fallback response
responses["unknown"] = "Oops 🤖! I'm not sure I got that. Try rephrasing? I promise I'm not ignoring you!"

# 🧹 Preprocessing with lemmatization
def preprocess_with_lemmatization(text):
    doc = nlp(text.lower())
    stop_words = set(stopwords.words('english'))
    return " ".join([token.lemma_ for token in doc if token.text not in stop_words and token.is_alpha])

# 🎯 Intent recognition using semantic similarity
def get_intent(user_input):
    processed_input = preprocess_with_lemmatization(user_input)
    user_doc = nlp(processed_input)

    best_intent = "unknown"
    max_score = 0.0
    threshold = 0.75

    for intent, patterns in intents.items():
        for pattern in patterns:
            processed_pattern = preprocess_with_lemmatization(pattern)
            pattern_doc = nlp(processed_pattern)

            if not user_doc.vector_norm or not pattern_doc.vector_norm:
                continue

            similarity = user_doc.similarity(pattern_doc)
            if similarity > max_score:
                max_score = similarity
                best_intent = intent

    return best_intent if max_score >= threshold else "unknown"

# 💬 Get personality response
def get_response(intent):
    return responses.get(intent, responses["unknown"])

# 🤖 Main chatbot loop
def chatbot():
    print("Jerry 🧠: Yo! I'm Jerry, your not-so-boring assistant 😎. Ask me anything or type 'exit' to dip out.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Jerry 🧠: Catch ya later, genius! ✌️")
            break

        intent = get_intent(user_input)
        response = get_response(intent)
        print("Jerry 🧠:", response)

# 🚀 Run chatbot
if __name__ == "__main__":
    chatbot()
