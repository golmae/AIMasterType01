# check_models.py
import google.generativeai as genai
import os

# 1. API 키 로드
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("오류: GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")
    sys.exit(1)

genai.configure(api_key=api_key)

# 2. 'generateContent'를 지원하는 모델 리스트 가져오기
print("API 키로 접근 가능한 모델 리스트를 확인합니다...")
print("('generateContent' 지원 모델만 표시됩니다.)\n")

try:
    count = 0
    for model in genai.list_models():
        # 'generateContent' (우리가 쓰려는 기능)를 지원하는 모델만 필터링
        if 'generateContent' in model.supported_generation_methods:
            print(f" - {model.name}")
            count += 1

    if count == 0:
        print("\n[중요] 'generateContent'를 지원하는 모델을 찾을 수 없습니다.")
        print("Google AI Studio 또는 Google Cloud Project에서 API 권한을 확인해야 할 수 있습니다.")

except Exception as e:
    print(f"모델 리스트를 가져오는 중 오류 발생: {e}")