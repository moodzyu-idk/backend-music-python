from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from ytmusicapi import YTMusic
import yt_dlp

app = FastAPI()
ytmusic = YTMusic()

# Biar website Vercel lu bisa akses API ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/search")
def search_music(q: str = Query(...)):
    try:
        # Nyari lagu pake ytmusicapi
        results = ytmusic.search(q, filter="songs")
        tracks = []
        for item in results[:10]:
            tracks.append({
                "id": item.get("videoId"),
                "title": item.get("title"),
                "artist": item.get("artists")[0]["name"] if item.get("artists") else "Unknown",
                "thumbnail": item.get("thumbnails")[-1]["url"] if item.get("thumbnails") else "",
                "duration": item.get("duration")
            })
        return {"status": True, "data": tracks}
    except Exception as e:
        return {"status": False, "error": str(e)}

@app.get("/api/stream")
def get_audio_url(id: str = Query(...)):
    try:
        # Pake yt-dlp buat dapetin link audio
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={id}", download=False)
            audio_url = info.get('url')
            
            if audio_url:
                return {"status": True, "audioUrl": audio_url}
            else:
                return {"status": False, "error": "Audio URL tidak ditemukan"}
    except Exception as e:
        return {"status": False, "error": str(e)}

# Endpoint buat ngecek server hidup atau nggak
@app.get("/")
def read_root():
    return {"status": "Backend Music Python Jalan!"}
