# Running Stitch: Sewing Pattern Database Project

## Overview
This project creates a relational database for sewing patterns, combining web-scraped data from The FoldLine with generated customer and order data. It was built as part of the CodeFirstGirls SQL course to demonstrate database design, data collection and SQL query writing skills.

## Project Components

### [Pattern Scraper](scraper/README.md)
Python-based web scraper that ethically collects sewing pattern data from The Fold Line, including:
- Pattern details (name, company, price)
- Technical specifications
- Images and descriptions

### [Pattern Database](database/README.md)
MySQL database implementing a snowflake schema that includes:
- Customer and order management
- Pattern categorization
- Complex SQL queries and views
- Images and descriptions

## Project Structure
```
sewing-patterns-db/
├── scraper/           # Web scraping component
├── database/          # Database implementation
└── docs/             # Project documentation
```

## Tech Stack
- Python (Beautiful Soup, Pandas)
- MySQL
- Git

---
Created as part of my 'Running Stitch' project for the CodeFirstGirls SQL course.