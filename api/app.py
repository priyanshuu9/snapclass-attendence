import os
from flask import Flask, render_template

current_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(current_dir, "../templates"),
    static_folder=os.path.join(current_dir, "../static")
)

@app.route('/')
def home():
    # Retrieve the Streamlit app URL from environment or default to localhost:8501
    streamlit_url = os.environ.get('STREAMLIT_URL', 'http://localhost:8501')
    return render_template('index.html', streamlit_url=streamlit_url)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
