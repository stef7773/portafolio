import json

def generar_html():
    try:
        with open('proyectos.json', 'r', encoding='utf-8') as f:
            proyectos = json.load(f)
    except Exception as e:
        print(f"Error al cargar proyectos.json: {e}")
        return

    destacado = next((p for p in proyectos if p.get('destacado')), proyectos[0] if proyectos else None)
    otros_proyectos = [p for p in proyectos if p != destacado]

    def render_media(url, titulo=""):
        if not url:
            return '<div class="w-full h-full bg-gray-950/80 flex items-center justify-center font-mono text-xs text-cyan-500 border border-cyan-900/40">[ VIDEO PREVIEW ]</div>'
        
        if "youtube.com" in url or "youtu.be" in url:
            yt_id = url.split('/')[-1].split('?')[0]
            if "watch?v=" in url:
                yt_id = url.split('v=')[1].split('&')[0]
            return f'''<iframe class="w-full h-full rounded-xl pointer-events-none" src="https://www.youtube.com/embed/{yt_id}?autoplay=1&mute=1&loop=1&playlist={yt_id}&controls=0" title="{titulo}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe>'''
        else:
            return f'''<video class="w-full h-full object-cover rounded-xl" autoplay loop muted playsinline preload="auto">
                <source src="{url}" type="video/mp4">
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
              dark: '#020617',
              card: '#081226',
              border: '#102a45'
            }}
          }}
        }}
      }}
    }}
  </script>
  <style>
    /* FONDO CIBERNÉTICO DE CUADRÍCULA VIBRANTE */
    body {{
      background-color: #020617;
      background-image: 
        linear-gradient(to right, rgba(0, 240, 255, 0.07) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(0, 240, 255, 0.07) 1px, transparent 1px),
        radial-gradient(circle at 50% 0%, rgba(0, 240, 255, 0.18) 0%, transparent 70%);
      background-size: 40px 40px, 40px 40px, 100% 100%;
    }}
    .glow-cyan {{
      box-shadow: 0 0 30px rgba(0, 240, 255, 0.12);
    }}
    .glow-cyan:hover {{
      box-shadow: 0 0 40px rgba(0, 240, 255, 0.28);
    }}
    .glow-text {{
      text-shadow: 0 0 25px rgba(0, 240, 255, 0.7);
    }}
  </style>
</head>
<body class="text-gray-100 min-h-screen font-sans antialiased pt-28">

  <!-- NAVBAR FIXED SIEMPRE VISIBLE CON NOMBRE Y STATUS -->
  <header class="fixed top-0 left-0 right-0 z-50 bg-[#020617]/90 backdrop-blur-xl border-b border-cyan-500/30 px-6 py-4 shadow-[0_4px_30px_rgba(0,240,255,0.15)]">
    <div class="max-w-7xl mx-auto flex justify-between items-center">
      <div class="flex items-center gap-3">
        <span class="relative flex h-3.5 w-3.5">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
          <span class="relative inline-flex rounded-full h-3.5 w-3.5 bg-cyan-400 shadow-[0_0_12px_#00f0ff]"></span>
        </span>
        <div>
          <h1 class="text-xl font-black text-white tracking-widest uppercase glow-text">STEFANO DEL MORO</h1>
          <p class="text-[10px] text-cyan-400 font-mono font-bold tracking-widest uppercase">Full-Stack Architect • Local AI Specialist</p>
        </div>
      </div>
      
      <div class="flex items-center gap-4">
        <div class="hidden sm:flex items-center gap-2 px-3 py-1 bg-cyan-950/60 border border-cyan-500/40 rounded-lg text-xs font-mono text-cyan-300">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>SYSTEM_ONLINE</span>
        </div>
        <a href="#contacto" class="px-5 py-2 bg-cyan-400 text-black font-extrabold text-xs tracking-wider font-mono rounded-lg hover:bg-cyan-300 transition duration-300 shadow-[0_0_20px_rgba(0,240,255,0.4)]">
          CONTACTAR
        </a>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-6">

    <!-- HERO SECTION IMPACTANTE -->
    <div class="text-center max-w-4xl mx-auto mb-20">
      <span class="px-4 py-1.5 rounded-full text-xs font-mono font-bold bg-cyan-400/10 text-cyan-400 border border-cyan-400/40 uppercase tracking-widest inline-block mb-6 shadow-[0_0_15px_rgba(0,240,255,0.2)]">
        High-Performance Engineering & On-Device AI
      </span>

      <h2 class="text-4xl sm:text-6xl font-black text-white leading-tight mb-6 tracking-tight">
        ARQUITECTURA MÓVIL,<br/>
        <span class="text-cyan-400 glow-text">IA LOCAL & HIGH-SCALE SYSTEMS</span>
      </h2>
      
      <p class="text-gray-300 text-base sm:text-lg leading-relaxed max-w-2xl mx-auto font-light">
        Desarrollo de ecosistemas nativos Android, integraciones de modelos LLM offline de ultra-baja latencia y automatización avanzada sobre infraestructura Linux Mint.
      </p>
    </div>

    <!-- PROYECTO INSIGNIA -->
    """

    if destacado:
        html_content += f"""
    <section class="mb-20">
      <div class="bg-cyber-card border border-cyan-400/60 rounded-3xl p-6 sm:p-10 glow-cyan relative overflow-hidden">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          <div class="lg:col-span-6 flex flex-col justify-between h-full">
            <div>
              <div class="mb-4">
                <span class="px-3 py-1 bg-cyan-400/15 border border-cyan-400/50 text-cyan-400 font-mono font-bold text-xs uppercase tracking-wider rounded-md">
                  {destacado.get('categoria', 'FLAGSHIP SYSTEM')}
                </span>
              </div>
              <h3 class="text-3xl sm:text-4xl font-black text-white mb-4 leading-tight tracking-wide">
                {destacado.get('titulo', '')}
              </h3>
              <p class="text-gray-300 text-sm sm:text-base leading-relaxed mb-6 font-normal">
                {destacado.get('descripcion', '')}
              </p>
              <div class="flex flex-wrap gap-2 mb-8">
                {"".join([f'<span class="text-xs font-mono bg-black/60 text-cyan-300 px-3 py-1 rounded-md border border-cyan-800/80">{tag}</span>' for tag in destacado.get('tags', [])])}
              </div>
            </div>
            
            <div class="flex flex-wrap items-center gap-4">
              <button onclick="openModal('{destacado.get('video_url', '')}', '{destacado.get('titulo', '')}')" class="px-6 py-3 bg-cyan-400 text-black font-black text-xs font-mono uppercase tracking-wider rounded-xl hover:bg-cyan-300 transition shadow-[0_0_25px_rgba(0,240,255,0.5)] flex items-center gap-2">
                <span>▶</span> VER DEMO HD AMPLADA
              </button>
              {f'<a href="{destacado["link"]}" target="_blank" class="px-6 py-3 bg-transparent border-2 border-cyan-400/60 text-cyan-400 font-bold text-xs font-mono uppercase tracking-wider rounded-xl hover:bg-cyan-400/10 transition">Google Play ➔</a>' if destacado.get('link') else ''}
            </div>
          </div>

          <div class="lg:col-span-6">
            <div class="relative group cursor-pointer aspect-video w-full rounded-2xl overflow-hidden border border-cyan-500/50 shadow-2xl bg-black" onclick="openModal('{destacado.get('video_url', '')}', '{destacado.get('titulo', '')}')">
              {render_media(destacado.get('video_url', ''), destacado.get('titulo', ''))}
              <div class="absolute inset-0 bg-black/40 group-hover:bg-black/10 transition flex items-center justify-center">
                <span class="px-4 py-2 bg-black/80 border border-cyan-400/80 text-cyan-400 font-mono text-xs rounded-lg backdrop-blur-md opacity-90 group-hover:scale-110 transition duration-300">
                  🔍 Clic para pantalla completa
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    """

    html_content += """
    <!-- OTHER PROJECTS GRID -->
    <section class="mb-24">
      <h3 class="text-2xl font-black text-white font-mono uppercase tracking-wider mb-8 text-cyan-400 border-l-4 border-cyan-400 pl-4">
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
            
            <h4 class="text-2xl font-bold text-white mb-3 leading-snug">{p.get('titulo', '')}</h4>
            <p class="text-gray-300 text-xs leading-relaxed mb-6 font-light">{p.get('descripcion', '')}</p>

            <div class="relative group cursor-pointer aspect-video w-full rounded-xl overflow-hidden border border-cyan-900/80 mb-6 bg-black" onclick="openModal('{p.get('video_url', '')}', '{p.get('titulo', '')}')">
              {render_media(p.get('video_url', ''), p.get('titulo', ''))}
              <div class="absolute inset-0 bg-black/40 group-hover:bg-black/10 transition flex items-center justify-center">
                <span class="px-3 py-1.5 bg-black/80 border border-cyan-400/80 text-cyan-400 font-mono text-[11px] rounded-lg backdrop-blur-md opacity-90 group-hover:scale-105 transition duration-300">
                  🔍 Clic para ampliar
                </span>
              </div>
            </div>
          </div>

          <div>
            <div class="flex flex-wrap gap-2 mb-6">
              {"".join([f'<span class="text-[10px] font-mono bg-black/60 text-gray-300 px-2.5 py-1 rounded-md border border-gray-800">{tag}</span>' for tag in p.get('tags', [])])}
            </div>
            <button onclick="openModal('{p.get('video_url', '')}', '{p.get('titulo', '')}')" class="w-full py-3 bg-cyan-950/80 border border-cyan-400/70 text-cyan-400 font-mono font-bold text-xs uppercase tracking-wider rounded-xl hover:bg-cyan-400 hover:text-black transition duration-300 shadow-[0_0_15px_rgba(0,240,255,0.2)] flex items-center justify-center gap-2">
              <span>🔍</span> AMPLIAR DEMO EN HD
            </button>
          </div>
        </div>
        """

    html_content += """
      </div>
    </section>

  </main>

  <!-- MODAL / LIGHTBOX HD PANTALLA COMPLETA -->
  <div id="videoModal" class="fixed inset-0 z-50 bg-black/95 backdrop-blur-2xl hidden flex items-center justify-center p-4 md:p-10 transition-all">
    <div class="relative w-full max-w-5xl bg-cyber-card border border-cyan-400 rounded-2xl overflow-hidden shadow-[0_0_60px_rgba(0,240,255,0.35)]">
      <div class="flex justify-between items-center px-6 py-4 border-b border-cyan-900/80 bg-[#020617]">
        <h3 id="modalTitle" class="text-sm font-bold text-cyan-400 font-mono uppercase tracking-wider">DEMO VIDEO</h3>
        <button onclick="closeModal()" class="text-cyan-400 hover:text-white font-mono text-lg font-bold px-3 py-1 bg-cyan-950 rounded-lg border border-cyan-800 hover:bg-cyan-800 transition">✕ CERRAR</button>
      </div>
      <div id="modalMediaContainer" class="aspect-video w-full bg-black">
        <!-- Inyectado dinámicamente -->
      </div>
    </div>
  </div>

  <script>
    function openModal(url, title) {
      if(!url) return;
      const modal = document.getElementById('videoModal');
      const modalTitle = document.getElementById('modalTitle');
      const container = document.getElementById('modalMediaContainer');

      modalTitle.innerText = title || "DEMO VIDEO";

      if (url.includes("youtube.com") || url.includes("youtu.be")) {
        let ytId = url.split('/').pop().split('?')[0];
        if (url.includes("watch?v=")) {
            ytId = url.split('v=')[1].split('&')[0];
        }
        container.innerHTML = `<iframe class="w-full h-full" src="https://www.youtube.com/embed/${ytId}?autoplay=1&controls=1" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;
      } else {
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

  <footer id="contacto" class="py-10 border-t border-cyan-900/60 text-center text-xs font-mono text-gray-400 bg-[#020617]">
    <p class="mb-2 text-cyan-400 font-bold">STEFANO DEL MORO</p>
    <p>Software & Android Engineering Portfolio • Quito, Ecuador</p>
  </footer>

</body>
</html>
"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("✅ Portafolio con diseño en cuadrícula, navbar fija y visualizador HD listo.")

if __name__ == '__main__':
    generar_html()
