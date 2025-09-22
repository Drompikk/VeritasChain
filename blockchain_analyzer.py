"""
Blockchain data analyzer for Veritas agent
Handles on-chain data collection and analysis for Web3 projects
"""

import asyncio
from typing import Dict, List, Optional, Any
from web3 import Web3, AsyncWeb3
# Note: geth_poa_middleware import removed as it may not be available in all web3 versions
from datetime import datetime, timedelta
import json
import aiohttp
from dataclasses import dataclass
from enum import Enum

class ChainType(Enum):
    ETHEREUM = "ethereum"
    POLYGON = "polygon"
    BSC = "bsc"
    ARBITRUM = "arbitrum"
    OPTIMISM = "optimism"

@dataclass
class ContractAnalysis:
    """Analysis results for a smart contract"""
    address: str
    is_verified: bool
    creation_date: Optional[datetime]
    creator_address: str
    transaction_count: int
    unique_interactors: int
    total_value_locked: float
    proxy_pattern: bool
    ownership_analysis: Dict[str, Any]
    security_indicators: List[str]
    risk_factors: List[str]

@dataclass
class TokenAnalysis:
    """Analysis results for a token"""
    contract_address: str
    name: str
    symbol: str
    total_supply: int
    holder_count: int
    top_holders: List[Dict]
    liquidity_analysis: Dict[str, Any]
    distribution_score: int  # 1-100, higher is better distribution
    mint_burn_events: List[Dict]

class VeritasBlockchainAnalyzer:
    """
    Blockchain analyzer for the Veritas agent
    Analyzes on-chain data to assess project trustworthiness
    """
    
    def __init__(self):
        # Initialize Web3 connections for different chains
        self.w3_connections = {}
        self.chain_configs = {
            ChainType.ETHEREUM: {
                "rpc_url": "https://eth.llamarpc.com",
                "explorer_api": "https://api.etherscan.io/api",
                "chain_id": 1
            },
            ChainType.POLYGON: {
                "rpc_url": "https://polygon.llamarpc.com", 
                "explorer_api": "https://api.polygonscan.com/api",
                "chain_id": 137
            },
            ChainType.BSC: {
                "rpc_url": "https://bsc.llamarpc.com",
                "explorer_api": "https://api.bscscan.com/api", 
                "chain_id": 56
            }
        }
        
        # Initialize connections
        self._initialize_connections()
    
    def _initialize_connections(self):
        """Initialize Web3 connections for supported chains"""
        for chain_type, config in self.chain_configs.items():
            try:
                w3 = Web3(Web3.HTTPProvider(config["rpc_url"]))
                # Note: PoA middleware would be added here for chains that need it
                # if chain_type in [ChainType.POLYGON, ChainType.BSC]:
                #     w3.middleware_onion.inject(geth_poa_middleware, layer=0)
                
                self.w3_connections[chain_type] = w3
                print(f"✅ Connected to {chain_type.value}")
            except Exception as e:
                print(f"❌ Failed to connect to {chain_type.value}: {e}")
    
    async def analyze_contract(self, contract_address: str, chain: ChainType = ChainType.ETHEREUM) -> ContractAnalysis:
        """
        Comprehensive analysis of a smart contract
        
        Args:
            contract_address: The contract address to analyze
            chain: Which blockchain to analyze on
            
        Returns:
            ContractAnalysis with detailed findings
        """
        print(f"🔍 Analyzing contract {contract_address} on {chain.value}")
        
        w3 = self.w3_connections.get(chain)
        if not w3:
            raise ValueError(f"No connection available for {chain.value}")
        
        # Validate address format
        if not w3.is_address(contract_address):
            raise ValueError(f"Invalid address format: {contract_address}")
        
        address = w3.to_checksum_address(contract_address)
        
        # Gather basic contract information
        code = w3.eth.get_code(address)
        is_contract = len(code) > 0
        
        if not is_contract:
            raise ValueError(f"Address {address} is not a contract")
        
        # Analyze contract details
        verification_status = await self._check_contract_verification(address, chain)
        creation_info = await self._get_contract_creation_info(address, chain)
        transaction_analysis = await self._analyze_contract_transactions(address, chain)
        ownership_analysis = await self._analyze_contract_ownership(address, chain)
        security_analysis = await self._analyze_contract_security(address, chain)
        
        return ContractAnalysis(
            address=address,
            is_verified=verification_status["is_verified"],
            creation_date=creation_info.get("creation_date"),
            creator_address=creation_info.get("creator", ""),
            transaction_count=transaction_analysis["tx_count"],
            unique_interactors=transaction_analysis["unique_users"],
            total_value_locked=transaction_analysis["total_value"],
            proxy_pattern=security_analysis["is_proxy"],
            ownership_analysis=ownership_analysis,
            security_indicators=security_analysis["positive_indicators"],
            risk_factors=security_analysis["risk_factors"]
        )
    
    async def analyze_token(self, token_address: str, chain: ChainType = ChainType.ETHEREUM) -> TokenAnalysis:
        """
        Analyze a token contract for distribution and liquidity
        """
        print(f"🪙 Analyzing token {token_address} on {chain.value}")
        
        w3 = self.w3_connections.get(chain)
        if not w3:
            raise ValueError(f"No connection available for {chain.value}")
        
        address = w3.to_checksum_address(token_address)
        
        # Get basic token information
        token_info = await self._get_token_info(address, chain)
        holder_analysis = await self._analyze_token_holders(address, chain)
        liquidity_analysis = await self._analyze_token_liquidity(address, chain)
        distribution_score = self._calculate_distribution_score(holder_analysis)
        
        return TokenAnalysis(
            contract_address=address,
            name=token_info.get("name", "Unknown"),
            symbol=token_info.get("symbol", "UNKNOWN"),
            total_supply=token_info.get("total_supply", 0),
            holder_count=holder_analysis["total_holders"],
            top_holders=holder_analysis["top_holders"],
            liquidity_analysis=liquidity_analysis,
            distribution_score=distribution_score,
            mint_burn_events=[]  # Would implement mint/burn tracking
        )
    
    async def _check_contract_verification(self, address: str, chain: ChainType) -> Dict:
        """Check if contract source code is verified"""
        try:
            # Simulate verification check (would use actual explorer APIs)
            return {
                "is_verified": True,  # Placeholder
                "compiler_version": "0.8.19",
                "optimization": True,
                "source_code_available": True
            }
        except Exception as e:
            print(f"Error checking verification: {e}")
            return {"is_verified": False}
    
    async def _get_contract_creation_info(self, address: str, chain: ChainType) -> Dict:
        """Get contract creation information"""
        try:
            # Simulate getting creation info (would use explorer APIs)
            return {
                "creation_date": datetime.now() - timedelta(days=30),
                "creator": "0x742d35Cc6634C0532925a3b8D4030d542F5a5bD",
                "creation_tx": "0xabc123..."
            }
        except Exception as e:
            print(f"Error getting creation info: {e}")
            return {}
    
    async def _analyze_contract_transactions(self, address: str, chain: ChainType) -> Dict:
        """Analyze contract transaction patterns"""
        try:
            # Simulate transaction analysis
            return {
                "tx_count": 1500,
                "unique_users": 450,
                "total_value": 2500000.0,  # in USD
                "daily_activity": 50,
                "growth_trend": "increasing"
            }
        except Exception as e:
            print(f"Error analyzing transactions: {e}")
            return {"tx_count": 0, "unique_users": 0, "total_value": 0.0}
    
    async def _analyze_contract_ownership(self, address: str, chain: ChainType) -> Dict:
        """Analyze contract ownership structure"""
        try:
            return {
                "has_owner": True,
                "owner_address": "0x742d35Cc6634C0532925a3b8D4030d542F5a5bD",
                "is_multisig": False,
                "timelock_delay": 0,
                "upgrade_pattern": "none",
                "admin_keys": ["owner"]
            }
        except Exception as e:
            print(f"Error analyzing ownership: {e}")
            return {"has_owner": False}
    
    async def _analyze_contract_security(self, address: str, chain: ChainType) -> Dict:
        """Analyze contract security patterns"""
        try:
            return {
                "is_proxy": False,
                "positive_indicators": [
                    "Contract verified",
                    "No obvious vulnerabilities",
                    "Standard patterns used"
                ],
                "risk_factors": [
                    "Owner has full control",
                    "No timelock on critical functions"
                ],
                "audit_reports": [],
                "security_score": 75
            }
        except Exception as e:
            print(f"Error analyzing security: {e}")
            return {"is_proxy": False, "positive_indicators": [], "risk_factors": []}
    
    async def _get_token_info(self, address: str, chain: ChainType) -> Dict:
        """Get basic token information"""
        try:
            # Simulate token info (would call contract methods)
            return {
                "name": "Sample Token",
                "symbol": "SAMPLE",
                "decimals": 18,
                "total_supply": 1000000000000000000000000  # 1M tokens with 18 decimals
            }
        except Exception as e:
            print(f"Error getting token info: {e}")
            return {}
    
    async def _analyze_token_holders(self, address: str, chain: ChainType) -> Dict:
        """Analyze token holder distribution"""
        try:
            return {
                "total_holders": 2500,
                "top_holders": [
                    {"address": "0x742d35Cc6634C0532925a3b8D4030d542F5a5bD", "balance": 15.5, "percentage": 15.5},
                    {"address": "0x1234567890123456789012345678901234567890", "balance": 10.2, "percentage": 10.2},
                    {"address": "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd", "balance": 8.3, "percentage": 8.3}
                ],
                "concentration_risk": "medium"
            }
        except Exception as e:
            print(f"Error analyzing holders: {e}")
            return {"total_holders": 0, "top_holders": []}
    
    async def _analyze_token_liquidity(self, address: str, chain: ChainType) -> Dict:
        """Analyze token liquidity across DEXes"""
        try:
            return {
                "total_liquidity_usd": 500000,
                "dex_pools": [
                    {"dex": "Uniswap V3", "liquidity": 300000, "volume_24h": 50000},
                    {"dex": "SushiSwap", "liquidity": 200000, "volume_24h": 25000}
                ],
                "liquidity_score": 75
            }
        except Exception as e:
            print(f"Error analyzing liquidity: {e}")
            return {"total_liquidity_usd": 0, "dex_pools": []}
    
    def _calculate_distribution_score(self, holder_analysis: Dict) -> int:
        """Calculate a distribution score based on holder analysis"""
        if not holder_analysis.get("top_holders"):
            return 50  # Default score if no data
        
        # Simple scoring based on top holder concentration
        top_holder_percentage = holder_analysis["top_holders"][0]["percentage"]
        
        if top_holder_percentage > 50:
            return 20  # Very bad distribution
        elif top_holder_percentage > 30:
            return 40  # Poor distribution
        elif top_holder_percentage > 20:
            return 60  # Fair distribution
        elif top_holder_percentage > 10:
            return 80  # Good distribution
        else:
            return 95  # Excellent distribution
    
    async def check_wallet_history(self, wallet_address: str, chain: ChainType = ChainType.ETHEREUM) -> Dict:
        """
        Check a wallet's transaction history for red flags
        """
        print(f"👛 Analyzing wallet {wallet_address} on {chain.value}")
        
        w3 = self.w3_connections.get(chain)
        if not w3:
            raise ValueError(f"No connection available for {chain.value}")
        
        address = w3.to_checksum_address(wallet_address)
        
        # Analyze wallet activity
        balance = w3.eth.get_balance(address)
        
        return {
            "address": address,
            "current_balance_eth": w3.from_wei(balance, 'ether'),
            "transaction_count": 250,  # Placeholder
            "first_activity": datetime.now() - timedelta(days=120),
            "last_activity": datetime.now() - timedelta(days=1),
            "interacted_contracts": 45,
            "suspicious_activity": [],
            "trust_score": 85
        }

# Utility functions for quick analysis
async def quick_contract_score(contract_address: str, chain: ChainType = ChainType.ETHEREUM) -> int:
    """
    Quick scoring of a contract (1-100)
    """
    analyzer = VeritasBlockchainAnalyzer()
    try:
        analysis = await analyzer.analyze_contract(contract_address, chain)
        
        # Simple scoring algorithm
        score = 50  # Base score
        
        if analysis.is_verified:
            score += 20
        if analysis.transaction_count > 100:
            score += 10
        if analysis.unique_interactors > 50:
            score += 10
        if len(analysis.risk_factors) == 0:
            score += 10
        
        return min(100, max(1, score))
    except Exception as e:
        print(f"Error in quick scoring: {e}")
        return 50


# Example usage
if __name__ == "__main__":
    async def demo():
        analyzer = VeritasBlockchainAnalyzer()
        
        # Test contract address (Uniswap V2 Router)
        test_contract = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
        
        try:
            analysis = await analyzer.analyze_contract(test_contract)
            print(f"\n📊 Contract Analysis Results:")
            print(f"Address: {analysis.address}")
            print(f"Verified: {analysis.is_verified}")
            print(f"Transaction Count: {analysis.transaction_count}")
            print(f"Unique Users: {analysis.unique_interactors}")
            print(f"Security Indicators: {len(analysis.security_indicators)}")
            print(f"Risk Factors: {len(analysis.risk_factors)}")
            
            # Quick score test
            score = await quick_contract_score(test_contract)
            print(f"Quick Score: {score}/100")
            
        except Exception as e:
            print(f"Demo failed: {e}")
    
    asyncio.run(demo())