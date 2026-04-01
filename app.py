from flask import Flask, request, send_file, jsonify, render_template_string
import io
import struct
import zlib
import datetime
import json
import os

app = Flask(__name__)


tracking_log = []

def create_1x1_png():
    
    def make_png_chunk(chunk_type, data):
        chunk_len = len(data)
        chunk_data = chunk_type + data
        crc = zlib.crc32(chunk_data) & 0xFFFFFFFF
        return struct.pack('>I', chunk_len) + chunk_data + struct.pack('>I', crc)

    png_header = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', 1, 1, 8, 6, 0, 0, 0)
    ihdr = make_png_chunk(b'IHDR', ihdr_data)
    raw_pixel = b'\x00\x00\x00\x00\x00'
    compressed = zlib.compress(raw_pixel)
    idat = make_png_chunk(b'IDAT', compressed)
    iend = make_png_chunk(b'IEND', b'')

    return png_header + ihdr + idat + iend





@app.route('/')
def index():
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()  

@app.route('/email')
def email_preview():
    path = os.path.join(os.path.dirname(__file__), 'email.html')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()  

@app.route('/pixel.png')
def tracking_pixel():
    
    now = datetime.datetime.now()

    
    event = {
        "id": len(tracking_log) + 1,
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "timestamp_ms": int(now.timestamp() * 1000),
        "ip_address": request.headers.get('X-Forwarded-For', request.remote_addr),
        "user_agent": request.headers.get('User-Agent', 'Unknown'),
        "referer": request.headers.get('Referer', 'Direct / No Referer'),
        "accept_language": request.headers.get('Accept-Language', 'Unknown'),
        "accept_encoding": request.headers.get('Accept-Encoding', 'Unknown'),
        "dnt": request.headers.get('DNT', 'Not set'),
        "campaign": request.args.get('campaign', 'none'),
        "user_id": request.args.get('uid', 'anonymous'),
        "email_id": request.args.get('eid', 'none'),
        "connection_type": request.headers.get('X-Connection-Type', 'Unknown'),
        "sec_fetch_site": request.headers.get('Sec-Fetch-Site', 'Unknown'),
        "sec_fetch_dest": request.headers.get('Sec-Fetch-Dest', 'Unknown'),
        "all_headers": dict(request.headers),
    }

    
    ua = event["user_agent"].lower()
    if 'firefox' in ua:
        event["browser"] = "Firefox"
    elif 'edg' in ua:
        event["browser"] = "Microsoft Edge"
    elif 'chrome' in ua:
        event["browser"] = "Chrome"
    elif 'safari' in ua:
        event["browser"] = "Safari"
    else:
        event["browser"] = "Unknown Browser"

    if 'windows' in ua:
        event["os"] = "Windows"
    elif 'mac' in ua:
        event["os"] = "macOS"
    elif 'linux' in ua:
        event["os"] = "Linux"
    elif 'android' in ua:
        event["os"] = "Android"
    elif 'iphone' in ua or 'ipad' in ua:
        event["os"] = "iOS"
    else:
        event["os"] = "Unknown OS"

    tracking_log.append(event)
    print(f"[PIXEL HIT] {event['timestamp']} | IP: {event['ip_address']} | {event['browser']} on {event['os']} | Campaign: {event['campaign']}")

    
    png_data = create_1x1_png()
    response = send_file(
        io.BytesIO(png_data),
        mimetype='image/png',
        as_attachment=False
    )
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/api/logs')
def get_logs():
    
    return jsonify({
        "total": len(tracking_log),
        "events": list(reversed(tracking_log))
    })


@app.route('/api/clear')
def clear_logs():
    tracking_log.clear()
    return jsonify({"status": "cleared"})


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  TRACKING PIXEL DEMO SERVER")
  
    print("="*60)
    print("\n  Dashboard: http://localhost:5001")
    print("  Fake Email: http://localhost:5001/email")
    print("  Pixel URL:  http://localhost:5001/pixel.png")
    print("\n  Watching for pixel hits...\n")
    
    app.run(debug=True, port=5001)


