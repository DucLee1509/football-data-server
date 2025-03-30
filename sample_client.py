import requests

# Server URL (change if needed)
SERVER_URL = "https://41c9-116-110-42-54.ngrok-free.app"

# Step 1: Send a GET request to /hello
response = requests.get(f"{SERVER_URL}/remove")
print("GET /remove Response:", response.text)

# Step 2: Upload a WAV file
# file_path = r"C:\Users\lehuu\Documents\Personal_Project\Football\audio_files\test.3gp"  # Replace with your actual file path

# try:
#     with open(file_path, "rb") as file:
#         files = {"file": (file_path, file, "audio/wav")}
#         upload_response = requests.post(f"{SERVER_URL}/upload", files=files)
#         print("POST /upload Response:", upload_response.text)
# except FileNotFoundError:
#     print(f"Error: File '{file_path}' not found.")
