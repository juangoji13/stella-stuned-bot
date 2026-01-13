import google.generativeai as genai
API_KEY = 'AIzaSyAOI2idlsMjDpV4CGJAC53JTvD0zWdZifg'
genai.configure(api_key=API_KEY)
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
