"""
API文档: https://api.nasa.gov/ (Mars Rover Photos栏中)

申请API KEY: https://api.nasa.gov/
"""
import requests
import gradio as gr

# Function to fetch Mars Rover photos
def fetch_mars_rover_photos(api_key, query_type, sol=1000, earth_date = None, page=1, camera = None):
    base_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos" #访问的网站API：Mars Rover Photos
    
    params = {
            'api_key': api_key,
            'page': page,
            'camera': camera,
        }
    
    if query_type == 'sol':
        params['sol'] = sol
        #print(params)
    elif query_type == 'earth_date':
        params['earth_date'] = earth_date
        #print(params)
    
    response = requests.get(base_url, params=params) # 向API发送请求和参数
    
    if response.status_code == 200: #检查HTTP返回状态码，200 indicates a successful request
        return response.json()
    else:
        return None

# Gradio interface setup
def mars_rover_photo_interface_sol(query_type,sol,earth_date,page,camera):
    """
    本函数主要调用API请求函数, 并处理API请求得到的JSON数据, 提取出图片的URL并返回
    
    通常一个API文档要说清楚它的输入参数和输出数据格式, 但NASA这个API文档没说清楚输出数据格式
    我们可以通过把返回的数据打印出来, 分析它的JSON结构, 用Key作为索引, 提取出我们需要的数据
    关于JSON: https://www.runoob.com/json/json-syntax.html
    """
    
    api_key = "VmLePQ9qA3ab3oxajX21K1EyjlWzp62qDSsc7SzO" # 我的API KEY
    data = fetch_mars_rover_photos(api_key, query_type, sol, earth_date,page, camera)
    #print(data)
    if data:
        photos = data.get('photos', [])
        photo_urls = [photo['img_src'] for photo in photos]
        #print(photo_urls)
        return photo_urls
    else:
        return []
    

# Define the input components for the Gradio interface
query_type_input = gr.Radio(label="Query Type", choices=["sol", "earth_date"], value='sol')
sol_input= gr.Number(label="Martian Sol", value=1000)
page_input = gr.Number(label="Page", value=1)
earth_date_input = gr.DateTime(label="Earth Date")
camera_input = gr.Dropdown(label = "Camera Type", choices = ["FHAZ", "RHAZ", "MAST", "CHEMCAM", "MAHLI", "MARDI", "NAVCAM", "PANCAM", "MINITES"], value=None)

# Create the Gradio interface
gr.Interface(fn=mars_rover_photo_interface_sol, 
    inputs=[query_type_input, sol_input,  earth_date_input, page_input, camera_input],
        outputs=gr.Gallery(label="Mars Rover Photos")).launch()



