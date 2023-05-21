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
TEXT_CLEANING_ORDER = [
    "core.text.text_cleaner.TrimTokens",
    "core.text.text_cleaner.RemoveWhiteSpaces",
    "core.text.text_cleaner.RemoveMultipleSpaces",
    "core.text.text_cleaner.TrimString",
    "core.text.text_cleaner.RemoveSpacesBeforePunctuation",
]


# EXTRACTORS
EXTRACTOR = "core.extractors.Extractor"


# TREE CLEANING ORDER
NODE_CONTENT_NORMALIZERS = [
    "core.cleaner.node_text_normalizer.NodeTextNormalizer",
    "core.cleaner.node_text_normalizer.NodeTailNormalizer",
    "core.cleaner.node_text_normalizer.NodeFlatteningNormalizer",
    "core.cleaner.node_text_normalizer.TextTailConnNormalizer",
]


# DOM CLEANERS
DOM_CLEANERS = [
    "core.cleaner.dom_cleaning_strategies.AttribiuteRemover",
    "core.cleaner.dom_cleaning_strategies.TagRemover",
    "core.cleaner.dom_cleaning_strategies.CommentsRemover",
    "core.cleaner.dom_cleaning_strategies.TextNormalizer",
    "core.cleaner.dom_cleaning_strategies.ByAttrValueRemover",
    "core.cleaner.dom_cleaning_strategies.NoTextRemover",
    "core.cleaner.dom_cleaning_strategies.NonArticleSubtreeRemover",
    "core.cleaner.dom_cleaning_strategies.NonSentenceRemover",
    "core.cleaner.dom_cleaning_strategies.SubtreeMergingStrategy",
    "core.cleaner.dom_cleaning_strategies.ReplaceTags",
    "core.cleaner.dom_cleaning_strategies.TransferUpTree",
]


# LIST OF WHITE TAGS VALUES FOR DocumentCLeaner
TAG_WHITELIST = ["body", "article"]


# LIST OF BLACK TAGS VALUES FOR DocumentCLeaner
TAG_BLACKLIST = [
    "script",
    "style",
    "aside",
    "noscript",
    "figure",
    "nav",
    "footer",
    "iframe",
    "picture",
    "img",
    "form",
    "button",
    "svg",
    "header",
    "svg",
    "label",
    "select",
    "amp-sidebar",
    "a",
    "title",
    "h1",
    "h2",
    "h3",
    "h4",
]


# LIST OF ATRRIB VALUES FOR DocumentCLeaner
# It contains attrib values for chack match with id and class values
ATTRIBIUTES_BLACKLIST = [
    "facebook",
    "tweet",
    "google",
    "social",
    "payu",
    "cookie",
    "comment",
    "OpenDiscussionBox",
    "Discussion",
    "question",
    "komentarz",
    "reklama",
    "ogloszenia",
    "announcements",
    "Promotions",
    "advertisement",
    "ads",
    "foot",
    "poster",
    "links",
    "footer-holder",
    "footer",
    "copyright",
    "author",
    "widget",
    "photo",
    "date",
    "^slider",
    "image120x90",
    "upgradebrowser",
    "msccBanner",
    "login",
    "menu",
    "aside",
    "popup",
    "am-article__description",
    "topbar",
    "RadioStream",
    "^share",
    "video_player",
    "bannergroup",
    "spotligh",
    "itemRelated",
    "Image",
    "blocker",
    "upprev_box",
    "claim",
    "author",
    "title",
    "plus18",
    "reglog",
]
