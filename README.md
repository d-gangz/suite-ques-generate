# Suite Question Generation

A comprehensive system for generating diverse evaluation questions to test AI assistants serving legal professionals. This project combines real discussion forum data analysis with systematic prompt classification to create robust evaluation datasets.

## Project Overview

This project serves The L Suite platform where Chief Legal Officers (CLOs) and General Counsels (GCs) from leading companies engage in peer discussions. The system generates evaluation questions across two key methodologies:

1. **Discussion Forum Questions** (70 generated) - Real-world questions derived from dimensional analysis of actual forum threads
2. **Prompt Classification Questions** (50 generated) - Systematic coverage of 13 distinct interaction categories

**Total Output**: 120 diverse evaluation questions testing various AI assistant capabilities

## Project Structure

```
suite-ques-generate/
├── 1-discussion-forum/           # Real discussion forum data analysis
│   ├── recent_threads_Aug2025.csv    # Raw forum data (500+ threads)
│   ├── threads_cleaned.json          # Processed unique threads
│   ├── process_threads.py            # Data cleaning & deduplication
│   ├── dimensions.json               # Initial dimensional framework
│   └── generate-questions/           
│       ├── final-dimensions/         
│       │   ├── generate-dimensions.py    # AI-powered dimension analysis
│       │   ├── final-dimensions.json     # Refined 4-category dimensions
│       │   └── results.md                 # Dimension analysis results
│       └── questions/                
│           ├── discussion-questions.py       # Question generation (70 questions)
│           ├── convert_json_to_csv.py       # JSON to CSV converter
│           ├── generated_discussion_questions.json    
│           └── generated_discussion_questions.csv     
│
├── 2-prompt-classification/      # Systematic prompt categorization
│   ├── Lloyd_Prompt_Classification.csv   # Complete taxonomy (13 categories)
│   ├── prompt_categories.json            # Structured category data
│   └── generate-questions/               
│       ├── prompt-classify-questions.py      # Question generation (50 questions)
│       ├── convert_json_to_csv.py           # JSON to CSV converter
│       ├── generated_prompt_classification_questions.json
│       └── generated_prompt_classification_questions.csv
│
├── requirements.txt              # Project dependencies
└── README.md                     # This file
```

## Implementation Details

### 1. Discussion Forum Analysis (`1-discussion-forum/`)

**Data Processing Pipeline**:
- **Raw Data**: 500+ discussion forum threads from August 2025 (`recent_threads_Aug2025.csv`)
- **Cleaning**: Removed duplicates using MD5 hashing, extracted title/body pairs (`process_threads.py`)
- **Analysis**: Generated dimensional analysis using Google Vertex AI Gemini 2.5 Pro (`generate-dimensions.py`)
- **Generation**: Created 70 questions using systematic dimensional combinations with GPT-5-mini

**4-Category Dimensional Framework** (from final-dimensions.json):

1. **Intent & Task Type**:
   - Seeking Referrals & Recommendations - Direct recommendations for service providers, tools, counsel
   - Benchmarking & Peer Insights - Understanding common practices and market standards
   - Seeking Templates & Precedents - Sample documents, policies, checklists to use as starting points
   - Problem Solving & Strategic Advice - Complex scenarios requiring strategic frameworks

2. **Request Specificity & Clarity**:
   - Highly Specified Request - Well-defined with clear, actionable parameters
   - Multi-Part & Complex Inquiry - Series of detailed questions within a single query
   - Vague or Exploratory Inquiry - Broad, open-ended requests in early research stages

3. **Domain & Subject Matter**:
   - Legal & Compliance Operations - Business of law, technology, process optimization, vendor management
   - Substantive Legal Practice Areas - Core legal disciplines (governance, M&A, IP, litigation, employment)
   - Cross-Functional & Business Strategy - Beyond legal department, involving other business units

4. **User & Contextual Profile**:
   - Company-Specific Context - Critical context about company stage, industry, specific situation
   - Personal or Pro Bono Request - Requests on behalf of third parties or pro bono matters

**Generation Method**:
- Systematically combines all 4 dimensions (4x3x3x2 = 72 possible combinations)
- Generated 70 questions from the 72 possible combinations
- Each question includes full dimensional metadata for analysis

### 2. Prompt Classification System (`2-prompt-classification/`)

**Classification-Based Generation**:
- **Source**: 13 carefully curated prompt categories from Lloyd_Prompt_Classification.csv
- **Method**: Cycled through categories to generate 50 questions (each category gets 3-4 questions)
- **Model**: GPT-5-mini with structured output using Pydantic models
- **Output**: JSON with full category metadata + CSV for easy analysis

**13 Prompt Categories**:
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

## Technical Stack

- **Python 3.11+** - Core programming language
- **LangChain** - LLM orchestration and structured output
- **OpenAI GPT-5-mini** - Question generation
- **Google Vertex AI (Gemini 2.5 Pro)** - Dimensional analysis
- **Pydantic** - Data validation and structured models
- **uv** - Python package management

## Setup and Usage

### Prerequisites

```bash
# Install dependencies using uv
uv pip install -r requirements.txt

# Set up environment variables in .env file
OPENAI_API_KEY=your_openai_key
GOOGLE_APPLICATION_CREDENTIALS=path_to_gcp_credentials.json
```

### Running the Pipeline

#### 1. Process Raw Forum Data
```bash
cd 1-discussion-forum/
uv run process_threads.py
# Output: threads_cleaned.json (deduplicated threads)
```

#### 2. Generate Dimensional Analysis
```bash
cd 1-discussion-forum/generate-questions/final-dimensions/
uv run generate-dimensions.py
# Output: results.md, final-dimensions.json
```

#### 3. Generate Discussion Forum Questions
```bash
cd 1-discussion-forum/generate-questions/questions/
uv run discussion-questions.py
# Output: 70 questions in generated_discussion_questions.json

# Convert to CSV
uv run convert_json_to_csv.py
# Output: generated_discussion_questions.csv
```

#### 4. Generate Prompt Classification Questions
```bash
cd 2-prompt-classification/generate-questions/
uv run prompt-classify-questions.py
# Output: 50 questions in generated_prompt_classification_questions.json

# Convert to CSV
uv run convert_json_to_csv.py
# Output: generated_prompt_classification_questions.csv
```

## Project Status

### ✅ Completed

- Raw discussion forum data collection (500+ threads)
- Data cleaning and deduplication pipeline
- AI-powered dimensional analysis framework
- Complete prompt classification taxonomy (13 categories)
- Discussion forum question generation (70 questions)
- Prompt classification question generation (50 questions)
- JSON to CSV conversion utilities
- Full dimensional and category metadata preservation

### 📊 Generated Outputs

- **Total Questions Generated**: 120
- **Discussion Forum Questions**: 70 (with 4-dimensional metadata)
- **Prompt Classification Questions**: 50 (across 13 categories)
- **Output Formats**: JSON (with full metadata) and CSV (for analysis)

## Key Files

| File | Purpose |
|------|---------|
| `1-discussion-forum/process_threads.py` | Data cleaning and deduplication script |
| `1-discussion-forum/threads_cleaned.json` | Processed unique forum threads |
| `1-discussion-forum/generate-questions/final-dimensions/generate-dimensions.py` | AI-powered dimension analysis tool |
| `1-discussion-forum/generate-questions/final-dimensions/final-dimensions.json` | Refined 4-category dimensional framework |
| `1-discussion-forum/generate-questions/questions/discussion-questions.py` | Discussion forum question generator |
| `2-prompt-classification/prompt_categories.json` | Structured category taxonomy |
| `2-prompt-classification/generate-questions/prompt-classify-questions.py` | Prompt classification question generator |
| `recent_threads_Aug2025.csv` | Raw forum data source (500+ threads) |
| `Lloyd_Prompt_Classification.csv` | Complete prompt classification system (13 categories) |

## Key Insights

### Target Audience Profile
The L Suite serves C-level legal executives (CLOs, GCs) at technology-forward companies including:
- Grammarly, Notion, Lyft, Mastercard, Hubspot
- Andreessen Horowitz, Google Ventures, Riskified
- Both early-stage startups and established public corporations

### Question Generation Approach
1. **Dimensional Combinations**: Systematically combines 4 dimension categories to ensure comprehensive coverage
2. **Authentic Voice**: Maintains peer-to-peer conversational tone matching real forum discussions
3. **Varied Openings**: Avoids repetitive patterns by varying question starters based on intent
4. **Context-Rich**: Includes industry-specific details and realistic scenarios

## Dependencies

Key Python packages (see `requirements.txt` for full list):
- `langchain-openai` - OpenAI LLM integration
- `langchain-google-vertexai` - Google AI integration
- `pydantic` - Data validation and structured output
- `python-dotenv` - Environment variable management

## Future Enhancements

- **Quality Scoring Algorithm**: Automated assessment of question difficulty and coverage
- **Real-time Generation**: Dynamic question creation based on emerging forum topics
- **Multi-Model Comparison**: Test questions across different AI assistants
- **Feedback Loop**: Incorporate user ratings to improve generation quality
- **Domain Expansion**: Extend framework to other professional communities