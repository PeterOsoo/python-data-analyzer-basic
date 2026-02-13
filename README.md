# Data Analyzer App

A Python application for data analysts to quickly load, clean, analyze, and visualize datasets.

## Features

- 📊 **Load Data**: Import CSV and Excel files
- 🧹 **Data Cleaning**: Remove duplicates and handle missing values
- 📈 **Statistics**: Get descriptive statistics and distributions
- 📉 **Visualizations**: Generate charts including histograms, bar charts, correlation heatmaps, and scatter plots
- 📄 **Reports**: Export analysis reports to text files
- 🎲 **Sample Data**: Built-in sample dataset for testing

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python data_analyzer.py
```

Then follow the interactive menu:
1. Load your own CSV/Excel file
2. Or use the sample dataset to explore features
3. View overview and statistics
4. Clean your data
5. Generate visualizations
6. Export reports

## Quick Example

```python
from data_analyzer import DataAnalyzer

# Create analyzer instance
analyzer = DataAnalyzer()

# Load data
analyzer.load_data('your_data.csv')

# Show overview
analyzer.show_overview()

# Clean data
analyzer.clean_data()

# Generate visualizations
analyzer.create_visualizations()

# Export report
analyzer.export_report()
```

## Output Files

- `analysis_dashboard.png` - Visual dashboard with 4 charts
- `analysis_report.txt` - Text summary of your analysis

## Requirements

- Python 3.7+
- pandas
- matplotlib
- seaborn
- openpyxl (for Excel support)
