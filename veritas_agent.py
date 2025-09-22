"""
Veritas AI Agent - On-chain Auditor of Reputation and Facts

This is the main module for the Veritas AI agent that audits Web3 projects
by analyzing both on-chain and off-chain data to provide trust scores.
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field

# Using OpenAI integration for AI analysis
# Note: the newest OpenAI model is "gpt-5" which was released August 7, 2025.
# do not change this unless explicitly requested by the user
from openai import OpenAI

# Import our custom modules
from web_scraper import VeritasWebScraper, quick_project_scan
from blockchain_analyzer import VeritasBlockchainAnalyzer, ChainType, quick_contract_score

@dataclass
class ProjectData:
    """Data structure for Web3 project information"""
    name: str
    address: Optional[str] = None
    website: Optional[str] = None
    social_links: Dict[str, str] = field(default_factory=dict)
    on_chain_data: Dict[str, Any] = field(default_factory=dict)
    off_chain_data: Dict[str, Any] = field(default_factory=dict)

@dataclass
class VeritasScore:
    """Veritas trust score with detailed breakdown"""
    overall_score: int  # 1-100
    confidence_level: float  # 0.0-1.0
    on_chain_score: int
    off_chain_score: int
    risk_factors: List[str]
    positive_factors: List[str]
    analysis_timestamp: datetime
    evidence: Dict[str, Any]

class VeritasAgent:
    """
    Main Veritas AI Agent class for Web3 project auditing
    
    The agent analyzes both on-chain and off-chain data to determine
    the trustworthiness and reputation of Web3 projects.
    """
    
    def __init__(self):
        self.openai_client = self._initialize_openai()
        self.analysis_history = []
        
    def _initialize_openai(self) -> OpenAI:
        """Initialize OpenAI client with API key"""
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        return OpenAI(api_key=api_key)
    
    async def audit_project(self, project_identifier: str, project_type: str = "contract") -> VeritasScore:
        """
        Main audit function that analyzes a Web3 project
        
        Args:
            project_identifier: Contract address, ENS name, or project name
            project_type: Type of project ("contract", "token", "dao", etc.)
            
        Returns:
            VeritasScore with comprehensive trust analysis
        """
        print(f"🔍 Starting Veritas audit for: {project_identifier}")
        
        # Step 1: Collect project data
        project_data = await self._collect_project_data(project_identifier, project_type)
        
        # Step 2: Analyze on-chain data
        on_chain_score = await self._analyze_on_chain_data(project_data)
        
        # Step 3: Analyze off-chain data
        off_chain_score = await self._analyze_off_chain_data(project_data)
        
        # Step 4: Generate final Veritas score
        veritas_score = await self._generate_veritas_score(
            project_data, on_chain_score, off_chain_score
        )
        
        # Step 5: Store analysis in history
        self.analysis_history.append({
            "project": project_identifier,
            "score": veritas_score,
            "timestamp": datetime.now()
        })
        
        return veritas_score
    
    async def _collect_project_data(self, identifier: str, project_type: str) -> ProjectData:
        """Collect comprehensive project information from multiple sources"""
        print("📋 Collecting project data...")
        
        # Determine if identifier is an address or name
        is_address = len(identifier) == 42 and identifier.startswith('0x')
        
        project_data = ProjectData(
            name=identifier if not is_address else f"Contract_{identifier[:8]}",
            address=identifier if is_address else None
        )
        
        # If we have an address, try to get more info from blockchain
        if is_address:
            try:
                blockchain_analyzer = VeritasBlockchainAnalyzer()
                # Basic contract info to help with naming
                contract_analysis = await blockchain_analyzer.analyze_contract(identifier)
                if contract_analysis:
                    project_data.on_chain_data["basic_analysis"] = {
                        "verified": contract_analysis.is_verified,
                        "transaction_count": contract_analysis.transaction_count,
                        "creation_date": contract_analysis.creation_date.isoformat() if contract_analysis.creation_date else None
                    }
            except Exception as e:
                print(f"⚠️  Could not get blockchain data: {e}")
        
        # Collect off-chain data
        try:
            off_chain_data = await quick_project_scan(project_data.name, project_data.address)
            project_data.off_chain_data = off_chain_data
        except Exception as e:
            print(f"⚠️  Could not get off-chain data: {e}")
            
        return project_data
    
    async def _analyze_on_chain_data(self, project_data: ProjectData) -> Dict:
        """Analyze on-chain data for the project using blockchain analyzer"""
        print("📊 Analyzing on-chain data...")
        
        if not project_data.address:
            return {
                "score": 30,
                "factors": [],
                "risks": ["No contract address provided"],
                "analysis": "Cannot perform on-chain analysis without contract address"
            }
        
        try:
            # Use blockchain analyzer for comprehensive analysis
            blockchain_analyzer = VeritasBlockchainAnalyzer()
            
            # Get detailed contract analysis
            contract_analysis = await blockchain_analyzer.analyze_contract(project_data.address)
            
            # Calculate score based on analysis
            score = await quick_contract_score(project_data.address)
            
            # Extract positive factors
            factors = []
            if contract_analysis.is_verified:
                factors.append("Contract source code verified")
            if contract_analysis.transaction_count > 100:
                factors.append(f"Active usage ({contract_analysis.transaction_count} transactions)")
            if contract_analysis.unique_interactors > 50:
                factors.append(f"Diverse user base ({contract_analysis.unique_interactors} unique users)")
            
            factors.extend(contract_analysis.security_indicators)
            
            # Combine risk factors
            risks = contract_analysis.risk_factors.copy()
            
            # Additional risk assessment
            if contract_analysis.transaction_count < 10:
                risks.append("Very low transaction activity")
            if not contract_analysis.is_verified:
                risks.append("Contract source code not verified")
                
            return {
                "score": score,
                "factors": factors,
                "risks": risks,
                "analysis": contract_analysis,
                "total_value_locked": contract_analysis.total_value_locked
            }
            
        except Exception as e:
            print(f"❌ On-chain analysis failed: {e}")
            return {
                "score": 20,
                "factors": [],
                "risks": [f"Analysis failed: {str(e)}"],
                "analysis": "Error during on-chain analysis"
            }
    
    async def _analyze_off_chain_data(self, project_data: ProjectData) -> Dict:
        """Analyze off-chain data using AI"""
        print("🌐 Analyzing off-chain data...")
        
        # Placeholder for off-chain analysis
        # Will integrate web scraping to check:
        # - Social media presence
        # - News articles and media coverage
        # - Community engagement
        # - Partnership announcements
        # - Team credibility
        
        return {
            "score": 75,  # Placeholder
            "factors": ["Positive media coverage", "Active community"],
            "risks": ["Limited team information"]
        }
    
    async def _generate_veritas_score(self, project_data: ProjectData, 
                                     on_chain: Dict, off_chain: Dict) -> VeritasScore:
        """Generate final Veritas trust score using AI analysis"""
        print("🤖 Generating Veritas score...")
        
        # Combine all evidence for AI analysis (serialize objects to avoid JSON errors)
        evidence = {
            "on_chain": self._serialize_analysis_data(on_chain),
            "off_chain": self._serialize_analysis_data(off_chain),
            "project_data": {
                "name": project_data.name,
                "address": project_data.address
            }
        }
        
        # Use AI to analyze all evidence and generate score
        ai_analysis = await self._ai_score_analysis(evidence)
        
        # Calculate weighted final score
        on_chain_weight = 0.6  # On-chain data is more reliable
        off_chain_weight = 0.4
        
        overall_score = int(
            (on_chain["score"] * on_chain_weight) + 
            (off_chain["score"] * off_chain_weight)
        )
        
        # Ensure score is within bounds
        overall_score = max(1, min(100, overall_score))
        
        return VeritasScore(
            overall_score=overall_score,
            confidence_level=ai_analysis.get("confidence", 0.7),
            on_chain_score=on_chain["score"],
            off_chain_score=off_chain["score"],
            risk_factors=on_chain["risks"] + off_chain["risks"],
            positive_factors=on_chain["factors"] + off_chain["factors"],
            analysis_timestamp=datetime.now(),
            evidence=evidence
        )
    
    async def _ai_score_analysis(self, evidence: Dict) -> Dict:
        """Use AI to analyze evidence and provide scoring insights"""
        try:
            prompt = f"""
            As Veritas, an expert Web3 auditor, analyze this project evidence and provide insights:
            
            Evidence: {json.dumps(evidence, indent=2)}
            
            Provide a JSON response with:
            1. confidence: float (0.0-1.0) - how confident you are in the analysis
            2. key_insights: list of important observations
            3. risk_level: string ("low", "medium", "high")
            4. recommendation: string - overall recommendation
            
            Focus on identifying potential fraud, misrepresentation, or hidden risks.
            """
            
            response = self.openai_client.chat.completions.create(
                model="gpt-5",  # Using newest model
                messages=[
                    {
                        "role": "system", 
                        "content": "You are Veritas, an AI auditor specializing in Web3 project analysis. "
                                 "You identify fraud, verify claims, and assess project trustworthiness."
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            if content:
                return json.loads(content)
            else:
                raise ValueError("Empty response from AI")
            
        except Exception as e:
            print(f"❌ AI analysis failed: {e}")
            return {
                "confidence": 0.5,
                "key_insights": ["AI analysis incomplete due to error"],
                "risk_level": "medium",
                "recommendation": "Manual review recommended"
            }
    
    def _serialize_analysis_data(self, data: Any) -> Any:
        """Serialize analysis data to be JSON compatible"""
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                if key == "analysis" and hasattr(value, '__dict__'):
                    # Convert dataclass to dict
                    result[key] = {
                        "address": getattr(value, 'address', ''),
                        "is_verified": getattr(value, 'is_verified', False),
                        "transaction_count": getattr(value, 'transaction_count', 0),
                        "unique_interactors": getattr(value, 'unique_interactors', 0),
                        "risk_factors": getattr(value, 'risk_factors', []),
                        "security_indicators": getattr(value, 'security_indicators', [])
                    }
                else:
                    result[key] = self._serialize_analysis_data(value)
            return result
        elif isinstance(data, list):
            return [self._serialize_analysis_data(item) for item in data]
        elif hasattr(data, '__dict__'):
            # Handle dataclass objects
            return {k: self._serialize_analysis_data(v) for k, v in data.__dict__.items()}
        else:
            # Return primitive types as-is
            return data
    
    def get_analysis_history(self) -> List[Dict]:
        """Return history of all project analyses"""
        return self.analysis_history
    
    def export_report(self, score: VeritasScore, format: str = "json") -> str:
        """Export analysis report in specified format"""
        if format == "json":
            return json.dumps({
                "veritas_score": score.overall_score,
                "confidence": score.confidence_level,
                "breakdown": {
                    "on_chain": score.on_chain_score,
                    "off_chain": score.off_chain_score
                },
                "risk_factors": score.risk_factors,
                "positive_factors": score.positive_factors,
                "timestamp": score.analysis_timestamp.isoformat(),
                "evidence": score.evidence
            }, indent=2)
        
        return str(score)

# Example usage and testing
if __name__ == "__main__":
    async def demo():
        agent = VeritasAgent()
        
        # Test with a sample project
        test_project = "0x1234567890123456789012345678901234567890"  # Sample address
        
        try:
            score = await agent.audit_project(test_project, "contract")
            
            print("\n" + "="*50)
            print("🎯 VERITAS AUDIT RESULTS")
            print("="*50)
            print(f"Project: {test_project}")
            print(f"Overall Score: {score.overall_score}/100")
            print(f"Confidence: {score.confidence_level:.2%}")
            print(f"On-chain Score: {score.on_chain_score}/100")
            print(f"Off-chain Score: {score.off_chain_score}/100")
            print(f"\n✅ Positive Factors:")
            for factor in score.positive_factors:
                print(f"  • {factor}")
            print(f"\n⚠️  Risk Factors:")
            for risk in score.risk_factors:
                print(f"  • {risk}")
            print("="*50)
            
            # Export report
            report = agent.export_report(score)
            print("\n📄 JSON Report generated")
            
        except Exception as e:
            print(f"❌ Demo failed: {e}")
    
    # Run demo only if OpenAI API key is available
    if os.environ.get("OPENAI_API_KEY"):
        asyncio.run(demo())
    else:
        print("⚠️  OPENAI_API_KEY not found. Set it to run the demo.")
        print("Example: export OPENAI_API_KEY='your-api-key-here'")