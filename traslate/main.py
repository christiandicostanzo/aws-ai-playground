import boto3
import boto_client
from loguru import logger

client = boto_client.get_boto_client("traslate")

SAMPLE_TEXTS = [
    ("Hello, how are you? I hope you are having a wonderful day.", "es"),
    ("The weather today is sunny with a light breeze.", "fr"),
    ("Artificial intelligence is transforming the world.", "de"),
    ("Please submit your report by the end of the week.", "ja"),
]

def translate_text(text: str, target_language: str, source_language: str = "auto") -> str:
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
    )
    detected = response.get("AppliedSettings", {})
    source = response["SourceLanguageCode"]
    translation = response["TranslatedText"]
    logger.debug(f"  [{source} -> {target_language}] {text!r}")
    logger.debug(f"  Translation: {translation!r}")
    return translation


def list_supported_languages() -> None:
    paginator = client.get_paginator("list_languages")
    languages = []
    for page in paginator.paginate():
        languages.extend(page["Languages"])
    logger.info(f"Supported languages: {len(languages)}")
    for lang in languages[:10]:
        logger.debug(f"  {lang['LanguageCode']:10s} {lang['LanguageName']}")
    if len(languages) > 10:
        logger.debug(f"  ... and {len(languages) - 10} more")


def main() -> None:
    logger.info("=== Supported Languages (sample) ===")
    list_supported_languages()

    logger.info("=== Text Translation ===")
    for text, target in SAMPLE_TEXTS:
        translate_text(text, target_language=target)
        logger.debug("")


if __name__ == "__main__":
    main()
