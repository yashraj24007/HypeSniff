# HypeSniff 👟

A comprehensive data analysis and visualization project for StockX sneaker resale market data. HypeSniff analyzes pricing trends, brand performance, regional buyer behavior, and profitability metrics in the sneaker resale market.

## 📊 Project Overview

HypeSniff is a Flask-based web application that executes and displays interactive Jupyter notebook analyses of sneaker resale data from StockX. The project provides insights into:

- **Price Analysis**: Retail vs. resale price comparisons
- **Brand Performance**: Analysis of top sneaker brands (Nike, Adidas, Yeezy, etc.)
- **Profit Margins**: Profitability analysis across different sneaker models
- **Regional Trends**: Buyer behavior across different US regions
- **Time Series Analysis**: Sales patterns over time
- **Market Demand**: Price ratios and date differentials

## 🚀 Features

- **Interactive Visualizations**: Rich charts and graphs using Matplotlib, Seaborn, and Plotly
- **Real-time Analysis**: Flask app that dynamically executes and renders Jupyter notebooks
- **Data Processing**: Comprehensive data cleaning and feature engineering
- **Statistical Insights**: Descriptive statistics and trend analysis
- **Responsive Web Interface**: HTML export of notebook analysis

## 📁 Project Structure

```
HypeSniff/
├── app.py                          # Flask application server
├── DAV_project_1_v1.ipynb         # Initial analysis notebook
├── DAV_project_1_v2.ipynb         # Enhanced analysis notebook
├── StockX_initial.csv             # Raw StockX dataset
├── processed_sneakers.csv         # Cleaned and processed data
├── requirements.txt               # Python dependencies
├── Procfile                       # Deployment configuration
├── last_render_500.html           # Rendered notebook output
└── README.md                      # Project documentation
```

## 🛠️ Technologies Used

- **Python 3.x**
- **Flask** - Web framework
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Matplotlib** - Static visualizations
- **Seaborn** - Statistical visualizations
- **Plotly** - Interactive visualizations
- **Jupyter Notebook** - Analysis environment
- **nbformat/nbclient/nbconvert** - Notebook execution and conversion

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yashraj24007/HypeSniff.git
   cd HypeSniff
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

### Running the Flask App

```bash
python app.py
```

The application will start on `http://localhost:5000` and display the full analysis.

### Running with Gunicorn (Production)

```bash
gunicorn app:app
```

### Analyzing the Data Locally

Open the Jupyter notebooks directly:

```bash
jupyter notebook DAV_project_1_v2.ipynb
```

## 📈 Dataset

The project uses StockX sneaker resale data containing:

- **99,956 transactions**
- **8 core features**:
  - Order Date
  - Brand
  - Sneaker Name
  - Sale Price
  - Retail Price
  - Release Date
  - Shoe Size
  - Buyer Region

### Engineered Features

- `order_month` - Month of transaction
- `order_year` - Year of transaction
- `profit` - Difference between sale and retail price
- `date_diff` - Days between release and sale
- `price_ratio` - Sale price to retail price ratio

## 🔍 Key Insights

The analysis reveals:

- Price premiums in the resale market
- Brand-specific demand patterns
- Regional buyer preferences
- Temporal trends in sneaker sales
- Correlation between release date and resale value

## 🚢 Deployment

The project includes a `Procfile` for easy deployment to platforms like Heroku:

```
web: gunicorn app:app
```

## 📝 Requirements

See `requirements.txt` for full dependency list. Key packages:

- flask >= 2.0
- pandas >= 1.0
- numpy >= 1.18
- plotly >= 4.0
- nbformat >= 5.0
- nbclient >= 0.5
- nbconvert >= 6.0

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available for educational and research purposes.

## 👨‍💻 Author

**Yashraj**
- GitHub: [@yashraj24007](https://github.com/yashraj24007)

## 🙏 Acknowledgments

- StockX for providing the dataset
- Data Analytics and Visualization community

---

**HypeSniff** - *Sniffing out the hype in sneaker resale data* 👟📊
