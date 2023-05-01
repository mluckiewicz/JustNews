from __future__ import annotations
from typing import List
import random
import re
import urllib.parse


def url_validator(url: str) -> bool:
    """The function checks the validity of the URL by validating the URL scheme, 
    netlock, and port. It also ensures that the URL length is within the allowed limit 
    and that the URL address has been specified.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.

    Raises:
        Exception: If the URL address has not been specified or the URL length is 
            greater than 2048 characters.
        Exception: If the URL scheme is not specified or is not http(s)/ftp(s).
        Exception: If the URL netlock is not specified or is malformed.


    """
    netlock_format = re.compile(
    # http basic authentication [optional]
    r"(?:^(\w{1,255}):(.{1,255})@|^)"
    # check full domain length to be less than or equal to 253 (starting after http basic auth, stopping before port)
    r"(?:(?:(?=\S{0,253}(?:$|:))"
    # check for at least one subdomain (maximum length per subdomain: 63 characters), dashes in between allowed
    r"((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+"
    # check for top level domain, no dashes allowed
    r"(?:[a-z0-9]{1,63})))"
    r"|localhost)"  # accept also "localhost" only
    r"(:\d{1,5})?",  # port [optional]
    re.IGNORECASE)

    scheme_format = re.compile(
    r"^(http|hxxp|ftp|fxp)s?$",  # scheme: http(s) or ftp(s)
    re.IGNORECASE)

    
    url = url.strip()
    if not url:
        raise Exception("URL address has not been specified!")

    if len(url) > 2048:
        raise Exception(
            f"URL lenght is > 2048 chars! Given lenght: {len(url)}")

    result = urllib.parse.urlparse(url)
    # minimum parts required => scheme and netlock
    scheme = result.scheme
    netlock = result.netloc

    if not scheme:
        raise Exception("No URL scheme specified")

    if not re.fullmatch(scheme_format, scheme):
        raise Exception(
            f"URL scheme must be http(s)/ftp(s). Given scheme: {scheme})")

    if not netlock:
        raise Exception("No URL netlock specified")

    if not re.fullmatch(netlock_format, netlock):
        raise Exception(f"URL netlock malformed. Given netlock: {netlock})")

    return True


def get_random_useragent(k: int = 1) -> List[str]:
    """Return a randomly selected user-agent string from a pre-defined list.
    
    Args:
        k (int): Number of user-agent strings to return. Defaults to 1.

    Returns:
        list: A list of k user-agent strings randomly selected from a pre-defined list.
    """
    
    ua_pct = {
        "ua": {
            "0": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "1": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "2": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41",
            "3": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
            "4": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "5": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78",
            "6": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
            "7": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "8": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0",
            "9": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "10": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0",
            "11": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "12": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76",
            "13": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
            "14": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0",
            "15": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67",
            "16": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
            "17": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.55",
            "18": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.0",
            "19": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0",
            "20": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.46",
            "21": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54",
            "22": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
            "23": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
            "24": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61",
            "25": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
            "26": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0",
            "27": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "28": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36",
            "29": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "30": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
            "31": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52",
            "32": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "33": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
            "34": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36",
            "35": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            "36": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
            "37": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.50",
            "38": "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
            "39": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "40": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42",
            "41": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70",
            "42": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362",
            "43": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36",
        },
        "pct": {
            "0": 23.1611454239,
            "1": 18.1078046042,
            "2": 14.4862436833,
            "3": 11.6788321168,
            "4": 7.1869736103,
            "5": 2.9197080292,
            "6": 2.6951151039,
            "7": 1.7967434026,
            "8": 1.7967434026,
            "9": 1.7967434026,
            "10": 1.2352610893,
            "11": 1.010668164,
            "12": 0.7860752386,
            "13": 0.7860752386,
            "14": 0.673778776,
            "15": 0.673778776,
            "16": 0.673778776,
            "17": 0.673778776,
            "18": 0.5614823133,
            "19": 0.4491858506,
            "20": 0.4491858506,
            "21": 0.4491858506,
            "22": 0.4491858506,
            "23": 0.336889388,
            "24": 0.336889388,
            "25": 0.336889388,
            "26": 0.336889388,
            "27": 0.336889388,
            "28": 0.336889388,
            "29": 0.336889388,
            "30": 0.2245929253,
            "31": 0.2245929253,
            "32": 0.2245929253,
            "33": 0.2245929253,
            "34": 0.2245929253,
            "35": 0.2245929253,
            "36": 0.2245929253,
            "37": 0.2245929253,
            "38": 0.2245929253,
            "39": 0.2245929253,
            "40": 0.2245929253,
            "41": 0.2245929253,
            "42": 0.2245929253,
            "43": 0.2245929253,
        },
    }

    return random.choices(
        list(ua_pct["ua"].values()), list(ua_pct["pct"].values()), k=k
    )