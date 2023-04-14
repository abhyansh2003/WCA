from urlextract import URLExtract

extractor = URLExtract()
urls = extractor.find_urls("lets www.gmail.com hello world www.youtube.com")
print(len(urls))
print(urls)