# AI Powered Web Scraping: ScrapeGraphAI

ScrapeGraphAI is a *web scraping* Python library that leverages LLM (Large Language Models) and direct graph logic to create advanced scraping pipelines for websites and local documents (XML, HTML, JSON, etc.). This library allows for seamless integration with various LLMs through APIs, such as **OpenAI**, **Groq**, **Azure**, and **Gemini**, or local models using **Ollama**.

<p align="center">
  <img src="https://raw.githubusercontent.com/VinciGit00/Scrapegraph-ai/main/docs/assets/scrapegraphai_logo.png" alt="Scrapegraph-ai Logo" style="width: 50%;">
</p>

## Key Features
- **API Integration:** I have integrated ScapeGraphAI with various LLMs using APIs, enabling users to easily connect with powerful models such as **OpenAI**, **Groq**, **Azure**, and **Gemini**.
- **Local Model Support:** I have added support for local models, allowing users to seamlessly integrate and utilize local models for web scraping tasks.
- **Optimized Web Scraping:** Using IPyWidgets, I have developed functions that optimize the web scraping process. Users can specify the number of websites to scrape, input URLs, and provide a prompt to get tailored outputs.
- **Multi-Language Support:** By integrating Python's translate library into the scraping pipeline, I have enabled multi-language support. Users can choose to translate the scraped data into their preferred language, with the output provided in JSON format.

## Case Study: SmartScraper using Local Models

To utilize local models, ensure you have [Ollama](https://ollama.com/) installed and download the necessary models using the `ollama pull` command.

## User Integration and Optimization

### IPyWidgets for Web Scraping Optimization

To facilitate a user-friendly and efficient web scraping experience, I have integrated IPyWidgets into the ScrapeGraphAI library. This integration allows users to interact with the scraping tool through a graphical interface. Users can specify:
- **The number of websites they wish to scrape:** This feature helps in managing the scope of the scraping task, ensuring that users can scale their scraping efforts according to their needs.
- **Input URLs:** Users can easily input multiple URLs from which data needs to be scraped. This flexibility ensures that diverse sources can be targeted within a single scraping session.
- **Provide a prompt:** Users can enter a specific prompt that guides the scraping process, ensuring that the output is relevant and tailored to their requirements.

The generated output, based on the given prompt, will be efficiently produced and displayed to the user, enhancing the overall usability and effectiveness of the web scraping process.

### Multi-Language Translation

To cater to a global audience, I have integrated Python's translate library into the ScrapeGraphAI pipeline. This feature enables users to:
- Opt for translation of the scraped data into their preferred language: By selecting the translation option, users can choose the target language for the output.
- Receive results in JSON format: The translated output will be provided in JSON format, ensuring that the data is structured, easy to understand, and can be readily used for further analysis or integration into other applications.

This multi-language support ensures that ScrapeGraphAI can be effectively used by non-English speakers and in multilingual environments, making the tool more versatile and accessible.

## Conclusion

ScrapeGraphAI empowers users with advanced web scraping capabilities, integrating powerful LLMs and optimization tools to deliver precise and customizable scraping solutions. Whether you are using APIs or local models, ScrapeGraphAI ensures efficient and multilingual data extraction for a wide range of applications.
