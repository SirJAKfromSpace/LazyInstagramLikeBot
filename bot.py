from selenium import webdriver
import urllib.request
import os
import time

class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome('./chromedriver.exe')
        self.base_url = 'https://www.instagram.com'

        self.login()

    def login(self):
        self.driver.get('{}/accounts/login/'.format(self.base_url))
        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)
        self.driver.find_elements_by_xpath("//div[contains(text(), 'Log In')]")[0].click()
        time.sleep(2)

    def nav_user(self, user):
        self.driver.get('{}/{}/'.format(self.base_url, user))


    def like_latest_posts(self, user, n_posts, like=True):
        action = 'Like' if like else 'Unlike'
        self.nav_user(user)

        imgs = []
        imgs.extend(self.driver.find_elements_by_class_name('_9AhH0'))

        for img in imgs[:n_posts]:
            try:
                img.click()
            except Exception as e:
                print(e)
            time.sleep(1)
            print('open img')
            try:
                self.driver.find_element_by_xpath("//*[@aria-label='{}']".format(action)).click()
            except Exception as e:
                print(e)
            #self.comment_post('beep boop testing bot')
            time.sleep(1)
            print('liked')
            try:
                self.driver.find_elements_by_class_name('ckWGn')[0].click()
            except Exception as e:
                print(e)


    def download_image(self, src, image_filename, folder):
        folder_path = './{}'.format(folder)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        img_filename = 'image_{}.jpg'.format(image_filename)
        urllib.request.urlretrieve(src, '{}/{}'.format(folder, img_filename))


    def download_user_images(self, user):
        self.nav_user(user)

        img_srcs = []
        finished = False
        while not finished:
            finished = self.infinite_scroll() # scroll down
            img_srcs.extend([img.get_attribute('src') for img in self.driver.find_elements_by_class_name('FFVAD')]) # scrape srcs

        print('done scrolling')
        img_srcs = list(set(img_srcs)) # clean up duplicates
        print(len(img_srcs))

        for idx, src in enumerate(img_srcs):
            self.download_image(src, idx, user)


    def infinite_scroll(self):
        self.last_height = self.driver.execute_script("return document.body.scrollHeight")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        self.new_height = self.driver.execute_script("return document.body.scrollHeight")

        if self.new_height == self.last_height:
            return True

        self.last_height = self.new_height
        return False



if __name__ == '__main__':
    igbot = InstagramBot('yourusername','yourpassword')
    igbot.like_latest_posts('subjectusername',5)
    # igbot.download_user_images('subjectusername')
