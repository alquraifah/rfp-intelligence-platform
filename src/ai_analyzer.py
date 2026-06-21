from src.rag_engine import ask_rfp

def show_result(result):
    print("\nANSWER:")
    print(result["answer"])

    print("\nSOURCES:")
    for source in result["sources"]:
        print(
            f"- {source['filename']} | "
            f"page: {source['page']} | "
            f"sheet: {source['sheet']}"
        )


def ask_custom_question():
    question = input("\nAsk a question about the RFP documents: ")
    return ask_rfp(question)


def analyze_rfp():
    prompt = """
Analyze the RFP documents and provide:

1. Executive Summary
- Project objective
- Scope of work
- Main deliverables

2. Evaluation Criteria
- Scoring criteria
- Weighting or points if available
- Evaluation methodology

3. Important Dates & Deadlines
- Submission deadline
- Clarification deadline
- Award timeline
- Other important milestones

4. General Opportunity Overview
- Overall opportunity description
- Business value
- Main proposal focus areas

Use only the retrieved RFP context.
If information is incomplete, clearly state that it is not fully available.
Format the output professionally with headings and bullet points.
"""
    return ask_rfp(prompt)


def requirement_intelligence():
    prompt = """
Perform Requirement Intelligence for the RFP documents.

Classify the requirements into:

1. Technical Requirements
2. Submission Requirements
3. Compliance Requirements
4. Legal Requirements
5. Financial / Pricing Requirements
6. Required Documents
7. Critical & Mandatory Requirements

For each section:
- List the requirements clearly.
- Mention if the requirement appears mandatory or rated.
- Mention uncertainty if the context is incomplete.

Use only the retrieved RFP context.
Format the output professionally with headings and bullet points.
"""
    return ask_rfp(prompt)


def bid_readiness_assessment():
    prompt = """
Perform a Bid Readiness Assessment based on the RFP documents.

Provide:

1. Readiness Score
- Give a score from 0 to 100.
- Explain the score.

2. Strengths
- Areas where a company may be well-positioned to bid.

3. Weaknesses
- Areas that may reduce readiness.

4. Missing Capabilities
- Skills, experience, certifications, or resources that may be needed.

5. Missing Documents
- Forms, references, pricing documents, certificates, or other required documents.

Use only the retrieved RFP context.
If company-specific information is not available, assess readiness based on RFP requirements and clearly state assumptions.
Format the output professionally with headings and bullet points.
"""
    return ask_rfp(prompt)


def go_no_go_recommendation():
    prompt = """
Based on the RFP documents, provide a Go / No-Go Recommendation.

Choose one:
- GO
- GO WITH CAUTION
- NO GO

Provide:
1. Final recommendation
2. Reasoning
3. Key factors supporting the decision
4. Key risks affecting the decision
5. Top actions before submission

Use only the retrieved RFP context.
If company-specific information is not available, clearly state that the recommendation is based on RFP requirements only.
Format the output professionally with headings and bullet points.
"""
    return ask_rfp(prompt)


def main():
    print("=" * 60)
    print("RFP AI Analyzer")
    print("=" * 60)

    while True:
        print("\nOptions:")
        print("1. Ask a Question")
        print("2. Analyze RFP")
        print("   - Executive Summary")
        print("   - Evaluation Criteria")
        print("   - Important Dates & Deadlines")
        print("   - General Opportunity Overview")
        print("3. Requirement Intelligence")
        print("   - Technical Requirements")
        print("   - Submission Requirements")
        print("   - Compliance Requirements")
        print("   - Legal Requirements")
        print("   - Financial Requirements")
        print("   - Required Documents")
        print("   - Critical & Mandatory Requirements")
        print("4. Bid Readiness Assessment")
        print("   - Readiness Score")
        print("   - Strengths")
        print("   - Weaknesses")
        print("   - Missing Capabilities")
        print("   - Missing Documents")
        print("5. Go / No-Go Recommendation")
        print("   - GO")
        print("   - GO WITH CAUTION")
        print("   - NO GO")
        print("   - Reasoning")
        print("6. Exit")

        choice = input("\nSelect option: ")

        if choice == "1":
            result = ask_custom_question()
            show_result(result)

        elif choice == "2":
            print("\nAnalyzing RFP...")
            result = analyze_rfp()
            show_result(result)

        elif choice == "3":
            print("\nRunning Requirement Intelligence...")
            result = requirement_intelligence()
            show_result(result)

        elif choice == "4":
            print("\nRunning Bid Readiness Assessment...")
            result = bid_readiness_assessment()
            show_result(result)

        elif choice == "5":
            print("\nGenerating Go / No-Go Recommendation...")
            result = go_no_go_recommendation()
            show_result(result)

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1, 2, 3, 4, 5, or 6.")


if __name__ == "__main__":
    main()