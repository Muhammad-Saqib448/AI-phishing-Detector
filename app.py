from flask import Flask, request, jsonify
from sklearn.ensemble import RandomForestClassifier
import numpy as np

app = Flask(__name__)

print("Training a simple model...")

X_train_dummy = [
    [10, 0, 0, 2, 1],
    [80, 1, 1, 5, 0],
    [15, 0, 0, 2, 1],
    [90, 1, 0, 4, 0]
]
y_train_dummy = [0, 1, 0, 1]

model = RandomForestClassifier(n_estimators=10)
model.fit(X_train_dummy, y_train_dummy)
print("Model Trained and ready!")

# 2. Define the Feature Extractor
def extract_features(url):
    features = []
    
    # Feature 1: Length of URL (long URLs are suspicious)
    features.append(1 if len(url) > 54 else 0)
    
    # Feature 2: Presence of '@' symbol
    features.append(1 if "@" in url else 0)
    
    # Feature 3: Presence of double slash '//' (after the initial https://)
    features.append(1 if url.rfind('//') > 7 else 0)
    
    # Feature 4: Count of dots (subdomains) - legitimate sites usually have fewer
    features.append(url.count('.'))
    
    # Feature 5: HTTPS token in domain (e.g., http://https-secure-login.com)
    features.append(1 if 'https' in url.split('//')[0] else 0) # Simple check for protocol
    
    # Note: In a real scenario, you would match these EXACTLY to the 30 UCI features.
    # For this demo, we are just using a few common ones to show the pipeline.
    
    return np.array(features).reshape(1, -1)

@app.route('/predict', methods=['POST'])
def predict():
    # Get json data from the user
    try:
        
      data = request.get_json()
      url_to_check = data.get('url')
    
      # 1. Convert URL -> Numbers (Feature Extraction)
      features = extract_features(url_to_check)

      # 2. Ask the AI for prediction
      prediction = model.predict(features)

      # 3. Return the result
      result = "PHISHING" if prediction[0] == 1 else "SAFE"

      return jsonify({
          'url': url_to_check,
          'prediction': result,
          'status': 200
      })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
@app.route('/')
def home():
    return "<h1>Cybersecurity AI is Active!</h1><p>Send a POST request to /predict to test the model.</p>"

if __name__ == '__main__':
    app.run(debug=True)
