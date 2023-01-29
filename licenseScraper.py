# Main Script
from playwright.sync_api import Playwright, sync_playwright, expect
from bs4 import BeautifulSoup

in_seconds = 1000 # aux variable to convert milli to seconds

def run(playwright: Playwright) -> None:
    ### Joining
    kidnappings = []

    # browser = playwright.chromium.launch(headless=False, slow_mo=5000)
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(record_video_dir="videos/")
    page = context.new_page()
    # while True:
    # goes the PBS warn
    page.goto("https://warn.pbs.org/") # Go to link
    page.wait_for_load_state()
    print("Wait for 20")
    page.wait_for_timeout(5*in_seconds)
    print("Done")

    # # all alerts logic
    # # XPATH
    # # expand alert list - //button[@id="root"]/section/section/main/div[1]/div/div[1]/button
    # page.screenshot(path="screenshots/11.png")
    # page.wait_for_load_state()
    # # page.get_by_role("button").first.click() # might delete the first idk
    # page.locator('//*[@id="root"]/section/section/main/div[1]/div/div[1]/button').click()
    # page.wait_for_load_state()
    
    # # This xpath opens the alert list filters - //button[@id="root"]/section/section/aside[1]/div/div/div[1]/div/div/div/button 
    # page.screenshot(path="screenshots/12.png")
    # page.locator('//button[@id="root"]/section/section/aside[1]/div/div/div[1]/div/div/div/button').click()
    
    # # Clicks the dropdown menu to set to all alerts from active alerts - //div[@id="root"]/section/section/aside[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div 
    # page.screenshot(path="screenshots/13.png")
    # page.get_by_role("span", name="Active alerts").click()
    # page.wait_for_load_state()
    # #page.locator('//div[@id="root"]/section/section/aside[1]/div/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div ').click()
    
    # # This selects the Active Alerts 
    # page.screenshot(path="screenshots/14.png")
    # page.get_by_role("span", name="All alerts").click()
    # page.wait_for_load_state()
    
    # # This closes the alert list filters - //button[@id="root"]/section/section/main/div[2]/div/button 
    # page.screenshot(path="screenshots/15.png")
    # page.locator('//button[@id="root"]/section/section/main/div[2]/div/button').click()
    # page.wait_for_load_state()
    # page.screenshot(path="screenshots/16.png")
    # #

    # roles
    page.screenshot(path="screenshots/1.png")
    page.get_by_role("button").first.click() # might delete the first idk
    page.wait_for_load_state()

    page.screenshot(path="screenshots/2.png") # change this so that it looks better T.T
    # page.query_selector(".ant-layout-sider-children").get_by_role("button").click() # gets the tree of the sidebar and clicks on the only button inside of the tree
    # page.get_by_role("button").click()
    page.get_by_role("complementary").filter(has_text="Alert ListThere are no active alerts. Click the filter icon to view expired aler").get_by_role("button").first.click()


    page.screenshot(path="screenshots/3.png")
    #page.query_selector(".ant-select-arrow").click().select_option("All alerts") # might need to get rid of click? dunno
    page.query_selector(".ant-select-selection-item").click()
    page.get_by_text("All alerts").click()
    page.wait_for_load_state()
    
    page.screenshot(path="screenshots/4.png")
    # # page.query_selector(".ant-space ant-space-vertical _1OdDIdGoEhOYqVK1LGkPbs").get_by_role("button").first.click() # clicks the button to resolve the screen
    # page.get_by_role("main").get_by_role("button").first.click()
    # page.wait_for_load_state()
    # page.wait_for_timeout(3*in_seconds)
    page.screenshot(path="screenshots/5.png")
    print("done")


    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # clicks a current alert
    # go through each of the active alerts and add it to a "seen set"
    # page.locator('//div[@class="_2PY_-Unzot-mgchwKKNgqk a4eoTN9WP9ad3-LhXHpuz"]').click() # i think that this should be the proper one to do. clicks on the div.
    # page.locator('//*[@id="collapsed-alerts-list"]/div/div/div[1]').click() # copy from xpath
    # page.locator("#collapsed-alerts-list div").click()
    ########################################################################

    page.locator('#card-alerts-list').first.first.nth(0).click() # clicks on the card alerts to open up the alert info
    page.screenshot(path="screenshots/6.png")
    print("done2")
    page.wait_for_load_state()
    page.get_by_role("button").nth(2).click() # clicks next to get the next alert info
    page.wait_for_load_state()
    page.screenshot(path="screenshots/7.png")
    print("done3")

    # what we need to do
    # get the words and save it to a db/set. Have var as time alert sent out for key to then break out of loop when hits that time again
    # filter through if we have seen the alert already
    # save the license plates to a hashset

    
    # # grabs all of the data from the side bar
    # page.wait_for_load_state()
    # #page.get_by_role("main").get_by_role("div").locator("._2PY_-Unzot-mgchwKKNgqk > .anticon").first.click()
    # #page.get_by_role("main").get_by_text("Missing Person").click()
    # page.locator('[class="_2PY_-Unzot-mgchwKKNgqk a4eoTN9WP9ad3-LhXHpuz"]').first.click()
    # #page.click('[class=_2PY_-Unzot-mgchwKKNgqk a4eoTN9WP9ad3-LhXHpuz]')
    # print("done2")
    # page.wait_for_timeout(3*in_seconds)
    # page.screenshot(path="screenshots/6.png")

    
    html = page.inner_html("._3hppmX6GqLF_toD4XOvBXz aLatcoPoKoAqweVTlcZId _1AEPF4RKn1ehVpDMKcErDr _1S8r8RZnqU7xI13MoBI3eJ _2T6JSna1WBLvwlkPoVN3XU")
    soup = BeautifulSoup(html, 'html.parser')
    print("souped up bitch")
    soup = soup.find_all('div').text
    if "child" or "amber" or " licence " or " reg " or " lic " in soup:
        kidnappings.append(soup)
        # after yoinking data from side bar put it into the database if it matches the above conditions (in the if statement)
    context.close()
    browser.close()

      
    
      # ---------------------

def go():
    with sync_playwright() as playwright:
        run(playwright)
    
go()