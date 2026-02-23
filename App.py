from flask import Flask, render_template_string, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Full OSINT Neon UI with Multiple Features
HTML_CODE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HARSH OSINT DOWNLOADER</title>
    <style>
        :root { --neon: #0ff; --magenta: #f0f; --dark: #050505; }
        body { background: var(--dark); color: var(--neon); font-family: 'Courier New', monospace; margin: 0; overflow-x: hidden; }
        
        /* Loading/Welcome Popup */
        #welcomePopup { position: fixed; inset: 0; background: rgba(0,0,0,0.95); z-index: 9999; display: flex; justify-content: center; align-items: center; border: 2px solid var(--magenta); }
        .popup-box { text-align: center; padding: 40px; border: 1px solid var(--neon); box-shadow: 0 0 30px var(--neon); border-radius: 15px; background: #111; }
        
        .container { max-width: 800px; margin: 50px auto; padding: 20px; text-align: center; }
        h1 { font-size: 3rem; text-shadow: 0 0 15px var(--neon); letter-spacing: 10px; margin-bottom: 10px; }
        .sub-header { color: var(--magenta); margin-bottom: 30px; font-weight: bold; }

        /* Navigation Buttons */
        .nav-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 40px; }
        .mode-btn { padding: 20px; border: 2px solid var(--neon); background: transparent; color: var(--neon); cursor: pointer; font-size: 1.2rem; transition: 0.3s; }
        .mode-btn:hover { background: var(--neon); color: #000; box-shadow: 0 0 20px var(--neon); }
        .mode-btn.active { background: var(--magenta); color: #fff; border-color: var(--magenta); box-shadow: 0 0 20px var(--magenta); }

        /* Form Area */
        .download-area { border: 1px dashed var(--neon); padding: 30px; border-radius: 10px; display: none; }
        .download-area.active { display: block; }
        
        input, select { width: 90%; padding: 15px; background: #111; border: 1px solid var(--magenta); color: #fff; margin: 10px 0; border-radius: 5px; outline: none; }
        .btn-main { padding: 15px 40px; background: transparent; border: 2px solid var(--magenta); color: var(--magenta); font-weight: bold; cursor: pointer; margin-top: 20px; }
        .btn-main:hover { background: var(--magenta); color: #000; box-shadow: 0 0 30px var(--magenta); }

        /* Footer */
        footer { position: fixed; bottom: 10px; width: 100%; text-align: center; font-size: 0.8rem; opacity: 0.7; }
        .tg-link { color: var(--magenta); text-decoration: none; border: 1px solid var(--magenta); padding: 5px 10px; border-radius: 5px; }
    </style>
</head>
<body onload="initSystem()">

    <div id="welcomePopup">
        <div class="popup-box">
            <h2 style="color:var(--magenta)">SYSTEM BREACHED</h2>
            <p>Welcome to Harsh OSINT Downloader v2.0</p>
            <p style="font-size: 0.8rem;">Connecting to Secure Node...</p>
            <button class="btn-main" onclick="closePopup()">ACCESS SYSTEM</button>
            <br><br>
            <a href="https://t.me/+DvSgQwffeiwxMzg1" target="_blank" class="tg-link">JOIN TELEGRAM FOR UPDATES</a>
        </div>
    </div>

    <div class="container">
        <h1>HARSH HUB</h1>
        <p class="sub-header">INTERNAL RECONNAISSANCE & DOWNLOAD TOOL</p>

        <div class="nav-grid">
            <button class="mode-btn" onclick="showTab('yt')">YOUTUBE MODULE</button>
            <button class="mode-btn" onclick="showTab('insta')">INSTA MODULE</button>
        </div>

        <div id="yt" class="download-area">
            <h3 style="color:var(--magenta)">YouTube Downloader</h3>
            <form method="POST">
                <input type="hidden" name="platform" value="youtube">
                <input type="text" name="url" placeholder="Paste YouTube Link Here..." required>
                <select name="type">
                    <option value="video_720">Video (High Quality - 720p)</option>
                    <option value="video_360">Video (Fast - 360p)</option>
                    <option value="music">Music (MP3 Audio)</option>
                    <option value="playlist">Full Playlist (ZIP)</option>
                </select>
                <button type="submit" class="btn-main">EXECUTE DOWNLOAD</button>
            </form>
        </div>

        <div id="insta" class="download-area">
            <h3 style="color:var(--magenta)">Instagram Downloader</h3>
            <form method="POST">
                <input type="hidden" name="platform" value="instagram">
                <input type="text" name="url" placeholder="Paste Reel/Post Link..." required>
                <button type="submit" class="btn-main">BYPASS & DOWNLOAD</button>
            </form>
        </div>

        <div style="margin-top: 30px; color: #0f0;">{{ status }}</div>
    </div>

    <footer>
        MADE BY HARSH | SECURED VIA NEON-OSINT | <a href="https://t.me/+DvSgQwffeiwxMzg1" style="color:#0ff">Join Telegram</a>
    </footer>

    <script>
        function initSystem() { console.log("System Initialized..."); }
        function closePopup() { document.getElementById('welcomePopup').style.display = 'none'; }
        function showTab(tabId) {
            document.querySelectorAll('.download-area').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.mode-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            event.target.classList.add('active');
        }
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    status = ""
    if request.method == 'POST':
        url = request.form['url']
        platform = request.form.get('platform')
        dtype = request.form.get('type', 'best')
        
        try:
            # Setting Quality based on user choice
            if dtype == 'music':
                ydl_opts = {'format': 'bestaudio/best', 'outtmpl': '/tmp/%(title)s.%(ext)s'}
            elif dtype == 'video_360':
                ydl_opts = {'format': 'best[height<=360]', 'outtmpl': '/tmp/%(title)s.%(ext)s'}
            else:
                ydl_opts = {'format': 'best', 'outtmpl': '/tmp/%(title)s.%(ext)s'}

            ydl_opts['no_check_certificate'] = True
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                path = ydl.prepare_filename(info)
                return send_file(path, as_attachment=True)
        except Exception as e:
            status = f"System Error: Traceback Ignored."
            
    return render_template_string(HTML_CODE, status=status)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    
