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

@p.tool
async def github_close_issue(context: p.ToolContext, issue_id: int) -> p.ToolResult:
    # Simulate closing an issue in a GitHub repository
    return p.ToolResult(data={"id": issue_id, "status": "closed"}, control={"lifespan": "session"})

@p.tool
async def github_reopen_issue(context: p.ToolContext, issue_id: int) -> p.ToolResult:
    # Simulate reopening an issue in a GitHub repository
    return p.ToolResult(data={"id": issue_id, "status": "reopened"}, control={"lifespan": "session"})

@p.tool
async def github_list_pull_requests(context: p.ToolContext, repo: str) -> p.ToolResult:
    # Simulate fetching open pull requests from a GitHub repository
    pull_requests = [
        {"id": 1, "title": "Implement feature Y", "status": "open"},
        {"id": 2, "title": "Fix bug in feature Z", "status": "open"},
    ]
    return p.ToolResult(data={"count": len(pull_requests), "pull_requests": pull_requests}, control={"lifespan": "session"})

@p.tool
async def github_get_pull_request_details(context: p.ToolContext, pr_id: int) -> p.ToolResult:
    # Simulate fetching details of a pull request from a GitHub repository
    pull_request = {"id": pr_id, "title": "Implement feature Y", "status": "open", "description": "Detailed description of the pull request."}
    return p.ToolResult(data=pull_request, control={"lifespan": "session"})

@p.tool
async def github_create_pull_request(context: p.ToolContext, title: str, description: str) -> p.ToolResult:
    # Simulate creating a new pull request in a GitHub repository
    new_pull_request = {"id": 3, "title": title, "status": "open", "description": description}
    return p.ToolResult(data=new_pull_request, control={"lifespan": "session"})

@p.tool
async def github_merge_pull_request(context: p.ToolContext, pr_id: int) -> p.ToolResult:
    # Simulate merging a pull request in a GitHub repository
    return p.ToolResult(data={"id": pr_id, "status": "merged"}, control={"lifespan": "session"})

