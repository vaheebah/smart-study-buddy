#!/usr/bin/env python
"""
Sample script to test the Smart Study Buddy system end-to-end
"""
import sys
sys.path.insert(0, '../backend')

import requests
import json

API_URL = "http://localhost:8000/api"

# Step 1: Register a test user
print("Step 1: Registering test user...")
register_response = requests.post(
    f"{API_URL}/auth/register",
    json={
        "name": "Test Student",
        "email": "student@example.com",
        "password": "testpass123"
    }
)
print(f"Register status: {register_response.status_code}")

# Step 2: Login
print("\nStep 2: Logging in...")
login_response = requests.post(
    f"{API_URL}/auth/login",
    json={
        "email": "student@example.com",
        "password": "testpass123"
    }
)
print(f"Login status: {login_response.status_code}")

if login_response.status_code == 200:
    token = login_response.json()['access_token']
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 3: List notes
    print("\nStep 3: Listing notes...")
    notes_response = requests.get(f"{API_URL}/notes/list", headers=headers)
    print(f"Notes: {notes_response.json()}")
    
    print("\n✅ Basic workflow test complete!")
else:
    print("❌ Login failed")
