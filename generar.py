import json
from jinja2 import Template

# 1. Cargar datos
with open('proyectos.json', 'r', encoding='utf-8') as f:
    proyectos = json.load(f)

categorias = sorted(list(set(p.get('categoria', 'General') for p in proyectos)))

STATUS_LABELS = {
    "PRODUCTION": "active (running)",
    "PROTOTYPE": "build (prototype)",
    "INTERNAL": "internal (deployed)",
}
STATUS_DOT = {
    "PRODUCTION": "dot-mint",
    "PROTOTYPE": "dot-amber",
    "INTERNAL": "dot-blue",
}

for i, p in enumerate(proyectos):
    p['unit'] = p['id'].replace('_', '-') + '.service'
    p['pid'] = 1000 + i * 137 + len(p['titulo'])
    p['status_label'] = STATUS_LABELS.get(p.get('status'), 'active (running)')
    p['status_dot'] = STATUS_DOT.get(p.get('status'), 'dot-mint')

# 2. Plantilla HTML
html_template = """<!DOCTYPE html>
<html lang="es" class="scroll-smooth">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Stefano Del Moro | Full Stack & AI Architect</title>
<meta name="description" content="Stefano Del Moro — desarrollo de software y soluciones de IA local y en la nube para Android, Linux, Windows y macOS.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='22' fill='%230b0d10'/%3E%3Ctext x='50' y='68' font-size='58' text-anchor='middle' fill='%238fd14f' font-family='monospace'%3E%3E%3C/text%3E%3C/svg%3E">
<script src="https://cdn.tailwindcss.com"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#0b0d10;
  --bg-alt:#0e1114;
  --surface:#12161b;
  --surface-2:#161b21;
  --border:rgba(255,255,255,0.08);
  --border-strong:rgba(255,255,255,0.14);
  --mint:#8fd14f;
  --mint-dim:#5a8f34;
  --mint-glow:rgba(143,209,79,0.35);
  --amber:#ffb454;
  --blue:#5ec8f0;
  --red:#f85149;
  --text:#e9edf0;
  --text-dim:#8b929b;
  --text-faint:#565d66;
}
*{box-sizing:border-box;}
html{background:var(--bg);}
body{
  font-family:'IBM Plex Sans', sans-serif;
  background-color:var(--bg);
  color:var(--text);
  overflow-x:hidden;
}
.font-display{font-family:'Space Grotesk', sans-serif;}
.font-mono{font-family:'JetBrains Mono', monospace;}

::selection{background:var(--mint); color:#0b0d10;}
::-webkit-scrollbar{width:10px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--surface-2); border-radius:8px; border:2px solid var(--bg);}
::-webkit-scrollbar-thumb:hover{background:var(--mint-dim);}

a, button{ -webkit-tap-highlight-color: transparent; }
:focus-visible{ outline:2px solid var(--mint); outline-offset:3px; border-radius:4px; }

/* ---------- background texture ---------- */
.bg-grid{
  position:fixed; inset:0; z-index:0; pointer-events:none;
  background-image:
    linear-gradient(to right, rgba(143,209,79,0.05) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(143,209,79,0.05) 1px, transparent 1px);
  background-size:42px 42px;
  mask-image: radial-gradient(ellipse 80% 60% at 50% 0%, black 40%, transparent 90%);
}
.bg-glow{
  position:fixed; z-index:0; pointer-events:none; border-radius:50%; filter:blur(120px);
  top:-200px; left:50%; transform:translateX(-50%);
  width:900px; height:600px;
  background:radial-gradient(closest-side, rgba(143,209,79,0.16), transparent 70%);
}
.scanline{
  position:fixed; inset:0; z-index:1; pointer-events:none; opacity:0.35;
  background:repeating-linear-gradient(to bottom, rgba(255,255,255,0.015) 0px, rgba(255,255,255,0.015) 1px, transparent 1px, transparent 3px);
}

/* ---------- top scroll progress ---------- */
#scrollbar{ position:fixed; top:0; left:0; height:2px; background:linear-gradient(90deg, var(--mint), var(--blue)); z-index:100; width:0%; box-shadow:0 0 8px var(--mint-glow); }

/* ---------- nav ---------- */
.glass-nav{
  background:rgba(11,13,16,0.72);
  backdrop-filter:blur(14px);
  border-bottom:1px solid var(--border);
}
.status-dot{
  width:8px; height:8px; border-radius:50%; background:var(--mint);
  box-shadow:0 0 0 0 rgba(143,209,79,0.6);
  animation:pulse-ring 2.2s cubic-bezier(0.4,0,0.6,1) infinite;
}
.dot-mint{ background:var(--mint); box-shadow:0 0 8px var(--mint-glow); }
.dot-amber{ background:var(--amber); box-shadow:0 0 8px rgba(255,180,84,0.35); }
.dot-blue{ background:var(--blue); box-shadow:0 0 8px rgba(94,200,240,0.35); }
@keyframes pulse-ring{
  0%{ box-shadow:0 0 0 0 rgba(143,209,79,0.55); }
  70%{ box-shadow:0 0 0 7px rgba(143,209,79,0); }
  100%{ box-shadow:0 0 0 0 rgba(143,209,79,0); }
}

/* ---------- terminal window ---------- */
.term-window{
  background:linear-gradient(180deg, var(--surface) 0%, var(--bg-alt) 100%);
  border:1px solid var(--border-strong);
  border-radius:14px;
  box-shadow:0 30px 60px -20px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.02) inset;
}
.term-bar{
  display:flex; align-items:center; gap:8px;
  padding:11px 14px; border-bottom:1px solid var(--border);
  background:rgba(255,255,255,0.02);
}
.term-dot{ width:10px; height:10px; border-radius:50%; }
.term-body{ padding:20px; min-height:230px; }
.caret{
  display:inline-block; width:8px; height:1.1em; background:var(--mint);
  margin-left:2px; vertical-align:-2px; animation:blink 1s step-end infinite;
}
@keyframes blink{ 50%{ opacity:0; } }
.term-line{ opacity:0; }
.term-line.shown{ opacity:1; }

/* ---------- headline ---------- */
.headline-accent{
  background:linear-gradient(90deg, var(--mint) 0%, #c7e88f 45%, var(--blue) 100%);
  -webkit-background-clip:text; background-clip:text; color:transparent;
}

/* ---------- stat cards ---------- */
.stat-box{
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:12px;
  transition:border-color .3s ease, transform .3s ease;
}
.stat-box:hover{ border-color:rgba(143,209,79,0.35); transform:translateY(-2px); }

/* ---------- platform badge ---------- */
.platform-chip{
  border:1px solid var(--border); background:var(--surface);
  border-radius:999px; padding:6px 14px;
  font-family:'JetBrains Mono', monospace; font-size:11px; letter-spacing:.04em;
  color:var(--text-dim);
}

/* ---------- filter chips ---------- */
.filter-btn{
  font-family:'JetBrains Mono', monospace;
  border:1px solid var(--border); background:var(--surface);
  color:var(--text-dim); border-radius:10px;
  padding:9px 16px; font-size:12px; font-weight:500; letter-spacing:.02em;
  transition:all .25s ease;
}
.filter-btn:hover{ border-color:var(--border-strong); color:var(--text); }
.filter-btn.active{
  background:rgba(143,209,79,0.1);
  border-color:var(--mint);
  color:var(--mint);
  box-shadow:0 0 0 1px rgba(143,209,79,0.15) inset, 0 0 18px rgba(143,209,79,0.12);
}

/* ---------- project cards ---------- */
.unit-card{
  position:relative;
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:16px;
  overflow:hidden;
  transition:transform .35s cubic-bezier(.16,1,.3,1), border-color .35s ease, box-shadow .35s ease;
}
.unit-card:hover{
  transform:translateY(-6px);
  border-color:rgba(143,209,79,0.4);
  box-shadow:0 24px 48px -20px rgba(0,0,0,0.55), 0 0 32px -8px rgba(143,209,79,0.18);
}
.unit-card::before{
  content:"";
  position:absolute; inset:0; z-index:0; opacity:0; pointer-events:none;
  background:radial-gradient(320px circle at var(--mx,50%) var(--my,50%), rgba(143,209,79,0.055), transparent 65%);
  transition:opacity .3s ease;
}
.unit-card:hover::before{ opacity:1; }
.unit-header, .thumb-wrap, .unit-card > .p-5{
  position:relative; z-index:1;
}
.unit-header{
  display:flex; align-items:center; justify-content:space-between;
  padding:10px 14px; border-bottom:1px solid var(--border);
  background:rgba(255,255,255,0.015);
  font-family:'JetBrains Mono', monospace; font-size:11px;
}
.thumb-wrap{ position:relative; height:190px; overflow:hidden; background:#000; cursor:pointer; }
.thumb-wrap img{ transition:transform .6s cubic-bezier(.16,1,.3,1), opacity .4s ease; }
.thumb-wrap:hover img{ transform:scale(1.06); opacity:1; }
.thumb-fade{ position:absolute; inset:0; background:linear-gradient(to top, var(--surface) 0%, transparent 55%); }
.play-glyph{
  position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
  opacity:0; transition:opacity .3s ease;
}
.thumb-wrap:hover .play-glyph{ opacity:1; }
.play-glyph span{
  width:52px; height:52px; border-radius:50%;
  background:rgba(11,13,16,0.7); border:1px solid rgba(143,209,79,0.5);
  backdrop-filter:blur(4px);
  display:flex; align-items:center; justify-content:center;
}

.tag-flag{
  font-family:'JetBrains Mono', monospace; font-size:10.5px; font-weight:500;
  color:var(--mint); background:rgba(143,209,79,0.07);
  border:1px solid rgba(143,209,79,0.18);
  padding:3px 8px; border-radius:6px;
}

.btn-primary{
  background:linear-gradient(135deg, var(--mint) 0%, #6bc229 100%);
  color:#0b0d10; font-weight:700;
  box-shadow:0 8px 20px -8px rgba(143,209,79,0.5);
  transition:transform .2s ease, box-shadow .2s ease, filter .2s ease;
}
.btn-primary:hover{ transform:translateY(-2px); filter:brightness(1.08); box-shadow:0 12px 26px -8px rgba(143,209,79,0.6); }
.btn-ghost{
  background:var(--surface-2); color:var(--text); border:1px solid var(--border-strong);
  transition:all .2s ease;
}
.btn-ghost:hover{ border-color:var(--mint); color:var(--mint); background:rgba(143,209,79,0.06); }

/* ---------- reveal on scroll ---------- */
.reveal{ opacity:0; transform:translateY(14px); transition:opacity .55s cubic-bezier(.16,1,.3,1), transform .55s cubic-bezier(.16,1,.3,1); }
.reveal.in{ opacity:1; transform:translateY(0); }

/* ---------- modal ---------- */
.modal-window{
  background:var(--surface); border:1px solid var(--border-strong); border-radius:14px;
  box-shadow:0 40px 90px -20px rgba(0,0,0,0.8);
}

@media (prefers-reduced-motion: reduce){
  *{ animation-duration:0.001ms !important; animation-iteration-count:1 !important; transition-duration:0.001ms !important; }
}
</style>
</head>
<body class="min-h-screen flex flex-col selection:bg-lime-400 selection:text-black">

<div id="scrollbar"></div>
<div class="bg-grid"></div>
<div class="bg-glow"></div>
<div class="scanline"></div>

<!-- Nav -->
<nav class="glass-nav sticky top-0 z-40 px-5 sm:px-8 py-3.5">
  <div class="max-w-7xl mx-auto flex justify-between items-center">
    <div class="flex items-center space-x-2.5">
      <span class="status-dot"></span>
      <span class="font-display font-bold text-[15px] sm:text-lg text-white tracking-tight">Stefano Del Moro</span>
      <span class="hidden sm:inline font-mono text-[11px] text-[var(--text-faint)] ml-2" id="clock">--:--:--</span>
    </div>
    <div class="flex items-center space-x-3">
      <span class="hidden md:inline-flex items-center gap-1.5 text-[11px] font-mono font-medium text-[var(--mint)] bg-[rgba(143,209,79,0.08)] border border-[rgba(143,209,79,0.25)] px-3 py-1.5 rounded-full tracking-wide">
        SYSTEM: ONLINE
      </span>
      <a href="#contacto" class="btn-primary text-xs font-bold uppercase tracking-wider px-4 sm:px-5 py-2.5 rounded-lg font-mono">
        contact --init
      </a>
    </div>
  </div>
</nav>

<!-- Hero -->
<section class="relative px-5 sm:px-8 pt-16 pb-14 z-10">
  <div class="max-w-7xl mx-auto grid lg:grid-cols-2 gap-12 items-center">

    <!-- Left: headline -->
    <div class="reveal">
      <span class="inline-flex items-center gap-2 mb-6 px-3.5 py-1.5 text-[11px] font-mono font-semibold tracking-wider text-[var(--mint)] uppercase bg-[rgba(143,209,79,0.07)] border border-[rgba(143,209,79,0.25)] rounded-full">
        <span class="w-1.5 h-1.5 rounded-full bg-[var(--mint)]"></span>
        Full Stack &amp; AI Architect
      </span>
      <h1 class="font-display text-4xl sm:text-5xl xl:text-[3.4rem] font-bold text-white leading-[1.08] tracking-tight uppercase mb-6">
        SOLUCIONES DE SOFTWARE<br/>
        <span class="headline-accent">IA LOCAL &amp; EN LA NUBE · MULTIPLATAFORMA</span>
      </h1>
      <p class="text-[var(--text-dim)] text-base sm:text-lg leading-relaxed mb-7 max-w-xl">
        Apps móviles con IA en la nube y offline, monitores de sistema en consola, visión artificial y bots de automatización — construidos para Linux, Windows y macOS.
      </p>

      <div class="flex flex-wrap gap-2.5 mb-9">
        <span class="platform-chip">macOS</span>
        <span class="platform-chip">Windows</span>
        <span class="platform-chip">Linux</span>
        <span class="platform-chip">Android</span>
      </div>

      <div class="flex flex-wrap gap-3 mb-10">
        <a href="#proyectos" class="btn-primary text-sm font-bold px-6 py-3.5 rounded-xl font-mono uppercase tracking-wide">Ver proyectos</a>
        <a href="#contacto" class="btn-ghost text-sm font-bold px-6 py-3.5 rounded-xl font-mono uppercase tracking-wide">Contactar</a>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div class="stat-box p-4">
          <div class="text-xl font-display font-bold text-[var(--mint)] counter" data-target="7" data-suffix="+ Años">0</div>
          <div class="text-[10.5px] text-[var(--text-faint)] uppercase tracking-wider font-bold font-mono mt-1">Android &amp; Kotlin</div>
        </div>
        <div class="stat-box p-4">
          <div class="text-xl font-display font-bold text-[var(--mint)]">LLM Local</div>
          <div class="text-[10.5px] text-[var(--text-faint)] uppercase tracking-wider font-bold font-mono mt-1">IA Offline / Nube</div>
        </div>
        <div class="stat-box p-4">
          <div class="text-[15px] sm:text-xl font-display font-bold text-[var(--mint)] leading-tight">Linux · Win · macOS</div>
          <div class="text-[10.5px] text-[var(--text-faint)] uppercase tracking-wider font-bold font-mono mt-1">Entorno Dev</div>
        </div>
        <div class="stat-box p-4">
          <div class="text-xl font-display font-bold text-[var(--mint)] counter" data-target="{{ proyectos|length }}">0</div>
          <div class="text-[10.5px] text-[var(--text-faint)] uppercase tracking-wider font-bold font-mono mt-1">Demos en Video</div>
        </div>
      </div>
    </div>

    <!-- Right: terminal -->
    <div class="reveal" style="transition-delay:.1s">
      <div class="term-window">
        <div class="term-bar">
          <span class="term-dot" style="background:#f85149"></span>
          <span class="term-dot" style="background:#ffb454"></span>
          <span class="term-dot" style="background:#8fd14f"></span>
          <span class="font-mono text-[11px] text-[var(--text-faint)] ml-2">stefano@dev — zsh</span>
        </div>
        <div class="term-body font-mono text-[13px] sm:text-sm leading-relaxed" id="termBody"></div>
      </div>
    </div>

  </div>
</section>

<!-- Main -->
<main class="max-w-7xl mx-auto px-5 sm:px-8 pb-6 flex-grow w-full relative z-10" id="proyectos">

  <div class="flex flex-wrap items-center justify-center gap-2 mb-3 reveal">
    <button data-filter="all" class="filter-btn active">
      $ ls --all ({{ proyectos|length }})
    </button>
    {% for cat in categorias %}
    <button data-filter="{{ cat }}" class="filter-btn">
      --{{ cat|lower|replace(' ', '-')|replace('&', 'n') }}
    </button>
    {% endfor %}
  </div>
  <p class="text-center font-mono text-[11px] text-[var(--text-faint)] mb-12 reveal">// haz clic en una miniatura o en "run --demo" para reproducir el video</p>

  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-7" id="projects-grid">
    {% for p in proyectos %}
    <div class="unit-card reveal" data-category="{{ p.categoria }}" style="transition-delay:{{ (loop.index0 % 3) * 0.08 }}s">

      <div class="unit-header">
        <div class="flex items-center gap-2 min-w-0">
          <span class="w-2 h-2 rounded-full {{ p.status_dot }} shrink-0"></span>
          <span class="text-[var(--text-dim)] truncate">{{ p.unit }}</span>
        </div>
        <span class="text-[var(--text-faint)] shrink-0">pid {{ p.pid }}</span>
      </div>

      <div class="thumb-wrap" onclick="openVideoModal('{{ p.media_url }}', '{{ p.unit }}')">
        <img src="{{ p.cover_image }}" alt="{{ p.titulo }}" loading="lazy" class="w-full h-full object-cover opacity-80">
        <div class="thumb-fade"></div>
        <span class="absolute top-3 left-3 text-[10px] uppercase tracking-widest text-[var(--mint)] font-bold font-mono px-2.5 py-1 bg-[rgba(11,13,16,0.75)] border border-[rgba(143,209,79,0.3)] rounded-md backdrop-blur-sm">
          {{ p.categoria }}
        </span>
        <span class="absolute top-3 right-3 text-[9.5px] uppercase tracking-widest font-bold font-mono px-2.5 py-1 bg-[rgba(11,13,16,0.75)] border border-[var(--border-strong)] rounded-md backdrop-blur-sm text-[var(--text-dim)]">
          {{ p.status_label }}
        </span>
        <div class="play-glyph">
          <span>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="#8fd14f"><path d="M8 5v14l11-7z"/></svg>
          </span>
        </div>
      </div>

      <div class="p-5">
        <h3 class="font-display text-lg font-bold text-white mb-0.5 tracking-tight">{{ p.titulo }}</h3>
        <p class="text-[11.5px] font-mono font-semibold text-[var(--mint)] mb-3">{{ p.subtitulo }}</p>
        <p class="text-[var(--text-dim)] text-[13.5px] leading-relaxed mb-5">{{ p.descripcion }}</p>

        <div class="flex flex-wrap gap-1.5 mb-5">
          {% for tech in p.techs %}
          <span class="tag-flag">--{{ tech|lower|replace(' ', '-') }}</span>
          {% endfor %}
        </div>

        <div class="flex gap-2">
          {% if p.link_demo %}
          <a href="{{ p.link_demo }}" target="_blank" rel="noopener" class="btn-primary flex-1 text-center py-2.5 px-3 rounded-lg text-[11px] font-mono font-bold uppercase tracking-wide">
            $ ./deploy
          </a>
          {% endif %}
          <button onclick="openVideoModal('{{ p.media_url }}', '{{ p.unit }}')" class="btn-ghost {{ 'flex-1' if p.link_demo else 'w-full' }} text-center py-2.5 px-3 rounded-lg text-[11px] font-mono font-bold uppercase tracking-wide">
            $ ./run --demo
          </button>
        </div>
      </div>
    </div>
    {% endfor %}
  </div>
</main>

<!-- Contact -->
<section id="contacto" class="relative border-t border-[var(--border)] py-20 px-5 sm:px-8 mt-20 z-10">
  <div class="max-w-3xl mx-auto text-center reveal">
    <p class="font-mono text-xs text-[var(--mint)] mb-4">stefano@dev:~$ contact --init</p>
    <h2 class="font-display text-3xl sm:text-4xl font-bold text-white mb-4 tracking-tight">¿Construimos algo juntos?</h2>
    <p class="text-[var(--text-dim)] mb-3 max-w-xl mx-auto">
      Disponible para roles como Full Stack Engineer, Android Developer o desarrollo de soluciones con Inteligencia Artificial.
    </p>
    <p class="font-mono text-[11px] text-[var(--text-faint)] mb-10 uppercase tracking-wider">status: open_to_work — true</p>
    <div class="flex flex-wrap justify-center gap-3">
      <a href="https://github.com/stef7773" target="_blank" rel="noopener" class="btn-primary font-mono text-sm px-6 py-3.5 rounded-xl flex items-center gap-2">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12 .5C5.73.5.98 5.24.98 11.52c0 5.02 3.26 9.28 7.78 10.78.57.1.78-.25.78-.55 0-.27-.01-1.16-.02-2.1-3.17.69-3.83-1.35-3.83-1.35-.52-1.31-1.26-1.66-1.26-1.66-1.03-.7.08-.69.08-.69 1.14.08 1.74 1.17 1.74 1.17 1.01 1.74 2.65 1.24 3.3.95.1-.73.4-1.24.72-1.53-2.53-.29-5.2-1.27-5.2-5.63 0-1.24.44-2.26 1.17-3.06-.12-.29-.51-1.45.11-3.02 0 0 .96-.31 3.14 1.17a10.9 10.9 0 0 1 5.72 0c2.18-1.48 3.14-1.17 3.14-1.17.62 1.57.23 2.73.11 3.02.73.8 1.17 1.82 1.17 3.06 0 4.37-2.68 5.34-5.22 5.62.41.36.77 1.06.77 2.14 0 1.55-.01 2.79-.01 3.17 0 .3.2.66.79.55A11.03 11.03 0 0 0 23 11.52C23 5.24 18.27.5 12 .5Z"/></svg>
        github.com/stef7773
      </a>
    </div>
  </div>
</section>

<footer class="text-center py-7 text-[var(--text-faint)] border-t border-[var(--border)] text-[11px] font-mono relative z-10">
  <span id="footerClock">stefano.service — active</span> · build for Linux · Windows · macOS · Android
</footer>

<!-- Video Modal -->
<div id="videoModal" class="fixed inset-0 bg-black/90 backdrop-blur-md hidden z-50 items-center justify-center p-4">
  <div class="modal-window max-w-5xl w-full overflow-hidden">
    <div class="term-bar">
      <span class="term-dot" style="background:#f85149"></span>
      <span class="term-dot" style="background:#ffb454"></span>
      <span class="term-dot" style="background:#8fd14f"></span>
      <span id="modalTitle" class="font-mono text-[12px] text-[var(--text-dim)] ml-2 truncate"></span>
      <button onclick="closeVideoModal()" class="ml-auto text-[var(--text-faint)] hover:text-white text-xl leading-none px-2">&times;</button>
    </div>
    <div id="modalBody" class="w-full flex justify-center items-center bg-black min-h-[320px]"></div>
  </div>
</div>

<script>
/* ---------- boot terminal ---------- */
const bootLines = [
  { t: 'stefano@dev:~$ whoami', cls:'text-[var(--text)]' },
  { t: 'Full Stack &amp; AI Architect', cls:'text-[var(--mint)] font-bold' },
  { t: '', cls:'' },
  { t: 'stefano@dev:~$ ./status --stack', cls:'text-[var(--text)]' },
  { t: 'lang     kotlin · python · sql', cls:'text-[var(--text-dim)]' },
  { t: 'mobile   android (kotlin / jetpack compose)', cls:'text-[var(--text-dim)]' },
  { t: 'ai       local llm (ollama) + cloud (gemini)', cls:'text-[var(--text-dim)]' },
  { t: 'targets  linux · windows · macos', cls:'text-[var(--text-dim)]' },
  { t: '', cls:'' },
  { t: 'stefano@dev:~$ ./status --availability', cls:'text-[var(--text)]' },
  { t: '[ OK ] open_to_work.......... true', cls:'text-[var(--mint)]' },
];

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const termBody = document.getElementById('termBody');

function renderStatic(){
  termBody.innerHTML = bootLines.map(l => `<div class="term-line shown ${l.cls}">${l.t || '&nbsp;'}</div>`).join('');
}

async function typeBoot(){
  if (reduceMotion){ renderStatic(); return; }
  for (const line of bootLines){
    const div = document.createElement('div');
    div.className = `term-line shown ${line.cls}`;
    termBody.appendChild(div);
    if (!line.t){ div.innerHTML = '&nbsp;'; await sleep(120); continue; }
    for (let i = 0; i <= line.t.length; i++){
      div.innerHTML = line.t.slice(0, i) + '<span class="caret"></span>';
      await sleep(line.t.startsWith('stefano@dev') ? 22 : 8);
    }
    div.innerHTML = line.t;
    await sleep(90);
  }
}
function sleep(ms){ return new Promise(r => setTimeout(r, ms)); }
typeBoot();

/* ---------- live clock ---------- */
function tickClock(){
  const now = new Date();
  const hh = String(now.getHours()).padStart(2,'0');
  const mm = String(now.getMinutes()).padStart(2,'0');
  const ss = String(now.getSeconds()).padStart(2,'0');
  const str = `${hh}:${mm}:${ss}`;
  const clock = document.getElementById('clock');
  const fclock = document.getElementById('footerClock');
  if (clock) clock.textContent = str;
  if (fclock) fclock.textContent = `stefano.service — active — ${str}`;
}
tickClock();
setInterval(tickClock, 1000);

/* ---------- scroll progress ---------- */
function onScroll(){
  const h = document.documentElement;
  const pct = (h.scrollTop) / (h.scrollHeight - h.clientHeight) * 100;
  document.getElementById('scrollbar').style.width = pct + '%';
}
document.addEventListener('scroll', onScroll, { passive:true });

/* ---------- reveal on scroll ---------- */
const revealEls = document.querySelectorAll('.reveal');
const io = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
}, { threshold: 0.08, rootMargin: '0px 0px -20px 0px' });
revealEls.forEach(el => io.observe(el));

/* ---------- animated counters ---------- */
const counters = document.querySelectorAll('.counter');
const counterIO = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (!e.isIntersecting) return;
    counterIO.unobserve(e.target);
    const el = e.target;
    const target = parseInt(el.dataset.target, 10);
    const suffix = el.dataset.suffix || '';
    if (reduceMotion){ el.textContent = target + suffix; return; }
    let cur = 0;
    const step = Math.max(1, Math.round(target / 24));
    const timer = setInterval(() => {
      cur += step;
      if (cur >= target){ cur = target; clearInterval(timer); }
      el.textContent = cur + suffix;
    }, 40);
  });
}, { threshold: 0.5 });
counters.forEach(el => counterIO.observe(el));

/* ---------- filters ---------- */
const filterBtns = document.querySelectorAll('.filter-btn');
const cards = document.querySelectorAll('.unit-card');
filterBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const cat = btn.dataset.filter;
    cards.forEach(card => {
      const match = cat === 'all' || card.getAttribute('data-category') === cat;
      card.style.display = match ? 'block' : 'none';
    });
  });
});

/* ---------- card spotlight (position only, no tilt — keeps scroll smooth) ---------- */
cards.forEach(card => {
  card.addEventListener('mousemove', (e) => {
    if (reduceMotion) return;
    const r = card.getBoundingClientRect();
    card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
    card.style.setProperty('--my', (e.clientY - r.top) + 'px');
  });
});

/* ---------- video modal ---------- */
function openVideoModal(url, title){
  const modal = document.getElementById('videoModal');
  const modalBody = document.getElementById('modalBody');
  document.getElementById('modalTitle').innerText = `$ ./run ${title} --demo`;
  modalBody.innerHTML = `<video controls autoplay loop playsinline class="max-h-[75vh] w-full object-contain"><source src="${url}" type="video/mp4">Tu navegador no soporta video.</video>`;
  modal.classList.remove('hidden');
  modal.classList.add('flex');
  document.body.style.overflow = 'hidden';
}
function closeVideoModal(){
  const modal = document.getElementById('videoModal');
  document.getElementById('modalBody').innerHTML = '';
  modal.classList.add('hidden');
  modal.classList.remove('flex');
  document.body.style.overflow = '';
}
document.getElementById('videoModal').addEventListener('click', (e) => {
  if (e.target.id === 'videoModal') closeVideoModal();
});
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeVideoModal(); });
</script>
</body>
</html>
"""

# Renderizar
template = Template(html_template)
output_html = template.render(proyectos=proyectos, categorias=categorias)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(output_html)

print("Listo: index.html generado con el nuevo diseño premium.")
