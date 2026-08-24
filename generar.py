#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Portfolio Generator - Professional Edition
Stefano Del Moro | Full Stack & AI Engineer
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from html import escape
from functools import lru_cache
import logging

# ============================================================
# CONFIGURATION
# ============================================================

@dataclass
class Config:
    """Configuration settings for the portfolio generator."""
    
    input_file: str = "proyectos.json"
    output_file: str = "index.html"
    template_dir: str = "templates"
    static_dir: str = "static"
    debug: bool = False
    minify_html: bool = True
    enable_animations: bool = True
    theme: str = "cyberpunk"  # cyberpunk | minimalist | retro
    locale: str = "es"
    
    # Grid configuration
    grid_cols: int = 3
    cards_per_row: Tuple[int, ...] = (1, 2, 3)  # mobile, tablet, desktop
    
    # Performance
    lazy_load_videos: bool = True
    preconnect_domains: Tuple[str, ...] = (
        "https://cdn.tailwindcss.com",
        "https://fonts.googleapis.com",
    )


# ============================================================
# DATA MODELS
# ============================================================

@dataclass
class Project:
    """Project data model with validation."""
    
    titulo: str
    descripcion: str
    categoria: str
    tags: List[str]
    video_url: str
    link: Optional[str] = None
    destacado: bool = False
    fecha: Optional[str] = None
    cliente: Optional[str] = None
    tecnologias: List[str] = field(default_factory=list)
    imagenes: List[str] = field(default_factory=list)
    github_url: Optional[str] = None
    stats: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate required fields."""
        if not self.titulo or not self.descripcion:
            raise ValueError("Project must have title and description")
        self.titulo = escape(self.titulo)
        self.descripcion = escape(self.descripcion)
        self.tags = [escape(tag) for tag in self.tags]
        self.tecnologias = [escape(tech) for tech in self.tecnologias]
    
    @property
    def slug(self) -> str:
        """Generate URL-friendly slug from title."""
        return self.titulo.lower().replace(" ", "-").replace("/", "-")
    
    @property
    def has_video(self) -> bool:
        """Check if project has a video URL."""
        return bool(self.video_url and self.video_url.strip())
    
    @property
    def has_link(self) -> bool:
        """Check if project has an external link."""
        return bool(self.link and self.link.strip())


# ============================================================
# TEMPLATE ENGINE
# ============================================================

class TemplateEngine:
    """Modern template engine with caching and inheritance."""
    
    def __init__(self, config: Config):
        self.config = config
        self.cache = {}
        self.partials = {}
    
    def render(self, template: str, context: Dict[str, Any]) -> str:
        """Render a template with the given context."""
        # Simple but powerful template rendering
        rendered = template
        
        # Replace variables
        for key, value in context.items():
            if isinstance(value, (str, int, float)):
                rendered = rendered.replace(f"{{{{{key}}}}}", str(value))
        
        # Process loops (simple iteration)
        if "{{#each" in rendered:
            rendered = self._process_loops(rendered, context)
        
        # Process conditionals
        if "{{#if" in rendered:
            rendered = self._process_conditionals(rendered, context)
        
        return rendered
    
    def _process_loops(self, template: str, context: Dict[str, Any]) -> str:
        """Process {{#each}} blocks."""
        import re
        pattern = r"{{#each (\w+)}}(.*?){{/each}}"
        
        def replacer(match):
            key = match.group(1)
            content = match.group(2)
            items = context.get(key, [])
            if not isinstance(items, list):
                return ""
            return "".join(
                self._render_item(content, {key: item})
                for item in items
            )
        
        return re.sub(pattern, replacer, template, flags=re.DOTALL)
    
    def _render_item(self, template: str, context: Dict[str, Any]) -> str:
        """Render a single item in a loop."""
        result = template
        for key, value in context.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    result = result.replace(f"{{{{{key}.{subkey}}}}}", str(subvalue))
            else:
                result = result.replace(f"{{{{{key}}}}}", str(value))
        return result
    
    def _process_conditionals(self, template: str, context: Dict[str, Any]) -> str:
        """Process {{#if}} blocks."""
        import re
        pattern = r"{{#if (\w+)}}(.*?){{/if}}"
        
        def replacer(match):
            key = match.group(1)
            content = match.group(2)
            if context.get(key):
                return content
            return ""
        
        return re.sub(pattern, replacer, template, flags=re.DOTALL)
    
    def get_partial(self, name: str) -> str:
        """Get a partial template by name."""
        if name not in self.partials:
            partial_path = Path(self.config.template_dir) / f"_{name}.html"
            if partial_path.exists():
                self.partials[name] = partial_path.read_text(encoding="utf-8")
            else:
                self.partials[name] = ""
        return self.partials[name]


# ============================================================
# PORTFOLIO GENERATOR
# ============================================================

class PortfolioGenerator:
    """Main generator class with modular design."""
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.template_engine = TemplateEngine(self.config)
        self._setup_logging()
        self._load_templates()
    
    def _setup_logging(self):
        """Configure logging."""
        level = logging.DEBUG if self.config.debug else logging.INFO
        logging.basicConfig(
            level=level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler(sys.stdout)]
        )
        self.logger = logging.getLogger(__name__)
    
    def _load_templates(self):
        """Load all templates from disk."""
        self.templates = {}
        template_path = Path(self.config.template_dir)
        if template_path.exists():
            for template_file in template_path.glob("*.html"):
                name = template_file.stem
                self.templates[name] = template_file.read_text(encoding="utf-8")
        else:
            # Use built-in templates if directory doesn't exist
            self.templates["base"] = self._get_base_template()
            self.templates["project_card"] = self._get_project_card_template()
            self.templates["featured_project"] = self._get_featured_template()
            self.templates["stats_section"] = self._get_stats_template()
    
    def _get_base_template(self) -> str:
        """Return the base HTML template."""
        return """<!DOCTYPE html>
<html lang="{{lang}}" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
    {{#each preconnect}}
    <link rel="preconnect" href="{{this}}">
    {{/each}}
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        neon: {
                            blue: '{{primary_color}}',
                            cyan: '{{secondary_color}}',
                            bg: '{{bg_color}}',
                            card: '{{card_color}}',
                            border: '{{primary_color}}'
                        }
                    },
                    animation: {
                        'glow': 'glow 2s ease-in-out infinite alternate',
                        'float': 'float 3s ease-in-out infinite',
                        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                    },
                    keyframes: {
                        glow: {
                            '0%': { 'box-shadow': '0 0 20px rgba({{primary_rgb}}, 0.1)' },
                            '100%': { 'box-shadow': '0 0 40px rgba({{primary_rgb}}, 0.3)' },
                        },
                        float: {
                            '0%, 100%': { transform: 'translateY(0px)' },
                            '50%': { transform: 'translateY(-10px)' },
                        }
                    }
                }
            }
        }
    </script>
    <style>
        body {
            background-color: {{bg_color}};
            background-image: 
                linear-gradient(to right, rgba({{primary_rgb}}, 0.04) 1px, transparent 1px),
                linear-gradient(to bottom, rgba({{primary_rgb}}, 0.04) 1px, transparent 1px);
            background-size: 32px 32px;
        }
        .glow-text {
            text-shadow: 0 0 30px rgba({{primary_rgb}}, 0.3);
        }
        .glow-card {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 0 20px rgba({{primary_rgb}}, 0.05);
        }
        .glow-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 0 40px rgba({{primary_rgb}}, 0.15);
        }
        .gradient-border {
            position: relative;
            border: 1px solid transparent;
            background-clip: padding-box;
        }
        .gradient-border::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            border-radius: inherit;
            background: linear-gradient(135deg, {{primary_color}}, transparent, {{secondary_color}});
            z-index: -1;
            opacity: 0.3;
            transition: opacity 0.3s;
        }
        .gradient-border:hover::before {
            opacity: 0.8;
        }
        @keyframes shimmer {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }
        .shimmer {
            background: linear-gradient(90deg, transparent, rgba({{primary_rgb}}, 0.1), transparent);
            background-size: 200% 100%;
            animation: shimmer 3s ease-in-out infinite;
        }
        .glass-effect {
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }
        @media (max-width: 768px) {
            .mobile-stack {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    {{content}}
    {{#if analytics}}
    <script>{{analytics}}</script>
    {{/if}}
</body>
</html>"""
    
    def _get_project_card_template(self) -> str:
        """Return the project card template."""
        return """<div class="bg-neon-card border border-cyan-900/80 hover:border-neon-blue/60 rounded-2xl p-6 transition-all duration-300 flex flex-col justify-between glow-card group">
    <div>
        <div class="mb-4 flex justify-between items-start">
            <span class="inline-block px-2.5 py-1 bg-neon-blue/10 border border-neon-blue/30 text-neon-blue text-[10px] font-mono font-bold tracking-wider uppercase rounded-md">
                {{categoria}}
            </span>
            {{#if destacado}}
            <span class="text-[10px] font-mono text-yellow-400 bg-yellow-400/10 px-2 py-0.5 rounded border border-yellow-400/30">
                ★ Destacado
            </span>
            {{/if}}
        </div>
        <h4 class="text-lg font-bold text-white mb-3 leading-snug group-hover:text-neon-blue transition-colors">
            {{titulo}}
        </h4>
        <p class="text-gray-400 text-xs leading-relaxed mb-6">{{descripcion}}</p>
        {{#if has_video}}
        <div class="aspect-video w-full bg-gray-950 rounded-xl overflow-hidden border border-cyan-900/60 mb-6 relative">
            <video class="w-full h-full object-cover" {{#if lazy_load}}loading="lazy"{{/if}} controls loop muted playsinline preload="metadata">
                <source src="{{video_url}}" type="video/mp4">
            </video>
            <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent pointer-events-none"></div>
        </div>
        {{/if}}
        {{#if stats}}
        <div class="grid grid-cols-2 gap-2 mb-4">
            {{#each stats}}
            <div class="bg-gray-900/50 rounded-lg p-2 text-center">
                <span class="text-neon-blue font-bold text-sm">{{value}}</span>
                <span class="text-gray-500 text-[8px] uppercase block">{{label}}</span>
            </div>
            {{/each}}
        </div>
        {{/if}}
    </div>
    <div>
        <div class="flex flex-wrap gap-1.5">
            {{#each tags}}
            <span class="text-[10px] font-mono bg-gray-950 text-gray-300 px-2 py-0.5 rounded border border-gray-800">{{this}}</span>
            {{/each}}
        </div>
        {{#if link}}
        <a href="{{link}}" target="_blank" class="mt-4 inline-flex items-center gap-2 text-neon-blue hover:text-white text-xs font-mono transition-colors">
            Ver proyecto →
        </a>
        {{/if}}
    </div>
</div>"""
    
    def _get_featured_template(self) -> str:
        """Return the featured project template."""
        return """<div class="bg-neon-card border border-neon-blue/60 rounded-2xl p-6 md:p-8 glow-card transition-all duration-300 gradient-border">
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
        <div class="lg:col-span-5 flex flex-col justify-between">
            <div>
                <div class="flex items-center gap-3 mb-4">
                    <span class="inline-block px-3 py-1 bg-neon-blue/10 border border-neon-blue/40 text-neon-blue font-mono font-bold text-xs uppercase tracking-wider rounded-md">
                        {{categoria}}
                    </span>
                    <span class="text-[10px] font-mono text-yellow-400 bg-yellow-400/10 px-2 py-0.5 rounded border border-yellow-400/30">
                        ⚡ Proyecto Destacado
                    </span>
                </div>
                <h3 class="text-2xl md:text-4xl font-extrabold text-white mb-4 glow-text leading-tight">
                    {{titulo}}
                </h3>
                <p class="text-gray-300 text-sm md:text-base leading-relaxed mb-6">
                    {{descripcion}}
                </p>
                <div class="flex flex-wrap gap-2 mb-6">
                    {{#each tags}}
                    <span class="text-xs font-mono bg-gray-950 text-neon-blue px-3 py-1 rounded-md border border-cyan-900">{{this}}</span>
                    {{/each}}
                </div>
                <div class="flex flex-wrap gap-3">
                    {{#if link}}
                    <a href="{{link}}" target="_blank" class="inline-flex items-center gap-2 px-6 py-3 bg-neon-blue text-black font-bold text-sm rounded-xl hover:bg-cyan-300 transition shadow-[0_0_30px_rgba({{primary_rgb}},0.3)]">
                        ▶ Ver en Google Play
                    </a>
                    {{/if}}
                    {{#if github_url}}
                    <a href="{{github_url}}" target="_blank" class="inline-flex items-center gap-2 px-6 py-3 bg-gray-800 text-white font-bold text-sm rounded-xl hover:bg-gray-700 transition border border-gray-700">
                        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.15 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.62.24 2.85.12 3.15.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
                        Código
                    </a>
                    {{/if}}
                </div>
            </div>
        </div>
        <div class="lg:col-span-7">
            <div class="aspect-video w-full bg-gray-950 rounded-xl overflow-hidden border border-cyan-800 shadow-inner relative">
                <video class="w-full h-full object-cover" controls autoplay loop muted playsinline preload="auto">
                    <source src="{{video_url}}" type="video/mp4">
                </video>
                <div class="absolute inset-0 bg-gradient-to-tr from-neon-blue/5 to-transparent pointer-events-none"></div>
            </div>
        </div>
    </div>
</div>"""
    
    def _get_stats_template(self) -> str:
        """Return the stats section template."""
        return """<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
    {{#each stats}}
    <div class="p-4 bg-neon-card/80 border border-cyan-900/60 rounded-xl glow-card text-center hover:border-neon-blue/60 transition-all duration-300">
        <span class="text-2xl font-black text-neon-blue block">{{value}}</span>
        <span class="text-[10px] font-mono text-gray-400 uppercase">{{label}}</span>
    </div>
    {{/each}}
</div>"""
    
    def generate(self) -> str:
        """Generate the complete portfolio HTML."""
        try:
            # Load data
            projects = self._load_projects()
            if not projects:
                raise ValueError("No projects loaded")
            
            # Prepare data
            featured = self._get_featured_projects(projects)
            others = [p for p in projects if p not in featured]
            
            # Calculate stats
            stats = self._calculate_stats(projects)
            
            # Generate HTML
            html = self._build_html(projects, featured, others, stats)
            
            # Minify if enabled
            if self.config.minify_html:
                html = self._minify_html(html)
            
            return html
            
        except Exception as e:
            self.logger.error(f"Generation failed: {e}", exc_info=self.config.debug)
            raise
    
    def _load_projects(self) -> List[Project]:
        """Load and validate projects from JSON file."""
        try:
            file_path = Path(self.config.input_file)
            if not file_path.exists():
                self.logger.warning(f"Input file not found: {file_path}")
                return self._get_demo_projects()
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                raise ValueError("JSON data must be a list")
            
            projects = []
            for item in data:
                try:
                    project = Project(**item)
                    projects.append(project)
                except Exception as e:
                    self.logger.warning(f"Skipping invalid project: {e}")
            
            return projects
            
        except Exception as e:
            self.logger.error(f"Error loading projects: {e}")
            return self._get_demo_projects()
    
    def _get_demo_projects(self) -> List[Project]:
        """Return demo projects for testing."""
        return [
            Project(
                titulo="AI Chat Assistant Pro",
                descripcion="Asistente conversacional con LLM local y reconocimiento de voz para Android nativo",
                categoria="Inteligencia Artificial",
                tags=["Android", "LLM", "Kotlin", "TFLite"],
                video_url="https://example.com/demo.mp4",
                link="https://play.google.com",
                destacado=True,
                stats={"descargas": {"value": "50K+", "label": "Descargas"}}
            ),
            Project(
                titulo="Linux System Monitor",
                descripcion="Monitor de recursos con análisis predictivo para Linux Mint",
                categoria="Herramientas",
                tags=["Python", "Linux", "GTK", "Machine Learning"],
                video_url="https://example.com/demo2.mp4",
                link="https://github.com",
            )
        ]
    
    def _get_featured_projects(self, projects: List[Project]) -> List[Project]:
        """Get featured projects (up to 2)."""
        featured = [p for p in projects if p.destacado]
        if not featured and projects:
            featured = [projects[0]]
        return featured[:2]
    
    def _calculate_stats(self, projects: List[Project]) -> List[Dict[str, str]]:
        """Calculate portfolio statistics."""
        stats = [
            {"label": "Proyectos", "value": str(len(projects))},
            {"label": "Tecnologías", "value": str(len(set().union(*[set(p.tecnologias) for p in projects if p.tecnologias])))},
            {"label": "Años de Experiencia", "value": "3+"},
            {"label": "Apps en Producción", "value": str(len([p for p in projects if p.link]))},
        ]
        return stats
    
    def _build_html(self, projects: List[Project], featured: List[Project], 
                   others: List[Project], stats: List[Dict[str, str]]) -> str:
        """Build the complete HTML content."""
        
        # Colors based on theme
        colors = {
            "cyberpunk": {
                "primary": "#00f0ff",
                "secondary": "#00d8f6",
                "bg": "#030712",
                "card": "#091322",
                "rgb": "0, 240, 255"
            },
            "minimalist": {
                "primary": "#3b82f6",
                "secondary": "#6366f1",
                "bg": "#0f172a",
                "card": "#1e293b",
                "rgb": "59, 130, 246"
            },
            "retro": {
                "primary": "#ff6b6b",
                "secondary": "#feca57",
                "bg": "#1a1a2e",
                "card": "#16213e",
                "rgb": "255, 107, 107"
            }
        }
        theme_colors = colors.get(self.config.theme, colors["cyberpunk"])
        
        context = {
            "lang": self.config.locale,
            "title": "Stefano Del Moro | Full Stack & AI Engineer",
            "primary_color": theme_colors["primary"],
            "secondary_color": theme_colors["secondary"],
            "bg_color": theme_colors["bg"],
            "card_color": theme_colors["card"],
            "primary_rgb": theme_colors["rgb"],
            "preconnect": self.config.preconnect_domains,
            "lazy_load": self.config.lazy_load_videos,
            "stats": stats,
            "year": datetime.now().year,
            "theme": self.config.theme,
        }
        
        # Generate sections
        hero_section = self._generate_hero(projects)
        featured_sections = "".join(
            self._generate_featured_section(p) for p in featured
        )
        projects_grid = self._generate_projects_grid(others) if others else ""
        
        content = f"""
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
            
            <!-- HEADER -->
            <header class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-12 border-b border-cyan-900/50 pb-6 gap-4">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 bg-neon-blue rounded-full flex items-center justify-center shadow-[0_0_30px_rgba(0,240,255,0.2)]">
                        <span class="text-black font-bold text-sm">SD</span>
                    </div>
                    <div>
                        <h1 class="text-xl font-bold text-white tracking-wide">Stefano Del Moro</h1>
                        <p class="text-xs text-neon-blue font-mono">Full Stack & AI Engineer • Android Architect</p>
                    </div>
                </div>
                <div class="flex gap-3 w-full sm:w-auto">
                    <a href="#proyectos" class="px-4 py-2 bg-gray-800/50 border border-gray-700 text-gray-300 text-xs font-mono font-bold rounded-lg hover:bg-gray-700 transition text-center flex-1 sm:flex-none">
                        PROYECTOS
                    </a>
                    <a href="#contacto" class="px-4 py-2 bg-neon-blue/10 border border-neon-blue/50 text-neon-blue text-xs font-mono font-bold rounded-lg hover:bg-neon-blue hover:text-black transition duration-300 text-center flex-1 sm:flex-none">
                        CONTACTAR
                    </a>
                </div>
            </header>
            
            <!-- HERO -->
            {hero_section}
            
            <!-- FEATURED PROJECTS -->
            {featured_sections}
            
            <!-- PROJECTS GRID -->
            <section id="proyectos" class="mt-16">
                <h2 class="text-2xl font-bold text-white mb-8 flex items-center gap-3">
                    <span class="w-1 h-8 bg-neon-blue rounded-full"></span>
                    Proyectos
                    <span class="text-sm font-normal text-gray-400 ml-2">({len(others)})</span>
                </h2>
                {projects_grid}
            </section>
            
            <!-- FOOTER -->
            <footer id="contacto" class="mt-20 pt-8 border-t border-cyan-900/50">
                <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div>
                        <h4 class="text-neon-blue font-mono text-sm font-bold mb-3">Stefano Del Moro</h4>
                        <p class="text-gray-400 text-sm">Full Stack & AI Engineer especializado en Android nativo y soluciones de IA local.</p>
                    </div>
                    <div>
                        <h4 class="text-neon-blue font-mono text-sm font-bold mb-3">Contacto</h4>
                        <p class="text-gray-400 text-sm">📧 stefano@example.com</p>
                        <p class="text-gray-400 text-sm">🐙 github.com/stefanodemoro</p>
                    </div>
                    <div>
                        <h4 class="text-neon-blue font-mono text-sm font-bold mb-3">Especialidades</h4>
                        <div class="flex flex-wrap gap-2">
                            <span class="text-[10px] font-mono bg-gray-950 text-gray-300 px-2 py-1 rounded border border-gray-800">Android</span>
                            <span class="text-[10px] font-mono bg-gray-950 text-gray-300 px-2 py-1 rounded border border-gray-800">AI/ML</span>
                            <span class="text-[10px] font-mono bg-gray-950 text-gray-300 px-2 py-1 rounded border border-gray-800">Linux</span>
                            <span class="text-[10px] font-mono bg-gray-950 text-gray-300 px-2 py-1 rounded border border-gray-800">Kotlin</span>
                        </div>
                    </div>
                </div>
                <p class="mt-8 text-center text-xs font-mono text-gray-500">
                    © {datetime.now().year} Stefano Del Moro • Software & Mobile Engineering Portfolio
                </p>
            </footer>
            
        </div>
        """
        
        # Combine with base template
        base_template = self.templates.get("base", self._get_base_template())
        return self.template_engine.render(base_template, {**context, "content": content})
    
    def _generate_hero(self, projects: List[Project]) -> str:
        """Generate hero section with stats."""
        stats = self._calculate_stats(projects)
        stats_html = self.template_engine.render(
            self._get_stats_template(),
            {"stats": stats}
        )
        
        return f"""
        <div class="text-center max-w-4xl mx-auto mb-16">
            {stats_html}
            
            <h2 class="text-3xl sm:text-4xl md:text-6xl font-black text-white leading-tight mb-6 glow-text">
                Soluciones de Alto Impacto con <br/>
                <span class="text-neon-blue">Inteligencia Artificial & Android NATIVO</span>
            </h2>
            <p class="text-gray-400 text-sm md:text-base leading-relaxed max-w-2xl mx-auto">
                Especializado en aplicaciones Android con IA local, herramientas de alto rendimiento para Linux Mint y automatizaciones avanzadas.
            </p>
        </div>
        """
    
    def _generate_featured_section(self, project: Project) -> str:
        """Generate a featured project section."""
        context = {
            "titulo": project.titulo,
            "descripcion": project.descripcion,
            "categoria": project.categoria,
            "tags": project.tags,
            "video_url": project.video_url,
            "link": project.link,
            "github_url": project.github_url,
            "primary_rgb": "0, 240, 255",  # Should come from config
            "stats": [{"value": v, "label": k} for k, v in project.stats.items()] if project.stats else []
        }
        
        template = self.templates.get("featured_project", self._get_featured_template())
        return self.template_engine.render(template, context)
    
    def _generate_projects_grid(self, projects: List[Project]) -> str:
        """Generate the projects grid."""
        cards = []
        for project in projects:
            context = {
                "titulo": project.titulo,
                "descripcion": project.descripcion,
                "categoria": project.categoria,
                "tags": project.tags,
                "video_url": project.video_url,
                "link": project.link,
                "destacado": project.destacado,
                "has_video": project.has_video,
                "lazy_load": self.config.lazy_load_videos,
                "stats": [{"value": v, "label": k} for k, v in project.stats.items()] if project.stats else []
            }
            template = self.templates.get("project_card", self._get_project_card_template())
            cards.append(self.template_engine.render(template, context))
        
        return f"""
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-{self.config.grid_cols} gap-6">
            {''.join(cards)}
        </div>
        """
    
    def _minify_html(self, html: str) -> str:
        """Minify HTML content."""
        import re
        html = re.sub(r'\s+', ' ', html)
        html = re.sub(r'>\s+<', '><', html)
        html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
        return html.strip()
    
    def save(self, html_content: str) -> None:
        """Save the generated HTML to file."""
        try:
            output_path = Path(self.config.output_file)
            output_path.write_text(html_content, encoding="utf-8")
            self.logger.info(f"✅ Portfolio saved to {output_path}")
            
            # Also save a minified version
            if self.config.minify_html:
                min_path = output_path.with_suffix(".min.html")
                min_path.write_text(html_content, encoding="utf-8")
                self.logger.info(f"✅ Minified version saved to {min_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to save HTML: {e}")
            raise


# ============================================================
# CLI ENTRY POINT
# ============================================================

def main():
    """Command-line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate a professional portfolio website from JSON data."
    )
    parser.add_argument(
        "-i", "--input",
        default="proyectos.json",
        help="Input JSON file path (default: proyectos.json)"
    )
    parser.add_argument(
        "-o", "--output",
        default="index.html",
        help="Output HTML file path (default: index.html)"
    )
    parser.add_argument(
        "-t", "--theme",
        choices=["cyberpunk", "minimalist", "retro"],
        default="cyberpunk",
        help="Theme style (default: cyberpunk)"
    )
    parser.add_argument(
        "--no-minify",
        action="store_true",
        help="Disable HTML minification"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    parser.add_argument(
        "--serve",
        action="store_true",
        help="Serve the generated page with a simple HTTP server"
    )
    
    args = parser.parse_args()
    
    # Create config
    config = Config(
        input_file=args.input,
        output_file=args.output,
        theme=args.theme,
        minify_html=not args.no_minify,
        debug=args.debug
    )
    
    # Generate portfolio
    generator = PortfolioGenerator(config)
    html = generator.generate()
    generator.save(html)
    
    # Serve if requested
    if args.serve:
        import http.server
        import socketserver
        import webbrowser
        
        port = 8000
        os.chdir(os.path.dirname(args.output) or ".")
        
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"🌐 Serving at http://localhost:{port}")
            webbrowser.open(f"http://localhost:{port}/{os.path.basename(args.output)}")
            httpd.serve_forever()


if __name__ == "__main__":
    main()
