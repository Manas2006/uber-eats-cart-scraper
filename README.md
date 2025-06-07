# 🍽️ Uber Eats Cart Scraper

A smart Uber Eats group cart scraper that extracts restaurant and item data from a shared Uber Eats group order link.

## 🌟 Features

- 🔗 Paste any Uber Eats group cart link
- 📦 Get restaurant and item details as JSON
- 🖥️ REST API endpoint (FastAPI, async)
- 🚀 Deployed on Render (free tier)

## 🛠️ Tech Stack

- **Backend/API**: FastAPI (Python, async)
- **Scraper**: Playwright (Python, async)
- **Data Models**: Pydantic
- **Hosting**: Render

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

### Running the API Locally

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
  "restaurant": "Restaurant Name",
  "items": [
    {"name": "Item Name", "quantity": 1, "price": 12.99, "person": "Person Name"}
  ],
  "total_price": 12.99
}
```

## 📁 Project Structure

```
uber-eats-cart-scraper/
├── scraper/
│   ├── api.py                # FastAPI app (async API)
│   ├── uber_scraper_async.py # Async Playwright scraper
│   └── models.py             # Pydantic models
├── requirements.txt          # Python dependencies
├── render.yaml              # Render deployment config
└── README.md               # Project documentation
```


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Uber Eats](https://www.ubereats.com/) for the inspiration
- [Playwright](https://playwright.dev/) for the web scraping capabilities
- [FastAPI](https://fastapi.tiangolo.com/) for the API framework
- [Render](https://render.com) for the hosting platform 
