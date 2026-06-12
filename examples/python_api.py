from apeiron import fetch_sync, search_sync


def main():
    result = fetch_sync("https://example.com", cache_ttl=0)
    print(result.verdict.value, result.tier.value)
    print(result.content[:300])

    for hit in search_sync("python web scraping", max_results=3):
        print(hit.source.value, hit.title, hit.url)


if __name__ == "__main__":
    main()
