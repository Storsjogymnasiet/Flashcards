import markdown
import re

def create_card_html(title, md_content, output_filename):
    # Dela upp vid '---' och rensa bort tomma kort
    raw_cards = [c.strip() for c in md_content.split('---') if c.strip()]
    cards_html = ""

    for card in raw_cards:
        lines = card.split('\n', 1)
        question_text = lines[0]
        answer_text = lines[1] if len(lines) > 1 else ""
        
        question_html = markdown.markdown(question_text)
        answer_html = markdown.markdown(answer_text)
        
        cards_html += f"""
        <div class="card" onclick="this.classList.toggle('flipped')">
            <div class="card-inner">
                <div class="card-front">{question_html}</div>
                <div class="card-back">{answer_html}</div>
            </div>
        </div>
        """

    full_html = f"""
    <!DOCTYPE html>
    <html lang="sv">
    <head>
        <meta charset="utf-8">
        <title>{title}</title>
        <style>
            body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #f0f2f5; margin: 0; padding: 40px; display: flex; flex-direction: column; align-items: center; }}
            .header-container {{ text-align: center; margin-bottom: 40px; }}
            h1 {{ color: #1a202c; font-size: 2.5rem; }}
            .nav-link {{ margin-bottom: 20px; display: inline-block; color: #3182ce; text-decoration: none; font-weight: bold; }}
            .btn {{ background: #3182ce; color: white; border: none; padding: 12px 24px; font-size: 1rem; border-radius: 8px; cursor: pointer; font-weight: 600; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: 0.2s; }}
            .btn:hover {{ background: #2b6cb0; }}
            #card-container {{ display: flex; flex-wrap: wrap; gap: 25px; justify-content: center; width: 100%; max-width: 1200px; }}
            .card {{ width: 320px; height: 220px; perspective: 1000px; cursor: pointer; }}
            .card-inner {{ position: relative; width: 100%; height: 100%; text-align: center; transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1); transform-style: preserve-3d; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); border-radius: 15px; }}
            .card.flipped .card-inner {{ transform: rotateY(180deg); }}
            .card-front, .card-back {{ position: absolute; width: 100%; height: 100%; backface-visibility: hidden; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 25px; box-sizing: border-box; border-radius: 15px; background: white; border: 1px solid rgba(0,0,0,0.05); }}
            .card-back {{ background: #fffdf0; transform: rotateY(180deg); border-top: 6px solid #ecc94b; }}
            code {{ background: #edf2f7; padding: 2px 6px; border-radius: 4px; font-family: monospace; }}
        </style>
    </head>
    <body>
        <div class="header-container">
            <a href="index.html" class="nav-link">← Tillbaka till menyn</a>
            <h1>{title}</h1>
            <button class="btn" onclick="shuffleCards()">🔀 Blanda korten</button>
        </div>
        <div id="card-container">{cards_html}</div>
        <script>
            function shuffleCards() {{
                const container = document.getElementById('card-container');
                const cards = Array.from(container.getElementsByClassName('card'));
                for (let i = cards.length - 1; i > 0; i--) {{
                    const j = Math.floor(Math.random() * (i + 1));
                    container.appendChild(cards[j]);
                }}
                cards.forEach(card => card.classList.remove('flipped'));
            }}
        </script>
    </body>
    </html>
    """
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(full_html)

def create_index_file(collections):
    links_html = ""
    for name, filename in collections:
        links_html += f'<a href="{filename}" class="menu-item"><h2>{name}</h2><p>Visa flashcards →</p></a>\n'

    index_html = f"""
    <!DOCTYPE html>
    <html lang="sv">
    <head>
        <meta charset="utf-8">
        <title>Flashcards</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; background: #f0f2f5; display: flex; flex-direction: column; align-items: center; padding: 60px 20px; }}
            h1 {{ color: #1a202c; font-size: 3rem; margin-bottom: 40px; }}
            .menu-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; width: 100%; max-width: 900px; }}
            .menu-item {{ background: white; padding: 30px; border-radius: 15px; text-decoration: none; color: inherit; box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: transform 0.2s, box-shadow 0.2s; text-align: center; border: 1px solid rgba(0,0,0,0.05); }}
            .menu-item:hover {{ transform: translateY(-5px); box-shadow: 0 12px 20px rgba(0,0,0,0.1); border-color: #3182ce; }}
            .menu-item h2 {{ margin: 0; color: #2d3748; }}
            .menu-item p {{ color: #718096; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <h1>📚 Kort Samlingar</h1>
        <div class="menu-grid">
            {links_html}
        </div>
    </body>
    </html>
    """
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)

def generate_all(input_md):
    try:
        with open(input_md, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Hittade inte {input_md}")
        return

    chunks = re.split(r'^#\s+(.+)$', content, flags=re.MULTILINE)
    if len(chunks) < 2:
        print("Inga samlingar funna.")
        return

    created_collections = []
    for i in range(1, len(chunks), 2):
        name = chunks[i].strip()
        body = chunks[i+1].strip()
        filename = f"{name.lower().replace(' ', '_')}.html"
        create_card_html(name, body, filename)
        created_collections.append((name, filename))
        print(f"✓ Skapade samling: {filename}")

    create_index_file(created_collections)
    print("✓ Skapade index.html")

if __name__ == "__main__":
    generate_all('cards.md')