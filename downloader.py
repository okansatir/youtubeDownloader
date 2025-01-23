#!/usr/bin/env python3
# downloader.py
# youtube video downloader
from yt_dlp import YoutubeDL
import os

def video_download():
    # İşletim sistemini kontrol et
    if os.name == 'posix':  # Mac OS veya Linux
        downloadPath = os.path.expanduser("~/Desktop/YoutubeDownload")  # Masaüstünde YoutubeDownload klasörü
        ffmpeg_path = '/opt/homebrew/bin/ffmpeg'
    elif os.name == 'nt':  # Windows
        downloadPath = os.path.join(os.path.expanduser("~"), "Videos", "YoutubeDownload")  # Videos klasöründe YoutubeDownload
        ffmpeg_path = 'ffmpeg'
    else:
        print("Desteklenmeyen işletim sistemi. İndirme klasörü belirlenemedi.")
        return
    
    # Klasör yoksa oluştur
    if not os.path.exists(downloadPath):
        os.makedirs(downloadPath)

    video_url = input("YouTube video URL'sini girin: ")
    
    filename = '%(title)s_%(epoch)s'
    outtmpl = os.path.join(downloadPath, filename + '.%(ext)s')
        
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': outtmpl,  # Dosya adına zaman damgası ekle
        'cookiesfrombrowser': ('chrome',),  # Chrome tarayıcısından çerezleri al
        'merge_output_format': [lambda d: print(f'İndiriliyor: %{d["_percent_str"]}') if d["status"] == "downloading" else None],
        'nocheckcertificate': True,  # SSL sertifika kontrolünü devre dışı bırak
        'ffmpeg_location': ffmpeg_path  # İşletim sistemine göre belirlenen yol
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            print("Video indiriliyor... Lütfen bekleyin.")
            info = ydl.extract_info(video_url, download=True)
            print(f"\nVideo başarıyla indirildi!\nKonum: {downloadPath}")
    except Exception as e:
        print(f"Hata oluştu: {str(e)}")

if __name__ == "__main__":
    video_download() 