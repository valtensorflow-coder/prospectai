# ProspectAI — AI-Powered B2B Email Generator

> Upload a CSV of companies → get personalized outreach emails in seconds, powered by Claude AI.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-black?style=flat-square&logo=flask)
![Claude API](https://img.shields.io/badge/Claude-Anthropic-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## What it does

ProspectAI takes a list of companies from a CSV file and automatically generates personalized B2B prospecting emails for each one using Claude AI.

- Upload a CSV with company names and sectors
- Choose a tone: **Professional**, **Casual**, or **Direct**
- Get a unique, tailored email for every company
- Export all results as **CSV** or **PDF**

---

## Demo

![ProspectAI Demo](assets/demo.gif)

---

## Features

- **AI-powered personalization** — each email is crafted based on the company name, sector, and website
- **3 tone options** — Professional, Casual, Direct
- **Drag & drop CSV upload** — no technical knowledge required
- **One-click export** — download all emails as CSV or PDF
- **Clean web interface** — works in any browser, no installation needed for the end user

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, Flask |
| AI | Anthropic Claude API (`claude-sonnet-4-5`) |
| Data | Pandas |
| PDF Export | ReportLab |
| Frontend | HTML, CSS, Vanilla JS |

---

## Project Structure

```
prospector/
├── app.py                  # Flask server — main entry point
├── prospector/
│   ├── generator.py        # Claude API calls & email generation
│   ├── parser.py           # CSV reading & validation
│   ├── exporter.py         # CSV & PDF export
│   └── templates/
│       └── index.html      # Web interface
├── input_example.csv       # Sample input file
├── requirements.txt
└── .env.example
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/prospectai.git
cd prospectai
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Create a `.env` file at the root of the project:

```bash
cp .env.example .env
```

Then open `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 5. Run the app

```bash
python app.py
```

Open your browser at **http://localhost:5000**

---

## CSV Format

Your input CSV must include the following columns:

| Column | Required | Example |
|---|---|---|
| `nom_entreprise` | ✅ Yes | Acme Corp |
| `secteur` | ✅ Yes | e-commerce |
| `site_web` | ❌ Optional | acme.fr |

A sample file is included: [`input_example.csv`](input_example.csv)

---

## Requirements

```
flask
anthropic
pandas
reportlab
python-dotenv
```

Install everything with:

```bash
pip install -r requirements.txt
```

---

## License

MIT — free to use, modify, and distribute.

---

## About

Built as a portfolio project to demonstrate AI automation, REST API integration, and full-stack Python development.

> Looking for a custom AI automation tool for your business? [Contact me on Fiverr](#)