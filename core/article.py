import json


class Article:
    """Klasa odpowiada za przechowywanie oczyszczonych danych"""

    def __init__(self):
        self.base_url = None
        self.title = None
        self.description = None
        self.lead = None
        self.key_words = None
        self.canonical = None
        self.content = None
        self.publish_date = None

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def lead(self):
        return self._lead

    @lead.setter
    def lead(self, value):
        self._lead = value

    @property
    def key_words(self):
        return self._key_words

    @key_words.setter
    def key_words(self, value):
        self._key_words = value

    @property
    def canonical(self):
        return self._canonical

    @canonical.setter
    def canonical(self, value):
        self._canonical = value

    @property
    def publish_date(self):
        return self._publish_date

    @publish_date.setter
    def publish_date(self, value):
        self._publish_date = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    def as_dict(self):
        return vars(self)

    def as_json(self):
        return json.dumps(
            self,
            default=lambda o: vars(o),
            indent=4,
            ensure_ascii=False)
