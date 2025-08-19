"""
Generates 70 discussion forum questions by systematically combining dimensions from 4 categories (intent, specificity, domain, persona) and using LLM to create authentic questions that match The L Suite user profile.

Input data sources: ../final-dimensions/final-dimensions.json
Output destinations: generated_discussion_questions.json 
Dependencies: OpenAI API key in .env file, langchain_openai, pydantic
Key exports: generate_questions(), DimensionInfo, GeneratedQuestion, QuestionResults
Side effects: Creates JSON output file, makes LLM API calls
"""

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import json
import itertools


class DimensionInfo(BaseModel):
    dimension: str
    description: str
    examples: List[str]


class GeneratedQuestion(BaseModel):
    question: str
    intent_dimension: DimensionInfo
    specificity_dimension: DimensionInfo
    domain_dimension: DimensionInfo
    persona_dimension: DimensionInfo


class QuestionResults(BaseModel):
    questions: List[GeneratedQuestion]
    total_generated: int


load_dotenv()


# Load dimensions data
def load_dimensions():
    import os

    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Navigate to the final-dimensions directory
    dimensions_file = os.path.join(
        script_dir, "..", "final-dimensions", "final-dimensions.json"
    )

    with open(dimensions_file, "r") as f:
        return json.load(f)


# Generate all possible combinations systematically
def generate_dimension_combinations(dimensions_data):
    intent_dims = dimensions_data["Intent & Task Type"]
    specificity_dims = dimensions_data["Request Specificity & Clarity"]
    domain_dims = dimensions_data["Domain & Subject Matter"]
    persona_dims = dimensions_data["User & Contextual Profile"]

    # Generate all possible combinations systematically
    all_combinations = list(
        itertools.product(intent_dims, specificity_dims, domain_dims, persona_dims)
    )

    total_combinations = len(all_combinations)
    print(f"Total possible combinations: {total_combinations}")
    print(f"Will generate {total_combinations} questions using all combinations")

    return all_combinations


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

Generate 1 question using the following dimensional context to shape the question:

**Request Intent Category - {intent_dimension}:**
Description: {intent_description}
Examples: {intent_examples}

**Request Specificity - {specificity_dimension}:**
Description: {specificity_description} 
Examples: {specificity_examples}

**Domain & Subject Matter - {domain_dimension}:**
Description: {domain_description}
Examples: {domain_examples}

**User Persona - {persona_dimension}:**
Description: {persona_description}
Examples: {persona_examples}

CRITICAL INSTRUCTIONS FOR STYLE MATCHING:
- Capture the INTENT and CONTEXT of the examples while VARYING the phrasing
- Match the level of detail and specificity shown in the examples
- Include similar contextual details based on the dimensional context that match the persona
- Use the same natural, peer-to-peer conversational tone as the examples

AVOID THESE REPETITIVE PATTERNS:
- Do NOT start every question with "For those of you..." or "For those..."
- Do NOT always use "For those leading..." or "For those at..."
- Do NOT always use "Curious to hear..." or "Has anyone..."
- Do NOT end every question with "Would love to hear..." or "much appreciated"
- AVOID using the exact same opening as previous questions

INSTEAD, VARY YOUR OPENINGS based on the intent:
- For Resource Acquisition: "Looking for recommendations on...", "Need help finding...", "Can anyone suggest...", "We need a consultant who..."
- For Knowledge Sharing: "What's your approach to...", "How do other companies handle...", "What strategies work for...", "Anyone have experience with..."
- For Problem Resolution: "We're struggling with...", "Running into issues with...", "Need guidance on...", "How do you solve..."
- For different personas: Adjust formality and technical depth appropriately

VARY YOUR CLOSINGS:
- Mix between: "Thanks!", "Any insights?", "Appreciate the help", or simply end without a closing
- Sometimes include context about urgency or specific needs
- Sometimes just end with the question

Your question should:
- Reflect the intent, specificity, domain, and persona through CONTENT not just phrasing
- Sound authentic to someone in that role/situation
- Feel natural and varied, not formulaic

Generate a question that captures the essence of the dimensional context while sounding fresh and different from typical patterns."""


# Simple question model for LLM output
class SimpleQuestion(BaseModel):
    question: str


def generate_questions():
    """Main function to generate all questions based on dimension combinations."""
    print("Loading dimensions...")
    dimensions_data = load_dimensions()

    print("Generating dimension combinations...")
    combinations = generate_dimension_combinations(dimensions_data)

    print("Setting up LLM...")
    llm = ChatOpenAI(model="gpt-5-mini")
    structured_llm = llm.with_structured_output(SimpleQuestion)

    prompt_template = create_prompt_template()

    generated_questions = []

    print(f"Generating {len(combinations)} questions...")
    for i, (intent_dim, specificity_dim, domain_dim, persona_dim) in enumerate(
        combinations, 1
    ):
        print(f"Generating question {i}/{len(combinations)}...")

        # Prepare the prompt with dimension values
        filled_prompt = prompt_template.format(
            intent_dimension=intent_dim["dimension"],
            intent_description=intent_dim["description"],
            intent_examples="\n".join(f"- {ex}" for ex in intent_dim["examples"]),
            specificity_dimension=specificity_dim["dimension"],
            specificity_description=specificity_dim["description"],
            specificity_examples="\n".join(
                f"- {ex}" for ex in specificity_dim["examples"]
            ),
            domain_dimension=domain_dim["dimension"],
            domain_description=domain_dim["description"],
            domain_examples="\n".join(f"- {ex}" for ex in domain_dim["examples"]),
            persona_dimension=persona_dim["dimension"],
            persona_description=persona_dim["description"],
            persona_examples="\n".join(f"- {ex}" for ex in persona_dim["examples"]),
        )

        # Generate the question using LLM
        try:
            response = structured_llm.invoke(filled_prompt)

            # Create the full question object with dimension metadata
            question_obj = GeneratedQuestion(
                question=response.question,
                intent_dimension=DimensionInfo(
                    dimension=intent_dim["dimension"],
                    description=intent_dim["description"],
                    examples=intent_dim["examples"],
                ),
                specificity_dimension=DimensionInfo(
                    dimension=specificity_dim["dimension"],
                    description=specificity_dim["description"],
                    examples=specificity_dim["examples"],
                ),
                domain_dimension=DimensionInfo(
                    dimension=domain_dim["dimension"],
                    description=domain_dim["description"],
                    examples=domain_dim["examples"],
                ),
                persona_dimension=DimensionInfo(
                    dimension=persona_dim["dimension"],
                    description=persona_dim["description"],
                    examples=persona_dim["examples"],
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

    # Save to JSON file in the same directory as this script
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "generated_discussion_questions.json")
    print(f"Saving {len(generated_questions)} questions to {output_path}...")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results.model_dump(), f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully generated {len(generated_questions)} questions!")
    print(f"📁 Output saved to: {output_path}")

    return results


if __name__ == "__main__":
    generate_questions()
