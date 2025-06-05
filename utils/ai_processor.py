class AIProcessor:
    def __init__(self):
        # Simple implementation without external dependencies
        pass
        
    def summarize(self, text):
        if not text or len(text) < 10:
            return "No content available to summarize."
            
        # Simple summarization by taking the first few sentences
        sentences = text.split('. ')
        summary = '. '.join(sentences[:3]) + '.' if len(sentences) > 3 else text
        
        return summary