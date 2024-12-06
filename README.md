# Smart Scraper App  

This repository leverages **Large Language Models (LLMs)** and direct graph logic to create advanced scraping pipelines for websites and local documents (XML, HTML, JSON, etc.). The app provides seamless integration with various LLMs via APIs, including OpenAI, Groq, Azure, and Gemini, as well as support for local models using **Ollama**.  

## Key Features  
- **Multi-Language Support**: Integrates Python's `translate` library, allowing users to translate scraped data into their preferred language.  
- **LLM Integration**: Compatible with LLMs like OpenAI, Groq, Azure, and Gemini through API connections or local models using `ollama`.  
- **Custom Scraping Pipelines**: Enables dynamic and precise scraping with support for JSON, HTML, and XML formats.  
- **User-Friendly Interface**: Built using **Streamlit** for an intuitive and responsive user experience.  
- **Output Flexibility**: Provides results in JSON format, ready for further analysis or download.  

## File Structure  
```
├── app.py # Main application file for Streamlit
├── Dockerfile # Docker configuration for deployment
├── requirements.txt # Python dependencies
├── Translatory_UpgradeD_Myscapegraph_Deployment.ipynb # Jupyter notebook with core logic
├── .gitattributes # Git settings
├── README.md # Repository documentation (this file)
```

## Getting Started  

### Prerequisites  
- Python 3.10+  
- Docker (optional for containerized deployment)  
- Ollama (for local model usage)  

### Installation  
1. Clone the repository:  
   ``` 
   git clone https://github.com/ayushadarsh7/AI-Powered-Web-Scrapping.git 
   cd AI-Powered-Web-Scraping ```
   
### Install dependencies:
```
pip install -r requirements.txt
```
### Install Playwright and its browsers:
```
playwright install  
```
### Running the App:
```
streamlit run app.py  
```
## Usage
* Enter the number of sources and their URLs in the provided fields.
* Input the prompt for scraping. Optionally, enable the "Translate Prompt" feature to translate it into English from your preferred language.
* Run the scraper to process the sources, and download the results in JSON format.

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to enhance the functionality.

## Requirements  

### Software  
- **Python**: Version 3.10 or higher  
- **Docker**: (Optional)  
- **Ollama**: (Optional)  

### Python Libraries  
- `streamlit==1.31.0`  
- `scrapegraphai==0.1.0`  
- `translate==3.6.1`  
- `playwright==1.41.0`  
- `nest-asyncio==1.5.8`  
- `aiohttp==3.9.1`  
- `asyncio==3.4.3`  

### Additional Setup  
- **Playwright Browsers**:  
  ```bash  
  playwright install  
