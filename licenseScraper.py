# Main Script
from playwright.sync_api import Playwright, sync_playwright, expect
from bs4 import BeautifulSoup
import re
import nltk # splitting by english words

in_seconds = 1000 # aux variable to convert milli to seconds

def run(playwright: Playwright) -> None:
    ### Joining
    kidnappings = set()

    # browser = playwright.chromium.launch(headless=False, slow_mo=5000)
    browser = playwright.chromium.launch(headless=True)
    # context = browser.new_context(record_video_dir="videos/")
    context = browser.new_context()
    page = context.new_page()
    # while True:
    # goes to the PBS warn
    page.goto("https://warn.pbs.org/") # Go to link
    page.wait_for_load_state()
    print("Waiting for load state...")
    page.wait_for_timeout(5*in_seconds)
    print("Navigated to https://warn.pbs.org")

    # roles
    page.screenshot(path="screenshots/1.png")
    page.get_by_role("button").first.click() # Open sidebar
    page.wait_for_load_state()

    page.screenshot(path="screenshots/2.png") # change this so that it looks better T.T
    page.get_by_role("complementary").filter(has_text="Alert ListThere are no active alerts. Click the filter icon to view expired aler").get_by_role("button").first.click() # Click the filters button to change from active alerts to all alerts


    page.screenshot(path="screenshots/3.png")
    page.query_selector(".ant-select-selection-item").click()
    page.get_by_text("All alerts").click() # Change alert type to all alert
    page.wait_for_load_state()
    print("Navigated to all alerts")
    page.screenshot(path="screenshots/4.png")

    page.locator('#card-alerts-list').first.first.nth(0).click() # clicks on the card alerts to open up the alert info
    page.screenshot(path="screenshots/6.png")
    print("Opened alert info")
    page.wait_for_load_state()
    
    def scrape():
        html = page.inner_html("._2T6JSna1WBLvwlkPoVN3XU")
        soup = BeautifulSoup(html, "html.parser")
        soup = soup.get_text()
        index1 = soup.find("Sent")+4
        timeSent = soup[index1:index1+19] # time sent
        # print("Time sent: " + timeSent)
        index1 = soup.find("360CH EN")+8
        index2 = soup.find("90CH")-4
        if index1 != 7 and index2 != -5:
            wea360ch = soup[index1:index2] # wea360ch
            # print("WEA 360CH EN: " + wea360ch)
        else: wea360ch = ''
        index1 = soup.find("Description EN")+14
        index2 = soup.find("ID")
        if index1 != 13 and index2 != -1:
            desc = soup[index1:index2] # description 
            # print("DESCRIPTION EN: " + desc)
        else:
            desc = ''
        return wea360ch, desc, timeSent

    wea360ch, desc, timeSentFirst = scrape()

    exceptions = ['WEA', '360CH']
    keywords = ['child', 'amber', 'plate', 'license', 'lic', 'reg']
    rejects = ['tornado', 'weather']
    def grab_license_plate(wea360ch, desc):
        license_plate = ''
        regex = '^(?=.*[A-Z])(?=.*\\d).+$'
        r = re.compile(regex)
        word_list = nltk.tokenize.word_tokenize((wea360ch + desc), language='english')
        
        valid = False
        for word in word_list: # validate word_list
            if word.casefold() in keywords:
                valid = True
                print('valid - contains: ', word)
                break
            if word.casefold() in rejects:
                print('rejected - contains: ', word)
                break
        if not valid: return ''
        
        for word in word_list:
            if (re.search(r, word)) and word not in exceptions and len(word) in [6,7,8]: # if the word is a license plate, aka if the word is 6-8 long (works for US), word is not an exception, and word has a number and a letter by regex
                license_plate = re.sub(r'[^\w\s]', '', word) # strip punctuation
        print("License Plate: " + license_plate)
        # print(wea360ch, desc)
        return license_plate


    kidnappings.add(grab_license_plate(wea360ch, desc))
    timeSent = ''
    print("Time Sent First: " + timeSentFirst)
    while timeSentFirst != timeSent:
        page.get_by_role("button").nth(2).click() # clicks next to get the next alert info
        page.wait_for_load_state()
        page.screenshot(path="screenshots/7.png")
        print()
        wea360ch, desc, timeSent = scrape()
        kidnappings.add(grab_license_plate(wea360ch, desc))
        page.wait_for_timeout(1*in_seconds) # prevent rate limiting. scrape only one alert per second
    
    context.close()
    browser.close()

      
    
      # ---------------------

def go():
    with sync_playwright() as playwright:
        run(playwright)
    
go()