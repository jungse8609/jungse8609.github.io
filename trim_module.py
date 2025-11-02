import os
import re
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- ⚙️ 설정: 이 부분을 사용자의 환경에 맞게 수정하세요 ---

# 1. 감시할 포스트 폴더
# 스크립트가 있는 위치를 기준으로 ./_posts/ 를 의미합니다.
WATCH_DIR = os.path.join(os.getcwd(), "_posts")

# 2. 이미지를 생성할 기본 폴더
# ./assets/img/posts/ 를 의미합니다.
IMG_BASE_DIR = os.path.join(os.getcwd(), "assets", "img", "posts")

# -----------------------------------------------------

# 이미지 카운터를 위한 변수
# re.sub 콜백 함수에서 사용하기 위해 리스트(변경 가능한 객체)로 만듭니다.
image_counter = [0]

def process_new_post(post_filepath):
    """새로운 포스트 파일이 생성될 때 실행될 메인 함수"""
    try:
        filename = os.path.basename(post_filepath)
        # 파일 확장자를 제거한 이름 (예: 2025-03-16-title)
        post_name = os.path.splitext(filename)[0]

        logging.info(f"🚀 새 포스트 감지: {filename}")

        # --- 작업 1: 이미지 폴더 생성 ---
        new_img_folder_path = os.path.join(IMG_BASE_DIR, post_name)
        os.makedirs(new_img_folder_path, exist_ok=True)
        logging.info(f"✅ 폴더 생성 완료: {new_img_folder_path}")

        # --- 작업 2: 포스트 내용 수정 ---
        
        # re.sub의 콜백 함수 정의
        def path_replacer(match):
            """
            정규식에 매칭되는 각 이미지 경로를 순차적으로 변경합니다.
            """
            # 원본 alt text (예: image.png)는 그대로 유지
            alt_text = match.group(1) 
            
            # 이미지 이름 생성 (image.png, image 1.png, image 2.png ...)
            count = image_counter[0]
            if count == 0:
                img_name = "image.png"
            else:
                img_name = f"image {count}.png"
            
            image_counter[0] += 1 # 카운터 증가

            # 사용자가 요청한 새 경로 형식
            new_path = f"../assets/img/posts/{post_name}/{img_name}"
            
            # 전체 마크다운 이미지 태그 반환
            return f"![{alt_text}]({new_path})"

        # 카운터 초기화
        image_counter[0] = 0
        
        # 파일이 완전히 쓰일 때까지 잠시 대기 (파일 생성 직후 읽으면 내용이 비어있을 수 있음)
        time.sleep(0.5) 

        # 파일 읽기
        with open(post_filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 정규식 패턴: ![모든문자](모든문자)
        # 그룹 1: alt_text, 그룹 2: old_path
        # (원본 경로가 어떻든 상관없이 순서대로 모두 바꿉니다)
        pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
        
        # 정규식을 사용해 내용 치환
        new_content = pattern.sub(path_replacer, content)

        # 변경된 내용이 있을 경우에만 파일 쓰기
        if content != new_content:
            with open(post_filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            logging.info(f"✅ 이미지 경로 수정 완료: {filename}")
        else:
            logging.info(f"ℹ️ 수정할 이미지 경로가 없습니다: {filename}")

    except Exception as e:
        logging.error(f"❌ 파일 처리 중 오류 발생: {filename}, 오류: {e}")

class PostEventHandler(FileSystemEventHandler):
    """파일 시스템 이벤트 핸들러"""
    
    def on_created(self, event):
        """파일이 생성되었을 때"""
        if not event.is_directory and event.src_path.endswith(('.md', '.markdown')):
            # 마크다운 파일일 경우에만 실행
            process_new_post(event.src_path)

    def on_modified(self, event):
        """파일이 수정되었을 때"""
        if not event.is_directory and event.src_path.endswith(('.md', '.markdown')):
            # 마크다운 파일일 경우에만 실행
            logging.info(f"📝 'on_modified' 이벤트 감지: {event.src_path}")
            process_new_post(event.src_path)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    logging.info(f"📁 감시 시작: {WATCH_DIR}")
    
    event_handler = PostEventHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=False) # 하위 폴더는 감시 안 함
    
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("🛑 감시 중지.")
    observer.join()