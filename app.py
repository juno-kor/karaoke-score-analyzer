import csv
import io
import json
import math
import os
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from statistics import mean, pstdev
from urllib.parse import quote

from flask import Flask, Response, jsonify, redirect, render_template, request, url_for

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "scores.json"

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


def load_records():
    DATA_FILE.parent.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_records(records):
    DATA_FILE.parent.mkdir(exist_ok=True)
    DATA_FILE.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")


def parse_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except Exception:
        return date.today()


def sorted_records(records):
    return sorted(records, key=lambda r: (parse_date(r.get("date", "")), int(r.get("id", 0))))


def group_records(records):
    groups = defaultdict(list)
    for record in sorted_records(records):
        groups[record["song"]].append(record)
    return groups


def safe_average(values):
    return round(mean(values), 1) if values else 0


def trend_label(delta):
    if delta >= 1.5:
        return "상승세"
    if delta <= -1.5:
        return "하락세"
    return "유지"


def trend_class(delta):
    if delta >= 1.5:
        return "good"
    if delta <= -1.5:
        return "bad"
    return "neutral"


def sparkline_points(scores, width=180, height=56, pad=8):
    if not scores:
        return ""
    if len(scores) == 1:
        y = height / 2
        return f"{pad},{y:.1f} {width-pad},{y:.1f}"
    min_s, max_s = min(scores), max(scores)
    span = max(max_s - min_s, 1)
    points = []
    for i, score in enumerate(scores):
        x = pad + (width - pad * 2) * i / (len(scores) - 1)
        y = pad + (height - pad * 2) * (1 - (score - min_s) / span)
        points.append(f"{x:.1f},{y:.1f}")
    return " ".join(points)


def song_stat(title, song_records):
    scores = [int(r["score"]) for r in song_records]
    first = scores[0]
    last = scores[-1]
    recent3 = scores[-3:]
    prev3 = scores[-6:-3]
    recent_avg = safe_average(recent3)
    previous_avg = safe_average(prev3) if prev3 else safe_average(scores[:-3]) if len(scores) > 3 else safe_average(scores[:1])
    delta_recent = round(recent_avg - previous_avg, 1) if previous_avg else 0
    improvement = last - first
    deviation = round(pstdev(scores), 1) if len(scores) >= 2 else 0
    consistency = max(0, round(100 - deviation * 8, 1))
    goal = min(100, max(scores) + 2)
    # 단기 목표는 해당 곡의 기존 최고점보다 2점 높은 점수로 잡는다.
    # 단, 노래방 점수 범위를 고려해 최대 100점을 넘지 않게 한다.
    # needed는 최근 3회 평균을 기준으로 목표까지 얼마나 남았는지 계산한다.
    needed = round(max(0, goal - recent_avg), 1)
    if delta_recent >= 1.5:
        comment = f"최근 평균이 이전보다 {delta_recent:+.1f}점 올라 상승세입니다. 이 곡은 지금 연습 효율이 좋습니다."
    elif delta_recent <= -1.5:
        comment = f"최근 평균이 이전보다 {delta_recent:+.1f}점 내려갔습니다. 같은 구간에서 틀리는 부분을 메모로 확인하는 것이 좋습니다."
    else:
        comment = "최근 점수가 큰 흔들림 없이 유지되고 있습니다. 최고점 갱신을 위해 세부 구간 연습이 필요합니다."
    return {
        "title": title,
        "artist": song_records[-1].get("artist", ""),
        "count": len(scores),
        "average": safe_average(scores),
        "best": max(scores),
        "worst": min(scores),
        "first": first,
        "last": last,
        "improvement": improvement,
        "recent_avg": recent_avg,
        "previous_avg": previous_avg,
        "delta_recent": delta_recent,
        "trend": trend_label(delta_recent),
        "trend_class": trend_class(delta_recent),
        "deviation": deviation,
        "consistency": consistency,
        "goal": goal,
        "needed": needed,
        "comment": comment,
        "sparkline": sparkline_points(scores),
        "records": song_records,
    }


def build_dashboard(records):
    records = sorted_records(records)
    groups = group_records(records)
    song_rows = [song_stat(title, rows) for title, rows in groups.items()]
    song_rows.sort(key=lambda x: (x["average"], x["best"]), reverse=True)

    scores = [int(r["score"]) for r in records]
    overall = {
        "total_records": len(records),
        "song_count": len(groups),
        "average": safe_average(scores),
        "best_record": max(records, key=lambda r: int(r["score"])) if records else None,
        "latest_record": records[-1] if records else None,
        "today": date.today().isoformat(),
        "timeline": sparkline_points(scores, width=520, height=120, pad=16),
    }

    insights = []
    if records:
        best = overall["best_record"]
        insights.append({
            "title": "최고점 기록",
            "body": f"현재 최고점은 '{best['song']}'의 {best['score']}점입니다. 지금까지 입력한 기록 중 가장 높은 점수입니다.",
            "tone": "good",
        })
    if song_rows:
        favorite = max(song_rows, key=lambda s: s["count"])
        insights.append({
            "title": "가장 많이 연습한 곡",
            "body": f"'{favorite['title']}'을/를 {favorite['count']}회 기록했습니다. 기록 횟수가 많아 점수 흐름을 비교하기 좋은 곡입니다.",
            "tone": "neutral",
        })
        improved_candidates = [s for s in song_rows if s["count"] >= 2]
        if improved_candidates:
            improved = max(improved_candidates, key=lambda s: s["improvement"])
            insights.append({
                "title": "가장 크게 오른 곡",
                "body": f"'{improved['title']}'은/는 첫 기록 대비 {improved['improvement']:+}점 변화했습니다. 처음 기록과 최근 기록의 차이가 가장 큰 곡입니다.",
                "tone": "good" if improved["improvement"] >= 0 else "bad",
            })
        stable_candidates = [s for s in song_rows if s["count"] >= 3]
        if stable_candidates:
            stable = max(stable_candidates, key=lambda s: s["consistency"])
            insights.append({
                "title": "가장 안정적인 곡",
                "body": f"'{stable['title']}'의 안정도 지수는 {stable['consistency']}점입니다. 점수 변동 폭이 작을수록 안정도가 높게 계산됩니다.",
                "tone": "neutral",
            })
        focus = min(song_rows, key=lambda s: (s["recent_avg"], -s["count"]))
        insights.append({
            "title": "다음 연습 추천",
            "body": f"'{focus['title']}'은/는 최근 평균 {focus['recent_avg']}점입니다. 기존 최고점보다 2점 높은 {focus['goal']}점을 단기 목표로 잡았습니다. 평균 기준 {focus['needed']}점 향상이 필요합니다.",
            "tone": "bad" if focus["needed"] >= 3 else "neutral",
        })
    return overall, song_rows, insights


@app.template_filter("urlquote")
def urlquote_filter(value):
    return quote(value)


@app.route("/")
def index():
    records = load_records()
    q = request.args.get("q", "").strip()
    filtered = records
    if q:
        filtered = [r for r in records if q.lower() in r.get("song", "").lower() or q.lower() in r.get("artist", "").lower()]
    overall, song_rows, insights = build_dashboard(filtered)
    latest = list(reversed(sorted_records(filtered)))[:10]
    return render_template("index.html", overall=overall, song_rows=song_rows, insights=insights, latest=latest, q=q)


@app.route("/add", methods=["POST"])
def add_score():
    records = load_records()
    song = request.form.get("song", "").strip()
    artist = request.form.get("artist", "").strip()
    memo = request.form.get("memo", "").strip()
    raw_score = request.form.get("score", "").strip()
    input_date = request.form.get("date", date.today().isoformat()).strip() or date.today().isoformat()
    try:
        score = int(raw_score)
    except ValueError:
        return redirect(url_for("index"))
    if not song or score < 0 or score > 100:
        return redirect(url_for("index"))
    next_id = max([int(r.get("id", 0)) for r in records], default=0) + 1
    records.append({"id": next_id, "date": input_date, "song": song, "artist": artist, "score": score, "memo": memo})
    save_records(records)
    return redirect(url_for("song_detail", title=song))


@app.route("/song/<path:title>")
def song_detail(title):
    records = [r for r in load_records() if r.get("song") == title]
    if not records:
        return redirect(url_for("index"))
    records = sorted_records(records)
    stat = song_stat(title, records)
    chart_points = sparkline_points([int(r["score"]) for r in records], width=720, height=180, pad=24)
    return render_template("song_detail.html", stat=stat, records=records, chart_points=chart_points)


@app.route("/delete/<int:record_id>", methods=["POST"])
def delete_record(record_id):
    records = load_records()
    records = [r for r in records if int(r.get("id", 0)) != record_id]
    save_records(records)
    return redirect(request.referrer or url_for("index"))


@app.route("/download.csv")
def download_csv():
    records = sorted_records(load_records())
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "date", "song", "artist", "score", "memo"])
    for r in records:
        writer.writerow([r.get("id"), r.get("date"), r.get("song"), r.get("artist"), r.get("score"), r.get("memo")])
    csv_text = "\ufeff" + output.getvalue()
    return Response(csv_text, mimetype="text/csv; charset=utf-8", headers={"Content-Disposition": "attachment; filename=karaoke_scores.csv"})


@app.route("/api/stats.json")
def api_stats():
    overall, song_rows, insights = build_dashboard(load_records())
    return jsonify({"overall": overall, "songs": song_rows, "insights": insights})


@app.route("/health")
def health():
    return "ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
