from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# variables
    #query = ''
    #price = ''

# login info
login_email = ''
login_password = ''

listing_num = 1
listing_time = 0
added_to_wishlist = 0

# processes time format
def Change_Time(Time):
    listing_time = ''
    Temp = Time[0:2]
    for char in Temp:
        if char.isdigit() == 1:
            listing_time += char
    return int(listing_time)

def dropdown_filter(filtered_by):
    # click on dropdown menu
    driver.find_element(By.XPATH, value='/html/body/div[5]/div[4]/div[1]/div/div[1]/div[3]/div[1]/div/span/button').click()
    time.sleep(1)
    # Sort by ending soonest
    driver.find_element(By.XPATH, value='//*[@id="s0-51-12-5-5[0]-36-1-content-menu"]/li[{}]/a'.format(filtered_by + 1)).click()
    time.sleep(1)

query = input('what would you like to search? ')
price = input('what is your maximum price? ')

while True:
    filtered_by = input('what would you like to filter your searches by?\n'
                        '\n Time: Ending Soonest: 1'
                        '\n Time: Newly Listed: 2'
                        '\n Price + shipping: Lowest First: 3'
                        '\n Price + shipping: Highest First: 4\n'
                        '\n Type the corresponding number: ')
    if filtered_by in '1234':
        filtered_by = int(filtered_by)
        break
    else:
        print('\nincorrect filter. Please try again.\n')

# creates webdriver for edge
os.environ['PATH'] += r"C:/EdgeDriver"
driver = webdriver.Edge()

# navigates to sign-in page
driver.get('https://www.ebay.ca/signin/')
time.sleep(1)

# Enters username
User = driver.find_element(By.ID, value='userid')
User.send_keys(login_email)
driver.implicitly_wait(1)

User = driver.find_element(By.ID, value='userid')
User.send_keys(Keys.ENTER)
driver.implicitly_wait(1)

# Enters password
try:
    Password = driver.find_element(By.XPATH, value='//*[@id="pass"]')
    Password.send_keys(login_password, Keys.ENTER)
    driver.implicitly_wait(1)
except:
    print("\nOops! Verification needed!")
    driver.quit()
    exit()

# Searches for products
Search = driver.find_element(By.XPATH, value='//*[@id="gh-ac"]')
Search.send_keys(query, Keys.ENTER)
driver.implicitly_wait(3)

# refreshes page (just in case)
driver.refresh()

# dropdown filter
dropdown_filter(filtered_by)

# select free shipping
driver.find_element(By.XPATH, value='/html/body/div[5]/div[3]/ul/li[1]/ul/li[7]/div[2]/ul/li/div/a/div/span/input').click()
driver.implicitly_wait(2)

# filter price
try:
    Price = driver.find_element(By.XPATH, value='//*[@id="s0-51-12-0-1-2-6-0-6[3]-0-textrange-endParamValue-textbox"]')
    Price.send_keys(price, Keys.ENTER)
    driver.implicitly_wait(2)
except:
    Price = driver.find_element(By.XPATH, value='//*[@id="s0-51-12-0-1-2-6-0-6[2]-0-textrange-endParamValue-textbox"]')
    Price.send_keys(price, Keys.ENTER)
    driver.implicitly_wait(2)

could_not_be_found = 0

# loops through each listing, checks for time, and if <24hrs, opens listing in new tab and saves to wishlist
while True:
    try:
        # returns string of the time
        try:
            Time = driver.find_element(By.XPATH, value='//*[@id="s0-51-12-6-3-3[1]-9-1-24[1[1[0]]]-2-0"]/span[2]'.format(listing_num)).text
        except:
            Time = driver.find_element(By.XPATH, value='//*[@id="s0-51-12-6-3-3[1]-9-1-24[1[2[0]]]-2-0"]/span[2]'.format(listing_num)).text
        # filters out listings whose 'Time' is 1 day or more
        if 'd' in Time:
            break
        else:
            # re-formats time
            listing_time = Change_Time(Time)
            if listing_time < 24:
                # click on link, opens link in new tab //*[@id="s0-51-12-6-3-3[1]-9-1-24[1[1[0]]]-2-0"]/span[2]
                link = driver.find_element(By.XPATH, value='//*[@id="srp-river-results"]/ul/li[{}]/div/div[2]/a'.format(listing_num + 1))
                link.click()
                driver.implicitly_wait(2)

                # switches to new tab
                driver.switch_to.window(driver.window_handles[1])
                listing_name = driver.find_element(By.XPATH, value='//*[@id="LeftSummaryPanel"]/div[1]/div[1]/div/h1/span').text
                driver.implicitly_wait(1)
                curr_price = driver.find_element(By.XPATH, value='//*[@id="prcIsum_bidPrice"]').text
                if driver.find_element(By.XPATH, value='//*[@id="vi-atl-lnk-99"]/span[2]').text == 'Watching':
                    # checks if already added to wishlist
                    print('\"{}\" has already been added to your wishlist.'.format(listing_name))
                else:
                    # clicks 'add to wishlist'
                    driver.find_element(By.XPATH, value='//*[@id="vi-atl-lnk-99"]').click()
                    print('\"{}\" (price: {}) was added to your wishlist.'.format(listing_name, curr_price))
                    added_to_wishlist += 1
                    driver.implicitly_wait(1)

                # closes tab and switches back to original page
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                # waits and goes to next listing
                listing_num += 1
                time.sleep(2)
            else:
                break
    except:
        # if listing could not be found, move onto next listing
        print("listing {} could not be found".format(listing_num))
        listing_num += 1
        could_not_be_found += 1
        if could_not_be_found >= 10:
            break
        else:
            continue

print("\nProgram successful! You've added {} items from your search \"{}\" to your wishlist".format(added_to_wishlist, query))

see_wishlist = input('\nDo you wish to see your wishlist? ')

if see_wishlist == 'yes':
    driver.execute_script("window.open('https://www.ebay.ca/mye/myebay/watchlist');")
else:
    print("\nexiting program...")
    time.sleep(2)
    driver.quit()
    print("Program Complete")
    exit()
