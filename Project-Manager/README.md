# GitHub Project Manager Agent 🚀

A sophisticated AI-powered GitHub project management assistant built with the Parlant framework and Google Gemini AI. This agent helps developers manage GitHub issues, pull requests, CI/CD pipelines, and code reviews through intelligent conversation flows.

## 🌟 Features

### Core GitHub Management
- **Issue Management**: Create, view, update, and close GitHub issues
- **Pull Request Management**: Handle PR creation, reviews, merging, and closing
- **Repository Operations**: Multi-repository support with context awareness

### Advanced Development Tools
- **CI/CD Troubleshooting**: Automated test execution and failure analysis
- **Code Review Assistance**: AI-powered code quality analysis and recommendations
- **Vector Search**: Intelligent documentation and code snippet retrieval
- **Deployment Monitoring**: Environment status checking and health monitoring

### Parlant Framework Features
- **Journeys**: Structured conversation flows for different workflows
- **Canned Responses**: Pre-approved response templates for consistency
- **Guidelines**: Behavioral rules for agent interactions
- **Variables**: Context-aware state management
- **Composition Modes**: Flexible response generation (Fluid, Strict, Composited)

## 🏗️ Architecture

### Tools Available
1. **GitHub API Tools**:
   - `github_list_open_issues` - List repository issues
   - `github_get_issue_details` - Get detailed issue information
   - `github_create_issue` - Create new issues
   - `github_close_issue` - Close existing issues
   - `github_reopen_issue` - Reopen closed issues
   - `github_list_pull_requests` - List pull requests
   - `github_get_pull_request_details` - Get PR details
   - `github_create_pull_request` - Create new PRs
   - `github_merge_pull_request` - Merge pull requests
   - `github_close_pull_request` - Close pull requests

2. **Development Tools**:
   - `sandbox_run_tests` - Execute tests in sandboxed environment
   - `vector_retriever_search` - Semantic search for documentation
   - `code_review_analyzer` - Analyze code quality and security
   - `deployment_status_checker` - Check environment deployment status

### Journeys Implemented
1. **Issue Management Journey**: Guides users through issue lifecycle
2. **Pull Request Management Journey**: Handles PR workflows
3. **CI/CD Troubleshooting Journey**: Diagnoses and resolves pipeline issues
4. **Code Review Journey**: Assists with code quality assurance

### Canned Responses
- **Greeting responses**: Welcome users and offer assistance
- **Issue management responses**: Handle issue-related interactions
- **Pull request responses**: Manage PR-related communications
- **CI/CD responses**: Provide test and deployment feedback
- **Code review responses**: Deliver analysis results
- **Error handling responses**: Manage error scenarios gracefully
- **Preamble responses**: Acknowledge user inputs while processing

## 📋 Prerequisites

- Python 3.13 or higher
- Google Gemini API key
- Parlant framework installed

## 🚀 Installation

1. **Clone and navigate to the project**:
   ```bash
   cd U:\Parlant-Practice\starter\Project-Manager
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   
   Or using the pyproject.toml:
   ```bash
   pip install -e .
   ```

3. **Set up environment variables**:
   ```bash
   # Copy the example file
   copy .env.example .env
   
   # Edit .env and add your Gemini API key
   # GEMINI_API_KEY=your_actual_api_key_here
   ```

4. **Get your Gemini API key**:
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a new API key
   - Add it to your `.env` file

## 🔧 Usage

### Running the Enhanced Agent

```bash
python main_enhanced.py
```

### Key Differences from Original

The enhanced version includes:

1. **Comprehensive Tools**: All tools now have proper error handling, detailed responses, and realistic data structures
2. **Journeys**: Four complete journey workflows for different use cases
3. **Canned Responses**: 15+ pre-defined response templates with template variables
4. **Guidelines**: 5 behavioral guidelines for consistent agent behavior
5. **Variables**: 6 context variables for state management
6. **Composition Mode**: Uses FLUID mode for balanced flexibility and control

### Example Interactions

**Issue Management**:
```
User: "I need to create a new issue for a login bug"
Agent: "I'll help you create a new issue. What's the title and description for this login bug?"
```

**CI/CD Troubleshooting**:
```
User: "Our tests are failing on the main branch"
Agent: "I'll help you troubleshoot the CI/CD issues. Let me start by running the latest tests."
```

**Code Review**:
```
User: "Can you review pull request #5?"
Agent: "I'll help you with the code review. Let me analyze the code changes in PR #5 for potential issues."
```

## 🏃‍♀️ Journeys in Detail

### 1. Issue Management Journey
- **Activation**: User mentions issues, bugs, or issue tracking
- **Flow**: Ask intent → Branch to create/view/close → Execute action → Confirm result

### 2. Pull Request Management Journey
- **Activation**: User mentions PRs, merging, or code reviews
- **Flow**: Determine action → Get details → Execute PR operation → Provide feedback

### 3. CI/CD Troubleshooting Journey
- **Activation**: Test failures, CI issues, build problems
- **Flow**: Gather context → Run tests → Analyze results → Provide solutions

### 4. Code Review Journey
- **Activation**: Code quality, review requests
- **Flow**: Get PR ID → Fetch details → Analyze code → Present findings

## 🎯 Canned Response Templates

The system uses template variables for dynamic content:

- `{{std.variables.repo_name}}` - Current repository name
- `{{generative.request_type}}` - AI-inferred request type
- `{{issue_count}}` - Number of issues found
- `{{pr_id}}` - Pull request ID
- `{{overall_score}}` - Code quality score

## 📊 Configuration

### Agent Variables
- `repo_name`: Current repository (default: "my-project-repo")
- `current_branch`: Active branch (default: "main")
- `commit_sha`: Latest commit for testing (default: "latest")
- `environment`: Deployment environment (default: "dev")
- `user_role`: User's role (default: "developer")
- `project_priority`: Project priority level (default: "medium")

### Guidelines
1. **Help & Confusion**: Provide clear, actionable guidance
2. **Critical Issues**: Immediately highlight severity and remediation
3. **CI/CD Requests**: Always run actual checks first
4. **Multiple Items**: Present organized information with prioritization options
5. **Urgency**: Acknowledge constraints and provide efficient solutions

## 🔧 Customization

### Adding New Tools
```python
@p.tool
async def your_custom_tool(context: p.ToolContext, param: str) -> p.ToolResult:
    try:
        # Your tool logic here
        return p.ToolResult(data={"result": "success"}, control={"lifespan": "session"})
    except Exception as e:
        return p.ToolResult(data={"error": str(e)}, control={"lifespan": "response"})
```

### Adding New Journeys
```python
async def create_custom_journey(agent: p.Agent) -> p.Journey:
    journey = await agent.create_journey(
        title="Custom Journey",
        description="Description of journey purpose",
        conditions=["Activation condition 1", "Activation condition 2"]
    )
    # Add states and transitions
    return journey
```

### Adding Canned Responses
```python
await agent.create_canned_response(
    template="Your template with {{variables}} here",
    tags=[p.Tag.preamble()]  # Optional tags
)
```

## 🐛 Troubleshooting

### Common Issues

1. **Missing API Key**:
   ```
   Error: GEMINI_API_KEY environment variable is required
   ```
   - Solution: Ensure your `.env` file has a valid `GEMINI_API_KEY`

2. **Import Errors**:
   ```
   ModuleNotFoundError: No module named 'parlant'
   ```
   - Solution: Install dependencies with `pip install -r requirements.txt`

3. **Connection Issues**:
   ```
   Failed to connect to Gemini API
   ```
   - Solution: Check your internet connection and API key validity

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is part of the Parlant framework ecosystem. See the original Parlant license for details.

## 🙏 Acknowledgments

- [Parlant Framework](https://github.com/emcie-co/parlant) - The conversational AI framework
- [Google Gemini AI](https://ai.google.dev/) - The underlying language model
- [Emcie](https://emcie.co/) - Creators of the Parlant framework

---

**Ready to manage your GitHub projects with AI? 🚀**

Run `python main_enhanced.py` and start your intelligent development workflow!
