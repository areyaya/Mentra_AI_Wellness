#!/usr/bin/env python3
"""
Quick test script to verify Mentra AI chatbot is working
Run this while backend is running to test the conversation flow
"""

import requests
import json
import time

API_URL = "http://localhost:5000/api"
USER_ID = f"test_user_{int(time.time())}"

def test_conversation():
    """Simulate a full conversation to test analysis"""
    
    print("=" * 60)
    print("MENTRA AI CHATBOT TEST")
    print("=" * 60)
    print()
    
    # Test messages that should trigger analysis
    messages = [
        "Hi, I need help",
        "I've been feeling really anxious lately",
        "It started about a month ago when work got stressful",
        "I can't sleep and my heart races all the time",
        "On a scale of 1-10, probably an 8",
    ]
    
    for i, message in enumerate(messages, 1):
        print(f"\n📤 Message {i}: \"{message}\"")
        print("-" * 60)
        
        try:
            response = requests.post(
                f"{API_URL}/analyze-message",
                json={
                    "message": message,
                    "user_id": USER_ID
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Show AI reply
                print(f"🤖 AI Reply: {data.get('reply', 'No reply')}")
                print(f"📊 Status: {data.get('status', 'unknown')}")
                
                # If analysis complete, show results
                if data.get('status') == 'complete':
                    print("\n" + "=" * 60)
                    print("✅ ANALYSIS COMPLETE!")
                    print("=" * 60)
                    
                    analysis = data.get('final_analysis', {})
                    
                    # Show detected concerns
                    concerns = analysis.get('detected_concerns', {})
                    if concerns:
                        print("\n🔍 Detected Concerns:")
                        for concern, details in concerns.items():
                            severity = details.get('severity', 'unknown')
                            confidence = details.get('confidence', 0) * 100
                            print(f"   - {concern.replace('_', ' ').title()}: {severity} (confidence: {confidence:.0f}%)")
                    
                    # Show recommended group
                    group = analysis.get('recommended_group_type', 'Not specified')
                    print(f"\n👥 Recommended Group: {group}")
                    
                    # Show urgency
                    urgency = analysis.get('urgency_level', 'normal')
                    print(f"⚠️  Urgency Level: {urgency}")
                    
                    # Show themes
                    themes = analysis.get('key_themes', [])
                    if themes:
                        print(f"\n🏷️  Key Themes: {', '.join(themes)}")
                    
                    print("\n" + "=" * 60)
                    break
                
            else:
                print(f"❌ Error: HTTP {response.status_code}")
                print(f"Response: {response.text}")
                break
                
        except requests.exceptions.ConnectionError:
            print("❌ ERROR: Cannot connect to backend!")
            print("   Make sure backend is running: python3 backend_api.py")
            return False
        except requests.exceptions.Timeout:
            print("⏱️  ERROR: Request timed out!")
            print("   This might mean OpenAI is slow or API key is invalid")
            return False
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            return False
        
        # Wait a bit between messages
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE!")
    print("=" * 60)
    return True

def test_health():
    """Test if backend is running"""
    print("Checking backend health...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend is running")
            print(f"   OpenAI Status: {data.get('openai_api', 'unknown')}")
            return True
        else:
            print(f"❌ Backend returned error: {response.status_code}")
            return False
    except:
        print("❌ Backend is not running!")
        print("   Start it with: cd backend && python3 backend_api.py")
        return False

if __name__ == "__main__":
    print()
    if test_health():
        print()
        test_conversation()
    else:
        print("\n⚠️  Fix backend connection and try again")
