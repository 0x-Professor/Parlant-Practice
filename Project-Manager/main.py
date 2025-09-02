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

@p.tool
async def github_close_pull_request(context: p.ToolContext, pr_id: int) -> p.ToolResult:
    # Simulate closing a pull request in a GitHub repository
    return p.ToolResult(data={"id": pr_id, "status": "closed"}, control={"lifespan": "session"})

@p.tool
async def sandbox_run_tests(context: p.ToolContext, repo: str, commit_sha: str, test_selector: Optional[str] = None) -> p.ToolResult:
    # stub: simulate running tests; in prod, orchestrator would run containerized tests and return results safely
    results = {"success": False, "failed_tests": ["tests/test_parser.py::test_empty_input"], "log_url": "https://internal-logs.example/run/12345"}
    return p.ToolResult(data=results, control={"lifespan": "response"})
@p.tool
async def vector_retriever_search(context: p.ToolContext, query: str, top_k: int = 5) -> p.ToolResult:
    # stub: semantic search results from vector DB
    hits = [
        {"id": "doc-1", "score": 0.98, "snippet": "Parsing behavior: empty input returns None"},
        {"id": "doc-2", "score": 0.85, "snippet": "How to reproduce crash with empty payload..."},
    ]
    return p.ToolResult(data={"hits": hits}, control={"lifespan": "response"})
async def main() -> None:
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is required")
        return
    
    try:
        async with p.Server(nlp_service=load_gemini_nlp_service, session_store="local", customer_store="local") as server:
            dev_agent = await server.create_agent(
                name="Dev Agent For Github",
                description="Developer assistant: diagnoses CI failures, runs tests in sandbox, suggests fixes and creates PR drafts.",
                tools=[
                    github_list_open_issues,
                    github_get_issue_details,
                    github_create_issue,
                    github_reopen_issue,
                    github_list_pull_requests,
                    github_get_pull_request_details,
                    github_create_pull_request,
                    github_merge_pull_request,
                    github_close_pull_request,
                    sandbox_run_tests,
                    vector_retriever_search,
                ],
            )
            await dev_agent.create_variable(name = "repo_name", initial_value="my-repo")
            await dev_agent.create_variable(name = "commit_sha", initial_value="main")
            await dev_agent.create_variable(name = "pr_title", initial_value="Fix CI Pipeline")
            await dev_agent.create_variable(name = "pr_description", initial_value="This PR fixes the CI pipeline by updating the workflow configuration.")
            await dev_agent.create_variable(name = "issue_id", initial_value="1")
            await dev_agent.create_variable(name = "pr_id", initial_value="1")
            
            await dev_agent.create_guidelines(
                condition= "if user request to create a pull request",
                action = "Ask the user for PR title and description",
                tools = [github_create_pull_request, github_merge_pull_request, github_close_pull_request]
                
            )
            await dev_agent.create_guidelines(
                condition= "if user request to run tests",
                action = "Run tests in sandbox environment",
                tools = [sandbox_run_tests]
                
            )
            await dev_agent.create_guidelines(
                condition= "if user request to get issue details",
                action = "Fetch issue details",
                tools = [github_get_issue_details]
            )
            await dev_agent.create_guidelines(
                condition= "if user request to get pull request details",
                action = "Fetch pull request details",
                tools = [github_get_pull_request_details]
            )
            await dev_agent.create_guidelines(
                condition= "if user request to search documentation",
                action = "Search documentation",
                tools = [vector_retriever_search]
            )
            await dev_agent.create_guidelines(
                condition = "If user to create an issue",
                action = "Ask the user for issue title and description",
                tools = [github_create_issue]
            )
            await dev_agent.create_guidelines(
                condition = "If user ask to fetch the issue details",
                action = "Fetch issue details",
                tools = [github_get_issue_details]
                
            )

    except Exception as e:
        print(f"An error occurred: {e}")