import time

import huspacy

from keywordExtractor import KeywordExtractor
from reviewCollector import ReviewCollector
from reviewsDatabase import ReviewsDatabase

# url = 'https://www.bonprix.hu/style/ruha-lepeshasitekkal-2-db-os-csomag-1871916561/'
# url = 'https://www.bonprix.hu/style/hosszu-boxy-polo-319618735/'
# url = 'https://www.bonprix.hu/style/polo-3-db-os-csomag-843857/'
# db = ReviewCollector.collect_from_bonprix(url)
# db.write_to_csv('resources/bonprix/843857.csv')
# db.refresh_csv("reviews_bp.csv")

# url = 'https://www.emag.hu/ihunt-s21-plus-2021-mobiltelefon-kartyafuggetlen-6-3-kepernyo-ips-2gb-ram-16gb-rom-dualsim-android-10-go-4000mah-kamera-13mp-kek-00001597/pd/D5T9VDMBM/ '
# url = 'https://www.emag.hu/ilike-x5-lite-mobiltelefon-kartyafuggetlen-dual-sim-8gb-arany-ilike-x5-lite-gold/pd/DVYRX0BBM/?ref=most_wished_product_4_1&provider=rec&recid=rec_41_dc27f56f37a0052e9205540acf5c4881b2e39b20243b0c94a1a3ce89895739be_1650549104&scenario_ID=41'

# url = 'https://www.emag.hu/xiaomi-redmi-note-10s-mobiltelefon-kartyafuggetlen-dual-sim-128gb-6gb-ram-4g-onyx-gray-redmi-note-10s-6-128-gray/pd/DJSYZ0MBM/?ref=most_wished_product_4_3&provider=rec&recid=rec_41_3b15e95994fc462190b336dd8213d596472d9e5bbce515a9e1c4bc2931231f22_1650556568&scenario_ID=41'
#url = 'https://www.emag.hu/xiaomi-redmi-9a-mobiltelefon-dual-sim-kartyafuggetlen-32gb-4g-karbonszurke-redmi-9a-32-2-gray/pd/DKD6P3MBM/?ref=profiled_categories_home_3_2&provider=rec&recid=rec_50_89040b52ea5d469a4e4a0a74a16030f063b5f000a4b6a74c5835fad2004d3f2f_1653142309&scenario_ID=50'
# db = ReviewCollector.collect_from_emag(url)

# db.write_to_csv("resources/emag/redmi9a.csv")


#db = ReviewsDatabase.from_csv("resources/emag/redmi9a.csv")
# print(KeywordExtractor.extract_keywords_hubert(db))
# print(KeywordExtractor.extract_keywords_textrank(db))

# url = "https://www.emag.hu/samsung-smart-led-televizio-138-cm-4k-ultra-hd-ue55tu7022kxxh/pd/DM6K02MBM/"
#url = "https://www.emag.hu/samsung-galaxy-a12-exynos-850-mobiltelefon-kartyafuggetlen-dual-sim-32gb-fekete-sm-a127fzkueue/pd/D6SWMPMBM/?"
#db = ReviewCollector.collect_from_emag(url)
#db.write_to_csv("resources/emag/galaxya12.csv")
db = ReviewsDatabase.from_csv("resources/bonprix/843857.csv")
start_time = time.time()
print("hubert: ", KeywordExtractor.extract_keywords_hubert(db, ngram=3, top_n=3, diversified=False))
# KeywordExtractor.extract_keywords_textrank_spacy(db)
# print("textrank: ", KeywordExtractor.extract_keywords_summa_textrank(db, top_n=3))
print(round(time.time() - start_time, 2))
# huspacy.download()
