import requests
import re
import os
from typing import Dict, List
from http.cookiejar import MozillaCookieJar

OK_RU_DESKTOP_URL = 'https://ok.ru'
OK_RU_MOBILE_URL = 'https://m.ok.ru'
HEADERS = {
    "Referer": f"{OK_RU_MOBILE_URL}",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
}

def load_cookies_from_file(file_path: str) -> Dict[str, str]:
    cookie_jar = MozillaCookieJar(file_path)
    cookie_jar.load(ignore_discard=True, ignore_expires=True)
    
    cookies = {}
    for cookie in cookie_jar:
        cookies[cookie.name] = cookie.value
    
    return cookies

def ok_ru_upload(input_file: str, filename: str, cookies: Dict[str, str]) -> Dict:
    if not cookies:
        raise TypeError("Cookies is required.")
    
    session = requests.Session()
    session.cookies.update(cookies)
    session.headers.update(HEADERS)

    update_data = {
        "fr.posted": "set",
        "fr.name": filename,
        "fr.privacy": "everybody",
        "button_save": "Save"
    }

    # Obtener la página de carga
    upload_page_link = f'{OK_RU_MOBILE_URL}/dk?st.cmd=userMovies'
    print('1. Fetching user upload page', upload_page_link)
    upload_page_res = session.get(upload_page_link)
    
    # Imprimir información de depuración
    print(f"Response status code: {upload_page_res.status_code}")
    print(f"Response URL: {upload_page_res.url}")
    print("Response headers:")
    for key, value in upload_page_res.headers.items():
        print(f"{key}: {value}")
    
    # Guardar el contenido HTML para inspección
    with open("upload_page.html", "w", encoding="utf-8") as f:
        f.write(upload_page_res.text)
    print("HTML content saved to 'upload_page.html'")

    # Encontrar el enlace de carga
    re_upload_btn = re.search(r'href="(/dk\?st\.cmd=addMovie.*?)">Upload video</a>', upload_page_res.text)
    if not re_upload_btn:
        raise ValueError("Upload link not found. Check 'upload_page.html' for details.")
    upload_btn_link = OK_RU_MOBILE_URL + re_upload_btn.group(1).replace('&amp;', '&')
    
    # Obtener la página de carga de videos
    print('2. Fetching upload link', upload_btn_link)
    upload_res = session.get(upload_btn_link)
    
    # Extraer los enlaces necesarios
    upload_link = "https://" + re.search(r'&quot;//(vu\.mycdn\.me/upload\.do.*?)&quot;,&quot;replace', upload_res.text).group(1).replace("\\u0026", "&")
    update_link = OK_RU_MOBILE_URL + re.search(r'action="(/dk\?bk=EditMovie&amp;.*?)" method="post"', upload_res.text).group(1).replace('&amp;', '&')
    print(f"Upload link: {upload_link} | Update link: {update_link}")
    
    # Subir el archivo
    print(f'3. Uploading {filename} ...')
    with open(input_file, 'rb') as file:
        files = {'upload_file': (filename, file, 'application/x-binary; charset=x-user-defined')}
        upload_link_res = session.post(upload_link, files=files)
    print("4. Upload status", upload_link_res.status_code, upload_link_res.text)
    
    # Actualizar los datos del archivo
    print("5. Updating file data")
    update_res = session.post(update_link, data=update_data)
    print("6. Update file status", update_res.status_code)
    
    # Extraer el ID del video
    file_id = re.search(r'id=(\d+)', upload_link).group(1)
    
    return {
        "status": upload_link_res.status_code,
        "id": file_id,
        "video_url": f"{OK_RU_DESKTOP_URL}/video/{file_id}",
        "update_link": update_link,
    }

def upload_multiple_videos(video_directory: str, cookies: Dict[str, str]) -> List[Dict]:
    results = []
    for filename in os.listdir(video_directory):
        if filename.endswith(('.mp4', '.avi', '.mov', '.flv', '.mkv')):  # Añade o quita extensiones según sea necesario
            file_path = os.path.join(video_directory, filename)
            try:
                result = ok_ru_upload(file_path, filename, cookies)
                results.append(result)
                print(f"Successfully uploaded {filename}")
            except Exception as e:
                print(f"Failed to upload {filename}: {str(e)}")
    return results

if __name__ == '__main__':
    cookie_file = 'cookie.txt'  # Asegúrate de que este archivo esté en el mismo directorio que tu script
    my_cookies = load_cookies_from_file(cookie_file)
    
    video_directory = 'video'  # Cambia esto a la ruta de tu directorio de videos
    uploaded_files = upload_multiple_videos(video_directory, my_cookies)
    for file in uploaded_files:
        print(file['video_url'])