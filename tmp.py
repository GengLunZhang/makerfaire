# import urllib.parse
# from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
# import os
# import json
# import requests
# from PIL import Image
# import time

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'uploads/'
# app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32 MB

# DATA_FILE = 'data/users.json'
# AMAP_KEY = "6154b79dac34c6441823145ad117ec31"

# # 确保必要的目录存在
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
# os.makedirs('data', exist_ok=True)

# if not os.path.exists(DATA_FILE):
#     with open(DATA_FILE, 'w') as f:
#         json.dump([], f)
# else:
#     with open(DATA_FILE, 'r+') as f:
#         content = f.read().strip()
#         if not content:
#             f.seek(0)
#             json.dump([], f)
# def get_country_coordinates(country):
#     """获取国家坐标（使用高德地图 API）"""
#     try:
#         url = "https://restapi.amap.com/v3/geocode/geo"
#         params = {
#             "address": country,
#             "key": AMAP_KEY,
#             "output": "JSON"
#         }
        
#         response = requests.get(url, params=params)
#         data = response.json()
        
#         if data.get("status") == "1" and data.get("geocodes"):
#             location = data["geocodes"][0]["location"].split(",")
#             return {
#                 'lng': float(location[0]),
#                 'lat': float(location[1])
#             }
#     except Exception as e:
#         print(f"Error getting country coordinates: {e}")
#     return {'lat': 39.90923, 'lng': 116.397428}  # 默认返回北京坐标

# def resize_image(image_path, max_size=(800, 800)):
#     """压缩图片尺寸"""
#     try:
#         with Image.open(image_path) as img:
#             # 保持原始图片格式
#             original_format = img.format
#             # 缩放图片
#             img.thumbnail(max_size, Image.Resampling.LANCZOS)
#             # 转换颜色模式（如果需要）
#             if img.mode in ('RGBA', 'P'):
#                 img = img.convert('RGB')
#             # 保存时使用原始格式
#             img.save(image_path, format=original_format, optimize=True, quality=85)
#     except Exception as e:
#         print(f"Error resizing image: {e}")

# @app.route('/api/countries')
# def get_countries():
#     """获取国家列表（使用预定义的列表）"""
#     countries = [
#         "中国", "日本", "韩国", "新加坡", "马来西亚", "泰国", "越南", "印度尼西亚",
#         "菲律宾", "印度", "巴基斯坦", "孟加拉国", "尼泊尔", "斯里兰卡",
#         "澳大利亚", "新西兰",
#         "美国", "加拿大", "墨西哥", "巴西", "阿根廷", "智利",
#         "英国", "法国", "德国", "意大利", "西班牙", "葡萄牙", "瑞士", "瑞典", "挪威",
#         "俄罗斯", "乌克兰", "哈萨克斯坦",
#         "埃及", "南非", "尼日利亚", "肯尼亚"
#     ]
#     return jsonify({"data": countries})

# @app.route('/api/cities', methods=['POST'])
# def get_cities():
#     """获取城市列表（使用高德地图 API）"""
#     try:
#         country = request.json.get('country')
        
#         # 如果是中国，使用高德地图行政区划接口
#         if country == "中国":
#             url = "https://restapi.amap.com/v3/config/district"
#             params = {
#                 "keywords": "中国",
#                 "key": AMAP_KEY,
#                 "subdistrict": 2,  # 获取到市级
#                 "output": "JSON"
#             }
            
#             response = requests.get(url, params=params)
#             data = response.json()
            
#             if data.get("status") == "1" and data.get("districts"):
#                 # 提取所有省份的城市
#                 cities = []
#                 provinces = data["districts"][0]["districts"]
#                 for province in provinces:
#                     province_cities = province.get("districts", [])
#                     cities.extend([city["name"] for city in province_cities])
#                 return jsonify({"data": sorted(list(set(cities)))})
        
#         # 对于其他国家，使用地理编码接口获取主要城市
#         else:
#             url = "https://restapi.amap.com/v3/geocode/geo"
#             params = {
#                 "address": country,
#                 "key": AMAP_KEY,
#                 "output": "JSON"
#             }
            
#             response = requests.get(url, params=params)
#             data = response.json()
            
#             if data.get("status") == "1" and data.get("geocodes"):
#                 # 根据国家返回一些主要城市
#                 # 这里可以根据需要扩展城市列表
#                 major_cities = {
#                     "日本": ["东京", "大阪", "京都", "名古屋", "福冈", "札幌"],
#                     "韩国": ["首尔", "釜山", "仁川", "大邱", "光州", "大田"],
#                     "美国": ["纽约", "洛杉矶", "芝加哥", "休斯顿", "旧金山", "西雅图"],
#                     # ... 可以添加更多国家的主要城市
#                 }
#                 return jsonify({"data": major_cities.get(country, [country + "市"])})
                
#     except Exception as e:
#         print(f"Error getting cities: {e}")
#         return jsonify({"error": str(e)}), 500
    
#     return jsonify({"data": []})
# # def get_city_coordinates(city, country):
# #     """获取城市的地理坐标"""
# #     try:
    
# #         time.sleep(1)
# #         search_query = f"{city}, {country}"
# #         response = requests.get(
# #             f"https://nominatim.openstreetmap.org/search",
# #             params={
# #                 'q': search_query,
# #                 'format': 'json',
# #                 'limit': 1
# #             },
# #             headers={'User-Agent': 'YourApp/1.0'}
# #         )
        
# #         if response.status_code == 200:
# #             data = response.json()
# #             if data:
# #                 return {
# #                     'lat': float(data[0]['lat']),
# #                     'lng': float(data[0]['lon'])
# #                 }
# #     except Exception as e:
# #         print(f"Error getting coordinates for {city}, {country}: {e}")
    
# #     # 如果获取失败，返回国家级别的坐标
# #     return get_country_coordinates(country)

# # def get_country_coordinates(country):
# #     try:
# #         response = requests.get(f"https://restcountries.com/v3.1/name/{country}")
# #         data = response.json()
# #         if data and len(data) > 0:
# #             latlng = data[0].get('latlng', [0, 0])
# #             return {'lat': latlng[0], 'lng': latlng[1]}
# #     except Exception as e:
# #         print(f"Error getting country coordinates: {e}")
# #     return {'lat': 0, 'lng': 0}

# # def resize_image(image_path, max_size=(800, 800)):
# #     """压缩图片尺寸"""
# #     try:
# #         with Image.open(image_path) as img:
# #             img.thumbnail(max_size, Image.Resampling.LANCZOS)
# #             img.save(image_path, optimize=True, quality=85)
# #     except Exception as e:
# #         print(f"Error resizing image: {e}")

# # @app.route('/api/countries')
# # def get_countries():
# #     """获取国家列表"""
# #     try:
# #         response = requests.get("https://countriesnow.space/api/v0.1/countries")
# #         return jsonify(response.json())
# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500

# # @app.route('/api/cities', methods=['POST'])
# # def get_cities():
# #     """获取城市列表"""
# #     try:
# #         country = request.json.get('country')
# #         response = requests.post(
# #             "https://countriesnow.space/api/v0.1/countries/cities",
# #             json={"country": country}
# #         )
# #         return jsonify(response.json())
# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         name = request.form['name']
#         phone = request.form['phone']
#         country = request.form['country']
#         city = request.form['city']
#         story = request.form['story'] 
        

#         photo = request.files['photo']
#         if photo:
#             photo_filename = f"{name}_{photo.filename}".replace(" ", "_")
#             photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
#             photo.save(photo_path)
#             resize_image(photo_path)
            
#             coordinates = get_city_coordinates(city, country)
            
#             user_data = {
#                 "name": name,
#                 "phone": phone,
#                 "country": country,
#                 "city": city,
#                 "story": story,  
#                 "photo": urllib.parse.quote(photo_filename),
#                 "coordinates": coordinates
#             }
            
#             with open(DATA_FILE, 'r+') as f:
#                 data = json.load(f)
#                 data.append(user_data)
#                 f.seek(0)
#                 f.truncate()
#                 json.dump(data, f, indent=4)

#             return redirect(url_for('map'))
    
#     return render_template('index.html')

# @app.route('/map')
# def map():
#     with open(DATA_FILE, 'r') as f:
#         users = json.load(f)
#     return render_template('map.html', users=users)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000, debug=True)