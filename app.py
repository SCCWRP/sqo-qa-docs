import markdown, glob, os
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_APP_SECRET_KEY')

@app.route('/', strict_slashes=False)
def serve_markdown():
    loe = request.args.get('loe')
    loe = loe if loe else 'menu'
    
    valid_files = [file.split('/')[-1].split('.')[0] for file in glob.glob("docs/*.html")]
    
    if loe not in valid_files:
        flash(f"Line of Evidence {loe} not found")
        loe = 'menu'
        
    # Load the Markdown file
    try:
        with open(f"docs/{loe}.html", "r") as file:
            content = file.read()
        
        # Convert Markdown to HTML
        html_content = markdown.markdown(content)
        
        return render_template('index.jinja2', title=loe, content=html_content)
    
    except FileNotFoundError:
        return "Markdown file not found.", 404

if __name__ == '__main__':
    app.run(debug=True)
