from automations.FacebookScraper import FacebookScraper
from automations.FacebookScraperUC import FacebookScraperUC

if __name__ == "__main__":
    # FacebookScraper.test_facebook_scraper()

    scraper = FacebookScraperUC()
    scraper.test_facebook_scraper()
    scraper.quit()
