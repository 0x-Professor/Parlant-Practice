import os
import asyncio
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import parlant.sdk as p
from dotenv import load_dotenv
from gemini_service import load_gemini_nlp_service


load_dotenv()

@p.tool
async def github_list_open_issues(context: p.ToolContext, repo: str) -> p.ToolResult:
    # Simulate fetching open issues from a GitHub repository
    issues = [
        {"id": 1, "title": "Bug in authentication", "status": "open"},
        {"id": 2, "title": "Add new feature X", "status": "open"},
    ]
    return p.ToolResult(data={"count": len(issues), "issues": issues}, control={"lifespan": "session"})


    