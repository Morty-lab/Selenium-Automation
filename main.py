from automations.FacebookScraper import FacebookScraper
from automations.FacebookScraperVideoUC import FacebookScraperVideoUC
from automations.FacebookScraperPostUC import FacebookScrapePostUC

if __name__ == "__main__":
    # FacebookScraper.test_facebook_scraper()

    # video_scraper = FacebookScraperVideoUC()
    # video_scraper.test_facebook_scraper()
    # video_scraper.quit()
    
    post_scraper = FacebookScrapePostUC()
    post_scraper.test_facebook_scraper()
    post_scraper.quit()

