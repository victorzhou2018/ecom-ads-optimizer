# Copyright 2026 Your Name. All rights reserved.
# This is a simplified example for Google Ads API Developer Token application.

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

def generate_keyword_ideas(
    client: GoogleAdsClient,
    customer_id: str,
    page_url: str = None,
    seed_keywords: list = None,
):
    """
    Generates keyword ideas using the Google Ads Keyword Planner API.
    
    Args:
        client: An authenticated GoogleAdsClient instance.
        customer_id: The authorized Google Ads account ID (e.g., '1234567890').
        page_url: Optional. A landing page URL provided by the user (e.g., 'https://example.com/product-x').
        seed_keywords: Optional. A list of seed keywords provided by the user (e.g., ['wireless earbuds', 'bluetooth headphones']).
    
    Returns:
        A list of keyword idea dictionaries containing text, average monthly searches, and competition level.
    """
    keyword_plan_service = client.get_service("KeywordPlanIdeaService")
    request = client.get_type("GenerateKeywordIdeasRequest")
    request.customer_id = customer_id

    # Set language (e.g., English)
    language_enum = client.get_type("LanguageEnum").Language.EN
    request.language = f"languageConstants/{language_enum}"

    # Set geographic target (e.g., United States)
    geo_target_constant_service = client.get_service("GeoTargetConstantService")
    us_geo_target = geo_target_constant_service.geo_target_constant_path(2048)  # Country code for US
    request.geo_target_constants.append(us_geo_target)

    # Choose input method based on user-provided data
    if page_url:
        request.page_url = page_url
        request.keyword_annotation = [
            client.get_type("KeywordAnnotationEnum").KeywordAnnotation.SEARCH_VOLUME
        ]
    elif seed_keywords:
        request.keyword_seed.keywords.extend(seed_keywords)
    else:
        raise ValueError("Either page_url or seed_keywords must be provided.")

    try:
        response = keyword_plan_service.generate_keyword_ideas(request=request)
        results = []
        for idea in response:
            results.append({
                "text": idea.text,
                "avg_monthly_searches": idea.keyword_idea_metrics.avg_monthly_searches,
                "competition": idea.keyword_idea_metrics.competition.name,
            })
        return results
    except GoogleAdsException as ex:
        print(f"Request failed with status {ex.error.code().name}")
        print(f"Errors: {ex.failure.errors}")
        raise