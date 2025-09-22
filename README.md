# Veritas AI Agent - On-chain Auditor of Reputation and Facts

## Overview

Veritas is a decentralized AI agent that acts as an auditor for Web3 projects. It addresses the problem of misinformation, fraudulent claims, and hidden risks in the Web3 space by providing comprehensive trust scoring based on both on-chain and off-chain data analysis.

## Problem Statement

The Web3 space suffers from:
- **Misinformation**: Projects making false claims about partnerships or capabilities
- **Fraudulent activities**: Rug pulls, exit scams, and deceptive projects  
- **Hidden risks**: Wallet histories, centralized control, or poor tokenomics
- **Information asymmetry**: Incomplete data leading to poor investment decisions

## Solution

Veritas provides:
- **Comprehensive auditing**: Analysis of both on-chain and off-chain data sources
- **AI-powered insights**: Advanced pattern recognition and fraud detection
- **Trust scoring**: Confidence scores from 1-100 for easy decision making
- **Evidence-based reports**: Detailed breakdowns of positive factors and risks

## Features

### 🔗 On-Chain Analysis
- Smart contract verification status
- Transaction history and patterns
- Token distribution analysis
- Wallet interaction patterns
- Governance and ownership structure
- Security indicators and risk factors

### 🌐 Off-Chain Analysis  
- Social media sentiment analysis
- News articles and media coverage
- Team member verification
- Partnership claim validation
- Community engagement metrics
- Official source verification

### 🤖 AI-Powered Scoring
- GPT-5 powered analysis and insights
- Pattern recognition for fraud detection
- Confidence level assessment
- Risk factor identification
- Comprehensive reporting

## Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API key
- Internet connection for blockchain and web data

### Installation
```bash
# Clone or download the project files
# Install dependencies (handled automatically by Replit)

# Set your OpenAI API key as an environment variable
export OPENAI_API_KEY="your-api-key-here"
```

### Basic Usage

#### Interactive Mode
```bash
python main.py
```
This launches an interactive session where you can enter project addresses or names to audit.

#### Command Line Mode  
```bash
# Audit a specific contract
python main.py 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D

# Audit with project type specification
python main.py 0xA0b86a33E6417c5A2b2b7C8b4e7A6B22b69c0A17 token
```

#### Demo Mode
```bash
python main.py demo
```
Runs audits on sample well-known contracts to demonstrate functionality.

### Python API Usage

```python
import asyncio
from veritas_agent import VeritasAgent

async def audit_project():
    agent = VeritasAgent()
    
    # Audit a project
    score = await agent.audit_project("0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")
    
    print(f"Trust Score: {score.overall_score}/100")
    print(f"Confidence: {score.confidence_level:.1%}")
    print(f"Risk Factors: {len(score.risk_factors)}")
    
    # Export detailed report
    report = agent.export_report(score)
    with open("audit_report.json", "w") as f:
        f.write(report)

# Run the audit
asyncio.run(audit_project())
```

## Architecture

### Core Components

1. **VeritasAgent** (`veritas_agent.py`)
   - Main orchestrator for audit process
   - Combines on-chain and off-chain analysis
   - Generates trust scores using AI insights

2. **BlockchainAnalyzer** (`blockchain_analyzer.py`)
   - Multi-chain Web3 integration (Ethereum, Polygon, BSC)
   - Contract verification and analysis
   - Token distribution assessment
   - Transaction pattern analysis

3. **VeritasWebScraper** (`web_scraper.py`)
   - News and media source monitoring
   - Social media sentiment analysis
   - Team verification and credibility checks
   - Partnership claim validation

4. **Main Interface** (`main.py`)
   - CLI and interactive interfaces
   - Report generation and export
   - Demo and testing utilities

### Data Flow

```
Project Input → Data Collection → Analysis → AI Scoring → Trust Score
     ↓              ↓              ↓          ↓           ↓
   Address/    On-chain Data   Contract    Evidence    1-100 Score
   Name      Off-chain Data   Analysis    Analysis    + Confidence
                              Social      AI Insights  + Risk Factors
                              Sentiment   Pattern      + Positive Factors
                              Team Info   Recognition  + Detailed Report
```

## Scoring Algorithm

The trust score (1-100) is calculated using:

1. **Weighted Combination**:
   - On-chain score: 60% weight (more reliable)
   - Off-chain score: 40% weight

2. **On-Chain Factors**:
   - Contract verification (+20 points)
   - High transaction activity (+10 points)
   - Diverse user base (+10 points)
   - Security indicators (variable)
   - Risk factors (negative points)

3. **Off-Chain Factors**:
   - Positive social sentiment (+15 points)
   - Verified team members (+10 points)
   - Good media coverage (+10 points)
   - Active community engagement (+5 points)

4. **AI Analysis**:
   - Pattern recognition for fraud indicators
   - Confidence level assessment
   - Additional insights and recommendations

## Sample Output

```
🎯 VERITAS AUDIT RESULTS
============================================================
Project: 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D
Audit Date: 2024-01-15 14:30:22 UTC

🏆 Overall Trust Score: 84/100
🎯 Confidence Level: 85.0%

📊 Score Breakdown:
  On-chain Score:  80/100
  Off-chain Score: 90/100
  Visual Score: 🟢 [████████████████████] 84%

✅ Positive Factors (6):
  1. Contract source code verified
  2. Active usage (1500 transactions)
  3. Diverse user base (450 unique users)
  4. No obvious vulnerabilities
  5. Standard patterns used
  6. Positive social sentiment

⚠️  Risk Factors (2):
  1. Owner has full control
  2. No timelock on critical functions

🎯 Recommendation: 🟢 Good trust - Generally safe but monitor for changes
============================================================
```

## Supported Blockchains

- **Ethereum** (Primary)
- **Polygon** 
- **Binance Smart Chain (BSC)**
- **Arbitrum** (Configurable)
- **Optimism** (Configurable)

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: Required for AI analysis
- `WEB3_PROVIDER_URL`: Custom RPC endpoint (optional)
- `VERITAS_DEBUG`: Enable debug logging (optional)

### Chain Configuration
Blockchain settings can be modified in `blockchain_analyzer.py`:
```python
self.chain_configs = {
    ChainType.ETHEREUM: {
        "rpc_url": "https://eth.llamarpc.com",
        "explorer_api": "https://api.etherscan.io/api",
        "chain_id": 1
    },
    # Add more chains as needed
}
```

## Limitations & Known Issues

1. **AI API Costs**: OpenAI API usage can be expensive for large-scale analysis
2. **Rate Limits**: Subject to blockchain RPC and API rate limits
3. **Off-chain Data**: Some social media APIs require additional authentication
4. **Real-time Data**: Analysis reflects data at time of audit, not real-time
5. **Demo Level**: Current implementation includes placeholder data for some features

## Future Enhancements

### Planned Features
- [ ] Integration with additional social media APIs (Twitter, Discord, Telegram)
- [ ] Advanced smart contract security analysis
- [ ] Historical trend analysis and scoring
- [ ] Real-time monitoring and alerts
- [ ] Web dashboard and API endpoints
- [ ] Integration with DeFi protocols for liquidity analysis
- [ ] Machine learning model training on audit results

### Technical Improvements
- [ ] Async/await optimization for better performance
- [ ] Caching layer for blockchain data
- [ ] Enhanced error handling and retry mechanisms
- [ ] Comprehensive test suite
- [ ] Production deployment configuration

## Contributing

This is a proof-of-concept implementation. Key areas for contribution:
1. Enhanced off-chain data collection
2. Improved scoring algorithms
3. Additional blockchain support
4. Security auditing and testing
5. Performance optimization

## Security Considerations

- API keys are handled as environment variables
- No private key storage or transaction signing
- Read-only blockchain interactions
- Input validation for addresses and parameters
- Rate limiting consideration for API usage

## License

This project is for demonstration and educational purposes. Please ensure compliance with relevant APIs' terms of service.

## Support

For questions or issues:
1. Check the console output for detailed error messages
2. Verify API keys and network connectivity
3. Review the code comments for implementation details
4. Consider the limitations section for known issues

---

**Disclaimer**: Veritas is an analytical tool and should not be the sole basis for investment decisions. Always conduct additional research and due diligence when evaluating Web3 projects.