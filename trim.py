import os
import re
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- ⚙️ 설정 ---
WATCH_DIR = os.path.join(os.getcwd(), "_posts")
IMG_BASE_DIR = os.path.join(os.getcwd(), "assets", "img", "posts")
# -----------------------------------------------------

image_counter = [0]

def create_image_folder(post_filepath):
    """(on_created용) 이미지 폴더만 생성"""
    try:
        filename = os.path.basename(post_filepath)
        post_name = os.path.splitext(filename)[0]
        
        new_img_folder_path = os.path.join(IMG_BASE_DIR, post_name)
        os.makedirs(new_img_folder_path, exist_ok=True)
        logging.info(f"✅ (Created) 이미지 폴더 생성: {new_img_folder_path}")
        
    except Exception as e:
        logging.error(f"❌ (Created) 폴더 생성 오류: {e}")

def fix_image_paths(post_filepath):
    """(on_modified용) 이미지 경로 수정"""
    try:
        filename = os.path.basename(post_filepath)
        post_name = os.path.splitext(filename)[0]

        # 콜백 함수
        def path_replacer(match):
            alt_text = match.group(1) 
            count = image_counter[0]
            img_name = f"image {count}.png" if count > 0 else "image.png"
            image_counter[0] += 1 
            new_path = f"../assets/img/posts/{post_name}/{img_name}"
            return f"![{alt_text}]({new_path})"

        image_counter[0] = 0 # 카운터 초기화
        
        time.sleep(0.5) # 파일 잠금 방지
        
        with open(post_filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        pattern = re.compile(r'!\[(.*?)\]\((.*?)\)')
        new_content = pattern.sub(path_replacer, content)

        if content != new_content:
            with open(post_filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            logging.info(f"✅ (Modified) 이미지 경로 수정 완료: {filename}")
        else:
            logging.info(f"ℹ️ (Modified) 이미지 경로 변경 없음: {filename}")

    except Exception as e:
        logging.error(f"❌ (Modified) 파일 처리 중 오류: {filename}, {e}")


class PostEventHandler(FileSystemEventHandler):
    """파일 시스템 이벤트 핸들러"""
    
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(('.md', '.markdown')):
            logging.info(f"🆕 'on_created' 감지: {event.src_path}")
            # 새 파일이 생성되면 -> 이미지 폴더만 만듭니다.
            create_image_folder(event.src_path)

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(('.md', '.markdown')):
            logging.info(f"📝 'on_modified' 감지: {event.src_path}")
            # 파일 내용이 수정되면 -> 이미지 경로를 고칩니다.
            fix_image_paths(event.src_path)

# --- (이하 스크립트 실행 부분은 동일) ---
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    os.makedirs(WATCH_DIR, exist_ok=True)
    os.makedirs(IMG_BASE_DIR, exist_ok=True)
    
    logging.info(f"📁 감시 시작: {WATCH_DIR}")
    
    event_handler = PostEventHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=False)
    
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logging.info("🛑 감시 중지.")
    observer.join()