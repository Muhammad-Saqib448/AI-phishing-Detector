import requests

api_url = "http://127.0.0.1:5000/predict"

print("------ PHISHING DETECtOR CLI -------")
print("Type a URL to scan it. Type 'Exit' to quit.")

while True:
    user_input = input("\nEnter URL to Scan: ")

    if user_input.lower() == 'exit':
        print("Exiting...")
        break
    try:
        payload = {'url': user_input}
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            result = response.json()
            prediction = result['prediction']
            print(f"Result: [{prediction}]")
            print(f"Scanned: {result['url']}")
        else:
            print(f"Error from server: {response.text}")
    except requests.exceptions.ConnectionError:
        print("ERROR: Is your app.py server running? I can't connect to it.")
        