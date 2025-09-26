#%%
import urllib.request
url_path = "https://www.censtatd.gov.hk/api/get.php?id=310-30001&lang=tc&param=N4KABGBEDGBukC4yghSBxAIgBQPoGEB5AWW0IDkBRcgFUTAG0BdcMAXwBpXIBneJFKkhFy9Bq1RQAmgHspuAIwATAA64ApLh6QJYJl0mQAygEEFY3WgCKMq4tUatOySwiduKgKYAnAJYylekE0HgAXAENvUPpIBQBOAHYAZgAGc1Z3NF9ApEgkhRSAWlSUtMgDKAAbcIA7AHMY0OgdNiA"
with urllib.request.urlopen(url_path) as url:
	s = url.read().decode("utf8")
	print(s)
# %%
