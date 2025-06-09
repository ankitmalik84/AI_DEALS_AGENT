import os
import json
from typing import Optional, List
from openai import OpenAI
from tavily import TavilyClient
from agents.deals import ScrapedDeal, DealSelection, Deal
from agents.agent import Agent
from config import Config


class TavilyDeal:
    """
    A class to represent a Deal retrieved from Tavily search
    """
    def __init__(self, title: str, content: str, url: str, price_info: str = ""):
        self.title = title
        self.summary = content[:500]  # Limit summary length
        self.url = url
        self.details = content
        self.features = price_info
        
    def __repr__(self):
        return f"<TavilyDeal: {self.title}>"
    
    def describe(self):
        """
        Return a description for model processing
        """
        return f"Title: {self.title}\nDetails: {self.details}\nFeatures: {self.features}\nURL: {self.url}"


class TavilyScannerAgent(Agent):
    """
    Scanner Agent that uses Tavily to find Indian deals from major e-commerce sites
    """
    
    MODEL = "gpt-4o-mini"
    
    SYSTEM_PROMPT = """You identify and summarize the 5 most detailed deals from a list of Indian e-commerce search results.
    Focus on deals from major Indian sites like Flipkart, Amazon India, Myntra, Snapdeal, etc.
    Select deals that have the most detailed product description and clear price in Indian Rupees (₹).
    Respond strictly in JSON with no explanation, using this format:
    
    {"deals": [
        {
            "product_description": "Clear summary of the product in 4-5 sentences focusing on features, specifications, and brand. Include model numbers if available.",
            "price": 2999.99,
            "url": "the url as provided"
        },
        ...
    ]}
    
    IMPORTANT: 
    - Only include products with clear prices in ₹ (Indian Rupees)
    - Avoid deals that say "price on request" or unclear pricing
    - Focus on electronics, gadgets, home appliances, and tech products
    - Ensure descriptions are detailed and specific about the product"""
    
    USER_PROMPT_PREFIX = """Find the 5 best deals from these Indian e-commerce search results.
    Select those with the most detailed product descriptions and clear pricing in Indian Rupees.
    Focus on genuine discounts and popular products.
    Respond strictly in JSON format only.
    
    Search Results:
    
    """
    
    USER_PROMPT_SUFFIX = "\n\nRespond with exactly 5 deals in JSON format, no additional text."
    
    name = "Tavily Scanner Agent"
    color = Agent.CYAN
    
    # Indian deal search queries for different categories
    SEARCH_QUERIES = [
        "best deals discounts electronics Flipkart Amazon India today",
        "smartphone mobile phone offers discount India 2024",
        "laptop computer deals Amazon India Flipkart sale",
        "home appliances discount offers India electronics",
        "gadgets deals India electronics accessories discount",
        "smart TV discount offers India sale today",
        "headphones earphones deals India Amazon Flipkart",
        "kitchen appliances discount India home deals"
    ]
    
    def __init__(self):
        """
        Initialize with Tavily and OpenAI clients
        """
        self.log("Tavily Scanner Agent is initializing")
        self.openai = OpenAI(api_key=Config.get_openai_key())
        
        tavily_key = Config.get_tavily_key()
        if not tavily_key:
            self.log("No Tavily API key found - Tavily scanner will not be available")
            self.tavily = None
        else:
            self.tavily = TavilyClient(api_key=tavily_key)
            self.log("Tavily Scanner Agent is ready")
    
    def search_indian_deals(self) -> List[TavilyDeal]:
        """
        Search for Indian deals using Tavily
        """
        if not self.tavily:
            self.log("Tavily not available - skipping search")
            return []
            
        self.log("Searching for Indian deals using Tavily")
        all_deals = []
        
        for query in self.SEARCH_QUERIES[:3]:  # Limit to 3 queries to manage API costs
            try:
                self.log(f"Searching: {query}")
                response = self.tavily.search(
                    query=query,
                    search_depth="basic",
                    include_domains=["flipkart.com", "amazon.in", "myntra.com", "snapdeal.com", "paytm.com", "tatacliq.com"],
                    max_results=5
                )
                
                for result in response.get('results', []):
                    deal = TavilyDeal(
                        title=result.get('title', ''),
                        content=result.get('content', ''),
                        url=result.get('url', ''),
                        price_info=self._extract_price_info(result.get('content', ''))
                    )
                    all_deals.append(deal)
                    
            except Exception as e:
                self.log(f"Error searching with query '{query}': {str(e)}")
                continue
        
        self.log(f"Found {len(all_deals)} potential deals from Tavily")
        return all_deals
    
    def _extract_price_info(self, content: str) -> str:
        """
        Extract price-related information from content
        """
        import re
        # Look for Indian rupee prices
        price_patterns = [
            r'₹[\d,]+',
            r'Rs\.?\s*[\d,]+',
            r'INR\s*[\d,]+',
            r'price.*?₹[\d,]+',
            r'cost.*?₹[\d,]+'
        ]
        
        prices = []
        for pattern in price_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            prices.extend(matches)
        
        return ' | '.join(prices[:3]) if prices else ""
    
    def fetch_deals(self, memory) -> List[TavilyDeal]:
        """
        Fetch deals using Tavily, filtering out those already in memory
        """
        self.log("Tavily Scanner Agent is fetching Indian deals")
        urls = [opp.deal.url for opp in memory]
        deals = self.search_indian_deals()
        result = [deal for deal in deals if deal.url not in urls]
        self.log(f"Tavily Scanner Agent found {len(result)} new deals not in memory")
        return result
    
    def make_user_prompt(self, deals) -> str:
        """
        Create a user prompt for OpenAI based on the Tavily deals
        """
        user_prompt = self.USER_PROMPT_PREFIX
        user_prompt += '\n\n'.join([deal.describe() for deal in deals])
        user_prompt += self.USER_PROMPT_SUFFIX
        return user_prompt
    
    def scan(self, memory: List[str] = []) -> Optional[DealSelection]:
        """
        Use Tavily to find Indian deals and OpenAI to curate them
        """
        if not self.tavily:
            self.log("Tavily not available - cannot scan for Indian deals")
            return None
            
        deals = self.fetch_deals(memory)
        if not deals:
            self.log("No new deals found")
            return None
        
        user_prompt = self.make_user_prompt(deals)
        self.log("Tavily Scanner Agent is calling OpenAI for deal curation")
        
        try:
            result = self.openai.beta.chat.completions.parse(
                model=self.MODEL,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                response_format=DealSelection
            )
            
            result = result.choices[0].message.parsed
            result.deals = [deal for deal in result.deals if deal.price > 0]
            self.log(f"Tavily Scanner Agent curated {len(result.deals)} Indian deals")
            return result
            
        except Exception as e:
            self.log(f"Error in OpenAI curation: {str(e)}")
            return None 