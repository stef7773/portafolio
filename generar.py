import json
from jinja2 import Template

# Cargar proyectos desde el archivo JSON
with open('proyectos.json', 'r', encoding='utf-8') as f:
    proyectos = json.load(f)

# Extraer categorías únicas para los filtros
categorias = sorted(list(set(p['categoria'] for p in proyectos)))

html_template = """<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stefano Del Moro | Software & AI Engineer</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
    <style>
        body { background-color: #030712; color: #f3f4f6; }
        .card-glow {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .card-glow:hover {
            box-shadow: 0 0 30px rgba(14, 165, 233, 0.25);
            transform: translateY(-6px);
            border-color: rgba(56, 189, 248, 0.5);
        }
        .filter-btn.active {
            background-color: #0284c7;
            color: #ffffff;
            border-color: #38bdf8;
        }
    </style>
</head>
<body class="font-sans antialiased selection:bg-cyan-500 selection:text-black min-h-screen flex flex-col justify-between">

    <!-- Hero Header -->
    <header class="relative text-center py-20 px-6 border-b border-slate-800/80 bg-slate-950/60 overflow-hidden">
        <div class="absolute inset-0 bg-[radial-gradient(circle_at_top,_var(--tw-gradient-stops))] from-cyan-950/30 via-transparent to-transparent pointer-events-none"></div>
        <div class="relative z-10 max-w-4xl mx-auto" data-aos="fade-down">
            <span class="inline-block px-3 py-1 mb-4 text-xs font-semibold tracking-wider text-cyan-400 uppercase bg-cyan-950/60 border border-cyan-800/50 rounded-full">
                Software & Full Stack Developer
            </span>
            <h1 class="text-5xl sm:text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-sky-300 to-blue-500 mb-4 tracking-tight">
                Portafolio de Proyectos
            </h1>
            <p class="text-slate-400 text-lg max-w-2xl mx-auto leading-relaxed">
                Ecosistema de aplicaciones Android, inteligencia artificial local, utilidades para Linux Mint y bots de automatización.
            </p>
        </div>
    </header>

    <!-- Filtros y Grid de Proyectos -->
    <main class="max-w-7xl mx-auto px-6 py-12 flex-grow w-full">
        
        <!-- Botones de Filtrado -->
        <div class="flex flex-wrap justify-center gap-2 mb-12" data-aos="fade-up">
            <button onclick="filterProjects('all')" class="filter-btn active text-xs font-bold uppercase tracking-wider px-4 py-2 rounded-xl border border-slate-800 bg-slate-900 text-slate-300 hover:border-cyan-500 transition">
                Todos ({{ proyectos|length }})
            </button>
            {% for cat in categorias %}
            <button onclick="filterProjects('{{ cat }}')" class="filter-btn text-xs font-bold uppercase tracking-wider px-4 py-2 rounded-xl border border-slate-800 bg-slate-900 text-slate-300 hover:border-cyan-500 transition">
                {{ cat }}
            </button>
            {% endfor %}
        </div>

        <!-- Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="projects-grid">
            {% for p in proyectos %}
            <div class="project-card bg-slate-900/90 border border-slate-800 rounded-2xl p-6 card-glow flex flex-col justify-between" 
                 data-category="{{ p.categoria }}" 
                 data-aos="fade-up">
                <div>
                    <div class="flex justify-between items-center mb-3">
                        <span class="text-[10px] uppercase tracking-widest text-cyan-400 font-extrabold px-2.5 py-1 bg-cyan-950/80 border border-cyan-900 rounded-md">
                            {{ p.categoria }}
                        </span>
                    </div>
                    <h3 class="text-2xl font-bold text-white mb-3 tracking-tight">{{ p.titulo }}</h3>
                    <p class="text-slate-400 text-sm mb-6 leading-relaxed">{{ p.descripcion }}</p>
                </div>
                
                <div>
                    <div class="flex flex-wrap gap-1.5 mb-6">
                        {% for tech in p.techs %}
                        <span class="bg-slate-950 border border-slate-800 text-cyan-300 text-[11px] px-2.5 py-1 rounded-md font-mono">
                            {{ tech }}
                        </span>
                        {% endfor %}
                    </div>
                    
                    <div class="flex gap-3">
                        {% if p.link_demo %}
                        <a href="{{ p.link_demo }}" target="_blank" class="flex-1 text-center bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold py-2.5 px-4 rounded-xl text-xs uppercase tracking-wider transition">
                            Ver App / Demo
                        </a>
                        {% endif %}
                        {% if p.link_repo %}
                        <a href="{{ p.link_repo }}" target="_blank" class="flex-1 text-center border border-slate-700 hover:bg-slate-800 text-white font-semibold py-2.5 px-4 rounded-xl text-xs uppercase tracking-wider transition">
                            Código
                        </a>
                        {% endif %}
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </main>

    <!-- Footer -->
    <footer class="text-center py-8 text-slate-600 border-t border-slate-900 text-xs">
        <p>© Stefano Del Moro — Desarrollado en Linux Mint & Python 3</p>
    </footer>

    <!-- Scripts de Interacción y Animaciones -->
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
    </script>
</body>
</html>
"""

template = Template(html_template)
output_html = template.render(proyectos=proyectos, categorias=categorias)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(output_html)

print("✅ Landing page 'index.html' generada exitosamente con todos tus proyectos.")
