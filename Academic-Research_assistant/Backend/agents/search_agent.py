import requests
import xml.etree.ElementTree as ET
import logging

class SearchAgent:
    def __init__(self):
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def search(self, topic):
        """
        Search for papers on a given topic using the arXiv API.
        
        Parameters:
            topic (str): The research topic to search for.
        
        Returns:
            list: A list of dictionaries containing paper details.
        """
        # Define the base URL for the arXiv API
        base_url = 'http://export.arxiv.org/api/query'
        
        # Define the query parameters
        params = {
            'search_query': f'all:{topic}',
            'start': 0,
            'max_results': 10
        }
        
        self.logger.info(f"Sending request to arXiv API for topic: {topic}")
        
        try:
            # Make the API request with proper URL encoding
            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors
        except requests.exceptions.RequestException as e:
            self.logger.error(f"HTTP Request failed: {e}")
            return []
        
        # Parse the XML response
        papers = self.parse_arxiv_response(response.text)
        
        if not papers:
            self.logger.warning(f"No papers found for the topic: {topic}")
        
        return papers
    
    def parse_arxiv_response(self, xml_data):
        """
        Parse the XML response from the arXiv API to extract paper details.
        
        Parameters:
            xml_data (str): The XML data returned by the arXiv API.
        
        Returns:
            list: A list of dictionaries containing paper details.
        """
        # Define the correct namespace for Atom
        namespaces = {'atom': 'http://www.w3.org/2005/Atom'}
        
        try:
            root = ET.fromstring(xml_data)
        except ET.ParseError as e:
            self.logger.error(f"Failed to parse XML: {e}")
            return []
        
        papers = []
        
        for entry in root.findall('atom:entry', namespaces):
            title = entry.find('atom:title', namespaces)
            id_element = entry.find('atom:id', namespaces)
            published = entry.find('atom:published', namespaces)
            

            
            # Validate that all elements are found
            if title is None or id_element is None or published is None:
                self.logger.warning("Incomplete entry found; skipping.")
                continue
            
            title_text = title.text.strip().replace('\n', ' ')
            arxiv_id = id_element.text.strip().split('/abs/')[-1]
            paper_url = f"https://arxiv.org/abs/{arxiv_id}"
            published_date = published.text.strip()
            
            papers.append({
                "title": title_text,
                "url": paper_url,
                "published": published_date
                
            })
        
        self.logger.info(f"Found {len(papers)} papers.")
        return papers



