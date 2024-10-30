import markdown, glob, os
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_APP_SECRET_KEY')

# Remove bogus query string arguments
@app.before_request
def clean_url():
    if request.args:
        if request.args.get('page') is None:
            return redirect(url_for(request.endpoint, **request.view_args), code=301)
        

@app.route('/<pagename>', strict_slashes=False)
@app.route('/', strict_slashes=False)
def serve_markdown(pagename="menu"):
    
    valid_files = [file.split('/')[-1].split('.')[0] for file in glob.glob("docs/*.html")]
    
    if pagename not in valid_files:
        flash(f"The page {pagename} was not found!")
        return redirect(url_for('serve_markdown'))
        
    # Load the Markdown file
    try:
        with open(f"docs/{pagename}.html", "r") as file:
            content = file.read()
        
        # Convert Markdown to HTML
        html_content = markdown.markdown(content)
        
        return render_template('index.jinja2', title=pagename, content=html_content)
    
    except FileNotFoundError:
        return "Markdown file not found.", 404

if __name__ == '__main__':
    app.run(debug=True)
