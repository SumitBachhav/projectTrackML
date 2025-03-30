import re
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the model (directly, no .pkl file)
model = SentenceTransformer('all-mpnet-base-v2')

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def getEmbedding(text):
    preprocessed = preprocess_text(text)
    return model.encode(preprocessed)

def string_to_list(string):
    cleaned_string = string.strip("[]")
    return np.array([float(num) for num in cleaned_string.split()]).reshape(1, -1)
