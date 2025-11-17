
from flask import Flask, request, render_template, jsonify, g
import joblib, sqlite3, os, logging
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'feedback.db')

app = Flask(__name__)
model = joblib.load(os.path.join(BASE_DIR, 'model.pkl'))
vectorizer = joblib.load(os.path.join(BASE_DIR, 'vectorizer.pkl'))

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('spam_detector')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
    return db

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            predicted INTEGER,
            actual INTEGER,
            prob REAL,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'no text provided'}), 400
    vec = vectorizer.transform([text])
    prob = model.predict_proba(vec)[0][1] if hasattr(model, 'predict_proba') else None
    pred = int(model.predict(vec)[0])
    logger.info(f'Prediction made: pred={pred}, prob={prob}')
    return jsonify({'prediction': int(pred), 'probability': float(prob) if prob is not None else None})

@app.route('/ui_predict', methods=['POST'])
def ui_predict():
    text = request.form.get('message', '')
    vec = vectorizer.transform([text])
    prob = model.predict_proba(vec)[0][1] if hasattr(model, 'predict_proba') else None
    pred = int(model.predict(vec)[0])
    return render_template('index.html', prediction=('Spam' if pred==1 else 'Not Spam'), probability=prob, message=text)

@app.route('/feedback', methods=['POST'])
def feedback():
    payload = request.get_json(force=True)
    text = payload.get('text')
    predicted = payload.get('predicted')
    actual = payload.get('actual')
    prob = payload.get('prob')
    created_at = datetime.utcnow().isoformat()
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO feedback (text, predicted, actual, prob, created_at) VALUES (?,?,?,?,?)',
              (text, predicted, actual, prob, created_at))
    conn.commit()
    return jsonify({'status': 'ok'}), 201

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
