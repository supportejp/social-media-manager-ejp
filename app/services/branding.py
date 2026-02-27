def enrich_post_with_branding(text: str) -> str:
    company_name = "EJP GROUP"
    hashtag = "#EJPGroup"
    cta = "Síguenos para más novedades."

    enriched_text = f"""🚀 {text}

En {company_name} seguimos impulsando soluciones Tecnológicas y de Recursos Humanos

{hashtag}

{cta}
"""

    return enriched_text