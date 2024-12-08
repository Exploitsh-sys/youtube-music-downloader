import os
import subprocess
import requests
from yt_dlp import YoutubeDL
from pystyle import Colors, Colorate, Center, Write


OUTPUT_PATH = "downloads"
UPDATE_URL = "https://github.com/Exploitsh-sys/youtube-music-downloader/blob/main/Universal/build.py"  


def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False
        
def check_update():
    print(Colorate.Horizontal(Colors.blue_to_white, "\n🔄 Vérification des mises à jour...\n"))
    try:
        response = requests.get(UPDATE_URL, timeout=10)
        response.raise_for_status()

        current_file = os.path.basename(__file__)
        with open(current_file, "wb") as f:
            f.write(response.content)

        print(Colorate.Horizontal(Colors.green_to_white, "\n✅ Mise à jour téléchargée avec succès ! Redémarrez le script.\n"))
        exit()
    except Exception as e:
        print(Colorate.Horizontal(Colors.red_to_white, f"❌ Erreur lors de la vérification ou du téléchargement : {e}\n"))


def display_title():
    title = """
██╗   ██╗███╗   ██╗██╗██╗   ██╗███████╗██████╗ ███████╗ █████╗ ██╗        [ Version: Beta  ]   
██║   ██║████╗  ██║██║██║   ██║██╔════╝██╔══██╗██╔════╝██╔══██╗██║        [ Premium: False ]
██║   ██║██╔██╗ ██║██║██║   ██║█████╗  ██████╔╝███████╗███████║██║        [   Copyright    ]
██║   ██║██║╚██╗██║██║╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██╔══██║██║        [[!] CHECK UPDATE]
╚██████╔╝██║ ╚████║██║ ╚████╔╝ ███████╗██║  ██║███████║██║  ██║███████╗
 ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝
                           Fuck Skid                        
    """
    print(Colorate.Horizontal(Colors.blue_to_white, Center.XCenter(title)))


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def download_audio(video_url, quality="best"):
    try:
        os.makedirs(OUTPUT_PATH, exist_ok=True)
        ydl_opts = {
            "format": "bestaudio/best" if quality == "best" else "worstaudio",
            "outtmpl": os.path.join(OUTPUT_PATH, "%(title)s.%(ext)s"),
            "postprocessors": [
                {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}
            ],
            "quiet": False,
        }

        print(Colorate.Horizontal(Colors.blue_to_white, "\n🔄 Téléchargement de l'audio en cours...\n"))
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            title = info.get("title", "Unknown Title")
            print(Colorate.Horizontal(Colors.green_to_white, f"✅ Audio téléchargé avec succès : {title}\n"))
    except Exception as e:
        print(Colorate.Horizontal(Colors.red_to_white, f"❌ Erreur : {e}\n"))


def download_video(video_url):
    if not check_ffmpeg():
        print(Colorate.Horizontal(Colors.red_to_white, "\n❌ FFmpeg n'est pas installé. Veuillez l'installer pour télécharger des vidéos.\n"))
        return

    try:
        os.makedirs(OUTPUT_PATH, exist_ok=True)
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": os.path.join(OUTPUT_PATH, "%(title)s.%(ext)s"),
            "quiet": False,
            "merge_output_format": "mp4",
        }

        print(Colorate.Horizontal(Colors.blue_to_white, "\n🔄 Téléchargement de la vidéo en cours...\n"))
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            title = info.get("title", "Unknown Title")
            print(Colorate.Horizontal(Colors.green_to_white, f"✅ Vidéo téléchargée avec succès : {title}\n"))
    except Exception as e:
        print(Colorate.Horizontal(Colors.red_to_white, f"❌ Erreur : {e}\n"))


def main():
    quality = "best"

    while True:
        clear_console()
        display_title()
        print(Colorate.Horizontal(Colors.blue_to_white, "[1] Rechercher et télécharger une musique"))
        print(Colorate.Horizontal(Colors.blue_to_white, "[2] Choisir la qualité audio (par défaut : meilleure qualité)"))
        print(Colorate.Horizontal(Colors.blue_to_white, "[3] Afficher les téléchargements"))
        print(Colorate.Horizontal(Colors.blue_to_white, "[4] Inclure les médias (télécharger la vidéo)"))
        print(Colorate.Horizontal(Colors.blue_to_white, "[!] Check Update"))
        print(Colorate.Horizontal(Colors.blue_to_white, "[0] Quitter\n"))

        choice = Write.Input("Que voulez-vous faire ? [1/2/3/4/!] : ", Colors.blue_to_white, interval=0.01)

        if choice == "1":
            video_url = Write.Input("Entrez l'URL YouTube : ", Colors.blue_to_white, interval=0.01)
            download_audio(video_url, quality)
            input(Colorate.Horizontal(Colors.blue_to_white, "\nAppuyez sur Entrée pour revenir au menu..."))
        elif choice == "2":
            print(Colorate.Horizontal(Colors.blue_to_white, "[1] Meilleure qualité (par défaut)"))
            print(Colorate.Horizontal(Colors.blue_to_white, "[2] Qualité la plus basse\n"))
            quality_choice = Write.Input("Choisissez la qualité [1/2] : ", Colors.blue_to_white, interval=0.01)
            quality = "best" if quality_choice == "1" else "lowest"
            print(Colorate.Horizontal(Colors.green_to_white, f"\nQualité sélectionnée : {quality}"))
            input(Colorate.Horizontal(Colors.blue_to_white, "\nAppuyez sur Entrée pour revenir au menu..."))
        elif choice == "3":
            files = os.listdir(OUTPUT_PATH)
            print(Colorate.Horizontal(Colors.blue_to_white, "\n📂 Téléchargements disponibles :\n"))
            for file in files:
                print(Colorate.Horizontal(Colors.green_to_white, f"- {file}"))
            input(Colorate.Horizontal(Colors.blue_to_white, "\nAppuyez sur Entrée pour revenir au menu..."))
        elif choice == "4":
            video_url = Write.Input("Entrez l'URL YouTube : ", Colors.blue_to_white, interval=0.01)
            download_video(video_url)
            input(Colorate.Horizontal(Colors.blue_to_white, "\nAppuyez sur Entrée pour revenir au menu..."))
        elif choice == "!":
            check_update()
        elif choice == "0":
            print(Colorate.Horizontal(Colors.green_to_white, "\nAu revoir !"))
            break
        else:
            print(Colorate.Horizontal(Colors.red_to_white, "\n❌ Choix invalide, réessayez !"))
            input(Colorate.Horizontal(Colors.blue_to_white, "\nAppuyez sur Entrée pour continuer..."))

if __name__ == "__main__":
    main()
