## Inuse Class

- TextCleaner
	- normalize
	- remove_stopwords
	- lemmatize
	- clean
	- clean_raw
	
- LinkCheckers
	- createTable
	- alreadyScrape
	- checkAccessibility
	- compareDomains
	- close
	
- DataPipelines
	- createTable
	- uncountRef
	- removeInvertedIndex
	- removeWebData
	- getUniqueID
	- fetch_data_by_url
	- updateReferenceDomain
	- updateWebData
	- updateInvertedIndexing
	- close
	
- get_raw_content
	- get_domain
	- crawl
	
- invertedIndexSearch
	- close
	- queryCleaner
	- getInvertedIndexDict
	- get_common_id
	- Link_from_ID
	- invertedIndexSearch
	- TFScore
	-IDFScore
	-TFIDFRank
	
- raw_database
	- get_row
	- delete_row
	- close
	
- main_database
	- get_domain
	- updateLink
	- removeData
	- word_frequency_dict
	
- rawKeeper
	- createTable
	- insertRaw
	- removeRaw
	- checkRaw
	- close
	
- pageScrapers
	- read_proxies_from_file
	- get_raw_html
	- scrape_raw_html
	- scrape_raw_text
	- scrape_all_urls
	- scrape_page
