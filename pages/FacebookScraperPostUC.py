import json
import time
import re
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date


class FacebookScrapePostUC:
    def __init__(self, Head = True):
        self.driver = uc.Chrome(headless= Head)  # Set to True if you want it headless
        self.wait = WebDriverWait(self.driver, 10)

    def test_facebook_scraper(self):
        try:
            self.driver.maximize_window()
            post_urls = self.get_urls_from_json("post.json")
            self.open_facebook_post_links(post_urls)
        finally:
            self.quit()

    def get_urls_from_json(self, filename):
        with open(filename) as file:
            data = json.load(file)
            return data["urls"]

    def open_facebook_post_links(self, urls):
        for url in urls:
            self.driver.get(url)
            try:
                company = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.xu06os2.x1ok221b"))).text
            except:
                company = "Unknown"
            
            # self.close_facebook_popups()
            # time.sleep(1)
            self.change_visibility_to_all()
            time.sleep(2)
            self.expand_comments()
            self.get_comments(company)
            time.sleep(2)

    def close_facebook_popups(self):
        try:
            popup = self.driver.find_element(By.CSS_SELECTOR, "div[role='dialog']")
            close_button = popup.find_element(By.CSS_SELECTOR, "[aria-label='Close'][role='button']")
            self.driver.execute_script("arguments[0].scrollIntoView(false);", close_button)
            close_button.click()
            time.sleep(1)
        except:
            pass

    def change_visibility_to_all(self):
        try:
            most_relevant = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Most relevant')]")))
            self.driver.execute_script("arguments[0].scrollIntoView(false);", most_relevant)
            most_relevant.click()
            time.sleep(1)
            
            show_all_comments = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'All comments')] | //div[@role='menuitem' and contains(text(),'Show all comments including potential spam')]")))
            self.driver.execute_script("arguments[0].scrollIntoView(false);", show_all_comments)
            show_all_comments.click()
            print("Comment visibility changed to 'All Comments'")
        except Exception as e:
            print(f"Unable to change comment visibility: {e}")

    def expand_comments(self):
        reply_divs = self.driver.find_elements(By.CSS_SELECTOR, "div.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x78zum5.x1iyjqo2.x21xpn4.x1n2onr6")
        if not reply_divs:
            print("No more replies visible.")
        else:
            for reply_div in reply_divs:
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView(false);", reply_div)
                    reply_div.click()
                    time.sleep(1)
                except Exception as e:
                    print(f"Failed to click 'View more': {e}")

    def get_comments(self, company):
        comments = []
        pattern = re.compile(r"(\d+(h|d|w))")

        while True:
            comments_div = self.driver.find_elements(By.CSS_SELECTOR, "div.x1n2onr6.x1ye3gou.x1iorvi4.x78zum5.x1q0g3np.x1a2a7pz")
            new_comments = []

            for comment_div in comments_div:
                comment_text = comment_div.text.split("\n")
                name = comment_text[0]
                today_date = date.today().strftime("%Y-%m-%d")

                match = pattern.search(comment_text[-1])
                how_long = match.group(0) if match else ""
                comment = "\n".join(comment_text[1:-1]) if match else "\n".join(comment_text[1:])

                try:
                    url = comment_div.find_element(By.TAG_NAME, "a").get_attribute("href")
                except:
                    url = ""

                new_comment = {
                    "date": today_date,
                    "name": name,
                    "company": company,
                    "comment": comment,
                    "how_long": how_long,
                    "url": url
                }
                new_comments.append(new_comment)

                # Get replies
                try:
                    replies_div = comment_div.find_element(By.CSS_SELECTOR, "div.x1n2onr6.x1e558r4.x1iorvi4.x78zum5.x1q0g3np.x1a2a7pz")
                    replies_content = replies_div.get_attribute("innerHTML")
                    print(f"Replies content: {replies_content}")
                except:
                    print("Failed to get replies")
                
                # for reply_div in replies_div:
                #     reply_text = reply_div.text.split("\n")
                #     reply_name = reply_text[0]
                #     reply_comment = "\n".join(reply_text[1:])

                #     try:
                #         reply_url = reply_div.find_element(By.TAG_NAME, "a").get_attribute("href")
                #     except:
                #         reply_url = ""

                #     new_reply = {
                #         "date": today_date,
                #         "name": reply_name,
                #         "company": company,
                #         "comment": reply_comment,
                #         "how_long": "",  # Assuming no 'how_long' for replies
                #         "url": reply_url
                #     }
                #     new_comments.append(new_reply)

            if not new_comments or all(comment in comments for comment in new_comments):
                break

            comments.extend(new_comments)
            time.sleep(0.5)

        with open('comments_posts.json', 'w') as file:
            json.dump({"comments": comments}, file, indent=4)
            
        print(f"Logged {len(comments)} comments.")

    def quit(self):
        self.driver.quit()

