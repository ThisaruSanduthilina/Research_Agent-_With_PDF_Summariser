from utils.web_scrapper import WebScraper  # Assuming the class is named WebScraper with one 'p'
from utils.ai_processor import AIProcessor
import time

class ResearchAgent:
    def __init__(self):
        from utils.web_scrapper import WebScraper
        from utils.ai_processor import AIProcessor
        
        # Initialize components
        self.scraper = WebScraper()
        self.processor = AIProcessor()
    
    def research(self, topic, depth=2):
        """
        Perform research on the specified topic.
        
        Args:
            topic: The research topic (string)
            depth: Number of sources to analyze (default: 2)
            
        Returns:
            List of research results, each containing topic, source, summary, and timestamp
        """
        print(f"Researching user query: '{topic}'")
        
        # Validate input
        if not topic or topic == "string":
            print("Warning: Empty or default topic provided. Using 'general information'")
            topic = "general information"
        
        # Search for relevant information sources
        search_results = self.scraper.search_web(topic)
        
        # Limit the number of results based on depth
        search_results = search_results[:depth] if search_results else []
        
        # If no results were found, provide a fallback
        if not search_results:
            print(f"No results found for topic: {topic}")
            return [{
                'topic': topic,
                'source': 'No sources found',
                'summary': f"Unable to find relevant information for '{topic}'. Please try a different search term or check your internet connection.",
                'timestamp': time.time()
            }]
        
        results = []
        for i, result in enumerate(search_results):
            source_url = result['link']
            print(f"Analyzing source {i+1}/{len(search_results)}: {source_url}")
            
            # Get the page content
            html_content = self.scraper.get_page(source_url)
            
            if html_content:
                # Extract main content
                main_content = self.scraper.extract_main_content(html_content)
                
                # Generate summary
                summary = self.processor.summarize(main_content)
                
                # Add to results
                results.append({
                    'topic': topic,  # Use the actual user-provided topic
                    'source': result['title'] if 'title' in result else source_url,
                    'summary': summary,
                    'timestamp': time.time()
                })
            else:
                # Add a placeholder for failed sources
                results.append({
                    'topic': topic,
                    'source': result['title'] if 'title' in result else source_url,
                    'summary': f"Unable to retrieve content from this source. The website may be unavailable or may have blocked the request.",
                    'timestamp': time.time()
                })
        
        print(f"Research complete. Found {len(results)} results for '{topic}'")
        return results

if __name__ == "__main__":
    # Create the research agent
    agent = ResearchAgent()
    
    # Define a research topic
    research_topic = "artificial intelligence"
    
    # Run the research
    results = agent.research(research_topic, depth=2)
    
    # Print the results
    print(f"\nResearch Results for '{research_topic}':")
    for i, item in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(f"Source: {item['source']}")
        print(f"Summary: {item['summary']}")