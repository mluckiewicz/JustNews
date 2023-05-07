"""
Global settings for application
"""

# Number of cores to work with
MAX_CONCURRENCY = 8

# BASE LANGUAGE
LANGUAGE = "PL"


# NETWORK
COOKIES_CONSENT = {"CONSENT": "YES+1"}


# STRING CLEANER SETTINGS
STRING_CLEANER = 'text.StringCleaner'
STRING_CLEANING_ORDER = [
    'text.TrimHandler',
    'text.WhiteSpaceHandler',
    'text.MultipleSpaceHandler',
    'text.BoundsHandler',
    'text.BeforePunctuationHandler',
]


# EXTRACTORS
EXTRACTORS = [
    'core.extractors.Extractor'
]