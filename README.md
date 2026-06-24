# 노래방 점수 분석 프로그램 PLUS

SW 프로그래밍 기말고사 구현과제 제출용 Flask 웹앱입니다. 13주차 TODO에서 작성한 "노래방 점수 분석 프로그램" 아이디어를 실제 작동하는 웹서비스 형태로 구현했습니다.

## 핵심 기능

- 노래방 점수 입력: 곡명, 가수, 점수, 날짜, 메모 저장
- JSON 파일 저장: 프로그램을 종료해도 기록 유지
- 대시보드: 총 기록 수, 등록 곡 수, 전체 평균, 최고점 표시
- 곡별 분석: 평균, 최고점, 최근 3회 변화, 첫 기록 대비 상승폭, 안정도 계산
- 자동 분석 리포트: 최고점, 가장 많이 연습한 곡, 가장 크게 오른 곡, 다음 연습 추천 제공
- 시각화: 전체 점수 추세 그래프, 곡별 미니 그래프, 상세 점수 그래프
- 데이터 관리: 기록 삭제, CSV 다운로드, JSON API 제공
- 외부 배포 대응: gunicorn, Procfile, runtime.txt, PORT 환경변수, 0.0.0.0 바인딩 포함

## 로컬 실행 방법

```bash
cd karaoke_score_analyzer_plus
python -m pip install -r requirements.txt
python app.py
```

브라우저에서 아래 주소로 접속합니다.

```text
http://127.0.0.1:5000
```

## 외부 접속용 배포 방법(Render 기준)

1. 이 폴더 전체를 GitHub 저장소에 업로드합니다.
2. Render.com에서 New Web Service를 선택합니다.
3. GitHub 저장소를 연결합니다.
4. Build Command를 아래처럼 설정합니다.

```bash
pip install -r requirements.txt
```

5. Start Command를 아래처럼 설정합니다.

```bash
gunicorn app:app
```

6. 배포가 완료되면 Render가 `https://프로젝트이름.onrender.com` 형태의 공개 접속 주소를 제공합니다.

## Replit 빠른 배포 방법

1. Replit에서 Python 프로젝트를 만듭니다.
2. 이 폴더의 파일을 업로드합니다.
3. Shell에서 `pip install -r requirements.txt`를 실행합니다.
4. Run command를 `gunicorn app:app --bind 0.0.0.0:5000`로 설정합니다.
5. Webview의 Open in new tab 주소를 제출 보고서의 공개 URL로 사용합니다.

## 파일 구조

```text
karaoke_score_analyzer_plus/
├─ app.py                  # Flask 서버와 분석 로직
├─ wsgi.py                 # 배포용 진입점
├─ requirements.txt         # Flask, gunicorn
├─ Procfile                 # Render 배포용 실행 명령
├─ runtime.txt              # Python 버전
├─ data/scores.json         # 점수 저장 데이터
├─ templates/base.html      # 공통 레이아웃
├─ templates/index.html     # 대시보드 화면
├─ templates/song_detail.html # 곡별 상세 분석 화면
├─ static/style.css         # 화면 디자인
└─ notes/vibe_coding_process.md # 제작 과정 기록
```
