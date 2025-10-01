# ⚽ Champions League Live Dashboard

A real-time interactive dashboard for UEFA Champions League standings, statistics, and match results built with Python and Streamlit.

## 🌟 Features

- **Live Standings**: Real-time Champions League team standings with automatic updates
- **Interactive Visualizations**: 
  - Points comparison charts
  - Goal difference analysis
  - Attack vs Defense scatter plots
- **Match Results**: View recent Champions League match scores
- **Key Statistics**: Track highest-scoring teams, best defenses, and goal differences
- **Auto-Refresh**: Configurable automatic data refresh (30-300 seconds)
- **Responsive Design**: Clean, modern interface with light theme

## 🚀 Live Demo

[View Live Dashboard](https://your-app-name.streamlit.app) *(Replace with your actual Streamlit Cloud URL)*

## 📸 Screenshots

*Add screenshots of your dashboard here*

## 🛠️ Built With

- **[Streamlit](https://streamlit.io/)** - Web application framework
- **[Plotly](https://plotly.com/)** - Interactive visualizations
- **[Pandas](https://pandas.pydata.org/)** - Data manipulation
- **[football-data.org API](https://www.football-data.org/)** - Live Champions League data

## 📋 Prerequisites

- Python 3.11 or higher
- A free API key from [football-data.org](https://www.football-data.org/client/register)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/champions-league-live-dashboard.git
   cd champions-league-live-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get your API key**
   - Visit [football-data.org](https://www.football-data.org/client/register)
   - Register for a free account
   - Copy your API key

4. **Run the application**
   ```bash
   streamlit run champions_dashboard.py
   ```

5. **Enter your API key**
   - Open the dashboard in your browser (usually `http://localhost:8501`)
   - Enter your API key in the sidebar
   - Start exploring live Champions League data!

## 🌐 Deployment

### Deploy to Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Connect your GitHub repository
4. Add your API key in the Secrets section:
   ```toml
   API_KEY = "your_api_key_here"
   ```
5. Deploy!

### Other Deployment Options

- **Heroku**: Follow the [Streamlit deployment guide](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)
- **Railway**: Connect your GitHub repo at [railway.app](https://railway.app/)
- **Google Cloud Run**: Use the included Dockerfile

## 📁 Project Structure

```
champions-league-live-dashboard/
├── .streamlit/
│   └── config.toml          # Streamlit configuration and theme
├── champions_dashboard.py    # Main application file
├── requirements.txt          # Python dependencies
├── .python-version          # Python version specification
└── README.md                # Project documentation
```

## ⚙️ Configuration

### Customizing the Theme

Edit `.streamlit/config.toml` to customize colors:

```toml
[theme]
primaryColor="#1e3a8a"
backgroundColor="#ffffff"
secondaryBackgroundColor="#f0f2f6"
textColor="#262730"
```

### Adjusting Refresh Rate

Use the sidebar slider to set auto-refresh interval (30-300 seconds)

## 📊 API Usage

This project uses the [football-data.org API](https://www.football-data.org/):
- **Free Tier**: 10 requests per minute
- **Coverage**: All UEFA Champions League matches and standings
- **Data Cache**: 60-second cache to optimize API usage

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [football-data.org](https://www.football-data.org/) for providing the Champions League API
- [Streamlit](https://streamlit.io/) for the amazing web framework
- UEFA for the Champions League data

## 📧 Contact

Fratu Victor Mihai - mihaifratu78@gmail.com

Project Link: [https://github.com/Fratu223/Champions-League-Live-Dashboard](https://github.com/Fratu223/Champions-League-Live-Dashboard)

## 🐛 Known Issues

- API rate limits may cause delays during high-traffic periods
- Some team names may appear differently than official UEFA names

## 🔮 Future Enhancements

- [ ] Add player statistics
- [ ] Include knockout stage bracket visualization
- [ ] Historical season comparisons
- [ ] Email notifications for match results
- [ ] Mobile app version
- [ ] Multi-language support

---

**⭐ Star this repository if you find it helpful!**