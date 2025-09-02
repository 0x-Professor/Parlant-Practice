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


@p.tool
async def github_get_issue_details(context: p.ToolContext, issue_id: int) -> p.ToolResult:
    # Simulate fetching details of an issue from a GitHub repository
    issue = {"id": issue_id, "title": "Bug in authentication", "status": "open", "description": "Detailed description of the issue."}
    return p.ToolResult(data=issue, control={"lifespan": "session"})

@p.tool
async def github_create_issue(context: p.ToolContext, title: str, description: str) -> p.ToolResult:
    # Simulate creating a new issue in a GitHub repository
    new_issue = {"id": 3, "title": title, "status": "open", "description": description}
    return p.ToolResult(data=new_issue, control={"lifespan": "session"})

