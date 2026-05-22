# 🚗 ValuDrive - Car Price Prediction System

ValuDrive is a Machine Learning based web application that predicts the resale value of cars using historical vehicle data. The project combines a trained regression model with a Flask web application to provide real-time price predictions through a clean and responsive interface.

---

## ✨ Features

- Predicts vehicle resale prices using Machine Learning
- Multiple regression models evaluated automatically
- Responsive and modern user interface
- Real-time predictions without page reload
- Data preprocessing with scaling and encoding
- Flask backend integration
- Structured and modular project architecture

---

## 🧠 Machine Learning Models Used

The system evaluates multiple regression algorithms to determine the best-performing model:

- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor
- Gradient Boosting Regressor

The best-performing trained model is automatically saved as:

```bash
car_price_model.pkl
```

---

## 📂 Project Structure

```plaintext
car-price-prediction/
│
├── model/
│   ├── train_model.py
│   └── car_price_model.pkl
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
├── templates/
│   ├── index.html
│   └── predict.html
│
├── app.py
├── requirements.txt
├── dataset.csv
└── README.md
```

---

## 🛠️ Technologies Used

- Python
- Flask
- Scikit-learn
- Pandas
- NumPy
- HTML5
- CSS3
- JavaScript

---

## ⚙️ Installation Guide

### 1. Clone the Repository

```bash
git clone <https://github.com/aqsaalirazajamali/car-price-prediction>
cd car-price-prediction
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Train the Machine Learning Model

```bash
python model/train_model.py
```

### 4. Run the Flask Application

```bash
python app.py
```

Open your browser and visit:

```plaintext
http://127.0.0.1:5000/
```

---

## 📊 Prediction Parameters

The model predicts vehicle prices using the following features:

- Vehicle Brand
- Manufacturing Year
- Fuel Type
- Transmission Type
- Kilometers Driven
- Seller Type
- Ownership History
- Showroom Price

---

## 👩‍💻 Author

Aqsa Jamali
