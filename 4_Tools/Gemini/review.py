# review.py (최종 수정본: """ 문법 제거)
import google.generativeai as genai
import os
import sys

# 1. API 키 로드 (환경 변수에서)
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("오류: GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")
    sys.exit(1)

try:
    genai.configure(api_key=api_key)
except Exception as e:
    print("API 키 설정 중 오류가 발생했습니다. 키가 유효한지 확인하세요.")
    print(e)
    sys.exit(1)

# 2. 프롬프트 및 모델 설정
model = genai.GenerativeModel('models/gemini-2.5-pro')

# 3. CLI 인자(프롬프트) 및 stdin(diff) 읽기
try:
    # CLI로 전달된 첫 번째 인자 (e.g., "이 코드 리뷰해줘")
    user_prompt = sys.argv[1]
except IndexError:
    print("오류: 프롬프트를 입력해야 합니다. e.g., python review.py \"코드 리뷰해줘\"")
    sys.exit(1)

# 파이프(|)로 전달된 git diff 내용 (stdin)
diff_content = sys.stdin.read()

# 4. Gemini API에 전송할 최종 프롬프트 구성
# """...""" 대신 ( ) 와 \n (줄바꿈)을 사용하는 안전한 방식으로 변경
prompt_template = (
    "당신은 나의 수석 아키텍트 조언자입니다.\n"
    "나는 유니티(C#)로 1인 게임을 개발 중이며, 재사용 가능한 프레임워크를 구축하는 것이 목표입니다.\n\n"
    "아래의 git diff 내용을 검토하고, 내가 요청한 사항에 대해 조언해 주세요.\n\n"
    "[나의 요청]\n"
    "{0}\n\n"
    "[Git Diff 내용]\n"
    "```diff\n"
    "{1}\n"
    "```\n\n"
    "[조언 시작]\n"
)

# 템플릿에 변수를 삽입
final_prompt = prompt_template.format(user_prompt, diff_content)

# 5. API 호출 및 응답 출력
try:
    response = model.generate_content(final_prompt)
    print(response.text)
except Exception as e:
    # .format()을 사용하도록 수정
    print("API 호출 중 오류 발생: {0}".format(e))
