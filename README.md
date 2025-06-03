# 🍽️ Uber Eats Cart Scraper

A smart Uber Eats group cart scraper that extracts restaurant and item data from a shared Uber Eats group order link.

## 🌟 Features

- 🔗 Paste any Uber Eats group cart link
- 📦 Get restaurant and item details as JSON
- 🖥️ REST API endpoint (FastAPI, async)
- 🐍 CLI/testing support (sync)

## 🛠️ Tech Stack

- **Backend/API**: FastAPI (Python, async)
- **Scraper**: Playwright (Python, async & sync)
- **Data Models**: Pydantic

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Playwright for Python

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Manas2006/uber-eats-cart-scraper.git
cd uber-eats-cart-scraper
```

2. Set up the Python environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install
```

### Running the Scraper (CLI)

To run the scraper directly (sync, for testing):
```bash
cd scraper
python uber_scraper.py
```

### Running the API (Async, Recommended)

From the project root, start the FastAPI server:
```bash
python -m scraper.api
```

The API will be available at: `http://localhost:8000`

#### Test the API Endpoint

Send a POST request to `/scrape` with your Uber Eats group order link:
```bash
curl -X POST http://localhost:8000/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://eats.uber.com/group-orders/YOUR-GROUP-ID/join"}'
```

#### Example Response
```json
{
  "restaurant": "Wayback Burgers (18321 West Airport Blvd)",
  "items": [
    {"name": "DOUBLE CHEESEBURGER BOX", "quantity": 1, "price": 12.69, "person": "Manas"},
    {"name": "REGULAR MILKSHAKE", "quantity": 1, "price": 6.89, "person": "Manas"}
  ],
  "total_price": 19.58
}
```

## 📁 Project Structure

```
uber-eats-cart-scraper/
└── scraper/
    ├── api.py                # FastAPI app (async API)
    ├── uber_scraper_async.py # Async Playwright scraper (used by API)
    ├── uber_scraper.py       # Sync Playwright scraper (CLI/testing)
    ├── models.py             # Pydantic models
    ├── test_scraper.py       # Test script for direct/API scraping
    └── requirements.txt      # Python dependencies
```

## 🔧 Configuration

- No special environment variables are required for basic scraping.
- If you use `.env` for Playwright or other secrets, place it in the `scraper/` directory.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Uber Eats](https://www.ubereats.com/) for the inspiration
- [Playwright](https://playwright.dev/) for the web scraping capabilities
- [FastAPI](https://fastapi.tiangolo.com/) for the API framework 