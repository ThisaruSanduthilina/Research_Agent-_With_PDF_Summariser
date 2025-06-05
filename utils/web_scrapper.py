class WebScraper:
    def __init__(self):
        import requests
        from bs4 import BeautifulSoup
        import random
        import time
        
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        
        # Dictionary of predefined sources for common topics
        self.topic_sources = {
            "artificial intelligence": [
                {'link': 'https://en.wikipedia.org/wiki/Artificial_intelligence', 'title': 'Artificial intelligence - Wikipedia'},
                {'link': 'https://www.ibm.com/topics/artificial-intelligence', 'title': 'What is Artificial Intelligence (AI)? | IBM'},
            ],
            # Add more predefined topics as needed
            "car sales": [
                {'link': 'https://www.statista.com/topics/1487/automotive-industry/', 'title': 'Automotive Industry - Statistics & Facts | Statista'},
                {'link': 'https://www.ibisworld.com/global/industry-trends/biggest-industries-by-revenue/manufacturing/car-automobile-manufacturing/', 'title': 'Car Manufacturing Industry Trends & Analysis | IBIS World'},
            ],
            "sri lanka": [
                {'link': 'https://en.wikipedia.org/wiki/Sri_Lanka', 'title': 'Sri Lanka - Wikipedia'},
                {'link': 'https://www.lmd.lk/category/sectors/', 'title': 'Business Sectors in Sri Lanka | LMD'},
            ],
        }
    
    def search_web(self, query):
        """
        Search the web for information related to the query.
        
        Args:
            query: The search query (topic)
            
        Returns:
            List of search results with links and titles
        """
        import re
        
        # Print the query for debugging
        print(f"Searching for: {query}")
        
        # Normalize query for dictionary lookup
        query_lower = query.lower()
        
        # Check if we have predefined sources for this topic
        for topic, sources in self.topic_sources.items():
            if topic in query_lower:
                print(f"Using predefined sources for topic: {topic}")
                return sources
        
        # If no predefined sources match, create dynamic search results
        # This is a more general approach based on the user query
        print(f"No exact predefined sources found for: '{query_lower}'. Using dynamic search.")
        
        # Format the query for use in URLs
        query_formatted = query.replace(' ', '+')
        
        # Create dynamic search results based on the actual query
        search_results = [
            {'link': f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}", 
             'title': f"{query} - Wikipedia"},
            {'link': f"https://www.google.com/search?q={query_formatted}",
             'title': f"Google Search: {query}"},
            {'link': f"https://scholar.google.com/scholar?q={query_formatted}",
             'title': f"Google Scholar: {query}"},
            {'link': f"https://www.sciencedirect.com/search?qs={query_formatted}",
             'title': f"ScienceDirect: {query}"}
        ]
        
        return search_results
    
    def get_page(self, url):
        """Get the HTML content of a webpage"""
        import requests
        import time
        import random
        
        try:
            # Add a short delay to avoid being blocked
            time.sleep(random.uniform(1, 3))
            
            # Send the request
            response = requests.get(url, headers=self.headers, timeout=10)
            
            # Check if the request was successful
            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed to retrieve page: {url}, Status code: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error fetching URL {url}: {str(e)}")
            return None
    
    def extract_main_content(self, html):
        """Extract the main content from an HTML page"""
        from bs4 import BeautifulSoup
        
        if not html:
            return "No content available."
            
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()
            
            # Get text
            text = soup.get_text()
            
            # Break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            
            # Break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            
            # Drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text
            
        except Exception as e:
            print(f"Error extracting content: {str(e)}")
            return "Error extracting content."