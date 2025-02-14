import json
from seleniumbase import BaseCase
from datetime import date
import re



class FacebookScraper(BaseCase):
    def test_facebook_scraper(self):
        self.maximize_window()
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
            company = self.get_text("div.xu06os2.x1ok221b")
            self.close_facebook_popups()
            self.sleep(1)
            self.change_visibility_to_all()
            self.sleep(2)
            self.expand_comments()
            self.get_comments(company)
            self.sleep(2)

    def close_facebook_popups(self):
        try:
            text_present = self.assert_text("See more on Facebook", "div[role='dialog']")

            if text_present and self.is_element_visible("[aria-label='Close'][role='button']"):
                self.execute_script("arguments[0].scrollIntoView(false);", self.find_element("[aria-label='Close'][role='button']"))
                self.click("[aria-label='Close'][role='button']")
                self.sleep(1)

        except:
            pass
        
    def change_visibility_to_all(self):
        try:
            self.execute_script("arguments[0].scrollIntoView(false);", self.find_element('span:contains("Most relevant")'))
            self.click('span:contains("Most relevant")')
            self.sleep(1)
            self.execute_script("arguments[0].scrollIntoView(false);", self.find_element('div[role="menuitem"]:contains("Show all comments, including potential spam.")'))
            self.click('div[role="menuitem"]:contains("Show all comments, including potential spam.")')
        except Exception as e:
            print(f"Unable to change comment visibility: {e}")
            
    def expand_comments(self):
        while self.is_element_visible('span:contains("View more")'):
            self.execute_script("arguments[0].scrollIntoView(false);", self.find_element('span:contains("View more")'))
            self.click('span:contains("View more")')
            self.sleep(1)
        else:
            print("No more 'View more' buttons are visible.")

    def get_comments(self, company):
        comments = []
        pattern = re.compile(r"(\d+(d|w))")
        while True:
            comments_div = self.find_elements("div.x1n2onr6.x1ye3gou.x1iorvi4.x78zum5.x1q0g3np.x1a2a7pz")
            new_comments = []
            for comment_div in comments_div:
                comment_text = comment_div.get_attribute("innerText")
                name, *comment_parts = comment_text.split("\n")
                today_date = date.today().strftime("%Y-%m-%d")
                match = pattern.search(comment_parts[-1])
                if match:
                    how_long = match.group(0)
                    comment = "\n".join(comment_parts[:-1])  # Everything except the 'how_long' part
                else:
                    how_long = ""
                    comment = "\n".join(comment_parts)  # All parts are part of the comment if no 'how_long'
                url = ""
                a_tags = comment_div.find_elements("tag name", "a")
                url = a_tags[0].get_attribute("href") if a_tags else ""

                new_comment = {
                    "date": today_date,
                    "name": name,
                    "company": company,
                    "comment": comment,
                    "how_long": how_long,
                    "url": url
                }
                new_comments.append(json.dumps(new_comment))

            if not new_comments or set(new_comments).issubset(set(comments)):
                break
            comments.extend(new_comments)
            self.sleep(0.5)

        with open('comments_videos.json', 'w') as file:
            for comment in comments:
                file.write(comment + "\n")

