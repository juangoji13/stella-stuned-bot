import requests
import json

BASE_URL = "http://localhost:5000"

def test_stella_flow():
    # 1. Start session
    print("--- Starting Session ---")
    res = requests.post(f"{BASE_URL}/api/stella/start")
    session_id = res.json()["session_id"]
    print(f"Stella: {res.json()['message']}\n")

    # 2. Send invalid message
    print("--- Sending Invalid Message ---")
    payload = {"session_id": session_id, "message": "Hola, ¿cómo estás? No quiero responder."}
    res = requests.post(f"{BASE_URL}/api/stella/message", json=payload)
    data = res.json()
    print(f"User: {payload['message']}")
    print(f"Stella: {data['response']}")
    print(f"Valid: {data['is_valid']}, Question Number: {data['question_number']}\n")

    # 3. Send valid message
    print("--- Sending Valid Message ---")
    payload = {"session_id": session_id, "message": "Prefiero una ciudad grande y cosmopolita."}
    res = requests.post(f"{BASE_URL}/api/stella/message", json=payload)
    data = res.json()
    print(f"User: {payload['message']}")
    print(f"Stella: {data['response']}")
    print(f"Valid: {data['is_valid']}, Question Number: {data['question_number']}\n")

if __name__ == "__main__":
    test_stella_flow()
