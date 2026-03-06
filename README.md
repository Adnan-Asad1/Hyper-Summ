# Parallelized Text Summarization using TF-IDF & TextRank

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive text summarization system implementing both **TextRank** and **TF-IDF** algorithms with sequential and parallel processing approaches. The project includes a Jupyter notebook for analysis and a Flask-based web interface for real-time text summarization.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
  - [Web Application](#web-application)
  - [Jupyter Notebook](#jupyter-notebook)
- [Algorithms](#algorithms)
- [Performance Metrics](#performance-metrics)
- [Team](#team)
- [License](#license)

---

## 🎯 Overview

This project is a **PDC (Parallel and Distributed Computing) term project** that explores the effectiveness of parallelization in natural language processing tasks. It implements automated text summarization using two popular algorithms:

1. **TextRank** - Graph-based ranking algorithm
2. **TF-IDF** - Statistical term frequency approach

Each algorithm is implemented in both **sequential** and **parallel** versions to demonstrate performance improvements through multiprocessing.

### Key Objectives

✅ Compare sequential vs. parallel processing performance  
✅ Analyze memory efficiency and CPU utilization  
✅ Demonstrate real-world speedup on multi-core systems  
✅ Provide interactive web interface for text summarization  

---

## ✨ Features

### Core Features

- **Multiple Algorithms**: TextRank and TF-IDF implementations
- **Sequential & Parallel Processing**: Compare performance between approaches
- **Real-time Web UI**: Flask-based interactive interface
- **Comprehensive Analysis**: Jupyter notebook with detailed metrics
- **Performance Visualization**: Charts comparing execution time, memory usage, and compression ratios
- **REST API**: JSON-based API for integration with other applications

### Advanced Features

- **Dynamic Summary Length**: Automatically calculates optimal summary length (30-40% of original)
- **Memory Profiling**: Tracks peak memory usage for both approaches
- **Compression Metrics**: Detailed statistics on text reduction
- **Multi-core Utilization**: Leverages all available CPU cores for parallel processing
- **NLTK Integration**: Professional-grade text preprocessing and tokenization

---

## 📁 Project Structure

```
Parallel-Summarizer-PDC/
│
├── text-summarizer-ui/          # Flask Web Application
│   ├── app.py                   # Main Flask application
│   ├── summarizers.py           # All summarization algorithms
│   ├── requirements.txt         # Python dependencies
│   ├── templates/
│   │   └── index.html          # Web UI template
│   └── static/
│       ├── css/                # Stylesheets
│       └── js/                 # JavaScript files
│
├── project.ipynb               # Main Jupyter notebook with analysis
├── News_Category_Dataset_v3.json  # Dataset (87MB+ news articles)
├── enhanced_articles.json      # Processed dataset
│
├── Performance Visualizations:
│   ├── performance_comparison.png
│   ├── tfidf_performance_comparison.png
│   ├── textrank_performance_comparison.png
│   ├── cross_technique_comparison.png
│   └── per_article_metrics.png
│
├── Utility Scripts:
│   ├── add_textrank.py         # TextRank implementation helper
│   ├── add_summary_display.py  # Summary display enhancement
│   ├── create_enhanced_dataset.py
│   ├── fix_tfidf_par.py
│   └── optimize_parallel.py
│
├── Documentation:
│   ├── README.md               # This file
│   ├── SUMMARY_DISPLAY_README.md
│   ├── project_report.txt      # Performance analysis report
│   └── Parallelized Text Sumarization PDC Term Project Proposel (1).docx
│
└── .gitignore
```

---

## 🛠️ Technologies Used

### Backend & Core

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Primary programming language |
| **Flask 3.0.0** | Web framework for UI |
| **scikit-learn** | TF-IDF vectorization |
| **NLTK 3.8.1** | Text tokenization and preprocessing |
| **NetworkX 3.2.1** | Graph algorithms for TextRank |
| **multiprocessing** | Parallel execution |

### Data Processing & Analysis

| Technology | Purpose |
|------------|---------|
| **pandas** | Data manipulation |
| **numpy** | Numerical computations |
| **psutil** | Performance monitoring |

### Visualization

| Technology | Purpose |
|------------|---------|
| **matplotlib** | Chart generation |
| **seaborn** | Statistical visualizations |

### Frontend

| Technology | Purpose |
|------------|---------|
| **HTML5/CSS3** | Web interface |
| **JavaScript** | Client-side interactivity |
| **Flask-CORS** | Cross-origin resource sharing |

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/Adnan-Asad1/Hyper-Summ.git
cd Hyper-Summ
```

### Step 2: Install Dependencies

#### For Web Application

```bash
cd text-summarizer-ui
pip install -r requirements.txt
```

#### For Jupyter Notebook

```bash
pip install jupyter notebook
pip install scikit-learn nltk networkx numpy pandas matplotlib seaborn psutil
```

### Step 3: Download NLTK Data

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

---

## 🚀 Usage

### Web Application

#### Start the Flask Server

```bash
cd text-summarizer-ui
python app.py
```

The application will start at `http://localhost:5000`

#### Web UI Features

1. **Text Input**: Paste or type your article text
2. **Algorithm Selection**: Choose from 4 options:
   - TextRank Sequential
   - TextRank Parallel
   - TF-IDF Sequential
   - TF-IDF Parallel
3. **Generate Summary**: Click to process
4. **View Results**: See summary with metrics:
   - Execution time
   - Compression ratio
   - Memory usage
   - Word counts

#### REST API Endpoint

**POST** `/summarize`

```json
{
  "text": "Your article text here...",
  "algorithm": "textrank_par"
}
```

**Response:**

```json
{
  "success": true,
  "summary": "Generated summary...",
  "metrics": {
    "execution_time": 0.0045,
    "compression_ratio": 65.5,
    "memory_used_mb": 12.3,
    "num_sentences": 15,
    "summary_sentences": 5
  }
}
```

### Jupyter Notebook

#### Launch Notebook

```bash
jupyter notebook project.ipynb
```

#### Notebook Sections

1. **Setup & Installation** - Install required libraries
2. **Import Libraries** - Load all dependencies
3. **Dataset Preparation** - Load CNN/Daily Mail news dataset
4. **TextRank Implementation**
   - Sequential approach
   - Parallel approach
   - Performance comparison
   - Sample summaries
5. **TF-IDF Implementation**
   - Sequential approach
   - Parallel approach
   - Performance comparison
   - Sample summaries
6. **Cross-Technique Comparison** - Compare all 4 approaches
7. **Visualizations** - Performance charts and metrics

---

## 🧮 Algorithms

### TextRank Algorithm

**How it works:**
1. Tokenize text into sentences
2. Build similarity graph between sentences
3. Apply PageRank algorithm to rank sentences
4. Extract top-ranked sentences as summary

**Advantages:**
- Graph-based, considers sentence relationships
- Language-independent
- No training required

### TF-IDF Algorithm

**How it works:**
1. Calculate term frequency for each word
2. Calculate inverse document frequency
3. Score sentences based on TF-IDF weights
4. Select highest-scoring sentences

**Advantages:**
- Fast and efficient
- Statistically sound
- Works well for keyword extraction

### Parallelization Strategy

Both algorithms use **multiprocessing** to:
- Split text into chunks
- Process chunks on separate CPU cores
- Aggregate results efficiently
- Achieve significant speedup on multi-core systems

---

## 📊 Performance Metrics

### Sample Results (from project_report.txt)

#### TF-IDF Performance

| Metric | Sequential | Parallel | Improvement |
|--------|-----------|----------|-------------|
| Execution Time | 0.0058s | 0.0033s | **42.31%** |
| Speedup Factor | 1.0x | **1.73x** | - |
| Parallel Efficiency | - | 43.33% | - |
| CPU Cores Used | 1 | 4 | - |

### Key Findings

✅ **1.73x speedup** achieved with parallel processing  
✅ **43.33% parallel efficiency** on 4-core system  
✅ Minimal memory overhead with multiprocessing  
✅ Similar compression ratios for both approaches  
✅ Performance gains increase with document size  

### Recommendations

- **Small documents (<1000 words)**: Use sequential for lower overhead
- **Large datasets**: Use parallel for better CPU utilization
- **Production systems**: Implement hybrid approach based on document size

---

## 👥 Team

**Team Members:**
- Adnan Asad
- Shiraz Nadeem
- Abdul Rehman

**Course:** Parallel and Distributed Computing (PDC)  
**Institution:** [Your Institution Name]

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 🙏 Acknowledgments

- CNN/Daily Mail dataset for news articles
- NLTK project for natural language processing tools
- scikit-learn for machine learning utilities
- NetworkX for graph algorithms

---

## 📧 Contact

For questions or suggestions, please open an issue or contact the team members.

---

## 🔗 Links

- **GitHub Repository**: [Adnan-Asad1/Hyper-Summ](https://github.com/Adnan-Asad1/Hyper-Summ)
- **Documentation**: See `SUMMARY_DISPLAY_README.md` for display enhancement details
- **Performance Report**: See `project_report.txt` for detailed analysis

---

**⭐ Star this repository if you find it helpful!**
