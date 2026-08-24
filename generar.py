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
            return '<div class="w-full h-full bg-gray-950 flex items-center justify-center font-mono text-xs text-gray-600">[ MEDIA PREVIEW ]</div>'
        if "youtube.com" in url or "youtu.be" in url:
            return f'<iframe class="w-full h-full rounded-xl" src="{url}" title="{titulo}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
        else:
            return f'''<video class="w-full h-full object-cover rounded-xl" controls loop muted playsinline>
                <source src="{url}" type="video/mp4">
                Tu navegador no soporta el formato de video.
            </video>'''

    html_content = f"""<!DOCTYPE html>
<html lang="es" class="dark scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Stefano Del Moro | Full Stack & AI Engineer</title>
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
              border: '#0d2d4a'
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
        radial-gradient(circle at 50% 0%, rgba(0, 240, 255, 0.08) 0%, transparent 50%),
        linear-gradient(to right, rgba(0, 240, 255, 0.03) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(0, 240, 255, 0.03) 1px, transparent 1px);
      background-size: 100% 100%, 32px 32px, 32px 32px;
    }}
    .glow-cyan {{
      box-shadow: 0 0 25px rgba(0, 240, 255, 0.15);
    }}
    .glow-cyan:hover {{
      box-shadow: 0 0 35px rgba(0, 240, 255, 0.3);
    }}
    .glow-text {{
      text-shadow: 0 0 15px rgba(0, 240, 255, 0.5);
    }}
  </style>
</head>
<body class="text-gray-200 min-h-screen font-sans antialiased pt-24">

  <!-- NAVBAR FIXED ROBUSTO -->
  <header class="fixed top-0 left-0 right-0 z-50 bg-cyber-dark/90 backdrop-blur-md border-b border-cyber-border/80 px-6 py-4 shadow-2xl">
    <div class="max-w-6xl mx-auto flex justify-between items-center">
      <div class="flex items-center gap-3">
        <span class="relative flex h-3 w-3">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyber-blue opacity-75"></span>
          <span class="relative inline-flex rounded-full h-3 w-3 bg-cyber-blue shadow-[0_0_10px_#00f0ff]"></span>
        </span>
        <div>
          <h1 class="text-lg font-black text-white tracking-wider uppercase">Stefano Del Moro</h1>
          <p class="text-[11px] text-cyber-blue font-mono font-semibold tracking-wide">Full Stack & AI Engineer • Android Architect</p>
        </div>
      </div>
      
      <div class="flex items-center gap-4">
        <div class="hidden sm:flex items-center gap-2 px-3 py-1 bg-cyber-card border border-cyber-border rounded-lg text-xs font-mono text-cyber-blue">
          <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
          <span>SYS_STATUS: ONLINE</span>
        </div>
        <a href="#contacto" class="px-5 py-2 bg-cyber-blue/10 border border-cyber-blue/60 text-cyber-blue text-xs font-mono font-bold rounded-xl hover:bg-cyber-blue hover:text-black transition duration-300 shadow-[0_0_15px_rgba(0,240,255,0.2)]">
          CONTACTAR
        </a>
      </div>
    </div>
  </header>

  <main class="max-w-6xl mx-auto px-6 py-6">

    <!-- HERO METRICS & TITLE -->
    <div class="text-center max-w-3xl mx-auto mb-16">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
        <div class="p-4 bg-cyber-card border border-cyber-border/80 rounded-2xl glow-cyan">
          <span class="text-2xl font-black text-cyber-blue block">3+ Años</span>
          <span class="text-[10px] font-mono text-gray-400 uppercase tracking-wider">Desarrollo Android</span>
        </div>
        <div class="p-4 bg-cyber-card border border-cyber-border/80 rounded-2xl glow-cyan">
          <span class="text-2xl font-black text-cyber-blue block">LLM Local</span>
          <span class="text-[10px] font-mono text-gray-400 uppercase tracking-wider">IA Offline Módulos</span>
        </div>
        <div class="p-4 bg-cyber-card border border-cyber-border/80 rounded-2xl glow-cyan">
          <span class="text-2xl font-black text-cyber-blue block">Linux Mint</span>
          <span class="text-[10px] font-mono text-gray-400 uppercase tracking-wider">Entorno & Tools</span>
        </div>
        <div class="p-4 bg-cyber-card border border-cyber-border/80 rounded-2xl glow-cyan">
          <span class="text-2xl font-black text-cyber-blue block">7+</span>
          <span class="text-[10px] font-mono text-gray-400 uppercase tracking-wider">Proyectos Clave</span>
        </div>
      </div>

      <span class="px-4 py-1.5 rounded-full text-xs font-mono font-semibold bg-cyber-blue/10 text-cyber-blue border border-cyber-blue/30 uppercase tracking-widest inline-block mb-4">
        Sistemas Autónomos & Movilidad Inteligente
      </span>

      <h2 class="text-3xl md:text-5xl font-black text-white leading-tight mb-4 glow-text">
        Soluciones de Alto Impacto con <br/>
        <span class="text-cyber-blue">Inteligencia Artificial & Android NATIVO</span>
      </h2>
      <p class="text-gray-400 text-sm md:text-base leading-relaxed">
        Especializado en aplicaciones Android con IA local, herramientas de alto rendimiento para Linux Mint y automatizaciones avanzadas.
      </p>
    </div>

    <!-- PROYECTO INSIGNIA -->
    """

    if destacado:
        html_content += f"""
    <section class="mb-16">
      <div class="bg-cyber-card border border-cyber-blue/60 rounded-3xl p-6 md:p-8 glow-cyan transition duration-300">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          <div class="lg:col-span-6 flex flex-col justify-between h-full">
            <div>
              <div class="mb-4">
                <span class="px-3 py-1 bg-cyber-blue/10 border border-cyber-blue/50 text-cyber-blue font-mono font-bold text-xs uppercase tracking-wider rounded-lg">
                  {destacado.get('categoria', 'PROYECTO INSIGNIA')}
                </span>
              </div>
              <h3 class="text-2xl md:text-3xl font-black text-white mb-4 leading-tight">
                {destacado.get('titulo', '')}
              </h3>
              <p class="text-gray-300 text-sm md:text-base leading-relaxed mb-6">
                {destacado.get('descripcion', '')}
              </p>
              <div class="flex flex-wrap gap-2 mb-8">
                {"".join([f'<span class="text-xs font-mono bg-gray-950 text-cyber-blue px-3 py-1 rounded-lg border border-cyber-border">{tag}</span>' for tag in destacado.get('tags', [])])}
              </div>
            </div>
            {f'<a href="{destacado["link"]}" target="_blank" class="inline-flex items-center gap-2 px-6 py-3 bg-cyber-blue text-black font-black text-xs uppercase tracking-wider rounded-xl hover:bg-cyan-300 transition shadow-[0_0_20px_rgba(0,240,255,0.4)] w-fit">▶ Ver en Google Play</a>' if destacado.get('link') else ''}
          </div>
          <div class="lg:col-span-6">
            <div class="aspect-video w-full bg-gray-950 rounded-2xl overflow-hidden border border-cyber-border shadow-2xl">
              {render_media(destacado.get('video_url', ''), destacado.get('titulo', ''))}
            </div>
          </div>
        </div>
      </div>
    </section>
    """

    html_content += """
    <!-- OTHER PROJECTS GRID -->
    <section>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
    """

    for p in otros_proyectos:
        html_content += f"""
        <div class="bg-cyber-card border border-cyber-border hover:border-cyber-blue/60 rounded-2xl p-6 transition duration-300 flex flex-col justify-between glow-cyan">
          <div>
            <div class="mb-3">
              <span class="px-2.5 py-1 bg-cyber-blue/10 border border-cyber-blue/40 text-cyber-blue text-[11px] font-mono font-bold tracking-wider uppercase rounded-md inline-block">
                {p.get('categoria', '')}
              </span>
            </div>
            
            <h4 class="text-xl font-bold text-white mb-3 leading-snug">{p.get('titulo', '')}</h4>
            <p class="text-gray-400 text-xs leading-relaxed mb-6">{p.get('descripcion', '')}</p>

            <div class="aspect-video w-full bg-gray-950 rounded-xl overflow-hidden border border-cyber-border mb-6">
              {render_media(p.get('video_url', ''), p.get('titulo', ''))}
            </div>
          </div>

          <div>
            <div class="flex flex-wrap gap-2">
              {"".join([f'<span class="text-[10px] font-mono bg-gray-950 text-gray-300 px-2.5 py-1 rounded-md border border-gray-800">{tag}</span>' for tag in p.get('tags', [])])}
            </div>
          </div>
        </div>
        """

    html_content += """
      </div>
    </section>

  </main>

  <footer id="contacto" class="mt-20 py-8 border-t border-cyber-border/80 text-center text-xs font-mono text-gray-500 bg-cyber-dark">
    <p>Stefano Del Moro • Software & Mobile Engineering Portfolio</p>
  </footer>

</body>
</html>
"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("✅ Portafolio Senior generado con Navbar fija, paleta cyber y embeds corregidos.")

if __name__ == '__main__':
    generar_html()
