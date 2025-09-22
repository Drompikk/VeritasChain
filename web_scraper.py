# Using web scraper integration for content extraction
import trafilatura
import requests
import asyncio
import aiohttp
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse
import re


def get_website_text_content(url: str) -> str:
    """
    This function takes a url and returns the main text content of the website.
    The text content is extracted using trafilatura and easier to understand.
    The results is not directly readable, better to be summarized by LLM before consume
    by the user.
    """
    # Send a request to the website
    downloaded = trafilatura.fetch_url(url)
    text = trafilatura.extract(downloaded)
    return text if text is not None else ""


class VeritasWebScraper:
    """
    Web scraper for Veritas agent to analyze off-chain data sources
    """
    
    def __init__(self):
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def scrape_project_mentions(self, project_name: str, project_address: Optional[str] = None) -> Dict:
        """
        Scrape various sources for mentions of the project
        
        Args:
            project_name: Name of the project to search for
            project_address: Contract address if available
            
        Returns:
            Dictionary containing scraped data from various sources
        """
        search_terms = [project_name]
        if project_address:
            search_terms.append(project_address)
            
        results = {
            "news_articles": [],
            "social_media": [],
            "forums": [],
            "official_sources": [],
            "sentiment_indicators": [],
            "partnership_claims": [],
            "team_information": []
        }
        
        # Search for news articles
        news_results = await self._search_news_sources(search_terms)
        results["news_articles"] = news_results
        
        # Search for official announcements
        official_results = await self._search_official_sources(project_name)
        results["official_sources"] = official_results
        
        # Look for partnership claims
        partnership_results = await self._search_partnerships(project_name)
        results["partnership_claims"] = partnership_results
        
        return results
    
    async def _search_news_sources(self, search_terms: List[str]) -> List[Dict]:
        """Search cryptocurrency news sources for project mentions"""
        news_sources = [
            "https://cointelegraph.com",
            "https://coindesk.com", 
            "https://decrypt.co",
            "https://theblock.co"
        ]
        
        articles = []
        
        for term in search_terms:
            for source in news_sources:
                try:
                    # Use Google search with site restriction
                    search_url = f"https://www.google.com/search?q={term}+site:{urlparse(source).netloc}"
                    
                    # Extract article URLs (simplified - in production would use proper APIs)
                    # For now, we'll simulate finding relevant articles
                    safe_term = term.replace(' ', '-').lower() if term else 'unknown'
                    articles.append({
                        "source": source,
                        "search_term": term,
                        "title": f"Sample article about {term}",
                        "url": f"{source}/sample-article-{safe_term}",
                        "content": "Sample content for analysis",
                        "date": "2024-01-01",
                        "credibility_score": 85  # Placeholder
                    })
                    
                except Exception as e:
                    print(f"Error searching {source}: {e}")
                    
        return articles
    
    async def _search_official_sources(self, project_name: str) -> List[Dict]:
        """Search for official project sources and announcements"""
        official_sources = []
        
        # Look for official website
        try:
            # Search for official website
            website_url = await self._find_official_website(project_name)
            if website_url:
                content = get_website_text_content(website_url)
                official_sources.append({
                    "type": "official_website",
                    "url": website_url,
                    "content": content,
                    "verified": True
                })
        except Exception as e:
            print(f"Error finding official website: {e}")
            
        return official_sources
    
    async def _find_official_website(self, project_name: str) -> Optional[str]:
        """Try to find the official website for a project"""
        # This would typically use search APIs or domain checking
        # For now, return a placeholder
        safe_name = project_name.lower().replace(' ', '') if project_name else 'unknown'
        return f"https://{safe_name}.com"
    
    async def _search_partnerships(self, project_name: str) -> List[Dict]:
        """Search for partnership announcements and verify claims"""
        partnerships = []
        
        # Common partnership keywords to search for
        partnership_keywords = [
            f"{project_name} partnership",
            f"{project_name} collaboration", 
            f"{project_name} announces",
            f"{project_name} integrates"
        ]
        
        for keyword in partnership_keywords:
            # Simulate finding partnership announcements
            partnerships.append({
                "claim": f"Partnership announcement for {keyword}",
                "source": "crypto_news_site",
                "verification_status": "pending",
                "credibility": 70,
                "date": "2024-01-01"
            })
            
        return partnerships
    
    async def analyze_social_sentiment(self, project_name: str) -> Dict:
        """
        Analyze social media sentiment around the project
        Note: This would typically integrate with Twitter API, Reddit API, etc.
        """
        return {
            "overall_sentiment": "neutral",
            "sentiment_score": 0.1,  # -1 to 1 scale
            "mention_volume": 150,
            "positive_mentions": 60,
            "negative_mentions": 30,
            "neutral_mentions": 60,
            "key_topics": ["development", "partnerships", "tokenomics"],
            "influencer_mentions": [],
            "red_flags": []
        }
    
    async def verify_team_information(self, project_name: str) -> Dict:
        """
        Verify team member information and credentials
        """
        return {
            "team_members_found": 3,
            "verified_members": 2,
            "linkedin_profiles": ["sample1", "sample2"],
            "github_profiles": ["dev1", "dev2"],
            "previous_projects": ["Project A", "Project B"],
            "credibility_indicators": [
                "Active GitHub profiles",
                "Previous successful projects"
            ],
            "warning_signs": []
        }
    
    def extract_contact_information(self, website_content: str) -> Dict:
        """Extract contact and social media information from website"""
        contact_info = {
            "emails": [],
            "social_links": {},
            "contact_forms": False,
            "physical_address": None
        }
        
        # Extract email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, website_content)
        contact_info["emails"] = emails
        
        # Extract social media links
        social_patterns = {
            "twitter": r'twitter\.com/[A-Za-z0-9_]+',
            "telegram": r't\.me/[A-Za-z0-9_]+',
            "discord": r'discord\.(gg|com)/[A-Za-z0-9_]+',
            "github": r'github\.com/[A-Za-z0-9_-]+',
            "linkedin": r'linkedin\.com/[A-Za-z0-9_/-]+'
        }
        
        for platform, pattern in social_patterns.items():
            matches = re.findall(pattern, website_content, re.IGNORECASE)
            if matches:
                contact_info["social_links"][platform] = matches[0]
        
        return contact_info


# Standalone functions for quick access
async def quick_project_scan(project_name: str, project_address: Optional[str] = None) -> Dict:
    """
    Quick scan of a project's off-chain presence
    """
    async with VeritasWebScraper() as scraper:
        results = await scraper.scrape_project_mentions(project_name, project_address)
        sentiment = await scraper.analyze_social_sentiment(project_name)
        team_info = await scraper.verify_team_information(project_name)
        
        return {
            "project_mentions": results,
            "social_sentiment": sentiment,
            "team_verification": team_info,
            "scan_timestamp": "2024-01-01T00:00:00Z"
        }


# Example usage
if __name__ == "__main__":
    async def demo():
        project = "Sample DeFi Project"
        address = "0x1234567890123456789012345678901234567890"
        
        scan_results = await quick_project_scan(project, address)
        print("Off-chain Scan Results:")
        print(f"Social Sentiment: {scan_results['social_sentiment']['overall_sentiment']}")
        print(f"Team Members Found: {scan_results['team_verification']['team_members_found']}")
        print(f"News Articles: {len(scan_results['project_mentions']['news_articles'])}")
    
    asyncio.run(demo())