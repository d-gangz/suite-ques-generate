"""
Script to generate dimensions analysis of discussion forum threads using AI.

Input data sources: ../threads_cleaned.json  
Output destinations: results.md
Dependencies: Google Vertex AI API, langchain libraries
Key exports: main()
Side effects: Creates results.md file, makes AI API calls
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import HumanMessage

# Load environment variables from .env file
load_dotenv()


def load_threads_data(filepath):
    """Load and return the threads data from JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def prepare_conversations_text(threads_data):
    """Prepare all conversations for analysis using only thread_body content."""
    threads = threads_data["threads"]

    conversations_text = ""
    for i, thread in enumerate(threads, 1):
        conversations_text += f"{i}. {thread['thread_body']}\n\n"

    return conversations_text


def create_full_prompt(conversations_text):
    """Create the full prompt with embedded template and conversation data."""

    prompt = f"""You are tasked with analyzing a set of conversations or queries to identify key dimensions that characterize different aspects of user interactions.

<context>
The Suite is a platform designed to help top executives—primarily in legal (CLOs) in curated, invite-only communities. These communities are tailored according to leadership functions and consist of peer executives from early-stage to public companies, as well as investment funds.

The platform's goal is to foster rapid information exchange and actionable insights through carefully curated peer groups, leveraging a mix of AI-driven tools, proprietary data, and a hybrid of online and in-person interactions. The Suite emphasizes privacy and trust, providing a "brain trust" environment where executives can solve complex problems, "gut check" ideas, and gain confidence in their approaches with support from peers.

Notable members include executives from companies such as Grammarly, Riskified, Notion, Google Ventures, Andreessen Horowitz, Hubspot, Mastercard, Lyft, and Nomad Health. Testimonials highlight the value members receive: actionable insights, new perspectives, meaningful connections, and a sense of trusted community.
</context>

<conversations>
{conversations_text}
</conversations>

Your goal is to analyze these conversations/queries and identify the key dimensions that categorize different aspects of user requests and interactions. These dimensions should represent axes of variation and help systematically understand the types of requests users make within the given context.

Guidelines for identifying dimensions:

1. Start with at least 4-6 primary dimension categories.
2. Within each category, identify 2-4 specific dimensions based on patterns in the data.
3. Base your choice of dimensions on areas where service providers might face challenges or where clear categorization would be valuable.
4. Consider core user intents (e.g., informational, action-oriented, problem-resolution).
5. Think about how clearly users express their needs (e.g., well-specified, ambiguous, multi-part).
6. Consider user characteristics or personas that emerge from the conversations.
7. Look for patterns in urgency, complexity, or domain-specific requirements.
8. Identify any temporal aspects (scheduling, modifications, deadlines).

For each dimension you identify, provide:

1. A name for the dimension
2. A clear description of what it represents
3. At least 2-3 examples from the conversations that illustrate this dimension. Make sure to include the entire quote from the conversation. DO NOT truncate the quote and omit any part of the quote.

Present your findings as a JSON object with the following structure:

- Top-level keys should be broad categories (e.g., "Request Clarity", "User Type", "Intent Category")
- Each category contains an array of dimension objects
- Each dimension object has: "dimension" (name), "description", and "examples" (array of quoted examples)

Example structure:

```json
{{
  "Category Name 1": [
    {{
      "dimension": "Dimension Name",
      "description": "Clear explanation of what this dimension represents",
      "examples": [
        "Direct FULL quote example 1",
        "Direct FULL quote example 2",
        "Direct FULL quote example 3"
      ]
    }}
  ],
  "Category Name 2": [
    ...
  ]
}}
```

Refer to this for some dimensions you can reference.

```json
{{
  "dimensions": {{
    "Legal Topic": [
      "Commercial Contracts",
      "Employment & HR",
      "Product Counseling",
      "Intellectual Property",
      "Regulatory / Compliance",
      "Corporate Governance",
      "Disputes & Litigation",
      "General / Other"
    ],
    "Intent Type": [
      "Ask for recommendation",
      "Interpret legal requirement",
      "Draft or review a document",
      "Learn from others / Benchmarking",
      "General advice / exploratory"
    ],
    "Jurisdiction": [
      "United States",
      "California",
      "New York",
      "Europe / UK",
      "UAE / International",
      "Unspecified / General"
    ],
    "Query Clarity": [
      "Clear and focused",
      "Moderately clear",
      "Multi-part or exploratory",
      "Vague or underspecified"
    ]
  }}
}}
```

After the JSON analysis, provide a summary of your findings in the following format:

<summary>
Provide a comprehensive summary (3-5 paragraphs) highlighting:
- The most significant patterns or insights observed
- How these dimensions relate to the context provided
- Key challenges or opportunities revealed by the analysis
- Recommendations for how these dimensions could be used to improve service delivery or user experience
- Any notable gaps or areas that might benefit from further investigation
</summary>
"""

    return prompt


def main():
    """Main function to generate dimensions analysis."""

    # Setup paths
    current_dir = Path(__file__).parent
    threads_file = current_dir.parent.parent / "threads_cleaned.json"
    results_file = current_dir / "results.md"

    print("Loading threads data...")
    threads_data = load_threads_data(threads_file)
    print(f"Loaded {len(threads_data['threads'])} threads")

    print("Preparing all conversations for analysis...")
    conversations_text = prepare_conversations_text(threads_data)

    print("Creating full prompt...")
    final_prompt = create_full_prompt(conversations_text)

    print("Initializing AI model...")
    llm = ChatVertexAI(model="gemini-2.5-pro")

    print("Generating dimensions analysis...")
    try:
        response = llm.invoke([HumanMessage(content=final_prompt)])
        response_text = response.content

        print("Saving results...")
        with open(results_file, "w", encoding="utf-8") as f:
            f.write(response_text)

        print(f"Analysis complete! Results saved to: {results_file}")

        # Print a preview
        print("\n" + "=" * 50)
        print("PREVIEW OF RESULTS:")
        print("=" * 50)
        print(
            response_text[:1000] + "..." if len(response_text) > 1000 else response_text
        )

    except Exception as e:
        print(f"Error during AI generation: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
