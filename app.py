 
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Online Quran API ke URLs (Poore 30 para aur 114 Surahs ke liye)
ARABIC_API = "https://api.alquran.cloud/v1/quran/quran-uthmani"
ENGLISH_API = "https://api.alquran.cloud/v1/quran/en.sahih"
HINDI_API = "https://api.alquran.cloud/v1/quran/hi.farooq"

# Global variables taaki data baar-baar download na karna pade
quran_data = {"arabic": [], "english": [], "hindi": []}

def fetch_all_quran():
    global quran_data
    print("🔄 Poora 30 para ka Quran data internet se load ho rha hai... Please wait...")
    try:
        ar_res = requests.get(ARABIC_API).json()
        en_res = requests.get(ENGLISH_API).json()
        hi_res = requests.get(HINDI_API).json()
        
        quran_data["arabic"] = ar_res['data']['surahs']
        quran_data["english"] = en_res['data']['surahs']
        quran_data["hindi"] = hi_res['data']['surahs']
        print("✅ Poora Quran data kamyabi se load ho gaya!")
    except Exception as e:
        print(f"❌ Data load karne mein dikkat aayi: {e}")

# Server start hote hi poora data download ho jayega
fetch_all_quran()

@app.route('/')
def home():
    # Home page par load kam rakhne ke liye hum Surahs ki list dikhayenge
    surah_list = []
    for s in quran_data["arabic"]:
        surah_list.append({
            "number": s["number"],
            "name": s["name"],
            "englishName": s["englishName"]
        })
    return render_template('index.html', surahs=surah_list, is_search=False, is_detail=False)

@app.route('/surah/<int:surah_num>')
def surah_detail(surah_num):
    # Kisi bhi Surah par click karne par uski poori aayatein dikhengis
    idx = surah_num - 1
    if 0 <= idx < len(quran_data["arabic"]):
        return render_template(
            'index.html',
            arabic_surah=quran_data["arabic"][idx],
            english_surah=quran_data["english"][idx],
            hindi_surah=quran_data["hindi"][idx],
            is_search=False,
            is_detail=True
        )
    return "Surah nahi mili!", 404

@app.route('/search')
def search_surah():
    query = request.args.get('query', '').strip().lower()
    results = []
    
    if query:
        for s in quran_data["arabic"]:
            eng_name = s.get('englishName', '').lower()
            ar_name = s.get('name', '').lower()
            num = str(s.get('number', ''))
            
            if query in eng_name or query in ar_name or query == num:
                results.append({
                    "number": s["number"],
                    "name": s["name"],
                    "englishName": s["englishName"]
                })
                
    return render_template('index.html', surahs=results, is_search=True, is_detail=False, query=query)

if __name__ == '__main__':
    app.run(debug=True)