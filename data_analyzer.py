"""
Interactive Data Analyzer App
A basic Python application for data analysts to load, clean, analyze, and visualize datasets.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

class DataAnalyzer:
    def __init__(self):
        self.df = None
        self.filename = None
        sns.set_style("whitegrid")
        
    def load_data(self, filepath):
        """Load CSV or Excel file"""
        try:
            file_ext = Path(filepath).suffix.lower()
            if file_ext == '.csv':
                self.df = pd.read_csv(filepath)
            elif file_ext in ['.xlsx', '.xls']:
                self.df = pd.read_excel(filepath)
            else:
                print(f"Unsupported file type: {file_ext}")
                return False
            
            self.filename = Path(filepath).name
            print(f"✓ Successfully loaded {self.filename}")
            print(f"  Shape: {self.df.shape[0]} rows × {self.df.shape[1]} columns\n")
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False
    
    def create_sample_data(self):
        """Create sample sales dataset for demonstration"""
        import numpy as np
        np.random.seed(42)
        
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        regions = np.random.choice(['North', 'South', 'East', 'West'], 100)
        products = np.random.choice(['Product A', 'Product B', 'Product C'], 100)
        sales = np.random.randint(1000, 10000, 100)
        units = np.random.randint(10, 100, 100)
        
        self.df = pd.DataFrame({
            'Date': dates,
            'Region': regions,
            'Product': products,
            'Sales': sales,
            'Units': units,
            'Price': (sales / units).round(2)
        })
        
        self.filename = "sample_sales_data.csv"
        print("✓ Sample dataset created (100 rows × 6 columns)\n")
        return True
    
    def show_overview(self):
        """Display dataset overview"""
        if self.df is None:
            print("No data loaded. Please load a file first.")
            return
        
        print("=" * 60)
        print("DATASET OVERVIEW")
        print("=" * 60)
        print(f"\nFile: {self.filename}")
        print(f"Rows: {self.df.shape[0]} | Columns: {self.df.shape[1]}")
        
        print("\n--- Column Information ---")
        print(self.df.dtypes.to_string())
        
        print("\n--- First 5 Rows ---")
        print(self.df.head().to_string())
        
        print("\n--- Missing Values ---")
        missing = self.df.isnull().sum()
        if missing.sum() > 0:
            print(missing[missing > 0].to_string())
        else:
            print("No missing values found ✓")
        print()
    
    def show_statistics(self):
        """Display statistical summary"""
        if self.df is None:
            print("No data loaded.")
            return
        
        print("=" * 60)
        print("STATISTICAL SUMMARY")
        print("=" * 60)
        
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            print("\n--- Numeric Columns ---")
            print(self.df[numeric_cols].describe().to_string())
        
        categorical_cols = self.df.select_dtypes(include=['object', 'category', 'str']).columns
        if len(categorical_cols) > 0:
            print("\n--- Categorical Columns ---")
            for col in categorical_cols:
                print(f"\n{col}:")
                print(self.df[col].value_counts().head().to_string())
        print()
    
    def clean_data(self):
        """Basic data cleaning operations"""
        if self.df is None:
            print("No data loaded.")
            return
        
        print("=" * 60)
        print("DATA CLEANING")
        print("=" * 60)
        
        initial_rows = len(self.df)
        
        # Remove duplicates
        duplicates = self.df.duplicated().sum()
        if duplicates > 0:
            self.df = self.df.drop_duplicates()
            print(f"✓ Removed {duplicates} duplicate rows")
        else:
            print("✓ No duplicate rows found")
        
        # Handle missing values
        missing = self.df.isnull().sum().sum()
        if missing > 0:
            # Fill numeric columns with median
            numeric_cols = self.df.select_dtypes(include=['number']).columns
            for col in numeric_cols:
                if self.df[col].isnull().sum() > 0:
                    self.df[col].fillna(self.df[col].median(), inplace=True)
            
            # Fill categorical with mode
            categorical_cols = self.df.select_dtypes(include=['object', 'str']).columns
            for col in categorical_cols:
                if self.df[col].isnull().sum() > 0:
                    self.df[col].fillna(self.df[col].mode()[0], inplace=True)
            
            print(f"✓ Filled {missing} missing values")
        else:
            print("✓ No missing values found")
        
        final_rows = len(self.df)
        print(f"\nRows before: {initial_rows} | Rows after: {final_rows}")
        print()
    
    def create_visualizations(self):
        """Generate common data visualizations"""
        if self.df is None:
            print("No data loaded.")
            return
        
        print("=" * 60)
        print("CREATING VISUALIZATIONS")
        print("=" * 60)
        
        numeric_cols = self.df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = self.df.select_dtypes(include=['object', 'category', 'str']).columns.tolist()
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle(f'Data Analysis Dashboard: {self.filename}', fontsize=16, fontweight='bold')
        
        # Plot 1: Distribution of first numeric column
        if len(numeric_cols) > 0:
            axes[0, 0].hist(self.df[numeric_cols[0]].dropna(), bins=30, color='skyblue', edgecolor='black')
            axes[0, 0].set_title(f'Distribution of {numeric_cols[0]}')
            axes[0, 0].set_xlabel(numeric_cols[0])
            axes[0, 0].set_ylabel('Frequency')
        
        # Plot 2: Bar chart of first categorical column
        if len(categorical_cols) > 0:
            value_counts = self.df[categorical_cols[0]].value_counts().head(10)
            axes[0, 1].bar(range(len(value_counts)), value_counts.values, color='coral')
            axes[0, 1].set_title(f'Top Values in {categorical_cols[0]}')
            axes[0, 1].set_xticks(range(len(value_counts)))
            axes[0, 1].set_xticklabels(value_counts.index, rotation=45, ha='right')
            axes[0, 1].set_ylabel('Count')
        
        # Plot 3: Correlation heatmap
        if len(numeric_cols) >= 2:
            corr_matrix = self.df[numeric_cols].corr()
            sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                       ax=axes[1, 0], cbar_kws={'label': 'Correlation'})
            axes[1, 0].set_title('Correlation Heatmap')
        
        # Plot 4: Scatter plot or box plot
        if len(numeric_cols) >= 2:
            axes[1, 1].scatter(self.df[numeric_cols[0]], self.df[numeric_cols[1]], 
                             alpha=0.5, color='green')
            axes[1, 1].set_title(f'{numeric_cols[0]} vs {numeric_cols[1]}')
            axes[1, 1].set_xlabel(numeric_cols[0])
            axes[1, 1].set_ylabel(numeric_cols[1])
        
        plt.tight_layout()
        
        # Save figure (cross-platform path)
        output_file = 'analysis_dashboard.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Dashboard saved to: {output_file}")
        plt.close()
        print()
    
    def export_report(self):
        """Export analysis report to text file"""
        if self.df is None:
            print("No data loaded.")
            return
        
        report_file = 'analysis_report.txt'
        
        with open(report_file, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("DATA ANALYSIS REPORT\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Dataset: {self.filename}\n")
            f.write(f"Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("--- DATASET OVERVIEW ---\n")
            f.write(f"Rows: {self.df.shape[0]}\n")
            f.write(f"Columns: {self.df.shape[1]}\n\n")
            
            f.write("--- COLUMN TYPES ---\n")
            f.write(self.df.dtypes.to_string() + "\n\n")
            
            f.write("--- STATISTICAL SUMMARY ---\n")
            f.write(self.df.describe().to_string() + "\n\n")
            
            f.write("--- TOP 5 ROWS ---\n")
            f.write(self.df.head().to_string() + "\n\n")
        
        print(f"✓ Report exported to: {report_file}\n")


def print_menu():
    """Display interactive menu"""
    print("\n" + "=" * 60)
    print("DATA ANALYZER APP - Main Menu")
    print("=" * 60)
    print("1. Load CSV/Excel file")
    print("2. Use sample dataset")
    print("3. Show dataset overview")
    print("4. Show statistics")
    print("5. Clean data")
    print("6. Create visualizations")
    print("7. Export report")
    print("8. Exit")
    print("=" * 60)


def main():
    """Main application loop"""
    analyzer = DataAnalyzer()
    
    print("\n" + "🔍" * 30)
    print("Welcome to the Data Analyzer App!")
    print("🔍" * 30)
    
    while True:
        print_menu()
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            filepath = input("Enter file path: ").strip()
            analyzer.load_data(filepath)
        
        elif choice == '2':
            analyzer.create_sample_data()
        
        elif choice == '3':
            analyzer.show_overview()
        
        elif choice == '4':
            analyzer.show_statistics()
        
        elif choice == '5':
            analyzer.clean_data()
        
        elif choice == '6':
            analyzer.create_visualizations()
        
        elif choice == '7':
            analyzer.export_report()
        
        elif choice == '8':
            print("\nThank you for using Data Analyzer App! Goodbye! 👋\n")
            break
        
        else:
            print("\n❌ Invalid choice. Please enter a number between 1-8.\n")


if __name__ == "__main__":
    main()