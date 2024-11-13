import urllib.parse
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
import os
import json
import requests
from PIL import Image
import time
import logging
import sys

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32 MB

DATA_FILE = 'data/users.json'

# 确保必要的目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('data', exist_ok=True)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)
else:
    with open(DATA_FILE, 'r+') as f:
        content = f.read().strip()
        if not content:
            f.seek(0)
            json.dump([], f)

def get_city_coordinates(city, country):
    """获取城市的地理坐标"""
    try:
    
        time.sleep(1)
        search_query = f"{city}, {country}"
        response = requests.get(
            f"https://nominatim.openstreetmap.org/search",
            params={
                'q': search_query,
                'format': 'json',
                'limit': 1
            },
            headers={'User-Agent': 'YourApp/1.0'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data:
                return {
                    'lat': float(data[0]['lat']),
                    'lng': float(data[0]['lon'])
                }
    except Exception as e:
        print(f"Error getting coordinates for {city}, {country}: {e}")
    
    # 如果获取失败，返回国家级别的坐标
    return get_country_coordinates(country)

def get_country_coordinates(country):
    try:
        response = requests.get(f"https://restcountries.com/v3.1/name/{country}")
        data = response.json()
        if data and len(data) > 0:
            latlng = data[0].get('latlng', [0, 0])
            return {'lat': latlng[0], 'lng': latlng[1]}
    except Exception as e:
        print(f"Error getting country coordinates: {e}")
    return {'lat': 0, 'lng': 0}

def resize_image(image_path, max_size=(800, 800)):
    """压缩图片尺寸"""
    try:
        with Image.open(image_path) as img:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            img.save(image_path, optimize=True, quality=85)
    except Exception as e:
        print(f"Error resizing image: {e}")

@app.route('/api/countries')
def get_countries():
    """获取国家列表"""
    try:
        response = requests.get("https://countriesnow.space/api/v0.1/countries")
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cities', methods=['POST'])
def get_cities():
    """获取城市列表"""
    try:
        country = request.json.get('country')
        response = requests.post(
            "https://countriesnow.space/api/v0.1/countries/cities",
            json={"country": country}
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        country = request.form['country']
        city = request.form['city']
        story = request.form['story'] 
        

        photo = request.files['photo']
        if photo:
            photo_filename = f"{name}_{photo.filename}".replace(" ", "_")
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
            photo.save(photo_path)
            resize_image(photo_path)
            
            coordinates = get_city_coordinates(city, country)
            
            user_data = {
                "name": name,
                "phone": phone,
                "country": country,
                "city": city,
                "story": story,  
                "photo": urllib.parse.quote(photo_filename),
                "coordinates": coordinates
            }
            
            with open(DATA_FILE, 'r+') as f:
                data = json.load(f)
                data.append(user_data)
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=4)

            return redirect(url_for('map'))
    
    return render_template('index.html')

@app.route('/map')
def map():
    with open(DATA_FILE, 'r') as f:
        users = json.load(f)
    return render_template('map.html', users=users)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Server error: {error}")
    return "Internal Server Error", 500

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {e}")
    return "Internal Server Error", 500

# 添加健康检查端点
@app.route('/health')
def health_check():
    return 'OK', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)