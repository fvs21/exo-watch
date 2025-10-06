# 🪐 exo-watch

[![Python](https://img.shields.io/badge/Python-41%25-blue?logo=python)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-34.6%25-blueviolet?logo=typescript)](https://www.typescriptlang.org/)
[![CSS](https://img.shields.io/badge/CSS-22.9%25-ff69b4?logo=css3)](https://developer.mozilla.org/docs/Web/CSS)

---

exo-watch is an interactive web workbench for exoplanet classification, built for the NASA Space Apps Challenge 2025. This tool allows you to train, compare, and fine-tune state-of-the-art machine learning models in real-time, using the official Kepler Objects of Interest (KOI) dataset.

## 🚀 Core Features

- Model Workbench: Don't settle for a single approach. Directly train and compare the performance of LightGBM, XGBoost, and Random Forest on the same dataset.

- Interactive Hyperparameter Tuning: Modify key model parameters (like learning_rate, n_estimators, max_depth) and instantly observe how they impact accuracy and performance.

- "What-If" Candidate Analysis: Manually input the features of a planetary candidate—real or hypothetical—and receive an instant classification from each of the trained models.

- Feature Insight: Analyze which planetary and stellar features (such as koi_depth, koi_impact, koi_srad) are the most decisive for each model through dynamic feature importance charts.

## 🎯 Who is exo-watch for?

- exo-watch is designed for technical users who want to explore the intersection of astronomy and artificial intelligence.

- Data Scientists & AI Enthusiasts: Experiment with model architectures and tune hyperparameters on a fascinating and complex real-world problem.

- Researchers & Astronomy Students: Gain a deeper intuition for which physical parameters are most predictive in distinguishing real planets from false positives.

- Advanced Educators: Use the tool to provide hands-on instruction in the concepts of training, evaluating, and comparing applied machine learning models.

## 🛠️ Tech Stack

| Language      | Role                                      |
|---------------|-------------------------------------------|
| **Python**    | AI models, backend logic                  |
| **TypeScript**| Interactive frontend, UI components       |
| **CSS**       | Beautiful, responsive layouts             |
| **Other**     | Supporting scripts and assets             |

---

## ⚡ Quickstart

### Prerequisites

- Python 3.8+
- Node.js & npm

### Installation

```bash
# Clone the repository
git clone https://github.com/fvs21/exo-watch.git
cd exo-watch

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install
```

### Run the App

```bash
# Start the backend
cd backend
uvicorn app.main:app --reload

#Open another terminal
#Go to frontend folder
cd frontend

# Launch the frontend (TypeScript)
npm run build
npm start
```
---

## 📝 License

MIT License. See [LICENSE](LICENSE) for details.

