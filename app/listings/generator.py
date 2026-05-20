import re
from dataclasses import dataclass
from typing import Iterable, List
from app.listings.schemas import GeneratedListing, ListingGenerationRequest, ListingQualityCheck, MarketplaceFormat

BLOCKED_TERMS = {
    "guaranteed cure", "miracle cure", "fake", "replica", "counterfeit",
    "weapon", "gun", "explosive", "illegal", "prescription only",
}
SENSITIVE_CLAIMS = {"guaranteed", "cure", "medical", "best in the world", "official"}

@dataclass(frozen=True)
class MarketplaceRules:
    title_limit: int
    max_bullets: int
    max_tags: int

RULES = {
    MarketplaceFormat.SHOPIFY: MarketplaceRules(title_limit=120, max_bullets=6, max_tags=12),
    MarketplaceFormat.EBAY: MarketplaceRules(title_limit=80, max_bullets=5, max_tags=10),
    MarketplaceFormat.GENERIC: MarketplaceRules(title_limit=90, max_bullets=6, max_tags=10),
}

class AutoListingGenerator:
    def generate(self, request: ListingGenerationRequest) -> GeneratedListing:
        rules = RULES[request.marketplace]
        title_limit = min(request.max_title_length, rules.title_limit)
        title = self._build_title(request, title_limit)
        bullets = self._build_bullets(request.key_features, rules.max_bullets)
        description = self._build_description(request, bullets)
        keywords = self._build_keywords(request, bullets)
        tags = keywords[: rules.max_tags]
        quality = self._quality_check(title, description, bullets)
        return GeneratedListing(
            title=title,
            description=description,
            bullet_points=bullets,
            seo_keywords=keywords,
            tags=tags,
            marketplace=request.marketplace,
            quality=quality,
        )

    def _build_title(self, request: ListingGenerationRequest, limit: int) -> str:
        pieces = []
        if request.brand:
            pieces.append(self._clean_text(request.brand))
        pieces.append(self._clean_text(request.product_title))
        if request.category.lower() not in request.product_title.lower():
            pieces.append(self._clean_text(request.category))
        if request.target_market.upper() in {"UK", "US", "EU"}:
            pieces.append(request.target_market.upper())
        title = " | ".join(dict.fromkeys([p for p in pieces if p]))
        return self._truncate_words(title, limit)

    def _build_bullets(self, features: Iterable[str], max_bullets: int) -> List[str]:
        cleaned = []
        for feature in features:
            text = self._clean_text(feature)
            if not text:
                continue
            if len(text) > 120:
                text = self._truncate_words(text, 120)
            cleaned.append(text[0].upper() + text[1:])
        if not cleaned:
            cleaned = [
                "Practical everyday design",
                "Easy to use and suitable for regular use",
                "Checked for value, availability and delivery feasibility",
            ]
        return cleaned[:max_bullets]

    def _build_description(self, request: ListingGenerationRequest, bullets: List[str]) -> str:
        intro = f"This {self._clean_text(request.product_title)} is selected for customers in {self._clean_text(request.target_market)} who want a practical, reliable product in the {self._clean_text(request.category)} category."
        feature_text = " ".join(f"{b}." for b in bullets)
        supplier = self._clean_text(request.supplier_description or "")
        if supplier:
            supplier = self._truncate_words(supplier, 700)
            return f"{intro}\n\nKey benefits: {feature_text}\n\nAdditional details: {supplier}"
        return f"{intro}\n\nKey benefits: {feature_text}\n\nBefore dispatch, availability and delivery options should be checked through the connected supplier workflow."

    def _build_keywords(self, request: ListingGenerationRequest, bullets: List[str]) -> List[str]:
        source = " ".join([request.product_title, request.category, request.brand or "", *bullets])
        words = [w.lower() for w in re.findall(r"[a-zA-Z0-9]+", source)]
        stop = {"and", "the", "for", "with", "this", "that", "from", "your", "you", "use", "easy"}
        result = []
        for word in words:
            if len(word) < 3 or word in stop:
                continue
            if word not in result:
                result.append(word)
        return result[:20]

    def _quality_check(self, title: str, description: str, bullets: List[str]) -> ListingQualityCheck:
        content = f"{title} {description} {' '.join(bullets)}".lower()
        blocked = sorted(term for term in BLOCKED_TERMS if term in content)
        warnings = []
        if any(term in content for term in SENSITIVE_CLAIMS):
            warnings.append("Potentially risky marketing/compliance claim detected.")
        if len(title) < 20:
            warnings.append("Title may be too short for search visibility.")
        if len(description) < 120:
            warnings.append("Description may be too short for conversion.")
        return ListingQualityCheck(
            passed=not blocked,
            warnings=warnings,
            blocked_terms_found=blocked,
            title_length=len(title),
            description_length=len(description),
        )

    def _clean_text(self, value: str) -> str:
        value = re.sub(r"<[^>]+>", "", value or "")
        value = re.sub(r"\s+", " ", value).strip()
        return value

    def _truncate_words(self, text: str, limit: int) -> str:
        if len(text) <= limit:
            return text
        cut = text[: limit - 1].rstrip()
        if " " in cut:
            cut = cut.rsplit(" ", 1)[0]
        return cut.rstrip(" |,-")
