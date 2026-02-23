from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Neon Hacker UI Code
HTML_CODE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Harsh Pro Downloader</title>
    <style>
        body { background: #050505; color: #0ff; font-family: 'Courier New', monospace; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; overflow: hidden; }
        .container { text-align: center; padding: 40px; border: 2px solid #0ff; border-radius: 20px; background: rgba(0, 0, 0, 0.9); box-shadow: 0 0 20px #0ff; width: 90%; max-width: 500px; }
        h1 { font-size: 2.5rem; text-shadow: 0 0 10px #0ff, 0 0 30px #f0f; letter-spacing: 5px; }
        input { width: 100%; padding: 15px; background: #111; border: 1px solid #f0f; color: #fff; margin: 20px 0; border-radius: 5px; outline: none; box-shadow: 0 0 5px #f0f; }
        .btn-neon { padding: 15px 30px; border: 2px solid #0ff; background: transparent; color: #0ff; font-weight: bold; cursor: pointer; border-radius: 5px; transition: 0.4s; width: 100%; }
        .btn-neon:hover { background: #0ff; color: #000; box-shadow: 0 0 40px #0ff; }
        #welcomePopup { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: #111; border: 3px solid #f0f; padding: 30px; z-index: 1000; box-shadow: 0 0 50px #f0f; border-radius: 15px; text-align: center; }
        .overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 999; }
    </style>
</head>
<body onload="showPopup()">
    <div class="overlay" id="overlay"></div>
    <div id="welcomePopup">
        <h2 style="color: #f0f;">System Breach Successful!</h2>
        <p>Welcome Harsh Download Website</p>
        <button class="btn-neon" onclick="closePopup()">ENTER SYSTEM</button>
    </div>
    <div class="container">
        <h1>HARSH HUB</h1>
        <form method="POST">
            <input type="text" name="url" placeholder="Paste YouTube/Insta Link..." required>
            <button type="submit" class="btn-neon">INITIALIZE DOWNLOAD</button>
        </form>
        <div style="margin-top:20px; color:#0f0;">{{ status }}</div>
    </div>
    <script>
        function showPopup() { document.getElementById('welcomePopup').style.display = 'block'; document.getElementById('overlay').style.display = 'block'; }
        function closePopup() { document.getElementById('welcomePopup').style.display = 'none'; document.getElementById('overlay').style.display = 'none'; }
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    status = ""
    if request.method == 'POST':
        url = request.form['url']
        try:
            ydl_opts = {'format': 'best', 'outtmpl': '/tmp/%(title)s.%(ext)s', 'no_check_certificate': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                path = ydl.prepare_filename(info)
                return send_file(path, as_attachment=True)
        except Exception:
            status = "Error: Link invalid or Server Busy!"
    return render_template_string(HTML_CODE, status=status)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
