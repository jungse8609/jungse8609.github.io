import os
import pytz
import re  # 👈 [추가] 정규식을 통해 파일명을 안전하게 만듭니다.
from datetime import datetime

# --- ⚙️ 설정 ---
POSTS_DIR = os.path.join(os.getcwd(), "_posts")
# ---------------

def create_new_post():
    print("--- ✍️  새 포스트 생성기 ---")
    
    # 1. KST 시간대 및 날짜 형식 설정 (동일)
    kst = pytz.timezone('Asia/Seoul')
    now = datetime.now(kst)
    date_str = now.strftime('%Y-%m-%d %H:%M:%S %z')
    filename_date = now.strftime('%Y-%m-%d') # 파일명에 사용할 날짜

    # 2. 사용자 입력 받기
    post_slug = input("📝 파일명(slug)을 입력하세요 (예: my-first-post): ")
    title_input = input("🏷️ 제목을 입력하세요 (예: 첫 포스트): ")
    categories_input = input("🗂️ 카테고리를 입력하세요 (쉼표(,)로 구분, 예: Blog, Python): ")

    # 3. 카테고리 및 태그 처리
    if categories_input:
        # "Blog, Python" 입력 시 -> ['Blog', 'Python']
        categories_list = [c.strip() for c in categories_input.split(',')]
        categories_str = f"[{', '.join(categories_list)}]"
        
        # tags: categories의 내용을 소문자로 (['blog', 'python'])
        tags_list = [c.strip().lower() for c in categories_input.split(',')]
        tags_str = f"[{', '.join(tags_list)}]"
    else:
        # 카테고리를 입력하지 않은 경우
        categories_list = [] # 👈 빈 리스트로 초기화
        categories_str = "[...]"
        tags_str = "[...]"

    # slug 후처리
    if post_slug:
        # 1. 소문자로 변경
        post_slug = post_slug.lower()
        # 2. 공백을 하이픈으로 변경
        post_slug = post_slug.replace(' ', '-')
        # 3. (안전장치) 알파벳, 숫자, 하이픈 외의 특수문자 모두 제거
        post_slug = re.sub(r'[^\w\-]', '', post_slug)
    else:
        # 입력이 없는 경우 기본값 사용
        post_slug = "post"
        print("⚠️ 파일명이 입력되지 않아 기본 파일명 'post'를 사용합니다.")

    # 4. 제목 처리
    if title_input:
        title_str = f'"{title_input}"'
    else:
        title_str = '"[] "'
        print("⚠️ 제목이 입력되지 않아 기본 제목 '[] '을 사용합니다.")

    # 5. 최종 템플릿 조합
    template = f"""---
title: {title_str}
date: {date_str} # 대한민국 기준
categories: {categories_str}
tags: {tags_str}  # TAG는 소문자로 만들어야 한다.
---

"""

    # 6. 파일 생성
    # 👈 [수정] 파일명이 날짜와 파생된 slug로 조합됩니다.
    final_filename = f"{filename_date}-{post_slug}.md"
    final_filepath = os.path.join(POSTS_DIR, final_filename)

    os.makedirs(POSTS_DIR, exist_ok=True)

    if os.path.exists(final_filepath):
        print(f"⚠️ 파일이 이미 존재합니다: {final_filepath}")
    else:
        with open(final_filepath, 'w', encoding='utf-8') as f:
            f.write(template)
        print(f"✅ 파일 생성 완료: {final_filepath}")
        print("이제 `automate_posts.py`가 폴더 생성을 처리합니다.")

if __name__ == "__main__":
    create_new_post()