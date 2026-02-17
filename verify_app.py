import urllib.request
import sys

url = "http://localhost:8501"
try:
    with urllib.request.urlopen(url) as response:
        if response.status == 200:
            print(f"Successfully connected to {url}")
            content = response.read().decode('utf-8')
            if "Streamlit" in content or "noscript" in content:
                print("Streamlit app signature found.")
            else:
                print("Warning: Content does not look like Streamlit.")
        else:
            print(f"Failed with status code: {response.status}")
            sys.exit(1)
except Exception as e:
    print(f"Connection failed: {e}")
    sys.exit(1)
