from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# مفتاح TMDB (محرك البحث العالمي)
API_KEY = "c2b1d2b1fd5d6e3b5b660c57fb691db4"

def fetch_data(endpoint, params=None):
    if params is None: params = {}
    base_url = f"https://api.themoviedb.org/3/{endpoint}"
    params['api_key'] = API_KEY
    params['language'] = 'ar'
    try:
        response = requests.get(base_url, params=params, timeout=5)
        return response.json()
    except: return {}

# --- الـ Layout السينمائي (التصميم الثابت) ---
def wrap_layout(content):
    return f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8"><title>DRACOLE MOVIES | THE MASTERPIECE</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;900&display=swap');
            body {{ background: #020202; color: white; font-family: 'Cairo', sans-serif; overflow-x: hidden; }}
            .glass {{ background: rgba(0, 0, 0, 0.8); backdrop-filter: blur(15px); border-bottom: 1px solid rgba(220, 38, 38, 0.3); }}
            .neon-card {{ transition: 0.4s; border: 1px solid #111; position: relative; }}
            .neon-card:hover {{ border-color: #dc2626; box-shadow: 0 0 30px rgba(220, 38, 38, 0.4); transform: scale(1.05); }}
            ::-webkit-scrollbar {{ width: 8px; }}
            ::-webkit-scrollbar-track {{ background: #000; }}
            ::-webkit-scrollbar-thumb {{ background: #dc2626; border-radius: 10px; }}
            .hero-bg {{ mask-image: linear-gradient(to top, transparent, black); }}
        </style>
    </head>
    <body>
        <nav class="p-4 glass sticky top-0 z-50 flex flex-wrap justify-between items-center px-8 md:px-16">
            <div class="flex items-center gap-8">
                <a href="/" class="text-4xl font-black text-red-600 tracking-tighter drop-shadow-[0_0_10px_rgba(220,38,38,0.5)]">DRACOLE<span class="text-white">MOVIES</span></a>
                <div class="hidden md:flex gap-6 text-sm font-bold text-gray-400">
                    <a href="/genre/28" class="hover:text-red-500 transition">أكشن</a>
                    <a href="/genre/27" class="hover:text-red-500 transition">رعب</a>
                    <a href="/genre/878" class="hover:text-red-500 transition">خيال علمي</a>
                </div>
            </div>
            <form action="/search" method="get">
                <input type="text" name="q" placeholder="ابحث عن فيلمك..." class="bg-black border border-gray-800 rounded-full px-6 py-2 text-sm focus:outline-none focus:border-red-600 w-64 text-white">
            </form>
        </nav>
        {content}
        <footer class="p-16 text-center border-t border-gray-900 mt-20">
            <h2 class="text-2xl font-black text-red-600 mb-4 italic italic">DRACOLE MOVIES</h2>
            <p class="text-gray-600 text-sm">تم التطوير هذا الموقع بواسطة  <br> <span class="text-white font-bold text-lg">Ahmed El kady</span></p>
        </footer>
    </body>
    </html>
    """

@app.route('/')
def home():
    data = fetch_data("trending/movie/week")
    movies = data.get('results', [])
    top = movies[0] if movies else None
    content = f"""
    <div class="relative h-[70vh] flex items-center px-8 md:px-16 shadow-2xl">
        <img src="https://image.tmdb.org/t/p/original/{top['backdrop_path'] if top else ''}" class="absolute inset-0 w-full h-full object-cover opacity-40 hero-bg">
        <div class="relative z-10 max-w-3xl space-y-6">
            <span class="bg-red-600 text-white px-4 py-1 rounded text-xs font-black uppercase tracking-widest">الأكثر رواجاً</span>
            <h2 class="text-6xl md:text-8xl font-black leading-tight">{top['title'] if top else ''}</h2>
            <p class="text-xl text-gray-300 line-clamp-3">{top['overview'] if top else ''}</p>
            <a href="/movie/{top['id'] if top else '#'}" class="inline-block bg-red-600 hover:bg-red-700 px-10 py-4 rounded-full font-black transition-all transform hover:scale-110">شاهد الآن</a>
        </div>
    </div>
    <div class="px-8 md:px-16 py-16">
        <h3 class="text-3xl font-black border-r-8 border-red-600 pr-6 mb-12 uppercase tracking-tighter">أحدث الإصدارات</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-8">
            {{% for movie in movies %}}
            <a href="/movie/{{{{ movie.id }}}}" class="neon-card group rounded-3xl overflow-hidden bg-zinc-900 shadow-2xl">
                <img src="https://image.tmdb.org/t/p/w500{{{{ movie.poster_path }}}}" class="w-full h-[400px] object-cover group-hover:scale-110 transition duration-500">
                <div class="p-4 bg-zinc-900">
                    <h4 class="font-bold truncate text-sm text-white">{{{{ movie.title }}}}</h4>
                    <div class="flex justify-between mt-2"><span class="text-red-500 font-bold">⭐ {{{{ movie.vote_average }}}}</span></div>
                </div>
            </a>
            {{% endfor %}}
        </div>
    </div>
    """
    return render_template_string(wrap_layout(content), movies=movies)

@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movie = fetch_data(f"movie/{movie_id}")
    # رابط سيرفر مشاهدة خارجي (لغرض التعليم)
    watch_url = f"https://vidsrc.me/embed/movie?tmdb={movie_id}"
    
    content = f"""
    <div class="p-8 md:p-20 max-w-7xl mx-auto">
        <div class="glass p-2 rounded-[40px] shadow-2xl overflow-hidden border-2 border-red-600">
            <iframe class="w-full aspect-video rounded-[35px]" src="{watch_url}" frameborder="0" allowfullscreen></iframe>
        </div>
        <div class="mt-16 grid md:grid-cols-[300px_1fr] gap-12">
            <img src="https://image.tmdb.org/t/p/w500{{ movie.poster_path }}" class="w-full rounded-[30px] border-4 border-zinc-800 shadow-2xl">
            <div class="space-y-6 text-right">
                <h2 class="text-6xl font-black text-white italic tracking-tighter underline decoration-red-600 underline-offset-8">{{ movie.title }}</h2>
                <div class="flex gap-4 justify-start">
                    <span class="bg-red-600 px-6 py-1 rounded-full font-black">⭐ {{ movie.vote_average }}</span>
                    <span class="bg-zinc-800 px-6 py-1 rounded-full font-bold">{{ movie.release_date }}</span>
                </div>
                <p class="text-2xl text-gray-400 leading-relaxed italic pr-6 border-r-4 border-red-600">{{ movie.overview }}</p>
                <div class="pt-8">
                    <p class="text-red-500 font-bold mb-4">⚠️ ملاحظة: السيرفر الخارجي قد يحتوي على إعلانات.</p>
                    <a href="/" class="bg-white text-black px-12 py-4 rounded-full font-black text-xl hover:bg-red-600 hover:text-white transition-all">العودة للرئيسية</a>
                </div>
            </div>
        </div>
    </div>
    """
    return render_template_string(wrap_layout(content), movie=movie)
@app.route('/search')
def search():
    query = request.args.get('q', '')
    data = fetch_data("search/movie", {"query": query})
    movies = data.get('results', [])
    content = f"""
    <div class="p-16">
        <h3 class="text-2xl mb-12 text-gray-400 font-bold">نتائج البحث عن: <span class="text-red-500 font-black tracking-widest uppercase italic underline">"{query}"</span></h3>
        <div class="grid grid-cols-2 md:grid-cols-5 gap-8">
            {{% for movie in movies %}}
            <a href="/movie/{{{{ movie.id }}}}" class="neon-card group rounded-3xl overflow-hidden bg-zinc-900 shadow-2xl">
                <img src="https://image.tmdb.org/t/p/w500{{{{ movie.poster_path }}}}" class="w-full h-[400px] object-cover group-hover:scale-110 transition duration-500">
                <div class="p-4 bg-zinc-900"><h4 class="font-bold truncate text-white">{{{{ movie.title }}}}</h4></div>
            </a>
            {{% endfor %}}
        </div>
    </div>
    """
    return render_template_string(wrap_layout(content), movies=movies)

@app.route('/genre/<int:genre_id>')
def genre(genre_id):
    data = fetch_data("discover/movie", {"with_genres": genre_id})
    movies = data.get('results', [])
    content = """
    <div class="p-16">
        <h3 class="text-4xl font-black mb-16 text-center text-red-600 uppercase tracking-widest italic">تصنيفات حصرية</h3>
        <div class="grid grid-cols-2 md:grid-cols-5 gap-8">
            {% for movie in movies %}
            <a href="/movie/{{ movie.id }}" class="neon-card group rounded-3xl overflow-hidden bg-zinc-900 shadow-2xl">
                <img src="https://image.tmdb.org/t/p/w500{{ movie.poster_path }}" class="w-full h-[400px] object-cover group-hover:scale-110 transition duration-500">
                <div class="p-4 bg-zinc-900"><h4 class="font-bold truncate text-white text-center">{{ movie.title }}</h4></div>
            </a>
            {% endfor %}
        </div>
    </div>
    """
    return render_template_string(wrap_layout(content), movies=movies)

if __name__ == '__main__':
    app.run(debug=True)