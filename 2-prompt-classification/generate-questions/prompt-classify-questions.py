"""
Generates 50 prompt classification questions by cycling through prompt categories and using LLM to create authentic questions that match The L Suite user profile for each category type.

Input data sources: ../prompt_categories.json
Output destinations: generated_prompt_classification_questions.json 
Dependencies: OpenAI API key in .env file, langchain_openai, pydantic
Key exports: generate_questions(), CategoryInfo, GeneratedQuestion, QuestionResults
Side effects: Creates JSON output file, makes LLM API calls
"""

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import json
import os


class CategoryInfo(BaseModel):
    category: str
    instruction: str
    examples: List[str]


class GeneratedQuestion(BaseModel):
    question: str
    category_info: CategoryInfo


class QuestionResults(BaseModel):
    questions: List[GeneratedQuestion]
    total_generated: int


load_dotenv()


# Load categories data
def load_categories():
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Navigate to the prompt_categories.json file
    categories_file = os.path.join(script_dir, "..", "prompt_categories.json")

    with open(categories_file, "r") as f:
        return json.load(f)


# Generate cycling sequence for 50 questions from 13 categories
def generate_category_sequence(categories_data, target_count=50):
    category_keys = list(categories_data.keys())
    category_sequence = []

    for i in range(target_count):
        # Cycle through categories
        category_key = category_keys[i % len(category_keys)]
        category_sequence.append((category_key, categories_data[category_key]))

    print(
        f"Will generate {target_count} questions cycling through {len(category_keys)} categories"
    )
    return category_sequence


# Create the prompt template
def create_prompt_template():
    return """You are an expert at generating contextually relevant questions that a target user would ask.

Put yourself in the shoes of these target users when generating the question. Because we are trying to simulate what these users will ask.
<target users>
The L Suite at TheSuite.com is used by a highly specific and exclusive audience consisting of:

Chief Legal Officers (CLOs) and General Counsels (GCs): These are the most senior legal executives within their organizations, responsible for all strategic legal, compliance, and governance matters.

Corporate Legal Leaders: Includes roles such as Corporate Secretary, Head of Global Policy, and similar senior positions within the legal function.

Executives from Leading Companies: Current users are GCs and CLOs at well-known, high-growth or leading organizations such as Grammarly, Notion, Lyft, Mastercard, Hubspot, Andreessen Horowitz, Riskified, Google Ventures, and Nomad Health.

Serves Both Early-Stage and Public Companies: Members come from both startups, growth-stage tech companies, and large, established public corporations, as well as investment funds involved in these markets.

Decision-Makers: All users hold significant decision-making authority and are typically accountable to their board of directors, C-suite, or investors on key legal issues.

In summary:
The L Suite's core users are C-level legal executives—specifically General Counsels, CLOs, and their direct peers—at technology-forward companies and investment funds, who are the ultimate legal decision-makers and thought leaders for their organizations.
</target users>

Generate 1 question using the following category context to shape the question:

**Category - {category_name}:**
Instruction: {category_instruction}
Examples: {category_examples}

CRITICAL INSTRUCTIONS FOR STYLE MATCHING:
- Capture the INTENT and CONTEXT of the examples while VARYING the phrasing
- Match the level of detail and specificity shown in the examples
- Include similar contextual details that match the category instruction
- Use the same natural, peer-to-peer conversational tone as the examples

AVOID THESE REPETITIVE PATTERNS:
- Do NOT start every question with "For those of you..." or "For those..."
- Do NOT always use "For those leading..." or "For those at..."
- Do NOT always use "Curious to hear..." or "Has anyone..."
- Do NOT end every question with "Would love to hear..." or "much appreciated"
- AVOID using the exact same opening as previous questions

INSTEAD, VARY YOUR OPENINGS based on the category:
- For seeking advice: "Looking for recommendations on...", "Need help with...", "Can anyone suggest...", "What's your approach to..."
- For research topics: "What's the latest on...", "Can someone help me understand...", "Need to research..."
- For finding vendors: "Anyone have experience with...", "Looking for a vendor who...", "Need recommendations for..."
- For document work: "Can you help me...", "Need assistance with...", "Looking for guidance on..."
- For community questions: "How do I...", "Can someone explain...", "What's the process for..."

VARY YOUR CLOSINGS:
- Mix between: "Thanks!", "Any insights?", "Appreciate the help", or simply end without a closing
- Sometimes include context about urgency or specific needs
- Sometimes just end with the question

Your question should:
- Reflect the category instruction through CONTENT not just phrasing
- Sound authentic to someone in that legal executive role
- Feel natural and varied, not formulaic
- Match the examples' style and context

Generate a question that captures the essence of the category while sounding fresh and different from typical patterns."""


# Simple question model for LLM output
class SimpleQuestion(BaseModel):
    question: str


def generate_questions():
    """Main function to generate 50 questions based on category cycling."""
    print("Loading categories...")
    categories_data = load_categories()

    print("Generating category sequence...")
    category_sequence = generate_category_sequence(categories_data, target_count=50)

    print("Setting up LLM...")
    llm = ChatOpenAI(model="gpt-5-mini")
    structured_llm = llm.with_structured_output(SimpleQuestion)

    prompt_template = create_prompt_template()

    generated_questions = []

    print(f"Generating {len(category_sequence)} questions...")
    for i, (_, category_data) in enumerate(category_sequence, 1):
        print(
            f"Generating question {i}/{len(category_sequence)} (Category: {category_data['category']})..."
        )

        # Prepare the prompt with category values
        filled_prompt = prompt_template.format(
            category_name=category_data["category"],
            category_instruction=category_data["instruction"],
            category_examples="\n".join(f"- {ex}" for ex in category_data["examples"]),
        )

        # Generate the question using LLM
        try:
            response = structured_llm.invoke(filled_prompt)

            # Create the full question object with category metadata
            question_obj = GeneratedQuestion(
                question=response.question,
                category_info=CategoryInfo(
                    category=category_data["category"],
                    instruction=category_data["instruction"],
                    examples=category_data["examples"],
                ),
            )

            generated_questions.append(question_obj)

        except Exception as e:
            print(f"Error generating question {i}: {e}")
            continue

    # Create final results object
    results = QuestionResults(
        questions=generated_questions, total_generated=len(generated_questions)
    )

    # Save to JSON file
    output_path = "generated_prompt_classification_questions.json"
    print(f"Saving {len(generated_questions)} questions to {output_path}...")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results.model_dump(), f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully generated {len(generated_questions)} questions!")
    print(f"📁 Output saved to: {output_path}")

    return results


if __name__ == "__main__":
    generate_questions()
