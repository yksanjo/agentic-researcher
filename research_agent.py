"""
Agentic Researcher - AI Research Assistant

An intelligent agent that autonomously researches topics by:
- Searching the web for relevant information
- Extracting key information from multiple sources
- Synthesizing findings into comprehensive reports
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import re


class ResearchState(Enum):
    IDLE = "idle"
    SEARCHING = "searching"
    EXTRACTING = "extracting"
    ANALYZING = "analyzing"
    SYNTHESIZING = "synthesizing"
    COMPLETE = "complete"
    ERROR = "error"


@dataclass
class Source:
    """A research source"""
    url: str
    title: str
    content: str = ""
    relevance: float = 0.0
    extracted_at: str = ""


@dataclass
class Finding:
    """A research finding"""
    topic: str
    content: str
    source: str
    confidence: float = 1.0
    key_points: list[str] = field(default_factory=list)


@dataclass
class ResearchReport:
    """Complete research report"""
    topic: str
    summary: str
    findings: list[Finding] = field(default_factory=list)
    sources: list[Source] = field(default_factory=list)
    key_insights: list[str] = field(default_factory=list)
    created_at: str = ""


class AgenticResearcher:
    """
    Autonomous research agent that:
    - Searches for relevant sources
    - Extracts key information
    - Synthesizes findings into reports
    """
    
    def __init__(self, scraper_agent=None, llm_provider=None):
        self.scraper = scraper_agent
        self.llm = llm_provider
        self.state = ResearchState.IDLE
        self.findings: list[Finding] = []
        self.sources: list[Source] = []
        self.action_history = []
        
    async def research(self, topic: str, depth: str = "medium") -> ResearchReport:
        """
        Research a topic and generate a comprehensive report.
        
        Args:
            topic: The research topic/question
            depth: Research depth (shallow, medium, deep)
            
        Returns:
            ResearchReport with findings and sources
        """
        self.state = ResearchState.SEARCHING
        self.log_action("research_started", {"topic": topic, "depth": depth})
        
        # Determine number of sources based on depth
        num_sources = {"shallow": 3, "medium": 5, "deep": 10}.get(depth, 5)
        
        try:
            # Step 1: Search for relevant sources
            sources = await self._find_sources(topic, num_sources)
            self.sources = sources
            
            # Step 2: Extract content from sources
            self.state = ResearchState.EXTRACTING
            await self._extract_from_sources(topic, sources)
            
            # Step 3: Analyze findings
            self.state = ResearchState.ANALYZING
            await self._analyze_findings(topic)
            
            # Step 4: Synthesize into report
            self.state = ResearchState.SYNTHESIZING
            report = await self._synthesize_report(topic)
            
            self.state = ResearchState.COMPLETE
            self.log_action("research_complete", {"findings": len(self.findings)})
            
            return report
            
        except Exception as e:
            self.state = ResearchState.ERROR
            return ResearchReport(
                topic=topic,
                summary=f"Error: {str(e)}"
            )
    
    async def _find_sources(self, topic: str, num_sources: int) -> list[Source]:
        """Find relevant sources for the topic"""
        
        # Generate search queries based on topic
        queries = self._generate_search_queries(topic)
        
        sources = []
        
        for query in queries:
            if len(sources) >= num_sources:
                break
                
            self.log_action("searching", {"query": query})
            
            # Use scraper to find sources (in demo mode, generate mock)
            if self.scraper:
                # Real scraping would go here
                pass
            
            # Generate mock sources for demo
            mock_sources = [
                Source(
                    url=f"https://example.com/{query.replace(' ', '-')}/1",
                    title=f"Article about {query} - Source 1",
                    relevance=0.9,
                    extracted_at=datetime.now().isoformat()
                ),
                Source(
                    url=f"https://example.com/{query.replace(' ', '-')}/2",
                    title=f"Guide to {query}",
                    relevance=0.8,
                    extracted_at=datetime.now().isoformat()
                )
            ]
            
            sources.extend(mock_sources)
        
        return sources[:num_sources]
    
    async def _extract_from_sources(self, topic: str, sources: list[Source]):
        """Extract relevant content from sources"""
        
        for source in sources:
            self.log_action("extracting", {"url": source.url})
            
            # Extract content (demo mode uses mock)
            content = await self._extract_content(source.url, topic)
            source.content = content
            
            # Extract key points
            finding = Finding(
                topic=topic,
                content=content[:500],  # First 500 chars
                source=source.url,
                key_points=self._extract_key_points(content)
            )
            
            self.findings.append(finding)
    
    async def _extract_content(self, url: str, topic: str) -> str:
        """Extract content from a URL"""
        
        # In demo mode, generate relevant mock content
        mock_content = f"""
        Research findings about {topic}:
        
        Key Information:
        - Overview: This is a comprehensive source about {topic}
        - The topic covers several important aspects
        - There are multiple perspectives on this subject
        
        Main Points:
        1. First key point about {topic}
        2. Second important aspect to consider
        3. Third notable finding from research
        
        Conclusion:
        Based on the analysis, {topic} is significant because it impacts
        various areas including technology, business, and society.
        """
        
        return mock_content.strip()
    
    def _extract_key_points(self, content: str) -> list[str]:
        """Extract key points from content"""
        
        # Simple extraction: look for bullet points and numbered items
        points = []
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith(('- ', '• ', '* ', '1.', '2.', '3.')):
                points.append(line.lstrip('-•*123. '))
        
        return points[:5]  # Limit to 5 key points
    
    async def _analyze_findings(self, topic: str):
        """Analyze and categorize findings"""
        
        # Use LLM if available for deeper analysis
        if self.llm:
            # Deep analysis would go here
            pass
        
        # Calculate relevance scores
        for finding in self.findings:
            # Simple keyword-based relevance
            topic_words = topic.lower().split()
            content_lower = finding.content.lower()
            
            matches = sum(1 for word in topic_words if word in content_lower)
            finding.confidence = min(matches / len(topic_words), 1.0)
        
        # Sort by confidence
        self.findings.sort(key=lambda f: f.confidence, reverse=True)
    
    async def _synthesize_report(self, topic: str) -> ResearchReport:
        """Synthesize all findings into a comprehensive report"""
        
        # Generate summary
        if self.llm:
            summary = await self.llm.generate(
                f"Summarize research on {topic} based on these findings:\n"
                + "\n".join(f.content for f in self.findings[:5])
            )
        else:
            summary = self._generate_summary(topic)
        
        # Extract key insights
        insights = self._generate_insights()
        
        return ResearchReport(
            topic=topic,
            summary=summary,
            findings=self.findings,
            sources=self.sources,
            key_insights=insights,
            created_at=datetime.now().isoformat()
        )
    
    def _generate_summary(self, topic: str) -> str:
        """Generate a summary of the research"""
        
        num_findings = len(self.findings)
        num_sources = len(self.sources)
        
        return f"""
        Research on '{topic}' completed successfully.
        
        This report contains {num_findings} key findings from {num_sources} sources.
        The research covers various aspects of {topic} including main concepts,
        important considerations, and practical applications.
        
        See key insights below for the most important takeaways.
        """.strip()
    
    def _generate_insights(self) -> list[str]:
        """Generate key insights from findings"""
        
        insights = []
        
        # Collect unique key points
        all_points = []
        for finding in self.findings:
            all_points.extend(finding.key_points)
        
        # Deduplicate and limit
        seen = set()
        for point in all_points:
            if point not in seen and len(insights) < 5:
                insights.append(point)
                seen.add(point)
        
        return insights
    
    def _generate_search_queries(self, topic: str) -> list[str]:
        """Generate search queries from a topic"""
        
        # Generate related queries
        base_topic = topic.lower()
        
        queries = [
            base_topic,
            f"what is {base_topic}",
            f"{base_topic} guide",
            f"best practices {base_topic}",
            f"{base_topic} tutorial"
        ]
        
        return queries
    
    def log_action(self, action: str, params: dict):
        """Log an action"""
        self.action_history.append({
            "action": action,
            "params": params,
            "timestamp": datetime.now().isoformat(),
            "state": self.state.value
        })
    
    def get_status(self) -> dict:
        """Get current agent status"""
        return {
            "state": self.state.value,
            "findings_count": len(self.findings),
            "sources_count": len(self.sources),
            "actions_taken": len(self.action_history)
        }


class MultiTopicResearcher:
    """Research agent that can handle multiple topics"""
    
    def __init__(self):
        self.researcher = AgenticResearcher()
    
    async def research_topics(self, topics: list[str], depth: str = "medium") -> dict:
        """Research multiple topics"""
        
        results = {}
        
        for topic in topics:
            report = await self.researcher.research(topic, depth)
            results[topic] = report
        
        return results


# Demo function
async def demo():
    """Demo the research agent"""
    print("🔬 Agentic Researcher - Demo")
    print("=" * 50)
    
    # Create researcher
    researcher = AgenticResearcher()
    
    # Research a topic
    report = await researcher.research("artificial intelligence trends", depth="medium")
    
    # Print results
    print(f"\n📊 Research Report: {report.topic}")
    print(f"📅 Created: {report.created_at}")
    print(f"\n📝 Summary:\n{report.summary}")
    
    print(f"\n🔍 Key Insights ({len(report.key_insights)}):")
    for i, insight in enumerate(report.key_insights, 1):
        print(f"  {i}. {insight}")
    
    print(f"\n📚 Sources ({len(report.sources)}):")
    for source in report.sources[:3]:
        print(f"  - {source.title}: {source.url}")
    
    print(f"\n✅ Status: {researcher.get_status()}")
    
    return report


if __name__ == "__main__":
    asyncio.run(demo())
