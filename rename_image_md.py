import re

def rename_images_in_markdown(md_file_path: str, post_name: str):
    # 1. 마크다운 파일 내용 읽어오기
    print(md_file_path)
    with open(md_file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 2. 새로 쓸 내용 초기화
    new_content = content

    # 3. 해당 패턴을 모두 찾는다. (정규식은 예시에 맞춰 구성)
    pattern = r"!\[image\.png\]\([^)]+\)"
    matches = re.findall(pattern, content)

    # 4. 찾은 순서대로 치환
    count = 0
    for match in matches:
        # 첫 번째 이미지는 image.png, 이후는 image 1.png, image 2.png ... 식으로 만들기
        if count == 0:
            new_file_name = "image.png"
        else:
            new_file_name = f"image {count}.png"
        
        # 치환될 새 경로
        replacement = f"![image.png](../assets/img/posts/{post_name}/{new_file_name})"
        
        # 한 번에 하나씩(순차적으로) 치환
        new_content = new_content.replace(match, replacement, 1)
        count += 1

    # 5. 최종 수정 내용을 원본 파일에 다시 덮어쓰기
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":

    filename = "2025-03-16-review_25_3_2"
    rename_images_in_markdown("_posts/" + filename + ".md", filename)
