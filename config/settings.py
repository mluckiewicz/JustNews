"""
Global settings for application
"""

# Number of cores to work with
THREADS = 8

# BASE LANGUAGE
LANGUAGE = "PL"


# NETWORK
COOKIES_CONSENT = {"CONSENT": "YES+1"}


# STRING CLEANER SETTINGS
STRING_SANITIZER = 'core.text.sanitizer.StringSanitizer'
SANITIZATION_ORDER = [
    'core.text.text_cleaner.TrimTokens',
    'core.text.text_cleaner.RemoveWhiteSpaces',
    'core.text.text_cleaner.RemoveMultipleSpaces',
    'core.text.text_cleaner.TrimString',
    'core.text.text_cleaner.RemoveSpacesBeforePunctuation',
]


# EXTRACTORS
EXTRACTOR = 'core.extractors.Extractor'


# TREE CLEANING ORDER
CLEANING_CHAIN = [
    'core.cleaner.node_text_normalizer.NodeTextNormalizer',
    'core.cleaner.node_text_normalizer.NodeTailNormalizer',
    'core.cleaner.node_text_normalizer.NodeFlatteningNormalizer',
    'core.cleaner.node_text_normalizer.TextTailConnNormalizer',
]
