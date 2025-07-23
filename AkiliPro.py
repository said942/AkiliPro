# chatbot_weather_app.py
import pickle, requests, openai

openai.api_key = "WEKA_OPENAI_KEY"
weather_api_key = "WEKA_OWM_KEY"

# Pata data ya sasa kutoka OpenWeatherMap
def pata_hali_hewa_sasa(jiji):
   url = f"http://api.openweathermap.org/data/2.5/weather?q={jiji}&appid={weather_api_key}&units=metric&lang=sw"
    res = requests.get(url).json()
    if res.get("cod") == 200:
        return {
            "temp": res["main"]["temp"],
            "humidity": res["main"]["humidity"],
            "wind": res["wind"]["speed"],
            "desc": res["weather"][0]["description"]
        }
    return None

# Load modeli ya ML
with open("weather_model.pkl", "rb") as f:
    ml_model = pickle.load(f)

def tabiri_ml(temp, humidity, wind):
    X = [[temp, humidity, wind, 0]]  # pressure haijatumika,weka 0
    return ml_model.predict(X)[0]

def chatbot():
    print("Chatbot: Habari! Uliza swali kuhusu hali ya hewa au jambo jingine.")
    while True:
        swali = input("Wewe: ")
        low = swali.lower()
        if "hali ya hewa sasa" in low:
            jiji = swali.replace("hali ya hewa sasa","").strip()
            d = pata_hali_hewa_sasa(jiji)
            if d:
                print(f"Chatbot: Hali ya hewa {jiji}: {d['desc']}, joto ni {d['temp']}°C, unyevu {d['humidity']}%, upepo {d['wind']} m/s.")
            else:
                print("Chatbot: Samahani, sijapata data kwa jiji hilo.")
        elif "tabiri hali ya hewa" in low:
            jiji = swali.replace("tabiri hali ya hewa","").strip()
            d = pata_hali_hewa_sasa(jiji)
            if d:
                ml = tabiri_ml(d['temp'], d['humidity'], d['wind'])
                print(f"Chatbot: Kwa msingi wa data ya sasa ya {jiji}, ninadhani kesho itakuwa: {ml}.")
            else:
                print("Chatbot: Hajaweza kupata data.")
        else:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role":"user","content":swali}]
            )
            print("Chatbot:", resp.choices[0].message.content)

if __name__ == "__main__":
    chatbot()
import React, { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  const sendMessage = async () => {
    const res = await fetch('http://localhost:5000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });

    const data = await res.json();
    setResponse(data.response);
  };

  return (
    <div className="App">
      <h1>Chatbot AI</h1>
      <input
        type="text"
        value={message}
        placeholder="Andika ujumbe..."
        onChange={(e) => setMessage(e.target.value)}
      />
      <button onClick={sendMessage}>Tuma</button>
      <p><strong>Jibu:</strong> {response}</p>
    </div>
  );
}

export default App;
.App {
  text-align: center;
  margin-top: 50px;
  font-family: sans-serif;
}

input {
  padding: 10px;
  width: 300px;
  margin-right: 10px;
}

button {
  padding: 10px 20px;
}

p {
  margin-top: 20px;
  font-size: 18px;
}
my_ai_project/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── chatbot/
│       └── chatbot.py
└── chatbot-frontend/
    └── (React files: App.js, App.css, etc.)
import openai

openai.api_key = "Weka_Hapa_API_KEY_YAKO"  # badilisha na key yako

def get_response(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Wewe ni msaidizi wa kirafiki"},
            {"role": "user", "content": message}
        ]
    )
    return response['choices'][0]['message']['content']
from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot.chatbot import get_response

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    response = get_response(user_message)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
npx create-react-app chatbot-frontend
cd chatbot-frontend
import React, { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  const sendMessage = async () => {
    const res = await fetch('http://localhost:5000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });

    const data = await res.json();
    setResponse(data.response);
  };

  return (
    <div className="App">
      <h1>Chatbot AI</h1>
      <input
        type="text"
        value={message}
        placeholder="Andika ujumbe..."
        onChange={(e) => setMessage(e.target.value)}
      />
      <button onClick={sendMessage}>Tuma</button>
      <p><strong>Jibu:</strong> {response}</p>
    </div>
  );
}

export default App;
.App {
  text-align: center;
  margin-top: 50px;
  font-family: sans-serif;
}

input {
  padding: 10px;
  width: 300px;
  margin-right: 10px;
}

button {
  padding: 10px 20px;
  cursor: pointer;
}

p {
  margin-top: 20px;
  font-size: 18px;
}
cd backend
pip install -r requirements.txt
python app.py
cd chatbot-frontend
npm start
scikit-learn
pandas
pip install -r requirements.txt
import pandas as pd
from sklearn.linear_model import LinearRegression

# Sample data: ukubwa wa bidhaa/nyumba na bei
data = {
    'size': [100, 150, 200, 250, 300],  # ukubwa
    'price': [1000, 1500, 2000, 2500, 3000]  # bei
}

df = pd.DataFrame(data)

model = LinearRegression()
model.fit(df[['size']], df['price'])

def predict_price(size):
    prediction = model.predict([[size]])[0]
    return round(prediction, 2)
from flask import Flask, request, jsonify
from flask_cors import CORS

from chatbot.chatbot import get_response
from prediction.predictor import predict_price

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    response = get_response(user_message)
    return jsonify({"response": response})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    size = data.get("size")
    price = predict_price(size)
    return jsonify({"predicted_price": price})

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS

from chatbot.chatbot import get_response
from prediction.predictor import predict_price

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    response = get_response(user_message)
    return jsonify({"response": response})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    size = data.get("size")
    price = predict_price(size)
    return jsonify({"predicted_price": price})

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS

from chatbot.chatbot import get_response
from prediction.predictor import predict_price

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    response = get_response(user_message)
    return jsonify({"response": response})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    size = data.get("size")
    price = predict_price(size)
    return jsonify({"predicted_price": price})

if __name__ == '__main__':
    app.run(debug=True)
import React, { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  const [size, setSize] = useState('');
  const [predictedPrice, setPredictedPrice] = useState(null);

  const sendMessage = async () => {
    const res = await fetch('http://localhost:5000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });

    const data = await res.json();
    setResponse(data.response);
  };

  const predictPrice = async () => {
    const res = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ size: parseFloat(size) })
    });

    const data = await res.json();
    setPredictedPrice(data.predicted_price);
  };

  return (
    <div className="App">
      <h1>Chatbot AI</h1>
      <input
        type="text"
        value={message}
        placeholder="Andika ujumbe..."
        onChange={(e) => setMessage(e.target.value)}
      />
      <button onClick={sendMessage}>Tuma</button>
      <p><strong>Jibu:</strong> {response}</p>

      <hr />

      <h2>Prediction: Bei kwa Ukubwa</h2>
      <input
        type="number"
        value={size}
        placeholder="Weka ukubwa (mfano 200)"
        onChange={(e) => setSize(e.target.value)}
      />
      <button onClick={predictPrice}>Tabiri Bei</button>
      {predictedPrice !== null && (
        <p><strong>Bei inayotabiriwa:</strong> ${predictedPrice}</p>
      )}
    </div>
  );
}

export default App;
import React, { useState } from 'react';

export default function Auth({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isSignup, setIsSignup] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = async () => {
    const route = isSignup ? 'signup' : 'login';
    const res = await fetch(`http://localhost:5000/${route}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    const data = await res.json();
    if (res.ok) {
      setMessage(data.message);
      onLogin(username); // keep track of who is logged in
    } else {
      setMessage(data.error);
    }
  };

  return (
    <div>
      <h2>{isSignup ? "Signup" : "Login"}</h2>
      <input value={username} placeholder="Username" onChange={e => setUsername(e.target.value)} />
      <input type="password" value={password} placeholder="Password" onChange={e => setPassword(e.target.value)} />
      <button onClick={handleSubmit}>{isSignup ? "Register" : "Login"}</button>
      <p>{message}</p>
      <button onClick={() => setIsSignup(!isSignup)}>
        {isSignup ? "Have an account? Login" : "New user? Signup"}
      </button>
    </div>
  );
}
from flask import Flask, request, jsonify
from flask_cors import CORS
from users.auth import auth_bp, db
from chatbot.chatbot import get_response
from prediction.predictor import predict_price

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    response = get_response(user_message)
    return jsonify({"response": response})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    size = data.get("size")
    price = predict_price(size)
    return jsonify({"predicted_price": price})

if __name__ == '__main__':
    app.run(debug=True)
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from users.auth import auth_bp, db
from chatbot.chatbot import get_response
from prediction.predictor import predict_price
from image_recognition.detector import detect_image

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp)

# Existing endpoints...

@app.route('/image-recognition', methods=['POST'])
def recognize_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    img_file = request.files['image']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], img_file.filename)
    img_file.save(filepath)

    result = detect_image(filepath)
    os.remove(filepath)  # clear after processing
    return jsonify(result)
import ImageUpload from './ImageUpload';

...

return (
  <div className="App">
    {/* Existing login + chatbot + prediction UI */}

    <hr />
    <ImageUpload />
  </div>
);
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from users.auth import auth_bp, db
from chatbot.chatbot import get_response
from prediction.predictor import predict_price
from image_recognition.detector import detect_image

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp)

# Existing endpoints...

@app.route('/image-recognition', methods=['POST'])
def recognize_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    img_file = request.files['image']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], img_file.filename)
    img_file.save(filepath)

    result = detect_image(filepath)
    os.remove(filepath)  # clear after processing
    return jsonify(result)
