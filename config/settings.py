"""
Global settings for application
"""

# Number of cores to work with

THREADS = 8


# BASE LANGUAGE

LANGUAGE = "pl"


# NETWORK SETTINGS

COOKIES_CONSENT = {"CONSENT": "YES+1"}


# PARSER SETTINGS

# Default
DEFAULT_PARSER = "core.parser.lxml_parser.LXMLParser"

# Available parsers
PARSAERS = {"lxml": "core.parser.lxml_parser.LXMLParser"}


# DOM CLEANER SETTINGS
# Base dom cleaner
CLEANER = "core.cleaner.dom_cleaner.DocumentCleaner"

# Dom cleaning strategies. Will be applied in order below
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

# Order of links from TextNormalizer class. Any node with text value will be pushed through those links in order to make node flat.
NODE_CONTENT_NORMALIZERS = [
    "core.cleaner.node_content_normalizer.NodeTextNormalizer",
    "core.cleaner.node_content_normalizer.NodeTailNormalizer",
    "core.cleaner.node_content_normalizer.NodeFlatteningNormalizer",
    "core.cleaner.node_content_normalizer.TextTailJoiner",
]

# List of tags that will never be deleted from dom
TAG_WHITELIST = ["body", "article"]

# List of tags taht will be deleted from dom
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

# List of atrrib values taht match will be check in id or class. If match is positive that node will be removed from dom
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


# STRING CLEANER SETTINGS

# List of chain links. Any text from content node will be pushed through before top node calculation. The goal is to remove any bad chars form nodes content.
TEXT_CLEANING_ORDER = [
    "core.text.text_cleaner.TrimTokens",
    "core.text.text_cleaner.RemoveWhiteSpaces",
    "core.text.text_cleaner.RemoveMultipleSpaces",
    "core.text.text_cleaner.TrimString",
    "core.text.text_cleaner.RemoveSpacesBeforePunctuation",
]


# EXTRACTION SETTINGS
# Extraction controler
EXTRACTOR = "core.extractors.Extractor"

# Concrete article parts extractor
EXTRACTORS = {
    "canonical_extractor": {
        "extractor": "core.extractors.canonical.CanonicalExtractor",
        "article_attr": "canonical",
        "patterns": [
            '//link[rel="canonical"]/@href',
            '//meta[@property="og:url"]/@content',
            '//meta[@http-equiv="Link" and contains(@content, "rel=canonical")]/@content',
            '//link[@itemprop="url"]/@href'
        ]
    },
    "title_extractor": {
        "extractor": "core.extractors.title.TitleExtractor",
        "article_attr": "title",
        "patterns": [
            '//title',
            '//meta[@property="og:url"]/@content',
        ]
    },
    "publishdate_extractor": {
        "extractor": "core.extractors.publishdate.PublishdateExtractor",
        "article_attr": "publish_date",
        "patterns": [
            '//meta[@property="rnews:datePublished"]/@content',
            '//meta[@property="article:published_time"]/@content',
            '//meta[@property="OriginalPublicationDate"]/@content',
            '//meta[@property="rnews:datePublished"]/@content',
            '//meta[@itemprop="datePublished"]/@content',
            '//meta[@property="article:published_time"]/@content',
        ]
    },
    "content_extractor": {
        "extractor": "core.extractors.content.ContentExtractor",
        "article_attr": "content",
        "string_len": 25,
        "stopwords_count": 2,
    }
}
