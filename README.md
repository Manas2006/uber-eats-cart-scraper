# 🍽️ OrderSmarter

A smart Uber Eats cart analyzer that helps you make healthier and more cost-effective food choices.

## 🌟 Features

- 🔗 Paste any Uber Eats cart link
- 📊 Get detailed nutritional analysis
- 💰 Find cheaper alternatives
- 🥗 Discover healthier options
- 📈 Track your spending and calories

## 🛠️ Tech Stack

- **Frontend**: React + Tailwind CSS
- **Backend**: Spring Boot
- **Scraper**: Python + Playwright
- **ML Model**: FastAPI (hosted separately)

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Java 17+
- Node.js 16+
- Playwright for Python

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/uber-eats-cart-scraper.git
cd uber-eats-cart-scraper
```

2. Set up the Python scraper:
```bash
cd scraper
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
playwright install
```

3. Set up the Spring Boot backend:
```bash
cd backend
./gradlew build
```

4. Set up the React frontend:
```bash
cd frontend
npm install
```

### Running the Application

1. Start the Python scraper:
```bash
cd scraper
python uber_scraper.py
```

2. Start the Spring Boot backend:
```bash
cd backend
./gradlew bootRun
```

3. Start the React frontend:
```bash
cd frontend
npm run dev
```

## 📁 Project Structure

```
order-smarter/
├── scraper/              # Python scraper using Playwright
├── backend/             # Spring Boot backend
├── frontend/            # React frontend
└── README.md
```

## 🔧 Configuration

The application requires the following environment variables:

- `CALORIE_API_URL`: URL of the calorie prediction API
- `UBER_EATS_API_KEY`: (if required) Your Uber Eats API key

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
- [Spring Boot](https://spring.io/projects/spring-boot) for the backend framework
- [React](https://reactjs.org/) for the frontend framework 