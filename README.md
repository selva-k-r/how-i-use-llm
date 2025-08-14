# DBT Automations

A collection of practical Generative AI use cases for data engineering, analytics, and automation. This repository showcases real-world applications of Large Language Models to solve common data problems.

## About This Project

After years of working with data pipelines and analytics, I've discovered that LLMs can automate many tedious tasks that traditionally required manual work. This repository documents my experiments and implementations, turning AI capabilities into practical tools.

## Projects Overview

### 🔄 Data Engineering Automation
- **dbt Documentation Automation**: Automatically generate comprehensive documentation from manifest.json using LLMs
- **Data Lineage Visualization**: Create interactive lineage maps for dbt projects
- **Synthetic Data Generation**: Generate realistic test data for unit testing and development

### 📊 Analytics Enhancement
- **SQL Query Optimization**: Use LLMs to suggest performance improvements
- **Data Quality Monitoring**: Automated data profiling and anomaly detection
- **Business Logic Documentation**: Transform technical SQL into business-friendly explanations

## Current Projects

### 1. dbt Documentation Automation
**Status**: ✅ Complete

Automates the creation of comprehensive dbt model documentation using manifest.json and LLM processing.

**Features**:
- Extracts model metadata from dbt artifacts
- Generates business-friendly documentation
- Creates structured prompts for LLMs
- Updates YAML files with doc block references
- Produces markdown files with proper dbt doc blocks

**Directory**: `/dbt-doc-automation/`

### 2. Synthetic Data Generation for Unit Tests
**Status**: 🚧 In Progress

Generates realistic synthetic data for testing data pipelines without using production data.

**Planned Features**:
- Schema-aware data generation
- Referential integrity maintenance
- Configurable data volumes
- Multiple output formats (CSV, JSON, Parquet)

**Directory**: `/synthetic-data-generator/`

### 3. dbt Project Data Lineage
**Status**: 📋 Planned

Creates visual data lineage maps and impact analysis for dbt projects.

**Planned Features**:
- Interactive lineage visualization
- Impact analysis for model changes
- Automated dependency tracking
- Integration with CI/CD pipelines

**Directory**: `/dbt-lineage-tracker/`

## Getting Started

### Prerequisites
- Python 3.8+
- OpenAI API key (or other LLM provider)
- dbt installed (for dbt-related projects)

### Installation
