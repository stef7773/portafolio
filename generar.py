import json
from jinja2 import Template

with open('proyectos.json', 'r', encoding='utf-8') as f:
    proyectos = json.load(f)

categorias = sorted(list(set(p['categoria'] for p in proyectos)))

html_template = """<!DOCTYPE html>
<html lang="es" class="dark scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stefano Del Moro | Full Stack & AI Engineer</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800;900&family=JetBrains+Mono:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #030712;
            color: #f3f4f6;
        }
        .font-mono { font-family: 'JetBrains Mono', monospace; }
        
        /* Grid background pattern */
        .bg-grid-pattern {
            background-size: 36px 36px;
            background-image: 
                linear-gradient(to right, rgba(6, 182, 212, 0.07) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(6, 182, 212, 0.07) 1px, transparent 1px);
        }

        /* Glow & Text Effects */
        .glow-title {
            text-shadow: 0 0 35px rgba(6, 182, 212, 0.45);
        }

        /* Neon Glow card animation */
        .project-card {
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .project-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 40px -15px rgba(6, 182, 212, 0.3);
            border-color: rgba(56, 189, 248, 0.5);
        }

        /* Filter buttons */
        .filter-btn.active {
            background: linear-gradient(135deg, #0284c7 0%, #06b6d4 100%);
            color: #ffffff;
            border-color: #38bdf8;
            box-shadow: 0 0 20px rgba(6, 182, 212, 0.5);
        }

        /* Glassmorphism */
        .glass-panel {
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(14px);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
    </style>
</head>
<body class="bg-grid-pattern min-h-screen flex flex-col justify-between selection:bg-cyan-500 selection:text-black">

    <!-- Navbar / Header -->
    <nav class="sticky top-0 z-40 glass-panel border-b border-slate-800/80 px-6 py-4 shadow-[0_4px_30px_rgba(0,0,0,0.8)]">
        <div class="max-w-7xl mx-auto flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <div class="w-3.5 h-3.5 rounded-full bg-cyan-400 animate-pulse shadow-[0_0_12px_#06b6d4]"></div>
                <span class="font-black text-xl text-white tracking-wider uppercase">Stefano Del Moro</span>
            </div>
            <div class="flex items-center space-x-4">
                <span class="text-xs font-mono font-bold text-cyan-400 bg-cyan-950/80 border border-cyan-800/80 px-4 py-1.5 rounded-full hidden sm:inline-block tracking-wider uppercase">
                    ⚡ Full Stack & AI Architect
                </span>
                <a href="#contacto" class="text-xs font-black uppercase tracking-widest bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white px-5 py-2.5 rounded-xl transition shadow-lg shadow-cyan-950/80">
                    Contactar
                </a>
            </div>
        </div>
    </nav>

    <!-- Hero Section con Titulares Potentes -->
    <section class="relative text-center py-20 px-6 overflow-hidden">
        <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[700px] bg-cyan-500/10 rounded-full blur-[140px] pointer-events-none"></div>
        
        <div class="relative z-10 max-w-5xl mx-auto" data-aos="fade-down">
            <span class="inline-flex items-center gap-2 px-4 py-2 mb-6 text-xs font-mono font-bold tracking-widest text-cyan-300 uppercase bg-slate-900/90 border border-cyan-500/40 rounded-full shadow-[0_0_15px_rgba(6,182,212,0.2)]">
                <span class="w-2 h-2 rounded-full bg-cyan-400"></span>
                Portafolio de Ingeniería de Software & Inteligencia Artificial
            </span>
            
            <h1 class="text-4xl sm:text-6xl md:text-7xl font-black text-white mb-6 tracking-tight leading-tight uppercase">
                ARQUITECTURA MÓVIL, <br/>
                <span class="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-cyan-200 to-blue-500 glow-title">IA LOCAL & HIGH-SCALE SYSTEMS</span>
            </h1>
            
            <p class="text-slate-300 text-base sm:text-lg max-w-3xl mx-auto leading-relaxed mb-10 font-normal">
                Especialista en aplicaciones Android nativas con motores LLM de inferencia offline, automatización avanzada en entornos Linux Mint y sistemas de alto rendimiento.
            </p>
            
            <!-- Quick Stats Bar -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto glass-panel p-5 rounded-2xl border border-slate-800/90 shadow-2xl">
                <div>
                    <div class="text-3xl font-black text-cyan-400 font-mono">3+ Años</div>
                    <div class="text-[11px] font-bold text-slate-400 uppercase tracking-wider mt-1">Desarrollo Android</div>
                </div>
                <div>
                    <div class="text-3xl font-black text-cyan-400 font-mono">LLM Local</div>
                    <div class="text-[11px] font-bold text-slate-400 uppercase tracking-wider mt-1">IA Offline Módulos</div>
                </div>
                <div>
                    <div class="text-3xl font-black text-cyan-400 font-mono">Linux Mint</div>
                    <div class="text-[11px] font-bold text-slate-400 uppercase tracking-wider mt-1">Entorno & Automation</div>
                </div>
                <div>
                    <div class="text-3xl font-black text-cyan-400 font-mono">7+</div>
                    <div class="text-[11px] font-bold text-slate-400 uppercase tracking-wider mt-1">Sistemas Clave</div>
                </div>
            </div>
        </div>
    </section>

    <!-- Main Projects Section -->
    <main class="max-w-7xl mx-auto px-6 py-4 flex-grow w-full">
        
        <!-- Filter Controls -->
        <div class="flex flex-wrap justify-center gap-2 mb-12" data-aos="fade-up">
            <button onclick="filterProjects('all')" class="filter-btn active text-xs font-bold uppercase tracking-wider px-5 py-2.5 rounded-xl border border-slate-800 bg-slate-900 text-slate-300 hover:border-cyan-500 transition">
                Todos los Proyectos ({{ proyectos|length }})
            </button>
            {% for cat in categorias %}
            <button onclick="filterProjects('{{ cat }}')" class="filter-btn text-xs font-bold uppercase tracking-wider px-5 py-2.5 rounded-xl border border-slate-800 bg-slate-900 text-slate-300 hover:border-cyan-500 transition">
                {{ cat }}
            </button>
            {% endfor %}
        </div>

        <!-- Projects Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="projects-grid">
            {% for p in proyectos %}
            <div class="project-card glass-panel border border-slate-800/90 rounded-2xl overflow-hidden flex flex-col justify-between" 
                 data-category="{{ p.categoria }}" data-aos="fade-up">
                
                <div>
                    <!-- Visual Header / Thumbnail -->
                    <div class="relative h-52 w-full overflow-hidden bg-slate-950 group cursor-pointer" onclick="openMediaModal('{{ p.media_type }}', '{{ p.media_url }}', '{{ p.titulo }}')">
                        {% if p.media_type == 'video' %}
                        <video autoplay loop muted playsinline class="w-full h-full object-cover group-hover:scale-105 transition duration-500 opacity-80 group-hover:opacity-100">
                            <source src="{{ p.media_url }}" type="video/mp4">
                        </video>
                        <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/20 to-transparent"></div>
                        <span class="absolute bottom-3 right-3 bg-cyan-950/90 text-cyan-300 border border-cyan-800 text-[10px] font-mono font-bold px-2.5 py-1 rounded-md flex items-center gap-1 shadow-md">
                            ▶ VER VIDEO DEMO
                        </span>
                        {% else %}
                        <img src="{{ p.media_url }}" alt="{{ p.titulo }}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500 opacity-80 group-hover:opacity-100">
                        <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/20 to-transparent"></div>
                        <span class="absolute bottom-3 right-3 bg-slate-900/90 text-cyan-300 border border-slate-700 text-[10px] font-mono font-bold px-2.5 py-1 rounded-md flex items-center gap-1 shadow-md">
                            🔍 AMPLIAR CAPTURA
                        </span>
                        {% endif %}

                        <span class="absolute top-3 left-3 text-[10px] uppercase tracking-widest text-cyan-300 font-extrabold px-3 py-1 bg-cyan-950/90 border border-cyan-800 rounded-lg">
                            {{ p.categoria }}
                        </span>
                    </div>

                    <!-- Card Body -->
                    <div class="p-6">
                        <h3 class="text-2xl font-bold text-white mb-1 tracking-tight">{{ p.titulo }}</h3>
                        <p class="text-xs font-mono font-bold text-cyan-400 mb-3">{{ p.subtitulo }}</p>
                        <p class="text-slate-400 text-sm mb-6 leading-relaxed">{{ p.descripcion }}</p>
                    </div>
                </div>

                <!-- Card Footer / Tech & Links -->
                <div class="px-6 pb-6">
                    <div class="flex flex-wrap gap-1.5 mb-6">
                        {% for tech in p.techs %}
                        <span class="bg-slate-950 border border-slate-800 text-cyan-300 text-[11px] font-mono px-2.5 py-1 rounded-md">
                            {{ tech }}
                        </span>
                        {% endfor %}
                    </div>

                    <div class="flex gap-2">
                        {% if p.link_demo %}
                        <a href="{{ p.link_demo }}" target="_blank" class="flex-1 text-center bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold py-2.5 px-3 rounded-xl text-xs uppercase tracking-wider transition shadow-lg shadow-cyan-950/50">
                            Play Store / Demo
                        </a>
                        {% endif %}

                        <button onclick="openMediaModal('{{ p.media_type }}', '{{ p.media_url }}', '{{ p.titulo }}')" class="flex-1 text-center bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-slate-700 font-bold py-2.5 px-3 rounded-xl text-xs uppercase tracking-wider transition">
                            {% if p.media_type == 'video' %}🎬 Ver Demo Video{% else %}🖼️ Captura HD{% endif %}
                        </button>
                    </div>
                </div>

            </div>
            {% endfor %}
        </div>
    </main>

    <!-- Contact & Footer Section -->
    <section id="contacto" class="border-t border-slate-800/80 bg-slate-950/80 py-16 px-6 mt-20">
        <div class="max-w-4xl mx-auto text-center">
            <h2 class="text-3xl font-black text-white mb-4">¿Interesado en colaborar o contratar?</h2>
            <p class="text-slate-400 mb-8 max-w-xl mx-auto">
                Disponible para oportunidades como Full Stack Developer, Android Engineer o desarrollador de soluciones de Inteligencia Artificial.
            </p>
            <div class="flex flex-wrap justify-center gap-4">
                <a href="https://github.com/stef7773" target="_blank" class="bg-slate-900 hover:bg-slate-800 text-white font-mono text-sm px-6 py-3 rounded-xl border border-slate-700 transition flex items-center gap-2">
                    💻 GitHub: @stef7773
                </a>
            </div>
        </div>
    </section>

    <footer class="text-center py-6 text-slate-600 border-t border-slate-900 text-xs font-mono">
        <p>© Stefano Del Moro — Desarrollado en Linux Mint & Python 3</p>
    </footer>

    <!-- Fullscreen Lightbox / Media Modal -->
    <div id="mediaModal" class="fixed inset-0 bg-black/95 backdrop-blur-xl hidden z-50 flex items-center justify-center p-4">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl max-w-5xl w-full p-4 relative overflow-hidden flex flex-col shadow-2xl">
            <div class="flex justify-between items-center mb-4 px-2 border-b border-slate-800 pb-3">
                <h3 id="modalTitle" class="text-xl font-bold text-cyan-400 font-mono"></h3>
                <button onclick="closeMediaModal()" class="text-slate-400 hover:text-white text-3xl font-bold leading-none px-3">&times;</button>
            </div>
            <div id="modalBody" class="w-full flex justify-center items-center rounded-xl overflow-hidden bg-black/80 min-h-[400px]">
                <!-- Media rendered here dynamically -->
            </div>
        </div>
    </div>

    <!-- Scripts -->
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    <script>
        AOS.init({ duration: 600, once: true });

        function filterProjects(category) {
            const cards = document.querySelectorAll('.project-card');
            const buttons = document.querySelectorAll('.filter-btn');
            
            buttons.forEach(btn => btn.classList.remove('active'));
            event.currentTarget.classList.add('active');

            cards.forEach(card => {
                if (category === 'all' || card.getAttribute('data-category') === category) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        }

        function openMediaModal(type, url, title) {
            const modal = document.getElementById('mediaModal');
            const modalBody = document.getElementById('modalBody');
            document.getElementById('modalTitle').innerText = title;

            if (type === 'video') {
                modalBody.innerHTML = `<video controls autoplay loop class="max-h-[80vh] w-full object-contain rounded-lg"><source src="${url}" type="video/mp4">Navegador no soporta video.</video>`;
            } else {
                modalBody.innerHTML = `<img src="${url}" class="max-h-[80vh] w-auto object-contain rounded-lg" alt="${title}">`;
            }

            modal.classList.remove('hidden');
        }

        function closeMediaModal() {
            const modal = document.getElementById('mediaModal');
            document.getElementById('modalBody').innerHTML = '';
            modal.classList.add('hidden');
        }

        document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeMediaModal(); });
    </script>
</body>
</html>
"""

template = Template(html_template)
output_html = template.render(proyectos=proyectos, categorias=categorias)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(output_html)

print("✅ Landing page 'index.html' generada con los videos funcionales y títulos mejorados.")
