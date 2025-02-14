import json
from seleniumbase import BaseCase


class FacebookScraper(BaseCase):
    def test_facebook_scraper(self):
        video_urls = self.get_urls_from_json("video.json")
        post_urls = self.get_urls_from_json("post.json")

        # self.open_facebook_links_in_parallel(video_urls, post_urls)
        self.open_facebook_video_links(video_urls)

    def get_urls_from_json(self, filename):
        with open(filename) as file:
            data = json.load(file)
            return data["urls"]

    # def open_facebook_links_in_parallel(self, video_urls, post_urls):
    #     from concurrent.futures import ThreadPoolExecutor

    #     with ThreadPoolExecutor() as executor:
    #         executor.map(self.open_facebook_links, [video_urls, post_urls])

    def open_facebook_video_links(self, urls):
        for url in urls:
            self.open(url)
            self.close_facebook_popups()
            self.sleep(1)
            self.change_visibility_to_all()
            self.sleep(2)
            self.expand_comments()
            self.sleep(2)
        
    def close_facebook_popups(self):
        try:
            text_present = self.assert_text("See more on Facebook", "div[role='dialog']")

            if text_present and self.is_element_visible("[aria-label='Close'][role='button']"):
                self.click("[aria-label='Close'][role='button']")
                self.sleep(1)

        except:
            pass
        
    def change_visibility_to_all(self):
        try:
            self.click('span:contains("Most relevant")')
            self.sleep(1)
            self.click('div[role="menuitem"]:contains("Show all comments, including potential spam.")')
            self.sleep(3)
        except Exception as e:
            print(f"Unable to change comment visibility: {e}")
            
    def expand_comments(self):
        view_more_button_visible = self.is_element_visible('span:contains("View more")')
        if view_more_button_visible:
            self.click('span:contains("View more")')
            self.sleep(1)
            self.execute_script("window.scrollTo(0, 0);")
            comments_div = self.find_element("div.x78zum5.xdt5ytf.x6ikm8r.x1odjw0f.x1iyjqo2.x1pi30zi.x1swvt13")
            self.execute_script("arguments[0].scrollIntoView(true);", comments_div)

        comments_div = self.find_element("div.x78zum5.xdt5ytf.x6ikm8r.x1odjw0f.x1iyjqo2.x1pi30zi.x1swvt13")
        for _ in range(20):
            self.execute_script("arguments[0].scrollBy(0, arguments[0].scrollHeight);", comments_div)
            self.sleep(0.5)


