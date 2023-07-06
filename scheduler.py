from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from random_word import RandomWords
import os
import time
import sched
import datetime

# Create a scheduler
s = sched.scheduler(time.time, time.sleep)

now = datetime.datetime.now()
target_time = now.replace(hour=2, minute=0, second=0, microsecond=0)
if target_time < now:
    # If the target time has already passed today, add one day to the target time
    target_time += datetime.timedelta(days=1)

# Calculate the number of seconds until the target time

# (target_time - now).total_seconds()
seconds = 1

def run_script():

    # set variables
    r = RandomWords()
    x = 0
    search_query = ''
    daily_set = 1
    special_set = 1


    # count number of cards in special set
    def count_special_set():
        count = 0
        while True:
            try:
                driver.find_element(By.XPATH, value="//*[@id='more-activities']/div/mee-card[{}]/div/card-content/mee-rewards-more-activities-card-item/div/a".format(count + 1))
                count += 1
            except:
                break
        return count

    # count number of questions in a quiz
    def find_Qnum():
        Qnum = 1
        while True:
            try:
                # try looking for question number
                driver.find_element(By.ID, value='rqQuestionState{}'.format(Qnum))
                Qnum += 1
            except:
                # if not found, return question number
                break
        return Qnum

    def quiz():
        icon.click()
        driver.switch_to.window(driver.window_handles[2])

        # if already signed in
        try:
            driver.find_element(By.ID, 'rqStartQuiz').click()
            driver.implicitly_wait(2)
        # otherwise sign in first
        except:
            driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/span/a').click()
            time.sleep(2)
            driver.find_element(By.ID, 'rqStartQuiz').click()
            driver.implicitly_wait(2)

        x = 0
        # loops through for every question
        while x < find_Qnum():
            choice_num = 0
            # loops for every option in each question
            while True:
                # if can click, then select the option
                try:
                    driver.find_element(By.XPATH, value='//*[@id="rqAnswerOption{}"]'.format(choice_num)).click()
                    driver.implicitly_wait(2)
                    choice_num += 1
                # if cannot select an option, move to next question
                except:
                    break
            x += 1
            driver.implicitly_wait(3)

        # when finished quiz, close window and switch back to rewards tab
        driver.close()
        driver.switch_to.window(driver.window_handles[1])

    def poll():
        # open in new tab
        icon.click()
        driver.implicitly_wait(2)
        driver.switch_to.window(driver.window_handles[2])
        driver.implicitly_wait(2)

        # if already signed in
        try:
            time.sleep(2)
            # select a poll option (first option by default)
            driver.find_element(By.XPATH, value='//*[@id="btoption0"]').click()
        # otherwise sign in first
        except:
            driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/span/a').click()
            time.sleep(2)
            driver.find_element(By.XPATH, value='//*[@id="btoption0"]').click()

        time.sleep(1)
        driver.close()
        driver.switch_to.window(driver.window_handles[1])

    def click():
        icon.click()
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[2])
        time.sleep(1)
        driver.close()
        driver.switch_to.window(driver.window_handles[1])


    # create webdriver
    os.environ['PATH'] += r"C:/C:\Users\Lyric\Downloads\edgedriver_win64"
    driver = webdriver.Edge()

    # navigate to microsoft rewards
    driver.get('https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1660781776&rver=7.0.6738.0&wp=MBI_SSL&wreply=https:%2F%2Faccount.microsoft.com%2Fauth%2Fcomplete-signin%3Fru%3Dhttps%253A%252F%252Faccount.microsoft.com%252F%253Frefp%253Dsignedout-index%2526refd%253Dwww.bing.com&lc=1033&id=292666&lw=1&fl=easi2')
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH, value='//*[@id="navs"]/div/div/div/div/div[4]/a').click()
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(4)

    # bing points before running the script
    points_before = int(driver.find_element(By.XPATH, '//*[@id="balanceToolTipDiv"]/p/mee-rewards-counter-animation/span').text.replace(",", ""))
    print("bing points: " + str(points_before))

    '''daily set'''

    # iterate through each card in daily set
    while daily_set <= 3:
        print("\ndaily set number: " + str(daily_set))
        icon = driver.find_element(By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[{}]/div/card-content/mee-rewards-daily-set-item-content/div/a/mee-rewards-points/div/div/span[1]'.format(daily_set))
        class_name = icon.get_attribute("class")
        # check if task hasn't been done yet
        if class_name == 'mee-icon mee-icon-AddMedium':
            h3 = driver.find_element(By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[{}]/div/card-content/mee-rewards-daily-set-item-content/div/a/div[2]/h3'.format(daily_set)).text
            # check the type of task
            if 'quiz' in h3:
                quiz()
            elif 'poll' in h3:
                poll()
            else:
                click()
        # task has been done already
        else:
            pass

        # move onto next card
        daily_set += 1
        time.sleep(1)


    # iterate through each card in special set
    while special_set <= count_special_set():
        try:
            icon = driver.find_element(By.XPATH, '//*[@id="more-activities"]/div/mee-card[{}]/div/card-content/mee-rewards-more-activities-card-item/div/a/mee-rewards-points/div/div/span[1]'.format(special_set))
            class_name = icon.get_attribute("class")

            # check if task hasn't been done yet
            if class_name == 'mee-icon mee-icon-AddMedium':
                h3 = driver.find_element(By.XPATH, '//*[@id="more-activities"]/div/mee-card[{}]/div/card-content/mee-rewards-more-activities-card-item/div/a/div[2]/h3'.format(special_set)).text
                # check the type of task
                if 'quiz' in h3:
                    quiz()
                elif 'poll' in h3:
                    poll()
                else:
                    click()
            # task has been done already
            else:
                pass

        # if card does not have icon - skip
        except:
            print("does not provide points")
            pass

        # move onto next card
        special_set += 1
        time.sleep(1)

    # generates random search string
    r = RandomWords()

    string = ''

    while True:
        string += r.get_random_word() + ' '
        if len(string) >= 30:
            break

    # navigate to bing.com
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[2])
    driver.get('https://www.bing.com/')
    driver.implicitly_wait(1)

    # initialize search
    search = driver.find_element(By.ID, value="sb_form_q")
    search.send_keys('search ', Keys.ENTER)
    driver.implicitly_wait(1)

    # refreshes page
    driver.refresh()
    driver.implicitly_wait(1)

    # repeatedly searches for 30+ times
    while (x < 31):
        search_bar = driver.find_element(By.XPATH, value="//*[@id='sb_form_q']")
        search_bar.clear()
        search_bar.send_keys(string, Keys.ENTER)
        string = string[slice(0, -1)]
        x += 1
        time.sleep(1)

    # gather user data after running script
    driver.switch_to.window(driver.window_handles[1])
    # bing points after running the script
    current_points = int(driver.find_element(By.XPATH, '//*[@id="balanceToolTipDiv"]/p/mee-rewards-counter-animation/span').text.replace(",", ""))
    streak = int(driver.find_element(By.XPATH, '//*[@id="streakToolTipDiv"]/p/mee-rewards-counter-animation/span').text)
    ms_gifts = current_points / 4800
    dollars = ms_gifts * 5

    # informs user program was successful and print earned bing points
    print('program was successful! You earned {} bing points!'.format(points_before - current_points))
    print('Your bing points: {}'.format(current_points))
    print('you are on a {} day streak! Keep it up!'.format(streak))
    print('you can afford approximately {} $5 microsoft gift cards! That\'s around ${} dollars!'.format(ms_gifts, dollars))

s.enter(seconds, 1, run_script)
s.run()
