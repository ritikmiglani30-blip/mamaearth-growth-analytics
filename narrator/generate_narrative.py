import json
import os
from google import genai


def generate_scr_narrative(findings: dict) -> dict:
    # System instruction defines the analyst role and strict output rules
    system_instruction = """
You are a senior data analyst writing for Mamaearth's regional ops and finance heads.

Write the business narrative using exactly three labeled sections:
Situation
Complication
Resolution

Every number in the output must come only from the supplied findings
and must appear with the same value. Do not invent, estimate, calculate,
or introduce any statistics that are not present in the supplied findings.
Keep the narrative factual and business-focused.
"""

    # Build the user prompt from the supplied findings dictionary
    contents = f"""
Create an SCR (Situation–Complication–Resolution) business narrative
from the following verified findings:

{json.dumps(findings, indent=2)}

Use the findings as the only source of numerical information.
"""

    # Create Gemini client using the API key from the environment
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return {
            "status": "error",
            "narrative": None,
            "message": "GEMINI_API_KEY is not set."
        }

    try:
        client = genai.Client(
            api_key=api_key,
            http_options={"timeout": 30000}
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.0,  # Deterministic setting for a factual business report
                max_output_tokens=500
            )
        )

        return {
            "status": "success",
            "narrative": response.text,
            "tokens": getattr(response.usage_metadata, "total_token_count", None)
        }

    except Exception as err:
        return {
            "status": "error",
            "narrative": None,
            "message": str(err)
        }

def generate_scr_narrative_offline(findings: dict) -> dict:
    """Generate a deterministic SCR narrative without API or network access."""

    cleaned_revenue = findings["cleaned_total_revenue_inr"]
    raw_revenue = findings["raw_total_revenue_inr"]
    duplicate_delta = findings["duplicate_reconciliation_delta_inr"]

    cod_rate = findings["return_rate_by_payment"]["COD"]
    card_rate = findings["return_rate_by_payment"]["CARD"]
    upi_rate = findings["return_rate_by_payment"]["UPI"]

    risk_payment = findings["highest_risk_segment"]["payment_method"]
    risk_tier = findings["highest_risk_segment"]["city_tier"]
    risk_rate = findings["highest_risk_segment"]["return_rate_pct"]

    peak_month = "March" if findings["true_peak_month"]["month"] == "2026-03" else findings["true_peak_month"]["month"]
    peak_revenue = findings["true_peak_month"]["revenue_inr"]

    inflated_month = findings["outlier_inflated_month"]["month"]
    apparent_revenue = findings["outlier_inflated_month"]["apparent_revenue_inr"]
    corrected_revenue = findings["outlier_inflated_month"]["corrected_revenue_inr"]

    narrative = f"""Situation

The cleaned dataset shows total revenue of {cleaned_revenue:.2f} INR,
compared with raw revenue of {raw_revenue:.2f} INR. The reconciliation
difference is {duplicate_delta:.2f} INR. Return rates are {cod_rate:.1f}%
for COD, {card_rate:.1f}% for CARD, and {upi_rate:.1f}% for UPI.

Complication

The highest-risk segment is {risk_payment} in city tier {risk_tier},
with a return rate of {risk_rate:.1f}%. The month with the highest
apparent revenue was {inflated_month}, at {apparent_revenue:.2f} INR,
but after correcting quantity outliers it becomes {corrected_revenue:.2f} INR.

Resolution

The true peak month after correcting quantity outliers is {peak_month},
with revenue of {peak_revenue:.2f} INR. Regional operations and finance
teams should use the cleaned revenue and return-rate findings when
evaluating performance and prioritizing return-risk actions.
"""

    return {
        "status": "success",
        "narrative": narrative,
        "tokens": None
    }
def check_numeric_accuracy(narrative: str) -> bool:
    """Check that all required verified figures appear in the narrative."""

    normalized = narrative.replace(",", "")

    checks = {
        "Cleaned revenue 97358.3": "97358.3" in normalized,
        "COD return rate 44.4": "44.4" in normalized,
        "Highest-risk rate 54.5": "54.5" in normalized,
        "Duplicate reconciliation 2501.9": "2501.9" in normalized,
        "March peak revenue 20318.9": (
            "March" in narrative and "20318.9" in normalized
        )
    }

    all_passed = True

    print("\nNumeric accuracy checklist:")

    for name, passed in checks.items():
        if passed:
            print(f"PASS - {name}")
        else:
            print(f"FAIL - {name}")
            all_passed = False

    return all_passed


if __name__ == "__main__":
    with open("narrator/findings.json", "r", encoding="utf-8") as f:
        findings = json.load(f)

    result = generate_scr_narrative(findings)

    if result["status"] == "error":
        print("Gemini unavailable. Using offline fallback.")
        result = generate_scr_narrative_offline(findings)
    print("\n" + result["narrative"])
    check_numeric_accuracy(result["narrative"])

    with open("narrator/sample_output.txt", "w", encoding="utf-8") as f:
        f.write(result["narrative"])

