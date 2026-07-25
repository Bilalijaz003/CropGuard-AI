# 🌱 CropGuard AI

### AI-Powered Crop Health Detection System

--- Press CNtrl+shift+v to open markdown preview.

## 📌 What is CropGuard AI?

CropGuard AI is a web-based application that uses Artificial Intelligence (AI) to detect diseases in crop plants. Farmers can upload a photo of a wheat or sugarcane leaf, and the system instantly analyzes the image to determine whether the crop is healthy or diseased. If a disease is detected, the system also provides practical farming advice to help farmers take the appropriate action.

---

## 🚜 The Problem It Solves

Crop diseases are one of the biggest causes of agricultural loss. Farmers, especially those in rural areas, often cannot afford agricultural experts or laboratory testing. As a result, diseases are usually detected too late, leading to significant crop damage and financial loss.

CropGuard AI solves this problem by providing a simple AI-powered tool that allows farmers to check crop health by uploading a leaf image. The AI analyzes the image within seconds and provides the disease name, confidence score, and recommended farming advice.

### Benefits

- Detect diseases before they spread
- Reduce crop loss and financial damage
- Avoid unnecessary pesticide use
- Make faster and better farming decisions

> CropGuard AI is designed for farmers, agricultural students, and field workers who need quick and reliable crop health information without technical complexity.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 AI Disease Detection | Detects crop diseases from uploaded leaf images |
| 🌾 Crop Support | Supports Wheat and Sugarcane |
| 🔍 Six-Class Classification | Detects six different crop conditions |
| 📋 Disease Status | Displays healthy or disease name |
| 📊 Confidence Score | Shows AI prediction confidence |
| 💡 Farming Advice | Provides advice for diseased crops |
| 🖼️ Image Preview | Preview uploaded image before analysis |
| 🌿 Crop Selection | Choose Wheat or Sugarcane |
| 📈 Dashboard | Displays total scans, healthy and diseased crops |
| 📉 Statistics Chart | Visual chart showing healthy vs diseased ratio |
| 📋 Scan History | Stores crop, prediction, confidence and date |
| 🕒 Recent Activity | Shows the last five scans |
| 💾 Local Storage | Saves scan history in the browser |
| 📱 Responsive Design | Works on desktop, tablet and mobile |
| 😊 User Friendly | Simple interface requiring no technical knowledge |

---

## 🤖 AI Feature

The AI model is the core component of CropGuard AI. It analyzes uploaded crop leaf images and classifies them into one of six possible classes.

### How It Works

1. Upload a crop leaf image.
2. Select the crop type.
3. The image is sent to the Flask backend.
4. The backend preprocesses the image.
5. The trained AI model predicts the crop condition.
6. The prediction, confidence score, and farming advice are displayed.

> **Note:** The AI model is trained only on Wheat and Sugarcane images. Images of other crops or objects may produce inaccurate results.

---

## 🧠 AI Model

The AI model uses **MobileNetV2** as the base architecture with **Transfer Learning**. MobileNetV2 is lightweight, fast, and highly suitable for image classification tasks.

### Model Information

| Detail | Information |
|---------|-------------|
| Model Name | CropGuardAI_Model |
| Model Format | `.keras` |
| Base Model | MobileNetV2 |
| Framework | TensorFlow / Keras |
| Training Images | 600 |
| Total Classes | 6 |
| Input Image Size | 224 × 224 pixels |

---

## 🌾 Supported Classes

### Wheat

- Wheat Healthy
- Wheat Brown Rust
- Wheat Yellow Rust

### Sugarcane

- Healthy
- Bacterial Blight
- Red Rot

---

## 📄 Prediction Result

The prediction page displays:

| Field | Description |
|---------|-------------|
| Crop | Selected crop |
| Status | Healthy or disease detected |
| Confidence | AI confidence percentage |
| Advice | Recommended farming advice |

---

## 🛠️ Technology Stack

### Frontend

- HTML5
- CSS3
- JavaScript

### Backend

- Python
- Flask

### AI & Machine Learning

- TensorFlow
- Keras
- MobileNetV2

### Other Libraries

- NumPy
- Pillow

---

## 📁 Project Structure

```text
cropguard-ai/
│
├── index.html
├── detection.html
├── dashboard.html
├── features.html
│
├── css/
│   └── style.css
│
├── js/
│   └── script.js
│
├── assets/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── CropGuardAI_Model.keras
│       
│
└── README.md
```

---

## 🚀 How to Run the Project

### Requirements

- Python 3.11 or updated
- pip
- Modern web browser (Chrome, Firefox, Edge)
- CropGuardAI_Model.keras

---

### Step 1 – Download the Project

Download or clone the project to your computer.

---

### Step 2 – Place the Model

Copy the model file into:

```text
backend/model/CropGuardAI_Model.keras
```

---

### Step 3 – Open Terminal

Navigate to the backend folder.

```bash
cd path/to/cropguard-ai/backend
```

---

### Step 4 – Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:

- Flask
- TensorFlow
- NumPy
- Pillow

---

### Step 5 – Start the Backend

```bash
python app.py
```

If everything is configured correctly, you should see:

```text
CropGuardAI_Model.keras loaded successfully
Running on http://localhost:5000
```

Keep this terminal open while using the application.

---

### Step 6 – Open the Frontend

Open `index.html` in your browser.

You can:

- Double-click the file
- Open it using VS Code Live Server
- Drag it into your browser

---

### Step 7 – Use the Application

1. Open **Detection**.
2. Upload a crop leaf image.
3. Select Wheat or Sugarcane.
4. Click **Analyze Crop**.
5. Wait for the prediction.
6. View the crop status, confidence score, and advice.
7. Open the Dashboard to view scan history and statistics.

---

## ⚠️ Important Note

The Flask backend must be running at:

```text
http://localhost:5000
```

If the backend is not running, the crop detection feature will not work.

---

## 📸 Working Screenshots

### 1: Detecting the Disease

![alt text](<PRoject 1 detecting-1.PNG>)


---

### 🔍 Disease Detection

![alt text](<Project 2 analyzed-1.PNG>)

---

### 📊Dashboard (History)

![alt text](<Project 3 dashboard-1.PNG>)

---

## 🔮 Future Improvements

- Support more crop species
- Real-time camera detection
- Cloud database integration
- User authentication
- Multi-language support
- Mobile application



© 2026 CropGuard AI | AI-Powered Crop Health Detection System