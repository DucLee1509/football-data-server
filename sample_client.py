import requests

# Server URL (change if needed)
SERVER_URL = "https://7f28-116-110-42-54.ngrok-free.app"

# Upload audio file
file_path = r"C:\Users\lehuu\Documents\Personal_Project\football-data-server\audio_files\test.3gp"  # Replace with your actual file path

try:
    with open(file_path, "rb") as file:
        files = {"file": (file_path, file, "audio/wav")}
        upload_response = requests.post(f"{SERVER_URL}/upload", files=files)
        print("POST /upload Response:", upload_response.text)
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")

# Update data
update_data = {
    "name": "Nam",
    "parameter": "Kiến tạo"
}

# update_data = {
#     "name": "",
#     "parameter": "Bàn thua"
# }

update_response = requests.post(f"{SERVER_URL}/update", json=update_data)
print("POST /update Response:", update_response.text)

# Revert latest data
response = requests.get(f"{SERVER_URL}/remove")
print("GET /remove Response:", response.text)

# Get members
response = requests.get(f"{SERVER_URL}/members")
# print("GET /members Response:", response.text)
with open('client.txt', 'w', encoding="utf-8") as file:
    file.write(f"GET /members Response: {response.text}\n")

# Get parameters
response = requests.get(f"{SERVER_URL}/parameters")
# print("GET /parameters Response:", response.text)
with open('client.txt', 'a', encoding="utf-8") as file:
    file.write(f"GET /parameters Response: {response.text}\n")
