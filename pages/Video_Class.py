import json
import datetime
from seleniumbase import BaseCase

class VideoTest(BaseCase):
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

    def close_facebook_popups(self):
        """Closes Facebook login pop-ups and cookie banners without closing post pop-ups."""
        try:
            # Check if the login modal is present
            text_present = self.assert_text("See more on Facebook", "div[role='dialog']")

            # Close login modal if present
            if text_present and self.is_element_visible("[aria-label='Close'][role='button']"):
                self.click("[aria-label='Close'][role='button']")
                self.sleep(1)

        except:
            # Ignore popups that were not closed
            pass
        
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
