from pages.FacebookScraperVideoUC import FacebookScraperVideoUC
from pages.FacebookScraperPostUC import FacebookScrapePostUC
import threading

def run_video_scraper():
        video_scraper = FacebookScraperVideoUC()
        video_scraper.test_facebook_scraper()
        video_scraper.quit()

def run_post_scraper():
    post_scraper = FacebookScrapePostUC()
    post_scraper.test_facebook_scraper()
    post_scraper.quit()

if __name__ == "__main__":

    video_thread = threading.Thread(target=run_video_scraper)
    post_thread = threading.Thread(target=run_post_scraper)

    video_thread.start()
    post_thread.start()

    video_thread.join()
    post_thread.join()

