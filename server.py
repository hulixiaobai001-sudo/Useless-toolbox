#!/usr/bin/env python3
"""小鲸鱼回传服务器 - 接收Useless Toolbox发来的数据"""
import http.server
import json
import os
from datetime import datetime

MESSAGES_FILE = "/workspace/whale_inbox.json"

class WhaleHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        body = self.read(content_len) if content_len else b'{}'
        
        try:
            data = json.loads(body)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data['_received_at'] = timestamp
            
            # Save to inbox
            messages = []
            if os.path.exists(MESSAGES_FILE):
                with open(MESSAGES_FILE, 'r') as f:
                    messages = json.load(f)
            messages.append(data)
            with open(MESSAGES_FILE, 'w') as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "message": "🐋 小鲸鱼收到！"}).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())
    
    def do_GET(self):
        if self.path == '/messages':
            messages = []
            if os.path.exists(MESSAGES_FILE):
                with open(MESSAGES_FILE, 'r') as f:
                    messages = json.load(f)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(messages[::-1], ensure_ascii=False, indent=2).encode())
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write('🐋 小鲸鱼回传服务器运行中'.encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    port = 8899
    server = http.server.HTTPServer(('127.0.0.1', port), WhaleHandler)
    print(f'🐋 小鲸鱼回传服务器启动在 http://127.0.0.1:{port}')
    print(f'📨 POST / - 接收消息')
    print(f'📖 GET /messages - 查看消息')
    server.serve_forever()
