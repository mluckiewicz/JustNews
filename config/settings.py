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
    'core.text.sanitizer.TrimHandler',
    'core.text.sanitizer.WhiteSpaceHandler',
    'core.text.sanitizer.MultipleSpaceHandler',
    'core.text.sanitizer.BoundsHandler',
    'core.text.sanitizer.BeforePunctuationHandler',
]


# EXTRACTORS
EXTRACTOR = 'core.extractors.Extractor'