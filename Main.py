#!/usr/bin/env python3
"""
Veritas Agent - Main Interface
Entry point for the Veritas AI agent that audits Web3 projects
"""

import asyncio
import sys
import json
from datetime import datetime
from veritas_agent import VeritasAgent
from blockchain_analyzer import ChainType

async def main():
    """Main entry point for Veritas agent"""
    print("🔍 Veritas AI Agent - On-chain Auditor of Reputation and Facts")
    print("=" * 60)
    
    # Initialize the agent
    agent = VeritasAgent()
    
    # Interactive mode for testing
    if len(sys.argv) < 2:
        print("Interactive mode - Enter project address or name to audit")
        print("Examples:")
        print("  - Contract address: 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")
        print("  - Project name: Uniswap")
        print("  - Type 'quit' to exit")
        print()
        
        while True:
            try:
                project_input = input("Enter project to audit: ").strip()
                
                if project_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not project_input:
                    continue
                
                print(f"\n🚀 Starting audit for: {project_input}")
                score = await agent.audit_project(project_input)
                
                # Display results
                display_audit_results(score, project_input)
                
                # Ask if user wants to export report
                export_choice = input("\nExport detailed report? (y/n): ").strip().lower()
                if export_choice in ['y', 'yes']:
                    report = agent.export_report(score)
                    filename = f"veritas_report_{project_input.replace('/', '_')[:20]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    with open(filename, 'w') as f:
                        f.write(report)
                    print(f"📄 Report saved to: {filename}")
                
                print("\n" + "-" * 60 + "\n")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error during audit: {e}")
                print("Please try again with a different project.")
    
    else:
        # Command line mode
        project_identifier = sys.argv[1]
        project_type = sys.argv[2] if len(sys.argv) > 2 else "contract"
        
        print(f"🚀 Auditing project: {project_identifier}")
        try:
            score = await agent.audit_project(project_identifier, project_type)
            display_audit_results(score, project_identifier)
            
            # Auto-export report in CLI mode
            report = agent.export_report(score)
            filename = f"veritas_report_{project_identifier.replace('/', '_')[:20]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                f.write(report)
            print(f"📄 Detailed report saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Audit failed: {e}")
            sys.exit(1)

def display_audit_results(score, project_identifier):
    """Display formatted audit results"""
    print("\n" + "=" * 60)
    print("🎯 VERITAS AUDIT RESULTS")
    print("=" * 60)
    print(f"Project: {project_identifier}")
    print(f"Audit Date: {score.analysis_timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print()
    
    # Overall score with visual indicator
    print(f"🏆 Overall Trust Score: {score.overall_score}/100")
    print(f"🎯 Confidence Level: {score.confidence_level:.1%}")
    
    # Score breakdown
    print("\n📊 Score Breakdown:")
    print(f"  On-chain Score:  {score.on_chain_score}/100")
    print(f"  Off-chain Score: {score.off_chain_score}/100")
    
    # Visual score indicator
    score_bar = get_score_bar(score.overall_score)
    print(f"  Visual Score: {score_bar}")
    
    # Positive factors
    if score.positive_factors:
        print(f"\n✅ Positive Factors ({len(score.positive_factors)}):")
        for i, factor in enumerate(score.positive_factors[:10], 1):  # Limit to top 10
            print(f"  {i}. {factor}")
        if len(score.positive_factors) > 10:
            print(f"  ... and {len(score.positive_factors) - 10} more")
    
    # Risk factors
    if score.risk_factors:
        print(f"\n⚠️  Risk Factors ({len(score.risk_factors)}):")
        for i, risk in enumerate(score.risk_factors[:10], 1):  # Limit to top 10
            print(f"  {i}. {risk}")
        if len(score.risk_factors) > 10:
            print(f"  ... and {len(score.risk_factors) - 10} more")
    
    # Overall recommendation
    recommendation = get_recommendation(score.overall_score, score.confidence_level)
    print(f"\n🎯 Recommendation: {recommendation}")
    
    print("=" * 60)

def get_score_bar(score):
    """Generate a visual score bar"""
    bar_length = 20
    filled_length = int(bar_length * score / 100)
    bar = "█" * filled_length + "░" * (bar_length - filled_length)
    
    if score >= 80:
        color = "🟢"
    elif score >= 60:
        color = "🟡"
    elif score >= 40:
        color = "🟠"
    else:
        color = "🔴"
    
    return f"{color} [{bar}] {score}%"

def get_recommendation(score, confidence):
    """Generate recommendation based on score and confidence"""
    if confidence < 0.5:
        return "❓ Low confidence - Manual review strongly recommended"
    
    if score >= 85:
        return "✅ High trust - Project appears legitimate with strong indicators"
    elif score >= 70:
        return "🟢 Good trust - Generally safe but monitor for changes"
    elif score >= 55:
        return "🟡 Moderate trust - Proceed with caution and additional research"
    elif score >= 40:
        return "🟠 Low trust - High risk, extensive due diligence required"
    else:
        return "🔴 Very low trust - Avoid or consider fraudulent"

# Quick audit function for simple command-line usage
async def quick_audit(project_address: str):
    """Quick audit function for API or simple usage"""
    agent = VeritasAgent()
    try:
        score = await agent.audit_project(project_address)
        return {
            "success": True,
            "overall_score": score.overall_score,
            "confidence": score.confidence_level,
            "on_chain_score": score.on_chain_score,
            "off_chain_score": score.off_chain_score,
            "risk_count": len(score.risk_factors),
            "positive_count": len(score.positive_factors),
            "timestamp": score.analysis_timestamp.isoformat(),
            "recommendation": get_recommendation(score.overall_score, score.confidence_level)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# Example usage for different project types
async def demo_audits():
    """Demo function showing different audit scenarios"""
    print("🎭 Veritas Agent Demo - Sample Audits")
    print("=" * 50)
    
    # Sample projects to audit (these are real contracts for demonstration)
    sample_projects = [
        {
            "name": "Uniswap V2 Router",
            "address": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
            "type": "contract"
        },
        {
            "name": "USDC Token", 
            "address": "0xA0b86a33E6417c5A2b2b7C8b4e7A6B22b69c0A17", 
            "type": "token"
        },
        {
            "name": "Chainlink Price Feed",
            "address": "0x5f4ec3df9cbd43714fe2740f5e3616155c5b8419",
            "type": "oracle"
        }
    ]
    
    agent = VeritasAgent()
    
    for project in sample_projects:
        print(f"\n📋 Auditing: {project['name']}")
        print(f"Address: {project['address']}")
        print("-" * 30)
        
        try:
            result = await quick_audit(project['address'])
            if result['success']:
                print(f"Score: {result['overall_score']}/100")
                print(f"Confidence: {result['confidence']:.1%}")
                print(f"Recommendation: {result['recommendation']}")
            else:
                print(f"❌ Audit failed: {result['error']}")
        except Exception as e:
            print(f"❌ Demo error: {e}")
        
        print()

if __name__ == "__main__":
    # Check if demo mode
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        asyncio.run(demo_audits())
    else:
        asyncio.run(main())