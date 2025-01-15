from PIL import Image
from PIL import PngImagePlugin
import os
from flask import Flask, render_template, request, send_file, url_for,redirect,flash

app = Flask(__name__)
app.secret_key='secret'

os.makedirs('decode_uploads', exist_ok=True)
os.makedirs('uploads', exist_ok=True)
os.makedirs('encoded', exist_ok=True)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ENCODED_FOLDER'] = 'encoded'
app.config['DECODE_UPLOAD_FOLDER'] = 'decode_uploads'

def encode_message_in_image(image_path, message):
    img = Image.open(image_path)
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("message", message)
    encoded_path = os.path.join(app.config['ENCODED_FOLDER'], "encoded_image.png")
    img.save(encoded_path, pnginfo=metadata)

def decode_message_from_image(image_path):
        img = Image.open(image_path)
        metadata = img.info
        message = metadata.get("message", None)
        return message


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/cod', methods=['GET', 'POST'])
def cod():
    encoded_image_url = None
    if request.method == 'POST':
        
        file = request.files['file']
        message = request.form.get('message', '')

        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(upload_path)
        encode_message_in_image(upload_path, message)
        encoded_image_url = url_for('download', filename='encoded_image.png')

    return render_template("cod.html", encoded_image_url=encoded_image_url)

@app.route('/download/<filename>')
def download(filename):
    encoded_image_path = os.path.join(app.config['ENCODED_FOLDER'], filename)

    absolute_path = os.path.abspath(encoded_image_path)

    return send_file(absolute_path, as_attachment=True)

@app.route('/dec', methods=['GET', 'POST'])
def dec():
    decoded_message = None
    if request.method == 'POST':
        file = request.files['file']
        upload_path = os.path.join(app.config['DECODE_UPLOAD_FOLDER'], file.filename)
        file.save(upload_path)

        decoded_message = decode_message_from_image(upload_path)
        if not decoded_message:
            flash("No message found in the image!", "warning")
            return redirect('/dec')

    return render_template("dec.html", decoded_message=decoded_message)

@app.route('/links')
def links():
    return render_template('links.html')

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True, port=8000)
