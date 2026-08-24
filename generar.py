#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║  PORTFOLIO GENERATOR PRO - Enterprise Edition              ║
║  Stefano Del Moro | Full Stack & AI Engineer               ║
║  Architecture: Modular | Scalable | Production-Ready       ║
╚══════════════════════════════════════════════════════════════╝
"""

import json
import os
import sys
import re
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field, asdict
from datetime import datetime
from html import escape
from functools import lru_cache, wraps
from enum import Enum
import logging
from concurrent.futures import ThreadPoolExecutor
import base64

# ============================================================
# LOGGING CONFIGURATION
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format='\033[36m%(asctime)s\033[0m | \033[32m%(levelname)s\033[0m | %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# ============================================================
# ENUMS & CONSTANTS
# ============================================================

class Theme(Enum):
    """Available themes for the portfolio."""
    CYBERPUNK = "cyberpunk"
    MINIMALIST = "minimalist"
    DARK_MATTER = "dark_matter"
    NEO_BRUTAL = "neo_brutal"
    AURORA = "aurora"
    MATRIX = "matrix"

class AnimationStyle(Enum):
    """Animation presets."""
    SMOOTH = "smooth"
    BOUNCE = "bounce"
    GLITCH = "glitch"
    NEO = "neo"
    SUBTLE = "subtle"

@dataclass
class ColorPalette:
    """Theme color palette."""
    primary: str
    secondary: str
    accent: str
    background: str
    card: str
    text: str
    border: str
    gradient_start: str
    gradient_end: str
    rgb_primary: str
    
    @classmethod
    def cyberpunk(cls) -> 'ColorPalette':
        return cls(
            primary="#00f0ff",
            secondary="#00d8f6",
            accent="#ff00ff",
            background="#030712",
            card="#08101e",
            text="#e2e8f0",
            border="#0e2338",
            gradient_start="#00f0ff",
            gradient_end="#ff00ff",
            rgb_primary="0, 240, 255"
        )
    
    @classmethod
    def dark_matter(cls) -> 'ColorPalette':
        return cls(
            primary="#8b5cf6",
            secondary="#6d28d9",
            accent="#ec4899",
            background="#0f0a1a",
            card="#1a1028",
            text="#e2e8f0",
            border="#2d1b4e",
            gradient_start="#8b5cf6",
            gradient_end="#ec4899",
            rgb_primary="139, 92, 246"
        )
    
    @classmethod
    def matrix(cls) -> 'ColorPalette':
        return cls(
            primary="#00ff41",
            secondary="#00cc33",
            accent="#00ff88",
            background="#000000",
            card="#0a1a0a",
            text="#00ff41",
            border="#003300",
            gradient_start="#00ff41",
            gradient_end="#00ff88",
            rgb_primary="0, 255, 65"
        )

# ============================================================
# DATA MODELS
# ============================================================

@dataclass
class Project:
    """Enhanced project data model with validation and computed properties."""
    
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
    play_store_url: Optional[str] = None
    stats: Dict[str, Any] = field(default_factory=dict)
    testimonio: Optional[str] = None
    autor_testimonio: Optional[str] = None
    
    def __post_init__(self):
        """Validate and sanitize project data."""
        if not self.titulo or not self.descripcion:
            raise ValueError("Project must have title and description")
        
        # HTML escaping for security
        self.titulo = escape(self.titulo)
        self.descripcion = escape(self.descripcion)
        self.tags = [escape(tag) for tag in self.tags]
        self.tecnologias = [escape(tech) for tech in self.tecnologias]
        
        # Auto-generate slug
        self._slug = self._generate_slug()
    
    def _generate_slug(self) -> str:
        """Generate URL-friendly slug."""
        slug = self.titulo.lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        return slug.strip('-')
    
    @property
    def slug(self) -> str:
        return self._slug
    
    @property
    def has_video(self) -> bool:
        return bool(self.video_url and self.video_url.strip())
    
    @property
    def is_youtube(self) -> bool:
        return self.has_video and ('youtube.com' in self.video_url or 'youtu.be' in self.video_url)
    
    @property
    def youtube_id(self) -> Optional[str]:
        """Extract YouTube video ID."""
        if not self.is_youtube:
            return None
        # Handle various YouTube URL formats
        patterns = [
            r'youtube\.com/watch\?v=([^&]+)',
            r'youtu\.be/([^?]+)',
            r'youtube\.com/embed/([^?]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, self.video_url)
            if match:
                return match.group(1)
        return None
    
    @property
    def embed_url(self) -> str:
        """Get optimized embed URL."""
        if self.is_youtube and self.youtube_id:
            return f"https://www.youtube.com/embed/{self.youtube_id}?autoplay=1&mute=1&loop=1&playlist={self.youtube_id}&controls=0&modestbranding=1&rel=0"
        return self.video_url

# ============================================================
# CACHE SYSTEM
# ============================================================

class Cache:
    """Simple caching system with TTL."""
    
    def __init__(self):
        self._cache = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value if not expired."""
        if key in self._cache:
            value, timestamp = self._cache[key]
            return value
        return None
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        """Set cached value with TTL in seconds."""
        self._cache[key] = (value, datetime.now().timestamp() + ttl)
    
    def clear(self):
        """Clear all cache."""
        self._cache.clear()

# ============================================================
# MEDIA OPTIMIZER
# ============================================================

class MediaOptimizer:
    """Optimize media for performance."""
    
    @staticmethod
    def get_thumbnail(url: str, size: str = "medium") -> str:
        """Generate thumbnail URL for various platforms."""
        if not url:
            return ""
        
        # YouTube thumbnails
        if 'youtube.com' in url or 'youtu.be' in url:
            yt_id = re.search(r'(?:v=|/)([a-zA-Z0-9_-]{11})', url)
            if yt_id:
                sizes = {
                    "small": "default.jpg",
                    "medium": "mqdefault.jpg",
                    "large": "hqdefault.jpg",
                    "max": "maxresdefault.jpg"
                }
                return f"https://img.youtube.com/vi/{yt_id.group(1)}/{sizes.get(size, 'mqdefault.jpg')}"
        
        # Local video - generate poster frame (in real implementation)
        return url
    
    @staticmethod
    def optimize_video_attributes(url: str) -> Dict[str, str]:
        """Get optimized video attributes."""
        attrs = {
            "playsinline": "playsinline",
            "muted": "muted",
            "autoplay": "autoplay",
            "loop": "loop",
            "preload": "metadata"
        }
        
        if 'youtube.com' in url or 'youtu.be' in url:
            return {"src": url, "type": "iframe"}
        
        return {"src": url, "type": "video", **attrs}

# ============================================================
# TEMPLATE ENGINE - ADVANCED
# ============================================================

class AdvancedTemplateEngine:
    """Next-generation template engine with partials, helpers, and caching."""
    
    def __init__(self):
        self.partials = {}
        self.helpers = {}
        self.cache = Cache()
        self._register_builtin_helpers()
    
    def _register_builtin_helpers(self):
        """Register built-in template helpers."""
        self.helpers.update({
            'upper': lambda x: x.upper() if x else '',
            'lower': lambda x: x.lower() if x else '',
            'truncate': lambda x, n=100: x[:n] + '...' if len(x) > n else x,
            'join': lambda x, sep=', ': sep.join(x) if x else '',
            'date': lambda x: datetime.strptime(x, '%Y-%m-%d').strftime('%b %Y') if x else '',
            'pluralize': lambda n, singular, plural=None: singular if n == 1 else (plural or singular + 's'),
        })
    
    def register_partial(self, name: str, content: str):
        """Register a partial template."""
        self.partials[name] = content
    
    def register_helper(self, name: str, func: Callable):
        """Register a custom helper function."""
        self.helpers[name] = func
    
    def render(self, template: str, context: Dict[str, Any]) -> str:
        """Render template with context, partials, and helpers."""
        cache_key = hashlib.md5(f"{template}{str(context)}".encode()).hexdigest()
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        
        result = template
        
        # Process partials
        result = self._process_partials(result)
        
        # Process helpers
        result = self._process_helpers(result, context)
        
        # Process variables
        result = self._process_variables(result, context)
        
        # Process loops
        result = self._process_loops(result, context)
        
        # Process conditionals
        result = self._process_conditionals(result, context)
        
        # Cache result
        self.cache.set(cache_key, result)
        
        return result
    
    def _process_partials(self, template: str) -> str:
        """Process {{> partial_name}} includes."""
        def replacer(match):
            name = match.group(1).strip()
            return self.partials.get(name, f'<!-- Partial "{name}" not found -->')
        
        return re.sub(r'{{>\s*([^}]+)\s*}}', replacer, template)
    
    def _process_helpers(self, template: str, context: Dict[str, Any]) -> str:
        """Process helper function calls: {{helper_name arg1 arg2}}."""
        def replacer(match):
            full = match.group(1)
            parts = full.split()
            helper_name = parts[0]
            args = parts[1:] if len(parts) > 1 else []
            
            if helper_name in self.helpers:
                # Resolve arguments from context
                resolved_args = []
                for arg in args:
                    if arg in context:
                        resolved_args.append(context[arg])
                    else:
                        resolved_args.append(arg)
                return str(self.helpers[helper_name](*resolved_args))
            return f'{{{{{full}}}}}'
        
        return re.sub(r'{{\s*([^}]+?)\s*}}', replacer, template)
    
    def _process_variables(self, template: str, context: Dict[str, Any]) -> str:
        """Process variable replacement with dot notation support."""
        def get_nested_value(obj, path):
            parts = path.split('.')
            current = obj
            for part in parts:
                if isinstance(current, dict):
                    current = current.get(part)
                elif isinstance(current, list) and part.isdigit():
                    current = current[int(part)]
                else:
                    current = getattr(current, part, None)
                if current is None:
                    break
            return current
        
        def replacer(match):
            path = match.group(1).strip()
            value = get_nested_value(context, path)
            if value is None:
                return ''
            if isinstance(value, (list, dict)):
                return str(value)
            return str(value)
        
        return re.sub(r'{{\s*([^#/>][^}]*?)\s*}}', replacer, template)
    
    def _process_loops(self, template: str, context: Dict[str, Any]) -> str:
        """Process {{#each}} blocks."""
        pattern = r'{{#each\s+([^}]+)}}(.*?){{/each}}'
        
        def replacer(match):
            path = match.group(1).strip()
            content = match.group(2)
            
            # Get the iterable
            iterable = context
            for part in path.split('.'):
                if isinstance(iterable, dict):
                    iterable = iterable.get(part)
                else:
                    iterable = getattr(iterable, part, None)
                if iterable is None:
                    return ''
            
            if not isinstance(iterable, (list, tuple)):
                return ''
            
            # Render each item
            results = []
            for item in iterable:
                item_context = {**context, 'this': item, 'item': item}
                # Add item properties to context
                if isinstance(item, dict):
                    item_context.update(item)
                elif hasattr(item, '__dict__'):
                    item_context.update(item.__dict__)
                results.append(self._process_variables(content, item_context))
            
            return ''.join(results)
        
        return re.sub(pattern, replacer, template, flags=re.DOTALL)
    
    def _process_conditionals(self, template: str, context: Dict[str, Any]) -> str:
        """Process {{#if}}, {{#unless}}, {{#else}} blocks."""
        # Process #if blocks
        pattern = r'{{#if\s+([^}]+)}}(.*?)(?:{{else}}(.*?))?{{/if}}'
        
        def replacer(match):
            condition_path = match.group(1).strip()
            true_content = match.group(2)
            false_content = match.group(3) if match.group(3) else ''
            
            # Evaluate condition
            value = context
            for part in condition_path.split('.'):
                if isinstance(value, dict):
                    value = value.get(part)
                else:
                    value = getattr(value, part, None)
                if value is None:
                    break
            
            # Render appropriate branch
            if value:
                return self._process_variables(true_content, context)
            else:
                return self._process_variables(false_content, context)
        
        return re.sub(pattern, replacer, template, flags=re.DOTALL)

# ============================================================
# PORTFOLIO GENERATOR - MAIN
# ============================================================

class PortfolioGenerator:
    """Main portfolio generator with enterprise features."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = self._default_config()
        if config:
            self.config.update(config)
        
        self.template_engine = AdvancedTemplateEngine()
        self.media_optimizer = MediaOptimizer()
        self.cache = Cache()
        
        # Load theme
        self.theme = self._load_theme()
        
        # Register partials
        self._register_partials()
        
        # Register helpers
        self._register_helpers()
        
        logger.info(f"🚀 Portfolio Generator initialized with theme: {self.config.get('theme', 'cyberpunk')}")
    
    def _default_config(self) -> Dict[str, Any]:
        return {
            'input_file': 'proyectos.json',
            'output_file': 'index.html',
            'theme': 'cyberpunk',
            'animation_style': 'smooth',
            'minify': True,
            'debug': False,
            'lazy_load': True,
            'preconnect': True,
            'service_worker': False,
            'pwa': False,
            'analytics_id': None,
            'grid_cols': 3,
            'max_featured': 2,
            'language': 'es',
            'timezone': 'America/Argentina/Buenos_Aires',
        }
    
    def _load_theme(self) -> ColorPalette:
        """Load theme color palette."""
        theme_name = self.config.get('theme', 'cyberpunk')
        theme_map = {
            'cyberpunk': ColorPalette.cyberpunk,
            'dark_matter': ColorPalette.dark_matter,
            'matrix': ColorPalette.matrix,
        }
        return theme_map.get(theme_name, ColorPalette.cyberpunk)()
    
    def _register_partials(self):
        """Register all template partials."""
        self.template_engine.register_partial('header', self._get_header_partial())
        self.template_engine.register_partial('footer', self._get_footer_partial())
        self.template_engine.register_partial('hero', self._get_hero_partial())
        self.template_engine.register_partial('project_card', self._get_project_card_partial())
        self.template_engine.register_partial('featured_project', self._get_featured_partial())
        self.template_engine.register_partial('stats_grid', self._get_stats_partial())
        self.template_engine.register_partial('modal', self._get_modal_partial())
        self.template_engine.register_partial('testimonial', self._get_testimonial_partial())
    
    def _register_helpers(self):
        """Register template helpers."""
        self.template_engine.register_helper('format_date', lambda d: datetime.strptime(d, '%Y-%m-%d').strftime('%d %b %Y') if d else '')
        self.template_engine.register_helper('count', lambda items: len(items) if items else 0)
        self.template_engine.register_helper('to_json', lambda obj: json.dumps(obj))
        self.template_engine.register_helper('escape_html', lambda text: escape(str(text)))
    
    # ============================================================
    # PARTIAL TEMPLATES
    # ============================================================
    
    def _get_header_partial(self) -> str:
        return """<header class="fixed top-0 left-0 right-0 z-50 bg-{{theme.background}}/90 backdrop-blur-xl border-b border-{{theme.border}}/80 px-6 py-4 shadow-2xl">
    <div class="max-w-7xl mx-auto flex justify-between items-center">
        <div class="flex items-center gap-4">
            <div class="relative">
                <span class="relative flex h-4 w-4">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-{{theme.primary}} opacity-75"></span>
                    <span class="relative inline-flex rounded-full h-4 w-4 bg-{{theme.primary}} shadow-[0_0_20px_{{theme.primary}}]"></span>
                </span>
            </div>
            <div>
                <h1 class="text-xl font-black text-white tracking-wider uppercase">Stefano Del Moro</h1>
                <p class="text-[11px] text-{{theme.primary}} font-mono font-semibold tracking-wider">Full Stack & AI Engineer • Android Architect</p>
            </div>
        </div>
        
        <div class="flex items-center gap-4">
            <div class="hidden md:flex items-center gap-3 px-4 py-2 bg-{{theme.card}} border border-{{theme.border}} rounded-xl text-xs font-mono text-{{theme.primary}}">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                <span>SYS_STATUS: ONLINE</span>
                <span class="w-px h-4 bg-{{theme.border}}"></span>
                <span class="text-gray-400">{{year}}</span>
            </div>
            <a href="#contacto" class="px-6 py-2.5 bg-{{theme.primary}}/10 border border-{{theme.primary}}/60 text-{{theme.primary}} text-xs font-mono font-bold rounded-xl hover:bg-{{theme.primary}} hover:text-black transition-all duration-300 shadow-[0_0_30px_rgba({{theme.rgb_primary}},0.2)] hover:shadow-[0_0_50px_rgba({{theme.rgb_primary}},0.4)]">
                CONTACTAR
            </a>
        </div>
    </div>
</header>"""
    
    def _get_hero_partial(self) -> str:
        return """<div class="text-center max-w-4xl mx-auto mb-16 mt-32">
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
        {{> stats_grid}}
    </div>
    
    <span class="px-5 py-2 rounded-full text-xs font-mono font-bold bg-{{theme.primary}}/10 text-{{theme.primary}} border border-{{theme.primary}}/30 uppercase tracking-widest inline-block mb-6 animate-pulse-slow">
        ⚡ Sistemas Autónomos & Movilidad Inteligente
    </span>
    
    <h2 class="text-4xl md:text-6xl font-black text-white leading-tight mb-6">
        Soluciones de Alto Impacto con <br/>
        <span class="text-{{theme.primary}} glow-text">Inteligencia Artificial & Android NATIVO</span>
    </h2>
    <p class="text-gray-400 text-sm md:text-lg leading-relaxed max-w-2xl mx-auto">
        Especializado en aplicaciones Android con IA local, herramientas de alto rendimiento para Linux Mint y automatizaciones avanzadas.
    </p>
    
    <div class="flex justify-center gap-4 mt-8">
        <a href="#proyectos" class="px-8 py-3 bg-{{theme.primary}} text-black font-black text-sm uppercase tracking-wider rounded-xl hover:bg-{{theme.secondary}} transition-all shadow-[0_0_30px_rgba({{theme.rgb_primary}},0.3)]">
            Explorar Proyectos ↓
        </a>
        <a href="#contacto" class="px-8 py-3 border border-{{theme.border}} text-white font-mono text-sm rounded-xl hover:bg-{{theme.card}} transition-all">
            Contacto
        </a>
    </div>
</div>"""
    
    def _get_stats_partial(self) -> str:
        return """<div class="p-4 bg-{{theme.card}} border border-{{theme.border}} rounded-2xl glow-cyan hover:border-{{theme.primary}}/60 transition-all group">
    <span class="text-2xl font-black text-{{theme.primary}} block group-hover:scale-110 transition-transform">{{value}}</span>
    <span class="text-[10px] font-mono text-gray-400 uppercase tracking-wider">{{label}}</span>
</div>"""
    
    def _get_featured_partial(self) -> str:
        return """<section class="mb-20">
    <div class="bg-{{theme.card}} border border-{{theme.primary}}/50 rounded-3xl p-6 md:p-10 glow-cyan transition-all duration-500 hover:shadow-[0_0_50px_rgba({{theme.rgb_primary}},0.15)]">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center">
            <div class="lg:col-span-5 flex flex-col justify-between h-full">
                <div>
                    <div class="flex items-center gap-4 mb-6">
                        <span class="px-4 py-1.5 bg-{{theme.primary}}/10 border border-{{theme.primary}}/50 text-{{theme.primary}} font-mono font-bold text-xs uppercase tracking-wider rounded-lg">
                            {{categoria}}
                        </span>
                        <span class="text-[10px] font-mono text-yellow-400 bg-yellow-400/10 px-3 py-1 rounded-full border border-yellow-400/30 animate-pulse">
                            ⚡ FEATURED
                        </span>
                    </div>
                    
                    <h3 class="text-3xl md:text-4xl font-black text-white mb-4 leading-tight glow-text">
                        {{titulo}}
                    </h3>
                    <p class="text-gray-300 text-sm md:text-base leading-relaxed mb-6">
                        {{descripcion}}
                    </p>
                    
                    <div class="flex flex-wrap gap-2 mb-8">
                        {{#each tags}}
                        <span class="text-xs font-mono bg-gray-950 text-{{../theme.primary}} px-4 py-1.5 rounded-full border border-{{../theme.border}}">{{this}}</span>
                        {{/each}}
                    </div>
                </div>
                
                <div class="flex flex-wrap items-center gap-4">
                    {{#if link}}
                    <a href="{{link}}" target="_blank" class="inline-flex items-center gap-2 px-8 py-3.5 bg-{{theme.primary}} text-black font-black text-xs uppercase tracking-wider rounded-xl hover:bg-{{theme.secondary}} transition-all shadow-[0_0_30px_rgba({{theme.rgb_primary}},0.4)] hover:shadow-[0_0_50px_rgba({{theme.rgb_primary}},0.6)]">
                        ▶ Ver en Google Play
                    </a>
                    {{/if}}
                    <button onclick="openModal('{{video_url}}', '{{titulo}}')" class="px-6 py-3 border border-{{theme.primary}}/60 text-{{theme.primary}} font-mono font-bold text-xs uppercase rounded-xl hover:bg-{{theme.primary}}/10 transition">
                        📺 Ver Demo HD
                    </button>
                </div>
            </div>
            
            <div class="lg:col-span-7">
                <div class="aspect-video w-full rounded-2xl overflow-hidden border border-{{theme.border}} shadow-2xl group">
                    {{> media_preview}}
                </div>
            </div>
        </div>
    </div>
</section>"""
    
    def _get_project_card_partial(self) -> str:
        return """<div class="bg-{{theme.card}} border border-{{theme.border}} hover:border-{{theme.primary}}/60 rounded-2xl p-6 transition-all duration-500 flex flex-col justify-between glow-cyan hover:shadow-[0_0_40px_rgba({{theme.rgb_primary}},0.1)] hover:-translate-y-1">
    <div>
        <div class="flex justify-between items-start mb-4">
            <span class="px-3 py-1 bg-{{theme.primary}}/10 border border-{{theme.primary}}/40 text-{{theme.primary}} text-[11px] font-mono font-bold tracking-wider uppercase rounded-lg">
                {{categoria}}
            </span>
            {{#if destacado}}
            <span class="text-[10px] font-mono text-yellow-400 bg-yellow-400/10 px-2 py-0.5 rounded-full border border-yellow-400/30">
                ★ Destacado
            </span>
            {{/if}}
        </div>
        
        <h4 class="text-xl font-bold text-white mb-3 leading-snug hover:text-{{theme.primary}} transition-colors">
            {{titulo}}
        </h4>
        <p class="text-gray-400 text-xs leading-relaxed mb-6">{{descripcion}}</p>
        
        <div class="aspect-video w-full rounded-xl overflow-hidden mb-6">
            {{> media_preview}}
        </div>
        
        {{#if stats}}
        <div class="grid grid-cols-2 gap-2 mb-4">
            {{#each stats}}
            <div class="bg-gray-900/50 rounded-lg p-2 text-center">
                <span class="text-{{../theme.primary}} font-bold text-sm">{{value}}</span>
                <span class="text-gray-500 text-[8px] uppercase block">{{label}}</span>
            </div>
            {{/each}}
        </div>
        {{/if}}
    </div>
    
    <div>
        <div class="flex flex-wrap gap-2 mb-4">
            {{#each tags}}
            <span class="text-[10px] font-mono bg-gray-950 text-gray-300 px-3 py-1 rounded-full border border-gray-800">{{this}}</span>
            {{/each}}
        </div>
        <button onclick="openModal('{{video_url}}', '{{titulo}}')" class="w-full py-3 bg-{{theme.primary}}/5 border border-{{theme.primary}}/30 text-{{theme.primary}} font-mono font-bold text-xs uppercase rounded-xl hover:bg-{{theme.primary}} hover:text-black transition-all">
            🔍 Ver Demo Completo
        </button>
    </div>
</div>"""
    
    def _get_media_preview_partial(self) -> str:
        return """<div class="w-full h-full bg-gray-950 flex items-center justify-center font-mono text-xs text-{{theme.primary}}/50">
    {{#if has_video}}
        {{#if is_youtube}}
        <iframe class="w-full h-full pointer-events-none scale-105" src="{{embed_url}}" title="{{titulo}}" frameborder="0" allow="autoplay; encrypted-media" loading="lazy"></iframe>
        {{else}}
        <video class="w-full h-full object-cover scale-100 group-hover:scale-105 transition duration-700" autoplay loop muted playsinline preload="metadata">
            <source src="{{video_url}}" type="video/mp4">
        </video>
        {{/if}}
        <div class="absolute inset-0 bg-gradient-to-t from-gray-950/80 via-transparent to-transparent flex items-center justify-center">
            <button onclick="openModal('{{video_url}}', '{{titulo}}')" class="opacity-90 hover:opacity-100 transition-all px-5 py-2.5 bg-{{theme.primary}} text-black font-mono font-bold text-xs rounded-lg shadow-[0_0_30px_rgba({{theme.rgb_primary}},0.3)] flex items-center gap-2 hover:scale-105 transform">
                <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
                VER DEMO
            </button>
        </div>
    {{else}}
        <div class="text-center">
            <svg class="w-12 h-12 mx-auto mb-2 text-{{theme.primary}}/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
            </svg>
            <span class="text-[10px]">DEMO NO DISPONIBLE</span>
        </div>
    {{/if}}
</div>"""
    
    def _get_modal_partial(self) -> str:
        return """<div id="videoModal" class="fixed inset-0 z-[100] bg-black/95 backdrop-blur-2xl hidden flex items-center justify-center p-4 md:p-10 transition-all duration-500">
    <div class="relative w-full max-w-6xl bg-{{theme.card}} border border-{{theme.primary}}/60 rounded-3xl overflow-hidden shadow-[0_0_80px_rgba({{theme.rgb_primary}},0.3)] animate-fade-in">
        <div class="flex justify-between items-center px-8 py-5 border-b border-{{theme.border}} bg-{{theme.background}}/80">
            <h3 id="modalTitle" class="text-lg font-bold text-white font-mono tracking-wider glow-text">DEMO VIDEO</h3>
            <button onclick="closeModal()" class="text-{{theme.primary}} hover:text-white font-mono text-xl font-bold px-4 py-2 bg-{{theme.primary}}/10 rounded-xl border border-{{theme.primary}}/30 hover:bg-{{theme.primary}}/20 transition-all">
                ✕ Cerrar
            </button>
        </div>
        <div class="aspect-video w-full bg-black">
            <iframe id="modalIframe" class="w-full h-full hidden" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
            <video id="modalVideo" class="w-full h-full hidden" controls autoplay></video>
        </div>
        <div class="px-8 py-4 bg-{{theme.background}}/80 border-t border-{{theme.border}}">
            <p class="text-xs text-gray-400 font-mono">💡 Presiona ESC para cerrar • Navegación con flechas ← →</p>
        </div>
    </div>
</div>"""
    
    def _get_footer_partial(self) -> str:
        return """<footer id="contacto" class="py-12 border-t border-{{theme.border}} text-center text-xs font-mono text-gray-500 bg-{{theme.background}}/50 backdrop-blur">
    <div class="max-w-6xl mx-auto px-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
            <div class="text-left">
                <h4 class="text-{{theme.primary}} font-bold text-sm mb-3">Stefano Del Moro</h4>
                <p class="text-gray-400 text-xs">Full Stack & AI Engineer • Android Architect</p>
                <p class="text-gray-500 text-[10px] mt-2">Buenos Aires, Argentina</p>
            </div>
            <div class="text-left">
                <h4 class="text-{{theme.primary}} font-bold text-sm mb-3">Contacto</h4>
                <div class="space-y-1 text-xs">
                    <p>📧 <a href="mailto:stefano@example.com" class="text-gray-400 hover:text-{{theme.primary}} transition">stefano@example.com</a></p>
                    <p>🐙 <a href="#" class="text-gray-400 hover:text-{{theme.primary}} transition">github.com/stefanodemoro</a></p>
                    <p>💼 <a href="#" class="text-gray-400 hover:text-{{theme.primary}} transition">linkedin.com/in/stefanodemoro</a></p>
                </div>
            </div>
            <div class="text-left">
                <h4 class="text-{{theme.primary}} font-bold text-sm mb-3">Especialidades</h4>
                <div class="flex flex-wrap gap-2">
                    <span class="text-[10px] font-mono bg-gray-950 text-gray-300 px-3 py-1 rounded-full border border-gray-800">Android</span>
                    <span class="text-[10px] font-mono bg-gray-950 text-gray-300 px-3 py-1 rounded-full border border-gray-800">AI/ML</span>
                    <span class="text-[10px] font-mono bg-gray-950 text-gray-300 px-3 py-1 rounded-full border border-gray-800">Linux</span>
                    <span class="text-[10px] font-mono bg-gray-950 text-gray-300 px-3 py-1 rounded-full border border-gray-800">Kotlin</span>
                    <span class="text-[10px] font-mono bg-gray-950 text-gray-300 px-3 py-1 rounded-full border border-gray-800">Python</span>
                    <span class="text-[10px] font-mono bg-gray-950 text-gray-300 px-3 py-1 rounded-full border border-gray-800">TFLite</span>
                </div>
            </div>
        </div>
        <div class="pt-8 border-t border-{{theme.border}}/50">
            <p>© {{year}} Stefano Del Moro • Software & Mobile Engineering Portfolio</p>
            <p class="text-[10px] text-gray-600 mt-1">⚡ Generado con AI • v3.0.0</p>
        </div>
    </div>
</footer>"""
    
    def _get_testimonial_partial(self) -> str:
        return """<div class="bg-{{theme.card}} border border-{{theme.border}} rounded-2xl p-6 glow-cyan">
    <div class="flex items-start gap-4">
        <div class="text-4xl text-{{theme.primary}} opacity-30">"</div>
        <div>
            <p class="text-gray-300 text-sm italic leading-relaxed">{{text}}</p>
            <p class="text-{{theme.primary}} font-bold text-xs mt-3">— {{author}}</p>
        </div>
    </div>
</div>"""
    
    # ============================================================
    # MAIN GENERATION LOGIC
    # ============================================================
    
    def generate(self) -> str:
        """Generate the complete portfolio HTML."""
        try:
            logger.info("📦 Loading projects...")
            projects = self._load_projects()
            
            if not projects:
                logger.warning("No projects found, using demo data")
                projects = self._get_demo_projects()
            
            logger.info(f"✅ Loaded {len(projects)} projects")
            
            # Separate featured and other projects
            featured = [p for p in projects if p.destacado]
            if not featured:
                featured = projects[:self.config.get('max_featured', 2)]
            
            others = [p for p in projects if p not in featured]
            
            # Build context
            context = self._build_context(projects, featured, others)
            
            logger.info("🎨 Rendering template...")
            html = self._render_template(context)
            
            if self.config.get('minify', True):
                logger.info("🗜️ Minifying HTML...")
                html = self._minify_html(html)
            
            logger.info("✅ Portfolio generated successfully!")
            return html
            
        except Exception as e:
            logger.error(f"❌ Generation failed: {e}")
            if self.config.get('debug', False):
                logger.exception("Detailed error:")
            raise
    
    def _load_projects(self) -> List[Project]:
        """Load projects from JSON file."""
        input_file = Path(self.config.get('input_file', 'proyectos.json'))
        
        if not input_file.exists():
            logger.warning(f"File not found: {input_file}")
            return []
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                logger.error("JSON data must be a list")
                return []
            
            projects = []
            for item in data:
                try:
                    projects.append(Project(**item))
                except Exception as e:
                    logger.warning(f"Skipping invalid project: {e}")
            
            return projects
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON: {e}")
            return []
        except Exception as e:
            logger.error(f"Error loading projects: {e}")
            return []
    
    def _get_demo_projects(self) -> List[Project]:
        """Return demo projects for testing."""
        return [
            Project(
                titulo="AI Chat Assistant Pro",
                descripcion="Asistente conversacional con LLM local y reconocimiento de voz para Android nativo. Procesamiento offline con TFLite.",
                categoria="Inteligencia Artificial",
                tags=["Android", "LLM", "Kotlin", "TFLite", "Voice Recognition"],
                video_url="https://www.youtube.com/embed/dQw4w9WgXcQ",
                link="https://play.google.com",
                destacado=True,
                stats={
                    "descargas": {"value": "50K+", "label": "Descargas"},
                    "rating": {"value": "4.8★", "label": "Calificación"}
                },
                testimonio="Revolucionó nuestra atención al cliente, reduciendo tiempos de respuesta en un 70%.",
                autor_testimonio="Juan Pérez, CTO TechCorp"
            ),
            Project(
                titulo="Linux System Monitor Pro",
                descripcion="Monitor de recursos con análisis predictivo y alertas inteligentes para Linux Mint.",
                categoria="Herramientas",
                tags=["Python", "Linux", "GTK", "Machine Learning"],
                video_url="https://www.youtube.com/embed/dQw4w9WgXcQ",
                destacado=True,
                stats={
                    "usuarios": {"value": "10K+", "label": "Usuarios Activos"},
                    "rendimiento": {"value": "40%", "label": "Mejora CPU"}
                }
            ),
            Project(
                titulo="Smart Home Controller",
                descripcion="Aplicación Android para control de dispositivos IoT con IA local para automatización predictiva.",
                categoria="IoT",
                tags=["Android", "IoT", "MQTT", "AI", "Home Automation"],
                video_url="https://www.youtube.com/embed/dQw4w9WgXcQ",
                stats={
                    "dispositivos": {"value": "25+", "label": "Compatible"}
                }
            ),
        ]
    
    def _build_context(self, projects: List[Project], featured: List[Project], 
                       others: List[Project]) -> Dict[str, Any]:
        """Build template context with all data."""
        
        # Calculate statistics
        total_techs = len(set().union(*[set(p.tecnologias) for p in projects if p.tecnologias]))
        
        stats = [
            {"value": f"{len(projects)}+", "label": "Proyectos"},
            {"value": f"{total_techs}", "label": "Tecnologías"},
            {"value": "3+", "label": "Años Experiencia"},
            {"value": str(len([p for p in projects if p.link])), "label": "Apps en Producción"},
        ]
        
        # Build context
        return {
            "theme": self.theme.__dict__ if hasattr(self.theme, '__dict__') else asdict(self.theme),
            "projects": [p.__dict__ for p in projects],
            "featured": [p.__dict__ for p in featured],
            "others": [p.__dict__ for p in others],
            "stats": stats,
            "year": datetime.now().year,
            "language": self.config.get('language', 'es'),
            "animation_style": self.config.get('animation_style', 'smooth'),
            "lazy_load": self.config.get('lazy_load', True),
            "grid_cols": self.config.get('grid_cols', 3),
        }
    
    def _render_template(self, context: Dict[str, Any]) -> str:
        """Render the main template."""
        # Build main content
        content = []
        
        # Header
        content.append(self.template_engine.render("{{> header}}", context))
        
        # Hero
        content.append(self.template_engine.render("{{> hero}}", context))
        
        # Featured projects
        if context.get('featured'):
            for project in context['featured']:
                proj_context = {**context, **project}
                content.append(self.template_engine.render("{{> featured_project}}", proj_context))
        
        # Project grid
        if context.get('others'):
            content.append("""
            <section id="proyectos" class="max-w-7xl mx-auto px-6 mb-20">
                <h2 class="text-2xl font-bold text-white mb-8 flex items-center gap-3">
                    <span class="w-1 h-8 bg-{{theme.primary}} rounded-full"></span>
                    Proyectos
                    <span class="text-sm font-normal text-gray-400 ml-2">({{count others}})</span>
                </h2>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-{{grid_cols}} gap-6">
                    {{#each others}}
                    {{> project_card}}
                    {{/each}}
                </div>
            </section>
            """)
        
        # Footer
        content.append(self.template_engine.render("{{> footer}}", context))
        
        # Modal
        content.append(self.template_engine.render("{{> modal}}", context))
        
        # JavaScript
        content.append(self._get_javascript())
        
        # Combine everything
        html = self._get_base_template()
        html = html.replace("{{CONTENT}}", "\n".join(content))
        html = self.template_engine.render(html, context)
        
        return html
    
    def _get_base_template(self) -> str:
        """Return the base HTML template."""
        return """<!DOCTYPE html>
<html lang="{{language}}" class="dark scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stefano Del Moro | Full Stack & AI Engineer</title>
    <meta name="description" content="Portafolio profesional de Stefano Del Moro - Full Stack & AI Engineer especializado en Android nativo e IA local">
    <meta name="theme-color" content="{{theme.primary}}">
    <meta property="og:title" content="Stefano Del Moro | Full Stack & AI Engineer">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://stefanodemoro.com">
    
    {{#if preconnect}}
    <link rel="preconnect" href="https://cdn.tailwindcss.com">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    {{/if}}
    
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        theme: {
                            primary: '{{theme.primary}}',
                            secondary: '{{theme.secondary}}',
                            accent: '{{theme.accent}}',
                            background: '{{theme.background}}',
                            card: '{{theme.card}}',
                            border: '{{theme.border}}',
                        }
                    },
                    animation: {
                        'fade-in': 'fadeIn 0.5s ease-out',
                        'slide-up': 'slideUp 0.6s ease-out',
                        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                        'glow-pulse': 'glowPulse 2s ease-in-out infinite',
                        'float': 'float 6s ease-in-out infinite',
                        'shimmer': 'shimmer 3s ease-in-out infinite',
                    },
                    keyframes: {
                        fadeIn: {
                            '0%': { opacity: '0' },
                            '100%': { opacity: '1' },
                        },
                        slideUp: {
                            '0%': { transform: 'translateY(20px)', opacity: '0' },
                            '100%': { transform: 'translateY(0)', opacity: '1' },
                        },
                        glowPulse: {
                            '0%, 100%': { 'box-shadow': '0 0 20px rgba({{theme.rgb_primary}}, 0.2)' },
                            '50%': { 'box-shadow': '0 0 40px rgba({{theme.rgb_primary}}, 0.4)' },
                        },
                        float: {
                            '0%, 100%': { transform: 'translateY(0px)' },
                            '50%': { transform: 'translateY(-10px)' },
                        },
                        shimmer: {
                            '0%': { 'background-position': '-200% 0' },
                            '100%': { 'background-position': '200% 0' },
                        },
                    }
                }
            }
        }
    </script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            background-color: {{theme.background}};
            background-image: 
                radial-gradient(circle at 50% 0%, rgba({{theme.rgb_primary}}, 0.08) 0%, transparent 60%),
                linear-gradient(to right, rgba({{theme.rgb_primary}}, 0.03) 1px, transparent 1px),
                linear-gradient(to bottom, rgba({{theme.rgb_primary}}, 0.03) 1px, transparent 1px);
            background-size: 100% 100%, 40px 40px, 40px 40px;
            min-height: 100vh;
            font-family: system-ui, -apple-system, sans-serif;
            scroll-behavior: smooth;
        }
        
        .glow-text {
            text-shadow: 0 0 30px rgba({{theme.rgb_primary}}, 0.3);
        }
        
        .glow-cyan {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 0 20px rgba({{theme.rgb_primary}}, 0.05);
        }
        
        .glow-cyan:hover {
            box-shadow: 0 0 40px rgba({{theme.rgb_primary}}, 0.15);
        }
        
        .animate-fade-in {
            animation: fadeIn 0.5s ease-out;
        }
        
        .animate-slide-up {
            animation: slideUp 0.6s ease-out;
        }
        
        .gradient-border {
            position: relative;
            border: 1px solid transparent;
            background-clip: padding-box;
        }
        
        .gradient-border::before {
            content: '';
            position: absolute;
            inset: -2px;
            border-radius: inherit;
            background: linear-gradient(135deg, {{theme.primary}}, transparent, {{theme.accent}});
            z-index: -1;
            opacity: 0.3;
            transition: opacity 0.3s;
        }
        
        .gradient-border:hover::before {
            opacity: 0.8;
        }
        
        .glass-effect {
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
        }
        
        .shimmer {
            background: linear-gradient(90deg, transparent, rgba({{theme.rgb_primary}}, 0.05), transparent);
            background-size: 200% 100%;
            animation: shimmer 3s ease-in-out infinite;
        }
        
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: {{theme.background}};
        }
        
        ::-webkit-scrollbar-thumb {
            background: {{theme.primary}};
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: {{theme.secondary}};
        }
        
        @media (max-width: 768px) {
            body { background-size: 100% 100%, 20px 20px, 20px 20px; }
        }
    </style>
</head>
<body>
    {{CONTENT}}
</body>
</html>"""
    
    def _get_javascript(self) -> str:
        """Return JavaScript for interactivity."""
        return """
<script>
    // ============================================================
    // MODAL CONTROLLER
    // ============================================================
    
    let currentVideoIndex = 0;
    let videoList = [];
    
    function openModal(url, title) {
        const modal = document.getElementById('videoModal');
        const modalTitle = document.getElementById('modalTitle');
        const iframe = document.getElementById('modalIframe');
        const video = document.getElementById('modalVideo');
        
        if (!url) {
            console.warn('No video URL provided');
            return;
        }
        
        modalTitle.textContent = title || 'DEMO VIDEO';
        
        // Detectar tipo de contenido
        if (url.includes('youtube.com') || url.includes('youtu.be')) {
            let ytId = url.split('/').pop().split('?')[0];
            iframe.src = 'https://www.youtube.com/embed/' + ytId + '?autoplay=1&controls=1&rel=0';
            iframe.classList.remove('hidden');
            video.classList.add('hidden');
            video.pause();
        } else {
            video.src = url;
            video.classList.remove('hidden');
            iframe.classList.add('hidden');
            iframe.src = '';
            video.play().catch(e => console.warn('Auto-play blocked:', e));
        }
        
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
        document.body.style.position = 'fixed';
        document.body.style.width = '100%';
        
        // Keyboard navigation
        document.addEventListener('keydown', handleModalKeydown);
    }
    
    function closeModal() {
        const modal = document.getElementById('videoModal');
        const iframe = document.getElementById('modalIframe');
        const video = document.getElementById('modalVideo');
        
        modal.classList.add('hidden');
        iframe.src = '';
        video.pause();
        video.src = '';
        document.body.style.overflow = 'auto';
        document.body.style.position = 'static';
        document.body.style.width = 'auto';
        
        document.removeEventListener('keydown', handleModalKeydown);
    }
    
    function handleModalKeydown(e) {
        if (e.key === 'Escape') {
            closeModal();
        }
        if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
            navigateVideo(e.key === 'ArrowRight' ? 1 : -1);
        }
    }
    
    // ============================================================
    // VIDEO NAVIGATION (for multiple videos)
    // ============================================================
    
    function navigateVideo(direction) {
        if (!videoList.length) return;
        currentVideoIndex = (currentVideoIndex + direction + videoList.length) % videoList.length;
        const video = videoList[currentVideoIndex];
        openModal(video.url, video.title);
    }
    
    // ============================================================
    // SMOOTH SCROLL
    // ============================================================
    
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offset = 80;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // ============================================================
    // INTERSECTION OBSERVER - Animations
    // ============================================================
    
    if (typeof IntersectionObserver !== 'undefined') {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
        
        document.querySelectorAll('.glow-cyan').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
            observer.observe(el);
        });
    }
    
    // ============================================================
    // CONSOLE EASTER EGG
    // ============================================================
    
    console.log('%c🚀 Stefano Del Moro - Portfolio v3.0', 
                'font-size:20px; font-weight:bold; color:#00f0ff;');
    console.log('%cFull Stack & AI Engineer | Android Architect', 
                'font-size:14px; color:#e2e8f0;');
    console.log('%c⚡ Built with passion, powered by AI', 
                'font-size:12px; color:#64748b;');
    
    // ============================================================
    // PERFORMANCE MONITORING
    // ============================================================
    
    if (typeof window.performance !== 'undefined') {
        const perfData = performance.getEntriesByType('navigation')[0];
        if (perfData) {
            console.log(`⏱️ Page load: ${Math.round(perfData.loadEventEnd - perfData.fetchStart)}ms`);
        }
    }
</script>"""
    
    def _minify_html(self, html: str) -> str:
        """Advanced HTML minification."""
        # Remove comments
        html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
        
        # Remove whitespace between tags
        html = re.sub(r'>\s+<', '><', html)
        
        # Remove multiple spaces
        html = re.sub(r'\s{2,}', ' ', html)
        
        # Remove whitespace around attributes
        html = re.sub(r'\s+=\s+', '=', html)
        
        # Remove trailing whitespace
        html = re.sub(r'\s+>', '>', html)
        
        return html.strip()
    
    def save(self, html: str) -> None:
        """Save generated HTML to file."""
        output_file = Path(self.config.get('output_file', 'index.html'))
        
        try:
            output_file.write_text(html, encoding='utf-8')
            logger.info(f"✅ Portfolio saved to: {output_file.absolute()}")
            
            # File size info
            size_kb = len(html) / 1024
            logger.info(f"📦 File size: {size_kb:.1f} KB")
            
        except Exception as e:
            logger.error(f"❌ Failed to save file: {e}")
            raise

# ============================================================
# CLI
# ============================================================

def main():
    """Command-line entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='🔥 Portfolio Generator Pro - Stefano Del Moro',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python portfolio.py -i proyectos.json -o index.html
  python portfolio.py --theme matrix --serve
  python portfolio.py --theme dark_matter --no-minify
        """
    )
    
    parser.add_argument('-i', '--input', default='proyectos.json',
                       help='Input JSON file (default: proyectos.json)')
    parser.add_argument('-o', '--output', default='index.html',
                       help='Output HTML file (default: index.html)')
    parser.add_argument('-t', '--theme', choices=['cyberpunk', 'dark_matter', 'matrix'],
                       default='cyberpunk', help='Theme style (default: cyberpunk)')
    parser.add_argument('--no-minify', action='store_true',
                       help='Disable HTML minification')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug mode')
    parser.add_argument('--serve', action='store_true',
                       help='Start a local server')
    parser.add_argument('--grid', type=int, choices=[2, 3, 4], default=3,
                       help='Number of grid columns (default: 3)')
    
    args = parser.parse_args()
    
    # Build config
    config = {
        'input_file': args.input,
        'output_file': args.output,
        'theme': args.theme,
        'minify': not args.no_minify,
        'debug': args.debug,
        'grid_cols': args.grid,
        'language': 'es',
    }
    
    # Generate portfolio
    try:
        generator = PortfolioGenerator(config)
        html = generator.generate()
        generator.save(html)
        
        if args.serve:
            import http.server
            import socketserver
            import webbrowser
            
            port = 8000
            os.chdir(os.path.dirname(args.output) or '.')
            
            handler = http.server.SimpleHTTPRequestHandler
            with socketserver.TCPServer(('', port), handler) as httpd:
                url = f'http://localhost:{port}/{os.path.basename(args.output)}'
                logger.info(f'🌐 Serving at: {url}')
                webbrowser.open(url)
                httpd.serve_forever()
                
    except KeyboardInterrupt:
        logger.info('🛑 Server stopped')
        sys.exit(0)
    except Exception as e:
        logger.error(f'❌ Error: {e}')
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
