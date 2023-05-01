"""
Global settings for application
"""

# Number of cores to work with
MAX_CONCURRENCY = 8


LANGUAGE = "PL"


# STRING CLEANER SETTINGS
STRING_CLEANER = 'text.StringCleaner'
STRING_CLEANING_ORDER = [
    'text.TrimHandler',
    'text.WhiteSpaceHandler',
    'text.MultipleSpaceHandler',
    'text.BoundsHandler',
    'text.BeforePunctuationHandler',
]
