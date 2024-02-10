from flask import Flask, render_template, request, send_file
import qrcode
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    url = request.form.get('url')
    if not url:
        return "URL is empty", 400

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)
    
    img_path = os.path.join(static_folder, 'qrcode.png')
    img.save(img_path)
    return render_template('result.html', img_path=img_path)

@app.route('/download')
def download():
    img_path = request.args.get('img_path')
    if not img_path or not os.path.exists(img_path):
        return "QR code file not found", 404
    
    return send_file(img_path, as_attachment=True)

