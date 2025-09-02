import os
import asyncio
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
import parlant.sdk as p
from dotenv import load_dotenv
from gemini_service import load_gemini_nlp_service


load_dotenv()

# Enhanced GitHub API Tools with proper error handling and data structure
@p.tool
async def github_list_open_issues(context: p.ToolContext, repo: str) -> p.ToolResult:
    """List all open issues in a GitHub repository"""
    try:
        # Simulate fetching open issues from a GitHub repository
        issues = [
            {
                "id": 1,
                "title": "Bug in authentication module",
                "status": "open",
                "assignee": "john.doe",
                "created_at": "2024-01-15T10:30:00Z",
                "priority": "high",
                "labels": ["bug", "authentication"]
            },
            {
                "id": 2,
                "title": "Add new user dashboard feature",
                "status": "open",
                "assignee": "jane.smith",
                "created_at": "2024-01-20T14:45:00Z",
                "priority": "medium",
                "labels": ["enhancement", "frontend"]
            },
            {
                "id": 3,
                "title": "Performance optimization for database queries",
                "status": "open",
                "assignee": "bob.wilson",
                "created_at": "2024-01-22T09:15:00Z",
                "priority": "low",
                "labels": ["performance", "database"]
            }
        ]
        
        # Filter by repository context
        filtered_issues = [issue for issue in issues if repo.lower() in ["my-repo", "project-repo", "main-repo"]]
        
        return p.ToolResult(
            data={
                "repository": repo,
                "count": len(filtered_issues),
                "issues": filtered_issues,
                "success": True
            },
            control={"lifespan": "session"}
        )
    except Exception as e:
        return p.ToolResult(
            data={"error": f"Failed to fetch issues: {str(e)}", "success": False},
            control={"lifespan": "response"}
        )

@p.tool
async def github_get_issue_details(context: p.ToolContext, issue_id: int) -> p.ToolResult:
    """Get detailed information about a specific GitHub issue"""
    try:
        # Simulate fetching detailed issue information
        issue_details = {
            1: {
                "id": 1,
                "title": "Bug in authentication module",
                "status": "open",
                "description": "Users are experiencing login failures with social OAuth providers. The error occurs intermittently and affects approximately 15% of login attempts.",
                "assignee": "john.doe",
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-25T16:22:00Z",
                "priority": "high",
                "labels": ["bug", "authentication"],
                "comments": 8,
                "milestone": "v2.1.0"
            },
            2: {
                "id": 2,
                "title": "Add new user dashboard feature",
                "status": "open",
                "description": "Create a comprehensive user dashboard with analytics, recent activity, and customizable widgets. This should improve user engagement and provide better insights.",
                "assignee": "jane.smith",
                "created_at": "2024-01-20T14:45:00Z",
                "updated_at": "2024-01-24T11:30:00Z",
                "priority": "medium",
                "labels": ["enhancement", "frontend"],
                "comments": 3,
                "milestone": "v2.2.0"
            }
        }
        
        issue = issue_details.get(issue_id)
        if not issue:
            return p.ToolResult(
                data={"error": f"Issue #{issue_id} not found", "success": False},
                control={"lifespan": "response"}
            )
            
        return p.ToolResult(data={**issue, "success": True}, control={"lifespan": "session"})
    except Exception as e:
        return p.ToolResult(
            data={"error": f"Failed to fetch issue details: {str(e)}", "success": False},
            control={"lifespan": "response"}
        )

@p.tool
async def github_create_issue(context: p.ToolContext, title: str, description: str) -> p.ToolResult:
    """Create a new issue in a GitHub repository"""
    try:
        # Simulate creating a new issue
        new_issue = {
            "id": 100 + len(title),  # Simple ID generation
            "title": title,
            "description": description,
            "status": "open",
            "assignee": "unassigned",
            "created_at": datetime.now().isoformat(),
            "labels": [],
            "priority": "medium",
            "comments": 0
        }
        
        return p.ToolResult(
            data={**new_issue, "success": True, "message": f"Issue '{title}' created successfully"},
            control={"lifespan": "session"}
        )
    except Exception as e:
        return p.ToolResult(
            data={"error": f"Failed to create issue: {str(e)}", "success": False},
            control={"lifespan": "response"}
        )

@p.tool
async def github_close_issue(context: p.ToolContext, issue_id: int) -> p.ToolResult:
    """Close an existing GitHub issue"""
    try:
        return p.ToolResult(
            data={
                "id": issue_id,
                "status": "closed",
                "closed_at": datetime.now().isoformat(),
                "reason": "resolved",
                "success": True,
                "message": f"Issue #{issue_id} closed successfully"
            },
            control={"lifespan": "session"}
        )
    except Exception as e:
        return p.ToolResult(
            data={"error": f"Failed to close issue: {str(e)}", "success": False},
            control={"lifespan": "response"}
        )

@p.tool
async def github_reopen_issue(context: p.ToolContext, issue_id: int) -> p.ToolResult:
    """Reopen a previously closed GitHub issue"""
    try:
        return p.ToolResult(
            data={
                "id": issue_id,
                "status": "reopened",
                "reopened_at": datetime.now().isoformat(),
                "success": True,
                "message": f"Issue #{issue_id} reopened successfully"
            },
            control={"lifespan": "session"}
        )
    except Exception as e:
        return p.ToolResult(
            data={"error": f"Failed to reopen issue: {str(e)}", "success": False},
            control={"lifespan": "response"}
        )

@p.tool
async def github_list_pull_requests(context: p.ToolContext, repo: str) -> p.ToolResult:
    """List pull requests in a GitHub repository"""
    try:
        pull_requests = [
            {
                "id": 1,
                "title": "Implement user authentication improvements",
                "status": "open",
                "author": "john.doe",
                "created_at": "2024-01-18T12:00:00Z",
                "branch": "feature/auth-improvements",
                "target_branch": "main",
                "commits": 5,
                "files_changed": 12,
                "additions": 234,
                "deletions": 89
            },
            {
                "id": 2,
                "title": "Fix critical bug in payment processing",
                "status": "open",
                "author": "jane.smith",
                "created_at": "2024-01-22T09:30:00Z",
                "branch": "hotfix/payment-bug",
                "target_branch": "main",
                "commits": 2,
                "files_changed": 3,
                "additions": 45,
                "deletions": 12
            }
        ]
        
        return p.ToolResult(
            data={
                "repository": repo,
                "count": len(pull_requests),
                "pull_requests": pull_requests,
                "success": True
            },
            control={"lifespan": "session"}
        )
    except Exception as e:
        return p.ToolResult(
            data={"error": f"Failed to fetch pull requests: {str(e)}", "success": False},
            control={"lifespan": "response"}
        )

@p.tool
async def github_get_pull_request_details(context: p.ToolContext, pr_id: int) -> p.ToolResult:
    """Get detailed information about a specific pull request"""
    try:
        pr_details = {
            1: {
                "id": 1,
                "title": "Implement user authentication improvements",
                "status": "open",
                "description": "This PR implements several authentication improvements including OAuth2 integration, enhanced security measures, and better error handling.",
                "author": "john.doe",
                "created_at": "2024-01-18T12:00:00Z",
                "updated_at": "2024-01-25T14:20:00Z",
                "branch": "feature/auth-improvements",
                "target_branch": "main",
                "commits": 5,
                "files_changed": 12,
                "additions": 234,
                "deletions": 89,
                "reviews": ["approved", "pending"],
                "checks": {"ci": "passing", "tests": "passing", "security": "passing"}
            },
            2: {
                "id": 2,
                "title": "Fix critical bug in payment processing",
                "status": "open",
                "description": "Urgent fix for payment processing bug that was causing transaction failures. Includes proper error handling and transaction rollback mechanisms.",
                "author": "jane.smith",
                "created_at": "2024-01-22T09:30:00Z",
                "updated_at": "2024-01-24T16:45:00Z",
                "branch": "hotfix/payment-bug",
                "target_branch": "main",
                "commits": 2,
                "files_changed": 3,
                "additions": 45,
                "deletions": 12,
                "reviews": ["approved"],
                "checks": {"ci": "passing", "tests": "passing", "security": "passing"}
            }
        }
        
        pr = pr_details.get(pr_id)
        if not pr:
            return p.ToolResult(
                data={"error": f"Pull request #{pr_id} not found", "success": False},
                control={"lifespan": "response"}
            )
            
        return p.ToolResult(data={**pr, "success": True}, control={"lifespan": "session"})
    except Exception as e:
        return p.ToolResult(
            data={"error": f"Failed to fetch PR details: {str(e)}", "success": False},
            control={"lifespan": "response"}
        )

@p.tool
async def github_create_pull_request(context: p.ToolContext, title: str, description: str, branch: str, target_branch: str = "main") -> p.ToolResult:
    """Create a new pull request in a GitHub repository"""
    try:
        new_pr = {
            "id": 200 + len(title),  # Simple ID generation
            "title": title,
            "description": description,
            "status": "open",
            "author": "dev-agent",
            "created_at": datetime.now().isoformat(),
            "branch": branch,
            "target_branch": target_branch,
            "commits": 1,
            "files_changed": 1,
            "additions": 50,
            "deletions": 10
        }
        
        return p.ToolResult(
            data={**new_pr, "success": True, "message": f"Pull request '{title}' created successfully"},
            control={"lifespan": "session"}
        )
    except Exception as e:
        return p.ToolResult(
            data={"error": f"Failed to create PR: {str(e)}", "success": False},
            control={"lifespan": "response"}
        )

@p.tool
async def github_merge_pull_request(context: p.ToolContext, pr_id: int, merge_method: str = "merge") -> p.ToolResult:
    """Merge a pull request in a GitHub repository"""
    try:
        return p.ToolResult(
            data={
                "id": pr_id,
                "status": "merged",
                "merged_at": datetime.now().isoformat(),
                "merge_method": merge_method,
                "success": True,
                "message": f"Pull request #{pr_id} merged successfully"
            },
            control={"lifespan": "session"}
        )
    except Exception as e:
        return p.ToolResult(
            data={"error": f"Failed to merge PR: {str(e)}", "success": False},
            control={"lifespan": "response"}
        )

@p.tool
async def github_close_pull_request(context: p.ToolContext, pr_id: int) -> p.ToolResult:
    """Close a pull request without merging"""
    try:
        return p.ToolResult(
            data={
                "id": pr_id,
                "status": "closed",
                "closed_at": datetime.now().isoformat(),
                "reason": "declined",
                "success": True,
                "message": f"Pull request #{pr_id} closed"
            },
            control={"lifespan": "session"}
        )
    except Exception as e:
        return p.ToolResult(
            data={"error": f"Failed to close PR: {str(e)}", "success": False},
            control={"lifespan": "response"}
        )

@p.tool
async def sandbox_run_tests(context: p.ToolContext, repo: str, commit_sha: str) -> p.ToolResult:
    """Run tests in a sandboxed environment"""
    try:
        # Simulate test execution
        import random
        success = random.choice([True, False])  # Random success/failure for demo
        
        if success:
            results = {
                "success": True,
                "tests_run": 45,
                "tests_passed": 45,
                "tests_failed": 0,
                "duration": "2m 34s",
                "coverage": "87%",
                "log_url": f"https://internal-logs.example/run/{commit_sha[:8]}"
            }
        else:
            results = {
                "success": False,
                "tests_run": 45,
                "tests_passed": 42,
                "tests_failed": 3,
                "failed_tests": [
                    "tests/test_authentication.py::test_oauth_login",
                    "tests/test_payment.py::test_invalid_card",
                    "tests/test_database.py::test_connection_timeout"
                ],
                "duration": "2m 12s",
                "coverage": "82%",
                "log_url": f"https://internal-logs.example/run/{commit_sha[:8]}"
            }
        
        return p.ToolResult(data=results, control={"lifespan": "response"})
    except Exception as e:
        return p.ToolResult(
            data={"error": f"Test execution failed: {str(e)}", "success": False},
            control={"lifespan": "response"}
        )

@p.tool
async def vector_retriever_search(context: p.ToolContext, query: str, top_k: int = 5) -> p.ToolResult:
    """Search for relevant documentation and code snippets using vector search"""
    try:
        # Simulate semantic search results
        search_results = [
            {
                "id": "doc-auth-001",
                "score": 0.95,
                "title": "Authentication Module Documentation",
                "snippet": "OAuth2 implementation with proper error handling. Common issues: token expiration, invalid client credentials.",
                "type": "documentation",
                "file_path": "docs/authentication.md"
            },
            {
                "id": "code-auth-002",
                "score": 0.89,
                "title": "Authentication Service Class",
                "snippet": "def handle_oauth_login(self, provider, token): if not token: raise AuthError('Invalid token') ...",
                "type": "code",
                "file_path": "src/auth/service.py"
            },
            {
                "id": "issue-auth-003",
                "score": 0.84,
                "title": "Similar Issue Resolution",
                "snippet": "Fixed similar OAuth login failures by updating token validation logic and improving error messages.",
                "type": "issue",
                "file_path": "issues/resolved/auth-fix-234.md"
            },
            {
                "id": "test-auth-004",
                "score": 0.78,
                "title": "Authentication Test Cases",
                "snippet": "Test cases covering OAuth flow, token validation, and error scenarios. Includes mock providers setup.",
                "type": "test",
                "file_path": "tests/test_authentication.py"
            }
        ]
        
        # Filter results based on top_k
        filtered_results = search_results[:top_k]
        
        return p.ToolResult(
            data={
                "query": query,
                "total_results": len(search_results),
                "returned_results": len(filtered_results),
                "hits": filtered_results,
                "success": True
            },
            control={"lifespan": "response"}
        )
    except Exception as e:
        return p.ToolResult(
            data={"error": f"Search failed: {str(e)}", "success": False},
            control={"lifespan": "response"}
        )

# Additional development tools
@p.tool
async def code_review_analyzer(context: p.ToolContext, pr_id: int) -> p.ToolResult:
    """Analyze code changes in a pull request for potential issues"""
    try:
        analysis = {
            "pr_id": pr_id,
            "security_issues": [
                {"severity": "medium", "description": "Potential SQL injection in user input handling"},
                {"severity": "low", "description": "Hardcoded API endpoint in configuration"}
            ],
            "performance_issues": [
                {"severity": "high", "description": "N+1 query detected in user data fetching"},
                {"severity": "medium", "description": "Large payload size in API response"}
            ],
            "best_practices": [
                {"type": "warning", "description": "Missing error handling in async function"},
                {"type": "suggestion", "description": "Consider using dependency injection pattern"}
            ],
            "test_coverage": {
                "current": "78%",
                "target": "85%",
                "missing_coverage": ["error_handler.py", "utils/validation.py"]
            },
            "overall_score": 7.5
        }
        
        return p.ToolResult(data=analysis, control={"lifespan": "response"})
    except Exception as e:
        return p.ToolResult(
            data={"error": f"Code analysis failed: {str(e)}", "success": False},
            control={"lifespan": "response"}
        )

@p.tool
async def deployment_status_checker(context: p.ToolContext, environment: str) -> p.ToolResult:
    """Check the deployment status of different environments"""
    try:
        environments = {
            "dev": {"status": "healthy", "version": "v2.1.3-dev", "uptime": "99.2%"},
            "staging": {"status": "healthy", "version": "v2.1.2", "uptime": "98.7%"},
            "production": {"status": "healthy", "version": "v2.1.1", "uptime": "99.9%"}
        }
        
        env_status = environments.get(environment.lower())
        if not env_status:
            return p.ToolResult(
                data={"error": f"Environment '{environment}' not found", "success": False},
                control={"lifespan": "response"}
            )
        
        return p.ToolResult(
            data={
                "environment": environment,
                **env_status,
                "last_checked": datetime.now().isoformat(),
                "success": True
            },
            control={"lifespan": "response"}
        )
    except Exception as e:
        return p.ToolResult(
            data={"error": f"Status check failed: {str(e)}", "success": False},
            control={"lifespan": "response"}
        )

# Journey Creation Functions
async def create_issue_management_journey(agent: p.Agent) -> p.Journey:
    """Create a journey for managing GitHub issues"""
    journey = await agent.create_journey(
        title="Issue Management",
        description="Guide users through creating, updating, and resolving GitHub issues",
        conditions=["User wants to manage GitHub issues", "User mentions bug reports", "User needs help with issue tracking"]
    )
    
    # Create journey-scoped canned responses
    await journey.create_canned_response(
        template="I'll help you manage your GitHub issues. What would you like to do with the issues?"
    )
    await journey.create_canned_response(
        template="Let me check the current status of issue #{issue_id} for you."
    )
    await journey.create_canned_response(
        template="I found {{issues_count}} open issues in the {{repo_name}} repository. Would you like me to show you the details?"
    )
    
    # Journey flow states
    initial_transition = await journey.initial_state.transition_to(
        chat_state="Ask user what they want to do with GitHub issues (create, view, update, close)"
    )
    
    # Branch for creating issues
    create_branch = await initial_transition.target.transition_to(
        condition="User wants to create a new issue",
        chat_state="Ask for the issue title and description"
    )
    
    create_issue_state = await create_branch.target.transition_to(
        tool_state=github_create_issue
    )
    
    await create_issue_state.target.transition_to(
        chat_state="Confirm the issue has been created successfully and ask if they need anything else"
    )
    
    # Branch for viewing issues
    view_branch = await initial_transition.target.transition_to(
        condition="User wants to view existing issues",
        tool_state=github_list_open_issues
    )
    
    await view_branch.target.transition_to(
        chat_state="Show the list of open issues and ask if they want details on any specific issue"
    )
    
    # Branch for closing issues
    close_branch = await initial_transition.target.transition_to(
        condition="User wants to close an issue",
        chat_state="Ask for the issue ID to close"
    )
    
    close_issue_state = await close_branch.target.transition_to(
        tool_state=github_close_issue
    )
    
    await close_issue_state.target.transition_to(
        chat_state="Confirm the issue has been closed and ask if they need help with anything else"
    )
    
    return journey

async def create_pull_request_management_journey(agent: p.Agent) -> p.Journey:
    """Create a journey for managing pull requests"""
    journey = await agent.create_journey(
        title="Pull Request Management",
        description="Help users create, review, and manage pull requests",
        conditions=["User wants to work with pull requests", "User mentions PR", "User wants to merge code"]
    )
    
    # Journey-scoped canned responses
    await journey.create_canned_response(
        template="I can help you with pull request management. What would you like to do?"
    )
    await journey.create_canned_response(
        template="Let me fetch the details for pull request #{pr_id}."
    )
    await journey.create_canned_response(
        template="I found {{pr_count}} open pull requests. Here are the details:"
    )
    await journey.create_canned_response(
        template="Pull request #{pr_id} has been {{action}} successfully!"
    )
    
    # Journey states
    initial_state = await journey.initial_state.transition_to(
        chat_state="Ask what they want to do with pull requests (create, view, merge, close)"
    )
    
    # Create PR branch
    create_pr_branch = await initial_state.target.transition_to(
        condition="User wants to create a pull request",
        chat_state="Ask for PR title, description, source branch, and target branch"
    )
    
    create_pr_state = await create_pr_branch.target.transition_to(
        tool_state=github_create_pull_request
    )
    
    await create_pr_state.target.transition_to(
        chat_state="Confirm PR creation and provide next steps for review"
    )
    
    # View PRs branch
    view_pr_branch = await initial_state.target.transition_to(
        condition="User wants to view pull requests",
        tool_state=github_list_pull_requests
    )
    
    await view_pr_branch.target.transition_to(
        chat_state="Present the list of PRs and offer to show details or perform actions"
    )
    
    # Merge PR branch
    merge_pr_branch = await initial_state.target.transition_to(
        condition="User wants to merge a pull request",
        chat_state="Ask for PR ID and confirm merge action"
    )
    
    merge_pr_state = await merge_pr_branch.target.transition_to(
        tool_state=github_merge_pull_request
    )
    
    await merge_pr_state.target.transition_to(
        chat_state="Confirm successful merge and suggest next steps"
    )
    
    return journey

async def create_ci_cd_troubleshooting_journey(agent: p.Agent) -> p.Journey:
    """Create a journey for CI/CD troubleshooting"""
    journey = await agent.create_journey(
        title="CI/CD Troubleshooting",
        description="Help diagnose and resolve CI/CD pipeline issues",
        conditions=["Tests are failing", "CI pipeline is broken", "User reports build failures", "Deployment issues"]
    )
    
    # Journey-scoped canned responses
    await journey.create_canned_response(
        template="I'll help you troubleshoot the CI/CD issues. Let me start by running the latest tests."
    )
    await journey.create_canned_response(
        template="The test results show {{failed_tests_count}} failing tests. Let me analyze the failures."
    )
    await journey.create_canned_response(
        template="Based on the error analysis, here are the recommended fixes:"
    )
    await journey.create_canned_response(
        template="I've found similar issues in our knowledge base. Here are potential solutions:"
    )
    
    # Journey states
    initial_state = await journey.initial_state.transition_to(
        chat_state="Acknowledge the CI/CD issue and ask for repository and commit details"
    )
    
    # Run tests
    run_tests_state = await initial_state.target.transition_to(
        tool_state=sandbox_run_tests
    )
    
    # Analyze results
    analyze_success = await run_tests_state.target.transition_to(
        condition="Tests pass successfully",
        chat_state="Inform that all tests are passing and suggest checking deployment status"
    )
    
    analyze_failure = await run_tests_state.target.transition_to(
        condition="Tests are failing",
        tool_state=vector_retriever_search
    )
    
    # Provide solutions
    await analyze_failure.target.transition_to(
        chat_state="Present analysis of test failures with suggested fixes and relevant documentation"
    )
    
    # Check deployment
    deployment_check = await analyze_success.target.transition_to(
        tool_state=deployment_status_checker
    )
    
    await deployment_check.target.transition_to(
        chat_state="Report deployment status and provide recommendations"
    )
    
    return journey

async def create_code_review_journey(agent: p.Agent) -> p.Journey:
    """Create a journey for code review assistance"""
    journey = await agent.create_journey(
        title="Code Review Assistance",
        description="Help with code review processes and quality assurance",
        conditions=["User needs code review", "User mentions code quality", "Pull request review needed"]
    )
    
    # Journey-scoped canned responses
    await journey.create_canned_response(
        template="I'll help you with the code review. Which pull request would you like me to analyze?"
    )
    await journey.create_canned_response(
        template="Let me analyze the code changes in PR #{pr_id} for potential issues."
    )
    await journey.create_canned_response(
        template="Code analysis complete! I found {{issue_count}} issues to address."
    )
    await journey.create_canned_response(
        template="The code quality score is {{score}}/10. Here are the main areas for improvement:"
    )
    
    # Journey states
    initial_state = await journey.initial_state.transition_to(
        chat_state="Ask for the pull request ID to review"
    )
    
    # Get PR details
    get_pr_details = await initial_state.target.transition_to(
        tool_state=github_get_pull_request_details
    )
    
    # Analyze code
    analyze_code = await get_pr_details.target.transition_to(
        tool_state=code_review_analyzer
    )
    
    # Present findings
    await analyze_code.target.transition_to(
        chat_state="Present detailed code review findings with actionable recommendations"
    )
    
    return journey

# Main application function
async def main() -> None:
    """Main application entry point"""
    if not os.environ.get("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY environment variable is required")
        print("Please create a .env file with your GEMINI_API_KEY")
        return
    
    try:
        async with p.Server(
            nlp_service=load_gemini_nlp_service,
            session_store="local",
            customer_store="local"
        ) as server:
            
            # Create the main developer agent with enhanced capabilities
            agent = await server.create_agent(
                name="GitHub Project Manager Agent",
                description="""
                Expert developer assistant specialized in GitHub project management, CI/CD troubleshooting, 
                and code review. I help diagnose build failures, manage issues and pull requests, 
                run tests in sandboxed environments, and provide intelligent code analysis.
                
                I follow best practices for software development workflows and provide actionable 
                recommendations based on analysis of code, tests, and deployment status.
                """,
                composition_mode=p.CompositionMode.FLUID  # Allow flexible responses with canned response guidance
            )
            
            # Attach tools to the agent
            tools_list = [
                # Core GitHub tools
                github_list_open_issues,
                github_get_issue_details,
                github_create_issue,
                github_close_issue,
                github_reopen_issue,
                
                # Pull request tools
                github_list_pull_requests,
                github_get_pull_request_details,
                github_create_pull_request,
                github_merge_pull_request,
                github_close_pull_request,
                
                # Development tools
                sandbox_run_tests,
                vector_retriever_search,
                code_review_analyzer,
                deployment_status_checker,
            ]
            
            # Create guidelines that attach tools to the agent
            # GitHub Issue Management Tools
            await agent.create_guideline(
                condition="User wants to list, view, create, close, or reopen GitHub issues",
                action="Use the appropriate GitHub issue management tools to help the user",
                tools=[github_list_open_issues, github_get_issue_details, github_create_issue, github_close_issue, github_reopen_issue]
            )
            
            # Pull Request Management Tools  
            await agent.create_guideline(
                condition="User wants to work with pull requests - list, view, create, merge, or close PRs",
                action="Use the appropriate pull request management tools to assist the user",
                tools=[github_list_pull_requests, github_get_pull_request_details, github_create_pull_request, github_merge_pull_request, github_close_pull_request]
            )
            
            # CI/CD and Testing Tools
            await agent.create_guideline(
                condition="User needs help with testing, CI/CD, code analysis, or deployment status",
                action="Use development and analysis tools to provide comprehensive assistance",
                tools=[sandbox_run_tests, vector_retriever_search, code_review_analyzer, deployment_status_checker]
            )
            
            # Create comprehensive canned responses for various scenarios
            
            # Greeting and general responses
            await agent.create_canned_response(
                template="Hello! I'm your GitHub Project Manager Agent. I can help you with issues, pull requests, CI/CD troubleshooting, and code reviews. What would you like to work on today?",
                tags=[p.Tag.preamble()]
            )
            
            await agent.create_canned_response(
                template="I understand you're looking for help with {{generative.request_type}}. Let me assist you with that.",
                tags=[p.Tag.preamble()]
            )
            
            # Issue management responses
            await agent.create_canned_response(
                template="I found {{issue_count}} open issues in the {{std.variables.repo_name}} repository. Here are the details:"
            )
            
            await agent.create_canned_response(
                template="Issue #{issue_id} '{{issue_title}}' has been {{action}} successfully. Is there anything else you'd like me to help you with?"
            )
            
            await agent.create_canned_response(
                template="I couldn't find that issue. Please verify the issue ID and try again, or would you like me to list all open issues?"
            )
            
            # Pull request responses
            await agent.create_canned_response(
                template="I found {{pr_count}} pull requests in {{pr_status}} status. Would you like me to show you the details or perform any actions?"
            )
            
            await agent.create_canned_response(
                template="Pull request #{pr_id} '{{pr_title}}' by {{pr_author}} is ready for review. The changes include {{files_changed}} files with {{additions}} additions and {{deletions}} deletions."
            )
            
            await agent.create_canned_response(
                template="Pull request #{pr_id} has been {{action}} successfully! {{generative.next_steps}}"
            )
            
            # CI/CD and testing responses
            await agent.create_canned_response(
                template="Test execution completed! {{tests_passed}}/{{tests_run}} tests passed. {% if failed_tests %}The following tests failed: {{failed_tests}}{% endif %}"
            )
            
            await agent.create_canned_response(
                template="I've analyzed the test failures and found potential solutions in our knowledge base. Here are the recommended fixes:"
            )
            
            await agent.create_canned_response(
                template="The {{environment}} environment is {{status}} with version {{version}}. Uptime: {{uptime}}"
            )
            
            # Code review responses
            await agent.create_canned_response(
                template="Code analysis completed for PR #{{pr_id}}. Overall quality score: {{overall_score}}/10. {% if security_issues %}⚠️ Found {{security_issues_count}} security issues.{% endif %}"
            )
            
            await agent.create_canned_response(
                template="I've identified several areas for improvement: {% for issue in issues %}• {{issue.severity}} priority: {{issue.description}}{% endfor %}"
            )
            
            # Error and fallback responses
            await agent.create_canned_response(
                template="I encountered an error: {{error_message}}. Let me try a different approach or would you like to try something else?"
            )
            
            await agent.create_canned_response(
                template="I'm not sure about that specific request. I can help you with GitHub issues, pull requests, CI/CD troubleshooting, and code reviews. What would you like to work on?"
            )
            
            # Helpful responses
            await agent.create_canned_response(
                template="Is there anything else I can help you with? I'm here to assist with your GitHub project management needs."
            )
            
            await agent.create_canned_response(
                template="Great! I've completed that task. Here's a summary of what I did: {{generative.task_summary}}"
            )
            
            # Create comprehensive journeys
            issue_journey = await create_issue_management_journey(agent)
            pr_journey = await create_pull_request_management_journey(agent)
            ci_journey = await create_ci_cd_troubleshooting_journey(agent)
            review_journey = await create_code_review_journey(agent)
            
            print(f"✅ Created Issue Management Journey: {issue_journey.id}")
            print(f"✅ Created Pull Request Journey: {pr_journey.id}")
            print(f"✅ Created CI/CD Troubleshooting Journey: {ci_journey.id}")
            print(f"✅ Created Code Review Journey: {review_journey.id}")
            
            # Create essential variables for context management
            await agent.create_variable(
                name="repo_name",
                description="The current repository name being worked on",
                initial_value="my-project-repo"
            )
            
            await agent.create_variable(
                name="current_branch", 
                description="The current git branch",
                initial_value="main"
            )
            
            await agent.create_variable(
                name="commit_sha",
                description="The latest commit SHA for testing",
                initial_value="latest"
            )
            
            await agent.create_variable(
                name="environment",
                description="Current deployment environment (dev, staging, production)",
                initial_value="dev"
            )
            
            await agent.create_variable(
                name="user_role",
                description="The role of the current user (developer, reviewer, manager)",
                initial_value="developer"
            )
            
            await agent.create_variable(
                name="project_priority",
                description="Current project priority level",
                initial_value="medium"
            )
            
            # Create guidelines for agent behavior
            await agent.create_guideline(
                condition="User asks for help or seems confused",
                action="Be helpful and provide clear, actionable guidance. Offer specific next steps and ask clarifying questions if needed."
            )
            
            await agent.create_guideline(
                condition="A critical error or security issue is detected",
                action="Immediately highlight the severity, provide clear explanations, and suggest urgent remediation steps."
            )
            
            await agent.create_guideline(
                condition="User requests information about tests or CI/CD",
                action="Always run the actual tests or checks first, then provide detailed analysis of the results with actionable recommendations."
            )
            
            await agent.create_guideline(
                condition="Multiple issues or PRs are found",
                action="Present information in a clear, organized manner and offer to help with specific items. Ask what the user wants to prioritize."
            )
            
            await agent.create_guideline(
                condition="User mentions deadlines or urgency",
                action="Acknowledge the time constraint and prioritize the most critical tasks. Provide efficient solutions and clear timelines."
            )
            
            print("✅ Agent created with comprehensive tools, journeys, and canned responses")
            print("✅ Variables and guidelines configured")
            print("\n🚀 GitHub Project Manager Agent is ready!")
            print("📊 Available features:")
            print("   • Issue Management (create, view, update, close)")
            print("   • Pull Request Management (create, review, merge)")
            print("   • CI/CD Troubleshooting (test execution, failure analysis)")
            print("   • Code Review Assistance (quality analysis, recommendations)")
            print("   • Smart context awareness with variables")
            print("   • Structured conversation flows with journeys")
            print("   • Professional responses with canned templates")
            
            # Keep the server running
            print(f"\n💡 The agent is now running and ready to help!")
            print("   You can interact with it through the Parlant interface.")
            
            # Optional: Add a simple CLI interface for testing
            while True:
                try:
                    await asyncio.sleep(1)
                except KeyboardInterrupt:
                    print("\n👋 Shutting down GitHub Project Manager Agent...")
                    break
                    
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
