from automations.FacebookScraper import FacebookScraper
from pages.FacebookScraperVideoUC import FacebookScraperVideoUC
from pages.FacebookScraperPostUC import FacebookScrapePostUC

if __name__ == "__main__":
    # FacebookScraper.test_facebook_scraper()

    # video_scraper = FacebookScraperVideoUC(False)
    # video_scraper.test_facebook_scraper()
    # video_scraper.quit()
    
    post_scraper = FacebookScrapePostUC(False)
    post_scraper.test_facebook_scraper()
    post_scraper.quit()

