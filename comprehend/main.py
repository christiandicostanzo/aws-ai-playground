"""
AWS Comprehend example: sentiment, entities, key phrases, and language detection.

Run with:
    uv run /comprehend/main.py
"""

import boto3

SAMPLE_TEXT = (
    "Amazon Web Services launched a new AI service in Seattle last Tuesday. "
    "CEO Andy Jassy said the product exceeded expectations and customers are thrilled. "
    "The stock rose 4% after the announcement."
)

client = boto3.client("comprehend", region_name="us-east-1")


def detect_language(text: str) -> str:
    response = client.detect_dominant_language(Text=text)
    languages = response["Languages"]
    top = max(languages, key=lambda x: x["Score"])
    print(f"Dominant language: {top['LanguageCode']} (confidence: {top['Score']:.2%})")
    return top["LanguageCode"]


def detect_sentiment(text: str, language_code: str) -> None:
    response = client.detect_sentiment(Text=text, LanguageCode=language_code)
    sentiment = response["Sentiment"]
    scores = response["SentimentScore"]
    print(f"\nSentiment: {sentiment}")
    for label, score in scores.items():
        print(f"  {label}: {score:.2%}")


def detect_entities(text: str, language_code: str) -> None:
    response = client.detect_entities(Text=text, LanguageCode=language_code)
    print("\nEntities:")
    for entity in response["Entities"]:
        print(f"  [{entity['Type']}] {entity['Text']} (confidence: {entity['Score']:.2%})")


def detect_key_phrases(text: str, language_code: str) -> None:
    response = client.detect_key_phrases(Text=text, LanguageCode=language_code)
    print("\nKey phrases:")
    for phrase in response["KeyPhrases"]:
        print(f"  {phrase['Text']} (confidence: {phrase['Score']:.2%})")


def main() -> None:
    print(f"Text: {SAMPLE_TEXT}\n")
    language_code = detect_language(SAMPLE_TEXT)
    detect_sentiment(SAMPLE_TEXT, language_code)
    detect_entities(SAMPLE_TEXT, language_code)
    detect_key_phrases(SAMPLE_TEXT, language_code)


if __name__ == "__main__":
    main()
