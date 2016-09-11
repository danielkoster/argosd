SINGLE_MATCHING_ITEM = """
<rss version="2.0">
    <channel>
        <item>
            <title>testshow</title>
            <link>testlink</link>
        </item>
    </channel>
</rss>
"""

SINGLE_ITEM_CAPITALISATION = """
<rss version="2.0">
    <channel>
        <item>
            <title>TestShow</title>
            <link>testlink</link>
        </item>
    </channel>
</rss>
"""

SINGLE_ITEM_SPECIAL_CHARS = """
<rss version="2.0">
    <channel>
        <item>
            <title>Mr Robot</title>
            <link>testlink</link>
        </item>
    </channel>
</rss>
"""

MULTIPLE_MATCHING_ITEMS = """
<rss version="2.0">
    <channel>
        <item>
            <title>testshow S02E03 720p</title>
            <link>testlink</link>
        </item>
        <item>
            <title>testshow S2E3 1080i</title>
            <link>testlink</link>
        </item>
        <item>
            <title>testshow 02x03 480p</title>
            <link>testlink</link>
        </item>
    </channel>
</rss>
"""
