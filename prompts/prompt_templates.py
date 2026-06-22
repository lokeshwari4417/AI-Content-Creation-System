# ============================================================
# prompts/prompt_templates.py - Prompt Engineering Module
#
# This module dynamically builds structured prompts for each
# content type using the user's inputs.
# ============================================================


# ── Length Word Count Mapping ────────────────────────────────
LENGTH_MAP = {
    'short':  {'words': '150–250',  'description': 'concise and punchy'},
    'medium': {'words': '400–600',  'description': 'well-developed with clear sections'},
    'long':   {'words': '800–1200', 'description': 'comprehensive and detailed'},
}

# ── Tone Style Descriptions ──────────────────────────────────
TONE_MAP = {
    'professional':  'authoritative, formal, and data-driven',
    'friendly':      'warm, conversational, and approachable',
    'casual':        'relaxed, fun, and informal',
    'marketing':     'persuasive, energetic, and action-oriented',
    'educational':   'clear, instructive, and easy to understand',
}


def build_prompt(content_type: str, topic: str, audience: str, tone: str, length: str) -> str:
    """
    Master dispatcher — selects the correct template based on content_type
    and returns a fully constructed prompt string.

    Args:
        content_type: One of Blog Post, Social Media Post, Marketing Email,
                      Product Description, Advertisement
        topic:        The subject the user wants content about
        audience:     The intended reader (e.g., "college students")
        tone:         Writing tone key (professional / friendly / casual /
                      marketing / educational)
        length:       Requested length key (short / medium / long)

    Returns:
        A detailed prompt string ready to send to the OpenAI API.
    """

    # Normalise inputs
    content_type = content_type.strip()
    tone_key     = tone.lower().strip()
    length_key   = length.lower().strip()

    tone_desc   = TONE_MAP.get(tone_key,   tone)
    length_info = LENGTH_MAP.get(length_key, {'words': '300–500', 'description': 'well-developed'})

    # Route to the matching template
    template_map = {
        'Blog Post':          _blog_post_prompt,
        'Social Media Post':  _social_media_prompt,
        'Marketing Email':    _marketing_email_prompt,
        'Product Description': _product_description_prompt,
        'Advertisement':      _advertisement_prompt,
    }

    builder = template_map.get(content_type, _generic_prompt)
    return builder(topic, audience, tone_desc, length_info)


# ── Individual Template Builders ─────────────────────────────

def _blog_post_prompt(topic, audience, tone_desc, length_info):
    return f"""You are an expert content writer and SEO specialist.

Write a {length_info['description']} blog post about "{topic}" targeted at {audience}.

Requirements:
- Tone: {tone_desc}
- Length: approximately {length_info['words']} words
- Structure: Include an engaging title (H1), 2–4 subheadings (H2), and a concluding paragraph with a call to action
- Begin with a hook that immediately captures the reader's attention
- Use real-world examples or analogies relevant to {audience}
- End with a thought-provoking question or actionable takeaway
- Do NOT include markdown code fences; use plain headings like "## Section Title"

Deliver the complete blog post now."""


def _social_media_prompt(topic, audience, tone_desc, length_info):
    return f"""You are a social media strategist with expertise in viral content.

Create a compelling social media post about "{topic}" for {audience}.

Requirements:
- Tone: {tone_desc}
- Length: {length_info['words']} words (keep it scannable)
- Include a strong opening line that stops the scroll
- Add 5–8 relevant and trending hashtags at the end
- Include one clear call-to-action (like, share, comment, or visit link)
- Use line breaks to make the post easy to read on mobile
- Optionally add 1–2 relevant emojis (don't overdo it)
- Suitable for LinkedIn, Instagram, or Twitter/X

Write the complete social media post now."""


def _marketing_email_prompt(topic, audience, tone_desc, length_info):
    return f"""You are a conversion-focused email marketing copywriter.

Write a {length_info['description']} marketing email about "{topic}" for {audience}.

Requirements:
- Tone: {tone_desc}
- Length: approximately {length_info['words']} words
- Structure:
    Subject Line: (compelling, under 60 characters)
    Preview Text: (under 90 characters)
    Greeting: personalised opener
    Body: value proposition + key benefits (use short paragraphs or bullet points)
    CTA: one strong, button-ready call-to-action phrase
    Sign-off: professional closing
- Highlight a clear benefit in the first two sentences
- Create urgency without being spammy

Write the complete marketing email now."""


def _product_description_prompt(topic, audience, tone_desc, length_info):
    return f"""You are a product copywriter skilled at turning features into benefits.

Write a {length_info['description']} product description for "{topic}" aimed at {audience}.

Requirements:
- Tone: {tone_desc}
- Length: approximately {length_info['words']} words
- Structure:
    Product Name / Headline
    One-sentence value proposition
    Key features (presented as customer benefits, not just specs)
    Who it's perfect for
    Closing persuasion line
- Focus on how the product solves a problem or improves the buyer's life
- Use sensory and emotional language where appropriate
- Avoid jargon; speak the language of {audience}

Write the complete product description now."""


def _advertisement_prompt(topic, audience, tone_desc, length_info):
    return f"""You are an award-winning advertising copywriter.

Write a {length_info['description']} advertisement copy for "{topic}" targeting {audience}.

Requirements:
- Tone: {tone_desc}
- Length: approximately {length_info['words']} words
- Structure:
    Headline: (attention-grabbing, under 10 words)
    Sub-headline: (support the headline, under 20 words)
    Body Copy: (develop the core message with 2–3 punchy paragraphs)
    Call to Action: (clear, urgent, one sentence)
    Tagline: (memorable, brand-aligned, under 8 words)
- Use the AIDA framework (Attention → Interest → Desire → Action)
- Make every word earn its place

Write the complete advertisement copy now."""


def _generic_prompt(topic, audience, tone_desc, length_info):
    """Fallback template for any unrecognised content type."""
    return f"""You are a versatile professional content writer.

Write {length_info['description']} content about "{topic}" for {audience}.

Requirements:
- Tone: {tone_desc}
- Length: approximately {length_info['words']} words
- Structure: Clear introduction, well-organised body, strong conclusion
- Be specific, accurate, and engaging throughout

Write the complete content now."""
