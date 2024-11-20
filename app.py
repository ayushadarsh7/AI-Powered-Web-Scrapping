import json
import streamlit as st
import nest_asyncio
import asyncio
from scrapegraphai.graphs import SmartScraperGraph
from translate import Translator
from playwright.async_api import async_playwright

# Apply nest_asyncio to allow nested async calls
nest_asyncio.apply()

# Configuration for the SmartScraperGraph
graph_config = {
    "llm": {
        "api_key": "AIzaSyDm4fQLnNgKF1UyTg44oU4VredpTFcc7rU",
        "model": "gemini-pro",
    },
    "embedding_model": {
        "name": "google",
        "api_key": "AIzaSyDm4fQLnNgKF1UyTg44oU4VredpTFcc7rU"
    },
    "verbose": True
}

# Streamlit app layout
st.title("Smart Scraper App")

# Input for the number of sources
num_sources = st.number_input("Number of sources:", min_value=1, value=1, step=1)

# List to store source URLs
sources = []

# Input for source URLs
for i in range(num_sources):
    source_url = st.text_input(f"Enter source {i + 1} URL:", "")
    sources.append(source_url)

# Input for the prompt
prompt_value = st.text_input("Enter your prompt:", "")

# Checkbox to select whether to translate the prompt
translate_prompt = st.checkbox("Translate prompt")

# Input for the language of the prompt (if translation is selected)
language_value = ""
if translate_prompt:
    language_value = st.text_input("Enter language of prompt (e.g. ko for Korean):", "")

# Define an asynchronous function to run the scraper
async def run_scraper(prompt_value, sources):
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        try:
            for source_value in sources:
                if source_value:  # Check if the source URL is not empty
                    try:
                        # Create a SmartScraperGraph instance
                        smart_scraper_graph = SmartScraperGraph(
                            prompt=prompt_value,
                            source=source_value,
                            config=graph_config
                        )
                        # Run the SmartScraperGraph and get the result
                        result = await smart_scraper_graph.run()  # Await the result
                        results.append({
                            "source": source_value,
                            "result": result
                        })
                    except Exception as e:
                        results.append({
                            "source": source_value,
                            "error": str(e)
                        })
        finally:
            await browser.close()
    return results

# Button to run the SmartScraperGraph
if st.button("Run"):
    try:
        with st.spinner("Processing..."):
            # Translate the prompt if necessary
            if translate_prompt and language_value:
                translator = Translator(from_lang=language_value, to_lang="en")
                prompt_value = translator.translate(prompt_value)

            # Validate inputs
            if not prompt_value:
                st.error("Please enter a prompt")
            elif not any(source.strip() for source in sources):
                st.error("Please enter at least one source URL")
            elif translate_prompt and not language_value:
                st.error("Please enter the language for translation")
            else:
                # Run the scraper and display results
                results = asyncio.run(run_scraper(prompt_value, sources))
                
                # Display results
                st.json(json.dumps(results, indent=2))
                
                # Add download button
                st.download_button(
                    label="Download Results",
                    data=json.dumps(results, indent=2),
                    file_name="scraper_results.json",
                    mime="application/json"
                )
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")