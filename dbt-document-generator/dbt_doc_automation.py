
"""
DBT Documentation Automation Tool

This program automates the generation of documentation for dbt models using manifest.json
and LLM-powered content generation.

Requirements:
- asyncio for async operations
- aiohttp for HTTP requests
- pyyaml for YAML manipulation
- openai for LLM integration

Usage:
    python dbt_doc_automation.py

Author: Generated for Medium Blog Post
"""

import os
import json
import yaml
import asyncio
import aiohttp
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ModelInfo:
    """Data class to store model information"""
    name: str
    unique_id: str
    description: str
    columns: Dict[str, Any]
    compiled_sql: str
    depends_on: List[str]
    tags: List[str]
    config: Dict[str, Any]

class DBTDocumentationAutomator:
    """Main class for dbt documentation automation"""

    def __init__(self, api_key: str, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize the automation tool

        Args:
            api_key: OpenAI API key
            model_name: LLM model to use (default: gpt-3.5-turbo)
        """
        self.api_key = api_key
        self.model_name = model_name
        self.project_root = None
        self.target_path = None
        self.manifest_path = None
        self.semaphore = asyncio.Semaphore(5)  # Limit concurrent requests

    def step_1_check_dbt_project(self) -> bool:
        """
        Step 1: Check if we're in a dbt project directory

        Returns:
            bool: True if valid dbt project, False otherwise
        """
        logger.info("Step 1: Checking for dbt project...")

        # Check current directory and parent directories
        current_dir = Path.cwd()
        for path in [current_dir] + list(current_dir.parents):
            dbt_project_file = path / "dbt_project.yml"
            if dbt_project_file.exists():
                self.project_root = path
                logger.info(f"Found dbt project at: {path}")
                return True

        logger.error("❌ dbt_project.yml not found. Please run this script from a dbt project directory.")
        return False

    def step_2_get_target_folder(self) -> bool:
        """
        Step 2: Get target folder name from dbt_project.yml

        Returns:
            bool: True if target folder found, False otherwise
        """
        logger.info("Step 2: Getting target folder from dbt_project.yml...")

        try:
            dbt_project_file = self.project_root / "dbt_project.yml"
            with open(dbt_project_file, 'r') as f:
                project_config = yaml.safe_load(f)

            # Get target-path, default to 'target' if not specified
            target_path = project_config.get('target-path', 'target')
            self.target_path = self.project_root / target_path

            logger.info(f"Target folder: {self.target_path}")

            # Check if manifest.json exists
            self.manifest_path = self.target_path / "manifest.json"
            if not self.manifest_path.exists():
                logger.error(f"❌ manifest.json not found at {self.manifest_path}")
                logger.error("Please run 'dbt compile', 'dbt run', or 'dbt build' to generate the manifest.json file.")
                return False

            logger.info(f"✅ Found manifest.json at: {self.manifest_path}")
            return True

        except Exception as e:
            logger.error(f"❌ Error reading dbt_project.yml: {e}")
            return False

    def step_3_extract_model_info(self) -> List[ModelInfo]:
        """
        Step 3: Extract model information from manifest.json

        Returns:
            List[ModelInfo]: List of model information objects
        """
        logger.info("Step 3: Extracting model information from manifest.json...")

        try:
            with open(self.manifest_path, 'r') as f:
                manifest = json.load(f)

            models = []

            # Extract model nodes
            for node_id, node in manifest.get('nodes', {}).items():
                if node.get('resource_type') == 'model':
                    model_info = ModelInfo(
                        name=node.get('name', ''),
                        unique_id=node_id,
                        description=node.get('description', ''),
                        columns=node.get('columns', {}),
                        compiled_sql=node.get('compiled_code', ''),
                        depends_on=node.get('depends_on', {}).get('nodes', []),
                        tags=node.get('tags', []),
                        config=node.get('config', {})
                    )
                    models.append(model_info)

            logger.info(f"✅ Extracted information for {len(models)} models")
            return models

        except Exception as e:
            logger.error(f"❌ Error extracting model info: {e}")
            return []

    def construct_prompt(self, model_info: ModelInfo) -> str:
        """
        Construct a prompt for LLM based on model information

        Args:
            model_info: Model information object

        Returns:
            str: Formatted prompt for LLM
        """
        # Get dependencies names
        dep_names = [dep.split('.')[-1] for dep in model_info.depends_on]

        # Get column information
        column_info = {}
        for col_name, col_data in model_info.columns.items():
            column_info[col_name] = {
                'data_type': col_data.get('data_type', 'unknown'),
                'description': col_data.get('description', '')
            }

        prompt = f"""
You are a data documentation expert. Based on the following dbt model information from manifest.json, create comprehensive documentation in three sections:

**MODEL CONTEXT:**
- Model Name: {model_info.name}
- Compiled SQL: {model_info.compiled_sql[:1000]}...  # Truncated for brevity
- Dependencies: {', '.join(dep_names)}
- Column Metadata: {json.dumps(column_info, indent=2)}
- Tags: {', '.join(model_info.tags)}
- Materialization: {model_info.config.get('materialized', 'table')}

**GENERATE DOCUMENTATION:**

## Business Overview
Provide a clear, non-technical explanation of what this model does, its business purpose, and how stakeholders should interpret the data. Focus on business value and use cases.

## Technical Implementation
Explain the key transformations, joins, and business logic. Highlight any complex calculations, window functions, or data quality considerations. Mention materialization strategy and refresh patterns.

## Data Dictionary
Create a comprehensive table with:
- Column Name
- Data Type
- Business Description
- Source Table/Calculation
- Example Values (if applicable)
- Data Quality Notes

Keep language accessible while maintaining technical accuracy.
"""
        return prompt

    async def call_llm_async(self, prompt: str, model_name: str) -> str:
        """
        Step 4: Make async call to LLM

        Args:
            prompt: The prompt to send to LLM
            model_name: Name of the model to use

        Returns:
            str: LLM response
        """
        async with self.semaphore:  # Limit concurrent requests
            try:
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                }

                payload = {
                    "model": self.model_name,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a technical documentation expert specializing in data engineering and dbt."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.3,
                    "max_tokens": 2000
                }

                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        'https://api.openai.com/v1/chat/completions',
                        headers=headers,
                        json=payload
                    ) as response:
                        if response.status == 200:
                            result = await response.json()
                            return result['choices'][0]['message']['content']
                        else:
                            error_text = await response.text()
                            logger.error(f"LLM API error: {response.status} - {error_text}")
                            return "Error generating documentation"

            except Exception as e:
                logger.error(f"Error calling LLM: {e}")
                return "Error generating documentation"

    def step_5_save_doc_blocks(self, model_info: ModelInfo, llm_response: str) -> bool:
        """
        Step 5: Save response as markdown file with doc blocks

        Args:
            model_info: Model information object
            llm_response: Response from LLM

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create docs directory if it doesn't exist
            docs_dir = self.project_root / "docs"
            docs_dir.mkdir(exist_ok=True)

            # Create markdown file with doc block
            doc_block_name = f"{model_info.name}_doc"
            markdown_content = f"""
{{% docs {doc_block_name} %}}
{llm_response}
{{% enddocs %}}
"""

            # Save to markdown file
            doc_file = docs_dir / f"{model_info.name}_doc.md"
            with open(doc_file, 'w') as f:
                f.write(markdown_content)

            logger.info(f"✅ Saved doc block for {model_info.name}")
            return True

        except Exception as e:
            logger.error(f"❌ Error saving doc block: {e}")
            return False

    def step_6_update_yaml_files(self, models: List[ModelInfo]) -> bool:
        """
        Step 6: Update YAML files with doc block references

        Args:
            models: List of model information objects

        Returns:
            bool: True if successful, False otherwise
        """
        logger.info("Step 6: Updating YAML files with doc block references...")

        try:
            # Find all YAML files in models directory
            models_dir = self.project_root / "models"
            yaml_files = list(models_dir.glob("**/*.yml")) + list(models_dir.glob("**/*.yaml"))

            for yaml_file in yaml_files:
                with open(yaml_file, 'r') as f:
                    yaml_content = yaml.safe_load(f)

                # Update models section
                if 'models' in yaml_content:
                    for model_config in yaml_content['models']:
                        model_name = model_config['name']

                        # Find matching model info
                        matching_model = next((m for m in models if m.name == model_name), None)
                        if matching_model:
                            # Update description with doc block reference
                            doc_block_name = f"{model_name}_doc"
                            model_config['description'] = f"{{{{ doc('{doc_block_name}') }}}}"

                            logger.info(f"Updated {model_name} in {yaml_file}")

                # Write updated YAML back to file
                with open(yaml_file, 'w') as f:
                    yaml.dump(yaml_content, f, default_flow_style=False, sort_keys=False)

            logger.info("✅ Updated YAML files with doc block references")
            return True

        except Exception as e:
            logger.error(f"❌ Error updating YAML files: {e}")
            return False

    async def run_automation(self):
        """
        Main method to run the complete automation process
        """
        logger.info("🚀 Starting dbt documentation automation...")

        # Step 1: Check dbt project
        if not self.step_1_check_dbt_project():
            return

        # Step 2: Get target folder
        if not self.step_2_get_target_folder():
            return

        # Step 3: Extract model information
        models = self.step_3_extract_model_info()
        if not models:
            return

        # Step 4 & 5: Process each model with LLM and save doc blocks
        tasks = []
        for model_info in models:
            task = self.process_model(model_info)
            tasks.append(task)

        # Run all tasks concurrently
        results = await asyncio.gather(*tasks)

        # Step 6: Update YAML files
        if all(results):
            self.step_6_update_yaml_files(models)
            logger.info("🎉 Documentation automation completed successfully!")
        else:
            logger.error("❌ Some models failed to process")

    async def process_model(self, model_info: ModelInfo) -> bool:
        """
        Process a single model: generate prompt, call LLM, save doc block

        Args:
            model_info: Model information object

        Returns:
            bool: True if successful, False otherwise
        """
        logger.info(f"Processing model: {model_info.name}")

        # Construct prompt
        prompt = self.construct_prompt(model_info)

        # Call LLM
        llm_response = await self.call_llm_async(prompt, model_info.name)

        # Save doc block
        return self.step_5_save_doc_blocks(model_info, llm_response)

# Main execution
async def main():
    """
    Main entry point for the automation tool
    """
    # Get API key from environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ Please set OPENAI_API_KEY environment variable")
        return

    # Initialize and run automation
    automator = DBTDocumentationAutomator(api_key)
    await automator.run_automation()

if __name__ == "__main__":
    asyncio.run(main())
