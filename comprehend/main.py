import boto3
import boto_client
from loguru import logger

SAMPLE_TEXT = (
    "Hello Zhang Wei, I am John. Your AnyCompany Financial Services, LLC credit card account 1111-0000-1111-0008 has a minimum payment of $24.53 that is due by July 31st. Based on your autopay settings, we will withdraw your payment on the due date from your bank account number XXXXXX1111 with the routing number XXXXX0000."
    "Customer feedback for Sunshine Spa, 123 Main St, Anywhere. Send comments to Alice at sunspa@mail.com." 
    "I enjoyed visiting the spa. It was very comfortable but it was also very expensive. The amenities were ok but the service made the spa a great experience."
)

client = boto_client.get_boto_client("comprehend")

def detect_language(text: str) -> str:
    response = client.detect_dominant_language(Text=text)
    languages = response["Languages"]
    top = max(languages, key=lambda x: x["Score"])
    logger.debug(f"Dominant language: {top['LanguageCode']} (confidence: {top['Score']:.2%})")
    return top["LanguageCode"]


def detect_sentiment(text: str, language_code: str) -> None:
    response = client.detect_sentiment(Text=text, LanguageCode=language_code)
    sentiment = response["Sentiment"]
    scores = response["SentimentScore"]
    logger.debug(f"\nSentiment: {sentiment}")
    for label, score in scores.items():
        logger.debug(f"  {label}: {score:.2%}")


def detect_entities(text: str, language_code: str) -> None:
    response = client.detect_entities(Text=text, LanguageCode=language_code)
    logger.debug("\nEntities:")
    for entity in response["Entities"]:
        logger.debug(f"  [{entity['Type']}] {entity['Text']} (confidence: {entity['Score']:.2%})")


def detect_key_phrases(text: str, language_code: str) -> None:
    response = client.detect_key_phrases(Text=text, LanguageCode=language_code)
    logger.debug("\nKey phrases:")
    for phrase in response["KeyPhrases"]:
        logger.debug(f"  {phrase['Text']} (confidence: {phrase['Score']:.2%})")


def main() -> None:
    logger.debug("Text: {SAMPLE_TEXT}\n")
    language_code = detect_language(SAMPLE_TEXT)
    detect_sentiment(SAMPLE_TEXT, language_code)
    detect_entities(SAMPLE_TEXT, language_code)
    detect_key_phrases(SAMPLE_TEXT, language_code)


if __name__ == "__main__":
    main()
