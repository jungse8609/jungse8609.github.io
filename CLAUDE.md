# 블로그 작업 지침

Chirpy 기반 Jekyll + GitHub Pages 블로그. 구조 상세: [.claude/blog-structure.md](.claude/blog-structure.md)

## 응답 규칙
1. **간결·짧게.** 불필요한 단어·토큰 최소화. 서론·군더더기 없이 핵심만.
2. **항상 한글.**
3. **사용자 글의 말투·어투는 절대 건드리지 않는다.** 내가 고치는 건 잘못된 *블로그 형식*(front matter, 이미지 경로, 태그 대소문자, 파일명/폴더명)뿐. 문장·어조·표현·오탈자는 손대지 않음. 형식 외 수정이 필요해 보이면 고치지 말고 짚어만 준다.

## 말투 (새 글 초안·다듬기 시)
- 반말·구어체. 격식체("~습니다") 금지.
- 회고: 솔직·캐주얼("~하자!!", "개같이 실패", "~지롱"), `TODO/KEEP/QUESTION` 구조.
- 기술글: 설명형 반말("~한다", "~겠다"), 개조식 불릿 + 코드블록 + 이미지.
- 에세이/독후감: 사색적 반말("~인 것 같다", "~일지도 모른다").
- 이모지 거의 안 씀.

## 새 글 발행
스킬 **new-post** 사용. 핵심만:
- 파일: `_posts/YYYY-MM-DD-slug.md` (KST 오늘 날짜).
- Front matter 고정 형식:
  ```yaml
  ---
  title: "제목"
  date: YYYY-MM-DD HH:MM:SS +0900 # 대한민국 기준
  categories: [Cat]
  tags: [tag]  # TAG는 소문자로 만들어야 한다.
  ---
  ```
- `tags`는 소문자(보통 categories 소문자판).
- 이미지: `assets/img/posts/<slug>/`, 본문 참조 `../assets/img/posts/<slug>/image.png`. 실제 파일명과 본문 참조 대조 필수.
- 발행: 파일·이미지 배치 → `git add` → `git commit -m 'feat: Upload a new post "제목"'` → `git push`. push하면 Actions가 자동 배포.

## 커밋 규칙
- **커밋 메시지에 `Co-Authored-By: Claude` 등 co-author 표기 절대 넣지 않는다.** 어떤 Claude/AI 서명·트레일러도 금지.

## 카테고리 관례
회고=`[Review]`/`[review]`, 블로그제작=`[Blog]`/`[blog]`, 운영체제=`[OS, CS]`/`[os, cs]`, 독후감=`[Book]`/`[book]`, 해커톤·대회후기(`[… 후기]`)=`[Hackathon]`/`[hackathon]`.
