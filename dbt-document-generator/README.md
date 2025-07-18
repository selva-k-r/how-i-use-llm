# dbt Documentation Automation Tool

> **Buzz**: This is it! The magic script that turns your manifest.json into AI-powered documentation!

> **Zen**: A systematic approach to automating dbt documentation using manifest.json and LLM integration.

## What This Tool Does

This Python program automates the creation of comprehensive dbt model documentation by:

1. **Validating your dbt project** - Ensures you're running in a valid dbt project directory
2. **Extracting metadata** - Reads your `manifest.json` to understand your models
3. **Generating intelligent documentation** - Uses LLM to create business-friendly docs
4. **Creating doc blocks** - Saves markdown files with reusable documentation blocks
5. **Updating YAML files** - Automatically references doc blocks in your schema files

## Quick Start

### Prerequisites

- Python 3.7+
- A dbt project with generated `manifest.json` (run `dbt compile` first)
- OpenAI API key

### Installation

1. **Clone or download** the automation files:
   ```bash
   # Download the files to your dbt project directory
   curl -O https://raw.githubusercontent.com/your-repo/dbt-manifest-automation/main/dbt_doc_automation.py
   curl -O https://raw.githubusercontent.com/your-repo/dbt-manifest-automation/main/requirements.txt
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your OpenAI API key**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

### Usage

1. **Navigate to your dbt project**:
   ```bash
   cd your-dbt-project
   ```

2. **Ensure manifest.json exists**:
   ```bash
   dbt compile  # or dbt run, dbt build
   ```

3. **Run the automation**:
   ```bash
   python dbt_doc_automation.py
   ```

## What Happens When You Run It

```
🚀 Starting dbt documentation automation...
Step 1: Checking for dbt project...
✅ Found dbt project at: /path/to/your/project
Step 2: Getting target folder from dbt_project.yml...
✅ Found manifest.json at: /path/to/your/project/target/manifest.json
Step 3: Extracting model information from manifest.json...
✅ Extracted information for 15 models
Processing model: customer_lifetime_value
Processing model: monthly_active_users
Processing model: revenue_by_product
...
✅ Updated YAML files with doc block references
🎉 Documentation automation completed successfully!
```

## Output Structure

After running the tool, you'll have:

```
your-dbt-project/
├── docs/
│   ├── customer_lifetime_value_doc.md
│   ├── monthly_active_users_doc.md
│   └── revenue_by_product_doc.md
├── models/
│   ├── schema.yml  # Updated with doc block references
│   └── marts/
│       └── schema.yml  # Updated with doc block references
└── target/
    └── manifest.json  # Your existing manifest file
```

## Generated Documentation Format

Each model gets documentation with three sections:

### Business Overview
- Non-technical explanation of the model's purpose
- Business value and use cases
- How stakeholders should interpret the data

### Technical Implementation
- Key transformations and business logic
- Complex calculations and window functions
- Materialization strategy and refresh patterns

### Data Dictionary
- Comprehensive table with column details
- Data types and business descriptions
- Source information and data quality notes

## Configuration Options

You can customize the tool by modifying these variables in the script:

```python
# Change the LLM model
automator = DBTDocumentationAutomator(api_key, model_name="gpt-4")

# Adjust concurrent request limits
self.semaphore = asyncio.Semaphore(3)  # Reduce from 5 to 3

# Modify prompt temperature for more/less creativity
"temperature": 0.1,  # More focused (default: 0.3)
```

## Error Handling

The tool includes comprehensive error handling:

- **Missing dbt_project.yml**: Alerts you to run from correct directory
- **Missing manifest.json**: Reminds you to run `dbt compile/run/build`
- **API rate limits**: Uses semaphore to limit concurrent requests
- **Network errors**: Graceful handling of API failures

## Troubleshooting

### Common Issues

1. **"dbt_project.yml not found"**
   - Ensure you're running the script from your dbt project root directory

2. **"manifest.json not found"**
   - Run `dbt compile`, `dbt run`, or `dbt build` first

3. **API rate limit errors**
   - Reduce the semaphore limit in the code
   - Check your OpenAI API usage limits

4. **Memory issues with large projects**
   - The tool processes models in batches to avoid memory problems
   - Consider running on subsets of models if needed

### Debug Mode

Enable debug logging by modifying the logging level:

```python
logging.basicConfig(level=logging.DEBUG)
```

## Extending the Tool

### Custom Prompts

Modify the `construct_prompt()` method to customize documentation format:

```python
def construct_prompt(self, model_info: ModelInfo) -> str:
    # Add your custom prompt template here
    return custom_prompt
```

### Different LLM Providers

Replace the OpenAI API call with your preferred provider:

```python
# Example: Replace with Anthropic, Cohere, or local models
async def call_llm_async(self, prompt: str, model_name: str) -> str:
    # Your custom LLM integration here
    pass
```

### Custom Output Formats

Modify the `step_5_save_doc_blocks()` method to change output format:

```python
# Example: Generate different markdown formats
markdown_content = f'''
# {model_info.name}

{llm_response}

---
*Generated by dbt Documentation Automation*
'''
```

## Contributing

This tool was created for the Medium blog post series on dbt automation. Feel free to:

- Report issues or suggest improvements
- Submit pull requests with enhancements
- Share your experience using the tool

## License

MIT License - feel free to use and modify as needed.

## Credits

Created for the "Automating dbt Documentation" blog post series, featuring the eternal conversation between **Buzz** (the excited dreamer) and **Zen** (the focused implementer).

---

*Remember: This tool transforms your dbt project's metadata into intelligent, AI-generated documentation that bridges the gap between technical implementation and business understanding.*
