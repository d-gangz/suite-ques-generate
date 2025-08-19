# Lloyd Evaluation Prompt Generator

A comprehensive system for generating diverse evaluation prompts to test Lloyd, an AI assistant designed for legal professionals. This project combines real discussion forum data with systematic prompt classification to create a robust evaluation dataset.

## Project Overview

Lloyd serves a legal community platform (The Suite) where members ask questions ranging from seeking peer advice to document drafting. To ensure Lloyd handles the full spectrum of user needs effectively, this project generates evaluation prompts across two key dimensions:

1. **Discussion Forum Questions** (~50 prompts) - Real questions from legal professionals with dimensional analysis
2. **Prompt Classification Categories** (~50 prompts) - Systematic coverage of all anticipated user interaction patterns

**Target Output**: ~100 diverse evaluation prompts that comprehensively test Lloyd's capabilities

## Project Structure

ques-generate/
├── 1-discussion-forum/ # Real discussion forum data analysis
│ ├── recent_threads_Aug2025.csv # Raw forum data (500+ threads)
│ ├── threads_cleaned.json # Processed unique threads
│ ├── process_threads.py # Data cleaning script
│ ├── legal_dimensions.json # Dimensional analysis framework
│ └── generate-questions/ # Generated prompts (future)
│
├── 2-prompt-classification/ # Systematic prompt categorization
│ ├── Lloyd_Prompt_Classification.csv # Complete taxonomy (13 categories)
│ ├── prompt_categories.json # Structured category data
│ └── generate-questions/ # Generated prompts (future)
│
├── requirements.txt # Project dependencies
└── README.md # This file

## Data Sources

### 1. Discussion Forum Analysis (`1-discussion-forum/`)

**Source**: 500+ recent discussion forum threads from August 2025

**Dimensional Framework**:

- **Legal Topics**: Commercial Contracts, Employment & HR, Product Counseling, Intellectual Property, Regulatory/Compliance, Corporate Governance, Disputes & Litigation, General/Other
- **Intent Types**: Ask for recommendation, Interpret legal requirement, Draft/review document, Learn from others/Benchmarking, General advice/exploratory
- **Jurisdictions**: United States, California, New York, Europe/UK, UAE/International, Unspecified/General
- **Query Clarity**: Clear and focused, Moderately clear, Multi-part or exploratory, Vague or underspecified

**Example Forum Questions**:

- "Seeking A Cost-effective Debt Collection Litigator in Texas"
- "Legal & Compliance Challenges Of Turning On-Prem Customers Into Cloud Users"
- "Digital Media Anti-Piracy Efforts"

### 2. Prompt Classification System (`2-prompt-classification/`)

**Complete Taxonomy** (13 categories covering all anticipated Lloyd interactions):

1. **Seek advice or guidance** - Peer insights, market practice, benchmarks
2. **Research a topic** - Information gathering, best practices, horizon scanning
3. **Find a vendor or outside counsel** - Service provider recommendations
4. **Find a member with expertise** - Connect with specialized knowledge
5. **Find members with profile attributes** - Networking based on role/location/expertise
6. **Brainstorm an idea** - Open-ended discussion, pressure testing decisions
7. **Review a document** - Contract analysis, policy review, compliance checking
8. **Draft a document** - Creating legal documents, templates, clauses from scratch
9. **Look up and summarize law** - Plain-language explanations of regulations
10. **Summarize or edit content** - Text processing, rephrasing, editing
11. **General community questions** - Membership, platform access, The Suite itself
12. **Find upcoming event info** - Event dates, details, RSVP information
13. **Redact a document** - PII and sensitive information removal

**Note**: Only categories 1-4 align with typical discussion forum questions. Categories 5-13 represent additional Lloyd capabilities beyond forum discussions.

## Setup and Usage

### Prerequisites

```bash
# Install dependencies
uv pip install -r requirements.txt
```

### Data Processing

```bash
# Process raw forum threads (remove duplicates, extract title/body)
cd 1-discussion-forum/
uv run process_threads.py
```

This creates `threads_cleaned.json` with unique forum threads and metadata.

### Current Status

**Completed**:

-  Raw discussion forum data collection (500+ threads)
-  Data cleaning and deduplication pipeline
-  Legal dimensional analysis framework
-  Complete prompt classification taxonomy
-  Structured data formats for both sources

**In Progress**:

- = Evaluation prompt generation algorithms
- = Dimensional sampling strategies
- = Quality assurance frameworks

**Planned**:

- � Generate ~50 prompts from discussion forum data
- � Generate ~50 prompts from classification categories
- � Validation and quality scoring
- � Final evaluation dataset assembly

## Methodology

### Discussion Forum Prompt Generation

1. **Dimensional Sampling**: Ensure coverage across legal topics, intent types, jurisdictions, and clarity levels
2. **Realistic Variation**: Maintain authentic language patterns from real legal professionals
3. **Complexity Distribution**: Include simple, moderate, and complex scenarios

### Classification-Based Prompt Generation

1. **Category Coverage**: Generate prompts for each of the 13 classification categories
2. **Edge Case Testing**: Include boundary conditions and ambiguous scenarios
3. **Integration Testing**: Test combinations of categories and multi-step workflows

### Quality Assurance

- **Diversity Metrics**: Measure coverage across all dimensional axes
- **Realism Validation**: Ensure prompts reflect actual user patterns
- **Difficulty Gradation**: Include prompts spanning novice to expert complexity
- **Lloyd-Specific Testing**: Focus on legal domain expertise and community platform features

## Key Files

| File                                             | Purpose                               |
| ------------------------------------------------ | ------------------------------------- |
| `1-discussion-forum/process_threads.py`          | Data cleaning and deduplication       |
| `1-discussion-forum/legal_dimensions.json`       | Dimensional analysis framework        |
| `2-prompt-classification/prompt_categories.json` | Structured category taxonomy          |
| `recent_threads_Aug2025.csv`                     | Raw forum data source                 |
| `Lloyd_Prompt_Classification.csv`                | Complete prompt classification system |

## Contributing

When extending this project:

1. **Maintain dimensional balance** - Ensure new prompts don't skew toward specific legal topics or intent types
2. **Preserve authenticity** - Keep language patterns consistent with legal professional communication
3. **Document methodology** - Update this README with any new generation approaches
4. **Validate outputs** - Test generated prompts against Lloyd's actual capabilities

## Future Enhancements

- **Automated Quality Scoring**: Develop metrics for prompt difficulty and coverage
- **Temporal Analysis**: Track how discussion forum patterns evolve over time
- **Personalization Framework**: Generate prompts tailored to specific user segments
- **Cross-Platform Validation**: Test prompts across different legal AI systems
- **Dynamic Generation**: Real-time prompt creation based on emerging forum topics
