import json
import re

def generar_html():
    try:
        with open('proyectos.json', 'r', encoding='utf-8') as f:
            proyectos = json.load(f)
    except Exception as e:
        print(f"Error al cargar proyectos.json: {e}")
        return

    destacado = next((p for p in proyectos if p.get('destacado')), proyectos[0] if proyectos else None)
    otros_proyectos = [p for p in proyectos if p != destacado]

    def process_url(url):
        if not url:
            return {"type": "none", "url": ""}
        
        # YouTube
        if "youtube.com" in url or "youtu.be" in url:
            yt_id = url.split('/')[-1].split('?')[0]
            if "watch?v=" in url:
                yt_id = url.split('v=')[1].split('&')[0]
            return {"type": "youtube", "id": yt_id}
        
        # Google Drive Video Embed
        elif "drive.google.com" in url:
            file_id = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
            if file_id:
                return {"type": "drive", "embed_url": f"https://drive.google.com/file/d/{file_id.group(1)}/preview"}
            return {"type": "drive", "embed_url": url.replace("/view", "/preview")}
        
        # Video MP4 directo
        else:
            return {"type": "video", "url": url}

    def render_media(url, titulo=""):
        media = process_url(url)
        
        if media["type"] == "none":
            return '<div class="w-full h-full bg-gray-950 flex items-center justify-center font-mono text-xs text-cyan-600">[ MEDIA PREVIEW ]</div>'
        
        elif media["type"] == "youtube":
            return f'''<iframe class="w-full h-full rounded-xl" src="https://www.youtube.com/embed/{media['id']}?autoplay=1&mute=1&loop=1&playlist={media['id']}" title="{titulo}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'''
        
        elif media["type"] == "drive":
            return f'''<iframe class="w-full h-full rounded-xl" src="{media['embed_url']}" allow="autoplay" frameborder="0" allowfullscreen></iframe>'''
        
        else:
            return f'''<video class="w-full h-full object-cover rounded-xl" autoplay loop muted playsinline preload="auto">
                <source src="{media['url']}" type="video/mp4">
                Tu navegador no soporta el formato de video.
            </video>'''

    html_content = f"""<!DOCTYPE html>
<html lang="es" class="dark scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Stefano Del Moro | Lead Software & AI Engineer</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          colors: {{
            cyber: {{
              blue: '#00f0ff',
              cyan: '#00d8f6',
              dark: '#030712',
              card: '#08101e',
              border: '#0e2338'
            }}
          }}
        }}
      }}
    }}
  </script>
  <style>
    body {{
      background-color: #030712;
      background-image: 
        linear-gradient(to right, rgba(0, 240, 255, 0.08) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(0, 240, 255, 0.08) 1px, transparent 1px),
        radial-gradient(circle at 50% 0%, rgba(0, 240, 255, 0.15) 0%, transparent 70%);
      background-size: 36px 36px, 36px 36px, 100% 100%;
    }}
    .glow-cyan {{
      box-shadow: 0 0 25px rgba(0, 240, 255, 0.15);
    }}
    .glow-cyan:hover {{
      box-shadow: 0 0 35px rgba(0, 240, 255, 0.3);
    }}
    .glow-text {{
      text-shadow: 0 0 20px rgba(0, 240, 255, 0.7);
    }}
  </style>
</head>
<body class="text-gray-200 min-h-screen font-sans antialiased pt-28">

  <!-- NAVBAR FIXED SUPERIOR PROFESIONAL -->
  <header class="fixed top-0 left-0 right-0 z-40 bg-[#030712]/95 backdrop-blur-md border-b border-cyan-500/30 px-6 py-4 shadow-[0_10px_30px_rgba(0,0,0,0.9)]">
    <div class="max-w-6xl mx-auto flex justify-between items-center">
      <div class="flex items-center gap-3">
        <span class="relative flex h-3.5 w-3.5">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
          <span class="relative inline-flex rounded-full h-3.5 w-3.5 bg-cyan-400 shadow-[0_0_12px_#00f0ff]"></span>
        </span>
        <div>
          <h1 class="text-xl font-black text-white tracking-widest uppercase glow-text">STEFANO DEL MORO</h1>
          <p class="text-[11px] text-cyan-400 font-mono font-bold tracking-widest uppercase">Full Stack & AI Engineer • Mobile Architect</p>
        </div>
      </div>
      
      <div class="flex items-center gap-4">
        <div class="hidden sm:flex items-center gap-2 px-3 py-1.5 bg-cyan-950/60 border border-cyan-500/40 rounded-xl text-xs font-mono text-cyan-400">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>SYSTEM_ONLINE</span>
        </div>
        <a href="#contacto" class="px-5 py-2.5 bg-cyan-400 text-black font-extrabold text-xs font-mono rounded-xl hover:bg-cyan-300 transition duration-300 shadow-[0_0_20px_rgba(0,240,255,0.4)] uppercase tracking-wider">
          CONTACTAR
        </a>
      </div>
    </div>
  </header>

  <main class="max-w-6xl mx-auto px-6">

    <!-- HERO METRICS / HEADER PROFESIONAL -->
    <div class="text-center max-w-4xl mx-auto mb-16">
      <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-mono font-bold bg-cyan-400/10 text-cyan-400 border border-cyan-400/40 uppercase tracking-widest mb-6 shadow-[0_0_15px_rgba(0,240,255,0.2)]">
        <span class="w-2 h-2 rounded-full bg-cyan-400"></span>
        <span>High-Scale Engineering & On-Device AI</span>
      </div>

      <h2 class="text-4xl md:text-6xl font-black text-white leading-none tracking-tight mb-6 uppercase">
        ARQUITECTURA MÓVIL, <br/>
        <span class="text-cyan-400 glow-text">IA LOCAL & SISTEMAS AUTÓNOMOS</span>
      </h2>
      <p class="text-gray-300 text-sm md:text-lg leading-relaxed max-w-2xl mx-auto font-light">
        Especialista en desarrollo Android Nativo (Kotlin/Compose), integración de LLMs locales con inferencia offline y automatización de procesos bajo Linux.
      </p>
    </div>

    <!-- PROYECTO INSIGNIA -->
    """

    if destacado:
        html_content += f"""
    <section class="mb-16">
      <div class="bg-cyber-card border border-cyan-400/60 rounded-3xl p-6 md:p-8 glow-cyan transition duration-300">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          <div class="lg:col-span-6 flex flex-col justify-between h-full">
            <div>
              <div class="mb-4">
                <span class="px-3 py-1 bg-cyan-400/15 border border-cyan-400/50 text-cyan-400 font-mono font-bold text-xs uppercase tracking-wider rounded-lg">
                  {destacado.get('categoria', 'PROYECTO INSIGNIA')}
                </span>
              </div>
              <h3 class="text-2xl md:text-4xl font-black text-white mb-4 leading-tight tracking-wide">
                {destacado.get('titulo', '')}
              </h3>
              <p class="text-gray-300 text-sm md:text-base leading-relaxed mb-6 font-normal">
                {destacado.get('descripcion', '')}
              </p>
              <div class="flex flex-wrap gap-2 mb-8">
                {"".join([f'<span class="text-xs font-mono bg-gray-950 text-cyan-400 px-3 py-1 rounded-lg border border-cyan-900/80">{tag}</span>' for tag in destacado.get('tags', [])])}
              </div>
            </div>
            
            <div class="flex flex-wrap items-center gap-4">
              <button onclick="openModal('{destacado.get('video_url', '')}', '{destacado.get('titulo', '')}')" class="px-6 py-3 bg-cyan-400 text-black font-black text-xs font-mono uppercase tracking-wider rounded-xl hover:bg-cyan-300 transition shadow-[0_0_20px_rgba(0,240,255,0.4)] flex items-center gap-2">
                <span>🔍</span> VER DEMO HD AMPLADA
              </button>
              {f'<a href="{destacado["link"]}" target="_blank" class="px-6 py-3 bg-cyan-950 border border-cyan-400/60 text-cyan-400 font-bold text-xs font-mono uppercase tracking-wider rounded-xl hover:bg-cyan-400 hover:text-black transition">Google Play ➔</a>' if destacado.get('link') else ''}
            </div>
          </div>

          <div class="lg:col-span-6">
            <div class="aspect-video w-full rounded-2xl overflow-hidden border border-cyan-900/80 shadow-2xl bg-gray-950">
              {render_media(destacado.get('video_url', ''), destacado.get('titulo', ''))}
            </div>
          </div>
        </div>
      </div>
    </section>
    """

    html_content += """
    <!-- OTHER PROJECTS GRID -->
    <section class="mb-20">
      <h3 class="text-xl font-black text-white font-mono uppercase tracking-wider mb-8 text-cyan-400 border-l-4 border-cyan-400 pl-4">
        Sistemas & Desarrollos Autónomos
      </h3>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
    """

    for p in otros_proyectos:
        html_content += f"""
        <div class="bg-cyber-card border border-cyber-border hover:border-cyan-400/60 rounded-2xl p-6 transition duration-300 flex flex-col justify-between glow-cyan">
          <div>
            <div class="mb-3">
              <span class="px-2.5 py-1 bg-cyan-400/10 border border-cyan-400/40 text-cyan-400 text-[11px] font-mono font-bold tracking-wider uppercase rounded-md inline-block">
                {p.get('categoria', '')}
              </span>
            </div>
            
            <h4 class="text-xl font-bold text-white mb-3 leading-snug">{p.get('titulo', '')}</h4>
            <p class="text-gray-400 text-xs leading-relaxed mb-6">{p.get('descripcion', '')}</p>

            <div class="aspect-video w-full rounded-xl overflow-hidden border border-cyan-900/80 mb-6 bg-gray-950">
              {render_media(p.get('video_url', ''), p.get('titulo', ''))}
            </div>
          </div>

          <div>
            <div class="flex flex-wrap gap-2 mb-5">
              {"".join([f'<span class="text-[10px] font-mono bg-gray-950 text-gray-300 px-2.5 py-1 rounded-md border border-gray-800">{tag}</span>' for tag in p.get('tags', [])])}
            </div>
            <button onclick="openModal('{p.get('video_url', '')}', '{p.get('titulo', '')}')" class="w-full py-3 bg-cyan-950 border border-cyan-400/80 text-cyan-400 font-mono font-bold text-xs uppercase rounded-xl hover:bg-cyan-400 hover:text-black transition shadow-[0_0_15px_rgba(0,240,255,0.15)] flex items-center justify-center gap-2">
              <span>🔍</span> VER DEMO HD
            </button>
          </div>
        </div>
        """

    html_content += """
      </div>
    </section>

  </main>

  <!-- MODAL / LIGHTBOX HD UNIVERSAL -->
  <div id="videoModal" class="fixed inset-0 z-50 bg-black/90 backdrop-blur-xl hidden flex items-center justify-center p-4 md:p-10 transition-all">
    <div class="relative w-full max-w-5xl bg-cyber-card border border-cyan-400/80 rounded-3xl overflow-hidden shadow-[0_0_50px_rgba(0,240,255,0.3)]">
      <div class="flex justify-between items-center px-6 py-4 border-b border-cyan-900/80 bg-gray-950">
        <h3 id="modalTitle" class="text-base font-bold text-cyan-400 font-mono uppercase tracking-wider">DEMO VIDEO</h3>
        <button onclick="closeModal()" class="text-cyan-400 hover:text-white font-mono text-base font-bold px-3 py-1 bg-cyan-950 rounded-lg border border-cyan-800">✕ CERRAR</button>
      </div>
      <div id="modalMediaContainer" class="aspect-video w-full bg-black">
        <!-- Inyectado dinámicamente -->
      </div>
    </div>
  </div>

  <script>
    function openModal(url, title) {
      if (!url) return;
      const modal = document.getElementById('videoModal');
      const modalTitle = document.getElementById('modalTitle');
      const container = document.getElementById('modalMediaContainer');

      modalTitle.innerText = title || "DEMO VIDEO";

      // YouTube
      if (url.includes("youtube.com") || url.includes("youtu.be")) {
        let ytId = url.split('/').pop().split('?')[0];
        if (url.includes("watch?v=")) {
            ytId = url.split('v=')[1].split('&')[0];
        }
        container.innerHTML = `<iframe class="w-full h-full" src="https://www.youtube.com/embed/${ytId}?autoplay=1&controls=1" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;
      } 
      // Google Drive
      else if (url.includes("drive.google.com")) {
        let embedUrl = url;
        const match = url.match(/\/d\/([a-zA-Z0-9_-]+)/);
        if (match) {
          embedUrl = `https://drive.google.com/file/d/${match[1]}/preview`;
        } else {
          embedUrl = url.replace("/view", "/preview");
        }
        container.innerHTML = `<iframe class="w-full h-full" src="${embedUrl}" allow="autoplay" frameborder="0" allowfullscreen></iframe>`;
      } 
      // Video MP4 directo
      else {
        container.innerHTML = `<video class="w-full h-full" controls autoplay><source src="${url}" type="video/mp4"></video>`;
      }

      modal.classList.remove('hidden');
      document.body.style.overflow = 'hidden';
    }

    function closeModal() {
      const modal = document.getElementById('videoModal');
      const container = document.getElementById('modalMediaContainer');

      modal.classList.add('hidden');
      container.innerHTML = "";
      document.body.style.overflow = 'auto';
    }

    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') closeModal();
    });
  </script>

  <footer id="contacto" class="py-8 border-t border-cyan-900/60 text-center text-xs font-mono text-gray-500 bg-cyber-dark">
    <p class="text-cyan-400 font-bold mb-1">STEFANO DEL MORO</p>
    <p>Software & Mobile Engineering Portfolio</p>
  </footer>

</body>
</html>
"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("✅ Portafolio con soporte universal de video y tipografía mejorada.")

if __name__ == '__main__':
    generar_html()
