# 🔬 Agentic Researcher

AI-powered research assistant that autonomously researches topics by searching, extracting, and synthesizing information from the web.

## Features

- **Autonomous Research**: Searches and extracts information from multiple sources
- **Source Analysis**: Evaluates relevance and confidence of sources
- **Report Synthesis**: Generates comprehensive research reports with key insights
- **Multi-depth Research**: Shallow, medium, or deep research levels

## Installation

```bash
cd agentic-researcher
pip install -r requirements.txt
```

## Usage

```python
import asyncio
from research_agent import AgenticResearcher

async def main():
    researcher = AgenticResearcher()
    report = await researcher.research("artificial intelligence trends", depth="medium")
    print(report.summary)

asyncio.run(main())
```

## Research Depth

- **shallow**: 3 sources, quick overview
- **medium**: 5 sources, balanced research
- **deep**: 10 sources, comprehensive analysis

## API Reference

### AgenticResearcher

```python
agent = AgenticResearcher()
report = await agent.research(topic, depth="medium")
```

Returns `ResearchReport` with:
- `topic`: Research topic
- `summary`: Synthesized summary
- `findings`: List of findings
- `sources`: List of sources
- `key_insights`: Key takeaways
