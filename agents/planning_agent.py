from typing import Optional, List
from agents.agent import Agent
from agents.deals import ScrapedDeal, DealSelection, Deal, Opportunity
from agents.scanner_agent import ScannerAgent
from agents.tavily_scanner_agent import TavilyScannerAgent
from agents.ensemble_agent import EnsembleAgent
from agents.messaging_agent import MessagingAgent
from config import Config


class PlanningAgent(Agent):

    name = "Planning Agent"
    color = Agent.GREEN
    DEAL_THRESHOLD = 50

    def __init__(self, collection):
        """
        Create instances of the Agents that this planner coordinates across
        Now includes both RSS and Tavily scanners for better coverage
        """
        self.log("Planning Agent is initializing")
        
        # Initialize both scanners
        self.rss_scanner = ScannerAgent()
        
        # Try to initialize Tavily scanner (graceful fallback if no API key)
        try:
            self.tavily_scanner = TavilyScannerAgent()
            self.has_tavily = self.tavily_scanner.tavily is not None
            if self.has_tavily:
                self.log("Planning Agent: Tavily scanner available for Indian deals")
            else:
                self.log("Planning Agent: Tavily scanner not available, using RSS only")
        except Exception as e:
            self.log(f"Planning Agent: Could not initialize Tavily scanner: {str(e)}")
            self.tavily_scanner = None
            self.has_tavily = False
        
        self.ensemble = EnsembleAgent(collection)
        self.messenger = MessagingAgent()
        self.log("Planning Agent is ready")

    def run(self, deal: Deal) -> Opportunity:
        """
        Run the workflow for a particular deal
        :param deal: the deal, summarized from an RSS scrape or Tavily search
        :returns: an opportunity including the discount
        """
        self.log("Planning Agent is pricing up a potential deal")
        estimate = self.ensemble.price(deal.product_description)
        discount = estimate - deal.price
        self.log(f"Planning Agent has processed a deal with discount ${discount:.2f}")
        return Opportunity(deal=deal, estimate=estimate, discount=discount)

    def plan(self, memory: List[str] = [], prefer_indian_deals: bool = True) -> Optional[Opportunity]:
        """
        Run the full workflow with improved deal discovery:
        1. Try Tavily scanner for Indian deals (if available and preferred)
        2. Fallback to RSS scanner for international deals
        3. Use the EnsembleAgent to estimate prices
        4. Use the MessagingAgent to send notifications
        
        :param memory: a list of URLs that have been surfaced in the past
        :param prefer_indian_deals: whether to prioritize Indian deals via Tavily
        :return: an Opportunity if one was surfaced, otherwise None
        """
        self.log("Planning Agent is kicking off an enhanced run")
        
        selection = None
        
        # Try Tavily scanner first if available and Indian deals are preferred
        if prefer_indian_deals and self.has_tavily:
            self.log("Planning Agent: Trying Tavily scanner for Indian deals")
            try:
                selection = self.tavily_scanner.scan(memory=memory)
                if selection and selection.deals:
                    self.log(f"Planning Agent: Found {len(selection.deals)} Indian deals via Tavily")
                else:
                    self.log("Planning Agent: No Indian deals found via Tavily")
            except Exception as e:
                self.log(f"Planning Agent: Tavily scanner error: {str(e)}")
        
        # Fallback to RSS scanner if no Tavily results or if international deals preferred
        if not selection or not selection.deals:
            self.log("Planning Agent: Using RSS scanner for international deals")
            try:
                selection = self.rss_scanner.scan(memory=memory)
                if selection and selection.deals:
                    self.log(f"Planning Agent: Found {len(selection.deals)} international deals via RSS")
                else:
                    self.log("Planning Agent: No deals found via RSS")
            except Exception as e:
                self.log(f"Planning Agent: RSS scanner error: {str(e)}")
        
        if selection and selection.deals:
            # Process up to 5 deals
            opportunities = [self.run(deal) for deal in selection.deals[:5]]
            opportunities.sort(key=lambda opp: opp.discount, reverse=True)
            best = opportunities[0]
            
            self.log(f"Planning Agent has identified the best deal with discount ${best.discount:.2f}")
            
            if best.discount > self.DEAL_THRESHOLD:
                self.messenger.alert(best)
                self.log("Planning Agent: Alert sent for qualifying deal")
            else:
                self.log(f"Planning Agent: Deal discount ${best.discount:.2f} below threshold ${self.DEAL_THRESHOLD}")
            
            self.log("Planning Agent has completed an enhanced run")
            return best if best.discount > self.DEAL_THRESHOLD else None
        
        self.log("Planning Agent: No deals found from any scanner")
        return None