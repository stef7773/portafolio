import json

def generar_html():
    try:
        with open('proyectos.json', 'r', encoding='utf-8') as f:
            proyectos = json.load(f)
    except Exception as e:
        print(f"Error al cargar proyectos.json: {e}")
        return

    # Separar proyecto destacado si existe
    destacado = next((p for p in proyectos if p.get('destacado')), proyectos[0] if proyectos else None)
    otros_proyectos = [p for p in proyectos if p != destacado]

    html_content = f"""<!DOCTYPE html>
<html lang="es" class="dark">
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
            neon: {{
              blue: '#00f0ff',
              cyan: '#00d8f6',
              bg: '#030712',
              card: '#091322',
              border: '#00f0ff'
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
        linear-gradient(to right, rgba(0, 240, 255, 0.04) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(0, 240, 255, 0.04) 1px, transparent 1px);
      background-size: 32px 32px;
    }}
    .glow-text {{
      text-shadow: 0 0 15px rgba(0, 240, 255, 0.6);
    }}
    .glow-card {{
      box-shadow: 0 0 20px rgba(0, 240, 255, 0.15);
    }}
    .glow-card:hover {{
      box-shadow: 0 0 30px rgba(0, 240, 255, 0.35);
    }}
  </style>
</head>
<body class="text-gray-200 min-h-screen font-sans antialiased">

  <div class="max-w-6xl mx-auto px-6 py-10">
    
    <!-- HEADER -->
    <header class="flex justify-between items-center mb-12 border-b border-cyan-900/50 pb-6">
      <div class="flex items-center gap-3">
        <span class="w-3 h-3 bg-neon-blue rounded-full shadow-[0_0_12px_#00f0ff]"></span>
        <div>
          <h1 class="text-xl font-bold text-white tracking-wide">Stefano Del Moro</h1>
          <p class="text-xs text-neon-blue font-mono">Full Stack & AI Engineer • Android Architect</p>
        </div>
      </div>
      <a href="#contacto" class="px-4 py-2 bg-neon-blue/10 border border-neon-blue/50 text-neon-blue text-xs font-mono font-bold rounded-lg hover:bg-neon-blue hover:text-black transition duration-300">
        CONTACTAR
      </a>
    </header>

    <!-- HERO SECTION -->
    <div class="text-center max-w-3xl mx-auto mb-16">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
        <div class="p-4 bg-neon-card/80 border border-cyan-900/60 rounded-xl glow-card">
          <span class="text-xl font-black text-neon-blue block">3+ Años</span>
          <span class="text-[10px] font-mono text-gray-400 uppercase">Desarrollo Android</span>
        </div>
        <div class="p-4 bg-neon-card/80 border border-cyan-900/60 rounded-xl glow-card">
          <span class="text-xl font-black text-neon-blue block">LLM Local</span>
          <span class="text-[10px] font-mono text-gray-400 uppercase">IA Offline Módulos</span>
        </div>
        <div class="p-4 bg-neon-card/80 border border-cyan-900/60 rounded-xl glow-card">
          <span class="text-xl font-black text-neon-blue block">Linux Mint</span>
          <span class="text-[10px] font-mono text-gray-400 uppercase">Entorno & Tools</span>
        </div>
        <div class="p-4 bg-neon-card/80 border border-cyan-900/60 rounded-xl glow-card">
          <span class="text-xl font-black text-neon-blue block">7+</span>
          <span class="text-[10px] font-mono text-gray-400 uppercase">Proyectos Clave</span>
        </div>
      </div>

      <h2 class="text-3xl md:text-5xl font-black text-white leading-tight mb-4 glow-text">
        Soluciones de Alto Impacto con <br/>
        <span class="text-neon-blue">Inteligencia Artificial & Android NATIVO</span>
      </h2>
      <p class="text-gray-400 text-sm md:text-base leading-relaxed">
        Especializado en aplicaciones Android con IA local, herramientas de alto rendimiento para Linux Mint y automatizaciones avanzadas.
      </p>
    </div>

    <!-- PROYECTO INSIGNIA / DESTACADO -->
    """

    if destacado:
        html_content += f"""
    <section class="mb-16">
      <div class="bg-neon-card border border-neon-blue/60 rounded-2xl p-6 md:p-8 glow-card transition duration-300">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          <div class="lg:col-span-6 flex flex-col justify-between">
            <div>
              <span class="inline-block px-3 py-1 bg-neon-blue/10 border border-neon-blue/40 text-neon-blue font-mono font-bold text-xs uppercase tracking-wider rounded-md mb-4">
                {destacado.get('categoria', 'PROYECTO INSIGNIA')}
              </span>
              <h3 class="text-2xl md:text-3xl font-extrabold text-white mb-4">
                {destacado.get('titulo', '')}
              </h3>
              <p class="text-gray-300 text-sm md:text-base leading-relaxed mb-6">
                {destacado.get('descripcion', '')}
              </p>
              <div class="flex flex-wrap gap-2 mb-6">
                {"".join([f'<span class="text-xs font-mono bg-gray-950 text-neon-blue px-3 py-1 rounded-md border border-cyan-900">{tag}</span>' for tag in destacado.get('tags', [])])}
              </div>
            </div>
            {f'<a href="{destacado["link"]}" target="_blank" class="inline-flex items-center gap-2 px-6 py-3 bg-neon-blue text-black font-bold text-sm rounded-xl hover:bg-cyan-300 transition shadow-[0_0_20px_rgba(0,240,255,0.4)] w-fit">▶ Ver en Google Play</a>' if destacado.get('link') else ''}
          </div>
          <div class="lg:col-span-6">
            <div class="aspect-video w-full bg-gray-950 rounded-xl overflow-hidden border border-cyan-800 shadow-inner">
              <video class="w-full h-full object-cover" controls autoplay loop muted playsinline>
                <source src="{destacado.get('video_url', '')}" type="video/mp4">
              </video>
            </div>
          </div>
        </div>
      </div>
    </section>
    """

    html_content += """
    <!-- GRID DE OTROS PROYECTOS -->
    <section>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    """

    for p in otros_proyectos:
        html_content += f"""
        <div class="bg-neon-card border border-cyan-900/80 hover:border-neon-blue/60 rounded-2xl p-6 transition duration-300 flex flex-col justify-between glow-card">
          <div>
            <!-- Badge superior con espacio suficiente -->
            <div class="mb-4">
              <span class="inline-block px-2.5 py-1 bg-neon-blue/10 border border-neon-blue/30 text-neon-blue text-[10px] font-mono font-bold tracking-wider uppercase rounded-md">
                {p.get('categoria', '')}
              </span>
            </div>
            
            <h4 class="text-lg font-bold text-white mb-3 leading-snug">{p.get('titulo', '')}</h4>
            <p class="text-gray-400 text-xs leading-relaxed mb-6">{p.get('descripcion', '')}</p>

            <div class="aspect-video w-full bg-gray-950 rounded-xl overflow-hidden border border-cyan-900/60 mb-6">
              <video class="w-full h-full object-cover" controls loop muted playsinline>
                <source src="{p.get('video_url', '')}" type="video/mp4">
              </video>
            </div>
          </div>

          <div>
            <div class="flex flex-wrap gap-1.5">
              {"".join([f'<span class="text-[10px] font-mono bg-gray-950 text-gray-300 px-2 py-0.5 rounded border border-gray-800">{tag}</span>' for tag in p.get('tags', [])])}
            </div>
          </div>
        </div>
        """

    html_content += """
      </div>
    </section>

    <footer id="contacto" class="mt-20 pt-8 border-t border-cyan-900/50 text-center text-xs font-mono text-gray-500">
      <p>Stefano Del Moro • Software & Mobile Engineering Portfolio</p>
    </footer>

  </div>

</body>
</html>
"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("✅ Portafolio generado correctamente con la nueva UI arreglada.")

if __name__ == '__main__':
    generar_html()
