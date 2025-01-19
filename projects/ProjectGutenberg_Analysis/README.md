# Project Gutenberg Analysis

## Overview
Project Gutenberg is a digital library of over 70,000 free eBooks, consisting primarily of works for which U.S. copyright has expired. Founded in 1971, it represents one of the oldest and largest collections of freely available digital books. While not a commercial publisher, analysing Project Gutenberg's data provides valuable insights into digital reading patterns for historical works across different languages. This analysis was conducted to demonstrate data analytics capabilities in a publishing context, specifically examining how historical works perform in digital formats across different languages and markets. By analysing download patterns and language distribution in Project Gutenberg's corpus, I can understand global digital engagement with classic literature - information that could be valuable for publishers considering digital republishing strategies, translation priorities, or market expansion opportunities. However, it's important to note that this analysis has specific limitations: the works are all out of copyright in the US, available only in digital format, and represent historical rather than contemporary content. Despite these constraints, the dataset provides a clean, well-structured sample for demonstrating publishing analytics capabilities, especially in visualising and interpreting multi-language market performance data.

## Data Sources
- Project Gutenberg API
- Available fields: languages, subjects, download counts
- Data limitations noted

## Project Structure
- `notebooks/`: Jupyter notebooks for analysis
  - `01_data_collection.ipynb`: Python-based data collection and initial analysis
  - `02_excel_clean.ipynb`: Documentation of Excel analysis
  - `03_language_analysis.ipynb`: Analysis of languages used
  - `04_subject_analysis.ipynb`: Analysis of subjects covered and co-occurrences
  - `05_dashboard_creation.ipynb`: Metrics used to form Interactive dashboard
  - `06_final_report.md`: Presentation of data in a Powerpoint and Report
- `data/`: Raw and processed data
- `excel/`: Excel analysis files and documentation

## Analysis Components
1. Language Distribution
   - Language availability
   - Download patterns by language

2. Subject/Genre Analysis
   - Subject categorization
   - Popular subjects
   - Download patterns


