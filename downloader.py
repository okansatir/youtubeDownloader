#!/usr/bin/env python3
# download.py
# youtube video downloader
from yt_dlp import YoutubeDL
import os
import subprocess

def resize_video(input_path, output_path):
    """FFmpeg ile videoyu 9:16 oranında yeniden boyutlandırır ve belirtilen süreyi alır"""
    try:
         # Kullanıcıdan başlangıç ve bitiş sürelerini al
        start_time = input("Videonun başlayacağı saniyeyi girin (örn: 10): ")
        duration = input("Video kaç saniye sürsün? (örn: 60): ")

        command = [
            'ffmpeg', '-i', input_path,
            '-ss', start_time,  # Başlangıç zamanı
            '-t', duration,     # Süre
            #'-vf', 'scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2', #tüm video boyutuna göre
            '-vf', 'crop=ih*9/16:ih,scale=1080:1920',  # Önce 9:16 oranında kırp, sonra ölçeklendir
            '-c:a', 'copy',
            output_path
        ]
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg hatası: {str(e)}")
        return False
    


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
            downloaded_file = ydl.prepare_filename(info)
            print(f"\nVideo başarıyla indirildi!\nKonum: {downloadPath}")

              # Resize işlemi
            output_path = downloaded_file.rsplit('.', 1)[0] + '_shorts.mp4'
            if resize_video(downloaded_file, output_path):
                print(f"Video Shorts formatına dönüştürüldü: {output_path}")

    except Exception as e:
        print(f"Hata oluştu: {str(e)}")

if __name__ == "__main__":
    video_download() 
