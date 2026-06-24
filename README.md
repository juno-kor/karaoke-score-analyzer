# 노래방 점수 분석 프로그램 PLUS

노래방에서 부른 곡의 점수를 기록하고, 곡별 점수 변화와 평균, 최고점, 안정도, 최근 추세를 확인할 수 있는 Flask 기반 웹 프로그램입니다.

## 1. 외부 접속 주소

아래 주소로 접속하면 별도 설치 없이 웹에서 바로 사용할 수 있습니다.

https://karaoke-score-analyzer.onrender.com

Render 무료 배포 환경 특성상 오랫동안 접속이 없으면 서버가 잠시 대기 상태가 될 수 있습니다. 이 경우 첫 접속 시 화면이 뜨기까지 약 30초에서 1분 정도 걸릴 수 있습니다. 한 번 열린 뒤에는 정상적으로 사용할 수 있습니다.

## 2. 주요 기능

- 곡명, 가수명, 점수, 메모 입력
- 입력한 노래방 점수 기록 저장
- 전체 기록 목록 확인
- 곡별 평균 점수, 최고 점수, 최저 점수 확인
- 최근 3회 평균과 이전 기록 비교
- 상승세, 하락세, 유지 상태 자동 판정
- 점수 안정도 계산
- 전체 점수 추세 그래프 확인
- 곡별 상세 페이지에서 개별 곡의 변화 확인
- 기록 CSV 다운로드
- 기록 삭제 기능

## 3. 로컬 실행 방법

외부 접속 사이트가 일시적으로 느리거나 접속되지 않을 경우, ZIP 파일을 내려받아 로컬 컴퓨터에서도 실행할 수 있습니다.

### 3-1. 필요한 패키지 설치

프로젝트 폴더에서 터미널 또는 PowerShell을 열고 아래 명령어를 실행합니다.

```bash
py -m pip install -r requirements.txt
```

만약 `py` 명령어가 동작하지 않으면 아래 명령어를 사용할 수 있습니다.

```bash
python -m pip install -r requirements.txt
```

### 3-2. 프로그램 실행

```bash
py app.py
```

또는

```bash
python app.py
```

실행 후 브라우저에서 아래 주소로 접속합니다.

http://127.0.0.1:5000

또는

http://localhost:5000

## 4. 폴더 구조

```text
karaoke_score_analyzer_plus/
├─ app.py
├─ requirements.txt
├─ Procfile
├─ runtime.txt
├─ data/
│  └─ scores.json
├─ static/
│  └─ style.css
└─ templates/
   ├─ base.html
   ├─ index.html
   └─ song_detail.html
```

## 5. 주요 파일 설명

- `app.py`: Flask 서버 실행, 기록 저장, 분석 계산, 페이지 연결을 담당합니다.
- `data/scores.json`: 노래방 점수 기록이 저장되는 파일입니다.
- `templates/base.html`: 공통 화면 구조를 담당합니다.
- `templates/index.html`: 메인 화면과 전체 분석 화면을 담당합니다.
- `templates/song_detail.html`: 곡별 상세 분석 화면을 담당합니다.
- `static/style.css`: 화면 디자인을 담당합니다.
- `requirements.txt`: 실행에 필요한 Python 패키지 목록입니다.
- `Procfile`: Render 배포 시 실행 명령을 알려주는 파일입니다.
- `runtime.txt`: Render 배포 시 사용할 Python 버전을 지정하는 파일입니다.

## 6. 배포 정보

이 프로젝트는 GitHub 저장소와 Render Web Service를 연결하여 배포했습니다.

- 배포 플랫폼: Render
- 실행 방식: Gunicorn으로 Flask 앱 실행
- Start Command: `gunicorn app:app`
- Build Command: `pip install -r requirements.txt`
- 외부 접속 주소: https://karaoke-score-analyzer.onrender.com
