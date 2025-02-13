import json
import datetime
from seleniumbase import BaseCase

class FacebookScraper(BaseCase):
    def open_facebook_links(self, urls):
        """Opens Facebook post URLs, handles popups, and extracts comments."""
        for url in urls:
            self.open(url)
            self.driver.maximize_window()
            self.close_facebook_popups()
            self.sleep(2)  # Pause to allow page load
            self.change_visibility_to_all()
            self.extract_comments(url)  # Scrape comments

    def close_facebook_popups(self):
        """Closes Facebook login pop-ups and cookie banners without closing post pop-ups."""
        try:
            # Check if the login modal is present
            text_present = self.assert_text("See more on Facebook", "div[role='dialog']")

            # Close login modal if present
            if text_present and self.is_element_visible("[aria-label='Close'][role='button']"):
                self.click("[aria-label='Close'][role='button']")
                self.sleep(1)

        except Exception as e:
            # Ignore popups that were not closed
            print(f"No popups found or could not close them: {e}")

    def change_visibility_to_all(self):
        """Clicks the button to change comment visibility to 'All Comments' including potential spam."""
        try:
            # Click the button to expand comment options
            self.click('span:contains("Most relevant")')
            self.sleep(1)  # Allow dropdown to appear

            # Click 'All Comments' option
            self.click('div[role="menuitem"]:contains("Show all comments, including potential spam.")')
            self.sleep(3)  # Ensure the change is registered
        except Exception as e:
            print(f"Unable to change comment visibility: {e}")
            
    def expand_comments(self):
        """Clicks 'View more' to expand comments section until all comments are loaded"""
        view_more_button_visible = self.is_element_visible('span:contains("View more")')
        if view_more_button_visible:
            self.click('span:contains("View more")')
            self.sleep(1)
            self.execute_script("window.scrollTo(0, 0);")  # Scroll to top after expanding
            comments_div = self.find_element("div.x78zum5.xdt5ytf.x6ikm8r.x1odjw0f.x1iyjqo2.x1pi30zi.x1swvt13")
            self.execute_script("arguments[0].scrollIntoView(true);", comments_div)

        # If the view more button is not visible, scroll through the div to load all comments
        comments_div = self.find_element("div.x78zum5.xdt5ytf.x6ikm8r.x1odjw0f.x1iyjqo2.x1pi30zi.x1swvt13")
        for _ in range(20):
            self.execute_script("arguments[0].scrollBy(0, arguments[0].scrollHeight);", comments_div)
            self.sleep(0.5)  # Allow time for new comments to load
            
            
            
            
    def get_comment_count(self):
        """Returns the number of comments on a post."""
        self.scroll_post()
        try:
            comment_count_text = self.get_text("span:contains(' comment')")
            if 'comments' in comment_count_text:
                comment_count = int(comment_count_text.split()[0])
            elif 'comment' in comment_count_text:
                comment_count = 1
            else:
                comment_count = 0
        except Exception as e:
            print(f"Failed to find comment count: {e}")
            comment_count = 0
        return comment_count
    
    def scroll_post(self):
        """Scrolls the post if the 'View more' span is not visible."""
        view_more_button_visible = self.is_element_visible('span:contains("View more")')
        if not view_more_button_visible:
            post_div = self.find_element("div.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x78zum5.xdt5ytf.x1iyjqo2.x1n2onr6.xqbnct6.xga75y6")
            self.execute_script("arguments[0].scrollIntoView(true);", post_div)
            self.sleep(1)
           

    def extract_comments(self, post_url):
        """Extracts comments from a Facebook post and saves them in JSON format."""
        comments_data = []
        comment_count = self.get_comment_count()
        
        # Ensure post is visible
        if not self.is_element_visible("div[role='article']"):
            self.close_facebook_popups()  # Try closing popups again
            self.sleep(2)
        
        # Expand comments section until all comments are loaded
        self.expand_comments()
        
        # Locate all comments
        comment_elements = self.find_elements("div[aria-label='Comment']")
        
        # Check if the comment count matches the comments found
        if len(comment_elements) != comment_count:
            print(f"Mismatched comments on {post_url}, expected {comment_count} but got {len(comment_elements)}")
        
        for comment in comment_elements:
            try:
                name = comment.find_element("xpath", ".//strong").text
                comment_text = comment.find_element("xpath", ".//span").text
                time_ago = comment.find_element("xpath", ".//abbr").text  # Example: "5m", "2h", "1d"
                comment_url = comment.find_element("xpath", ".//a").get_attribute("href")

                comments_data.append({
                    "date": datetime.date.today().isoformat(),
                    "name": name,
                    "company": "",  # Leave empty for now
                    "comment": comment_text,
                    "how_long": time_ago,
                    "url": comment_url
                })

            except Exception as e:
                print(f"Error extracting comment data: {e}")

        # Save to JSON
        with open("facebook_comments.json", "w", encoding="utf-8") as file:
            json.dump(comments_data, file, ensure_ascii=False, indent=4)

    def test_facebook_scraper(self):
        urls = [
            "https://www.facebook.com/share/v/14RQthf5Kd/",
            "https://www.facebook.com/share/19xUdMf1Yf/",
            # "https://www.facebook.com/instaautosolutions/posts/1120214880111966?ref=embed_post",
            # "https://www.facebook.com/WinnipegVehicleFinancingAndLeasing/posts/968053645425631?ref=embed_post",
            # "https://www.facebook.com/bcautoclearance/posts/1221549349249014?ref=embed_post",
            # "https://www.facebook.com/firstnationfinance/posts/1018157893662171?ref=embed_post",
            # "https://www.facebook.com/permalink.php?story_fbid=948401194065860&id=100066879633019&ref=embed_post",
            # "https://www.facebook.com/NSMitsubishi/posts/608094538232595?ref=embed_post",
            # "https://www.facebook.com/firstnationapproved/posts/1044698081007682?ref=embed_post",
            # "https://www.facebook.com/Prioautosales/posts/1085711573560900?ref=embed_post",
            # "https://www.facebook.com/SignNDrive.ca/posts/1015320693945787?ref=embed_post",
            # "https://www.facebook.com/CarDealsDirectON/videos/601877359424067/",
            # "https://www.facebook.com/permalink.php?story_fbid=527400586682356&id=100082372579993&ref=embed_post",
            # "https://www.facebook.com/101773595710752/videos/604121224191590/",
            # "https://www.facebook.com/philcanfinance/posts/922317296671022?ref=embed_post",
            # "https://www.facebook.com/permalink.php?story_fbid=807577688148212&id=100066879633019&ref=embed_post",
            # "https://www.facebook.com/Firstnationapprovalcentre/videos/1249814416258609/",
            # "https://www.facebook.com/firstnationfinance/posts/1091184348270247?ref=embed_post",
            # "https://www.facebook.com/firstnationsdrives/posts/1061874632610314?ref=embed_post",
            # "https://www.facebook.com/permalink.php?story_fbid=939444421628204&id=100066879633019&ref=embed_post",
            # "https://www.facebook.com/permalink.php?story_fbid=122114434532648288&id=61569448665354&ref=embed_post",
            # "https://www.facebook.com/JourneyApproved.ca/posts/397520390028434?ref=embed_post",
            # "https://www.facebook.com/share/1Da1XNbdQP/",
            # "https://www.facebook.com/share/v/16CaV7CiPq/",
            # "https://www.facebook.com/share/19pQJtf7kp/"
            # Add more URLs as needed
        ]
        self.open_facebook_links(urls)
