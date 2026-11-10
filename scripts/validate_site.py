#!/usr/bin/env python3
"""Validação editorial/técnica do site estático ECOAR — sem bibliotecas externas."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlsplit, unquote

ROOT = Path("site")
DOMAIN = "https://ecoar.grupoeduardabispo.com.br"
PATHS = [
    "/", "/aprender/", "/laboratorio/", "/seu-palco/", "/mentoria/",
    "/organizacoes/", "/metodologia/", "/experiencias/", "/contato/",
    "/privacidade/", "/termos/", "/acessibilidade/", "/mapa-do-site/",
]
FILES = [ROOT / ("index.html" if p == "/" else p.lstrip("/") + "index.html") for p in PATHS]
STATIC = [ROOT / "assets/css/ecoar.css", ROOT / "assets/js/ecoar.js",
          ROOT / "assets/favicon.svg", ROOT / "robots.txt", ROOT / "sitemap.xml"]
ERRORS = []

class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.links = []
        self.buttons = []
        self.images = []
        self.canonicals = []
        self.description = []
        self.titles = []
        self.headings = 0
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append(tag)
        if tag == "h1":
            self.headings += 1
        if tag == "title":
            self._in_title = True
        if tag == "a":
            self.links.append(a.get("href", ""))
            if "button" in a.get("class", "").split():
                self.buttons.append(a.get("href", ""))
        if tag == "img":
            self.images.append(a)
        if tag == "link" and a.get("rel") == "canonical":
            self.canonicals.append(a.get("href"))
        if tag == "meta" and a.get("name") == "description":
            self.description.append(a.get("content", ""))
        for attr in ("src", "href"):
            if attr in a:
                self._check_link(a[attr])

    def _check_link(self, link):
        if not link.startswith("/"):
            return
        pathname = unquote(urlsplit(link).path)
        local = ROOT / (pathname.lstrip("/") + "index.html" if pathname.endswith("/") else pathname.lstrip("/"))
        if not local.is_file():
            ERRORS.append(f"Link interno não localizado: {link} => {local}")

    def handle_data(self, data):
        if self._in_title:
            self.titles.append(data)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

for local, path in zip(FILES, PATHS):
    if not local.is_file():
        ERRORS.append(f"Página inexistente: {local}")
        continue
    content = local.read_text(encoding="utf-8")
    p = Document()
    p.feed(content)
    if p.canonicals != [DOMAIN + path]:
        ERRORS.append(f"Canonical incoerente: {local} -> {p.canonicals}")
    if p.headings != 1 or not p.description or not p.titles:
        ERRORS.append(f"SEO sem título, descrição ou H1 único: {local}")
    if "lang=\"pt-BR\"" not in content or "application/ld+json" not in content:
        ERRORS.append(f"Idioma/JSON-LD ausente: {local}")
    if "site-footer" not in content or "/mapa-do-site/" not in content:
        ERRORS.append(f"Rodapé ou mapa do site ausente: {local}")
    for anchor in p.buttons:
        if not anchor.startswith("https://wa.me/551121105473"):
            ERRORS.append(f"CTA não encaminha ao WhatsApp oficial: {local}: {anchor}")
    for photo in p.images:
        if not photo.get("alt", "").strip() or not photo.get("width") or not photo.get("height"):
            ERRORS.append(f"Imagem sem alt ou dimensões: {local}")
    if "images.unsplash.com" in content:
        ERRORS.append(f"Imagem de banco remanescente: {local}")

for f in STATIC:
    if not f.is_file() or not f.stat().st_size:
        ERRORS.append(f"Arquivo estrutural ausente/vazio: {f}")

home = (ROOT / "index.html").read_text(encoding="utf-8")
if home.count('class="offer-card"') != 6:
    ERRORS.append("A Home precisa apresentar exatamente 6 cards de produtos")
if (ROOT / "metodologia/index.html").read_text(encoding="utf-8").count("Jornada não é um sétimo produto") != 1:
    ERRORS.append("A Jornada precisa aparecer como metodologia, não produto")

if (ROOT / "sitemap.xml").exists():
    tree = ET.parse(ROOT / "sitemap.xml")
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [node.text for node in tree.findall(".//s:loc", ns)]
    expected = [DOMAIN + p for p in PATHS]
    if set(urls) != set(expected) or len(urls) != len(expected):
        ERRORS.append(f"Sitemap incompleto/duplicado: {len(urls)} urls em vez de {len(expected)}")

if (ROOT / "robots.txt").exists():
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if f"Sitemap: {DOMAIN}/sitemap.xml" not in robots:
        ERRORS.append("robots.txt sem referência ao sitemap exclusivo do ECOAR")

if ERRORS:
    print("\n".join("ERRO: " + e for e in ERRORS), file=sys.stderr)
    raise SystemExit(1)
print(f"ECOAR OK: {len(PATHS)} páginas, 6 produtos, CTAs WhatsApp, rodapé, links internos e sitemap.")
