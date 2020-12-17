from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import string, random
import pyperclip
import time 

LENGTH_PASS = 12

"""from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By"""
"""WebDriverWait(self.driver, 40).until(
                    EC.presence_of_element_located((By.ID, 'userIdStatus'))"""


def randomStringGenerator(length=13):
    """create random string ascii values"""
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


password = randomStringGenerator(LENGTH_PASS)
initialUserName = 'TheGreatEncryption'
randomStr = randomStringGenerator(13)
finalUserName = initialUserName + randomStr

links = [
    'https://www.guerrillamail.com/', 'https://account.protonvpn.com/signup'
]
browser = webdriver.Firefox()

browser.get(links[1])
browser.implicitly_wait(10)
button = browser.find_element_by_xpath(
    '/html/body/div/main/main/div/div[4]/div[1]/div[3]/button')
button.click()

#username is frame

browser.switch_to.frame(0)
time.sleep(3)
button = browser.find_element_by_id('username')
button.click()
time.sleep(3)
button.send_keys(finalUserName)
button.send_keys(Keys.TAB)

time.sleep(1)
#password is not in frame
browser.switch_to.default_content()
writable = browser.find_elements_by_id('password')[1]  #loc 1 is the real?
time.sleep(1)
writable.click()
time.sleep(3)
writable.send_keys(password)

#password confirm no frame
writable.send_keys(Keys.TAB)
writable = browser.find_elements_by_id('passwordConfirmation')[0]
time.sleep(1)
writable.click()
time.sleep(3)
writable.send_keys(password)

#open the tmpmail web
control_str = "window.open('{0}')".format(links[0])
browser.execute_script(control_str)
time.sleep(3)
browser.switch_to.window(browser.window_handles[-1])
time.sleep(3)
button = browser.find_element_by_xpath('//*[@id="use-alias"]')
button.click()
button = browser.find_element_by_xpath('//*[@id="email-widget"]')
button.click()
body = browser.find_element_by_tag_name('body')
body.send_keys(Keys.CONTROL + 'c')  #copy mail to clipboard

#fill mail in account
browser.switch_to.window(browser.window_handles[0])
mail = pyperclip.paste()  #save mail from clipboard
browser.switch_to.frame(1)
button = browser.find_element_by_id('email')
time.sleep(1)
button.click()
time.sleep(3)
button.send_keys(mail)

#create account
browser.switch_to.default_content()
button = browser.find_element_by_xpath(
    '/html/body/div/main/main/div/div[2]/div/div[1]/form/div[3]/div/button')
button.click()
time.sleep(1)
button = browser.find_element_by_xpath(
    '/html/body/div/main/main/div/div[2]/div/div[1]/div[2]/div/div/div[2]/form/div[2]/button'
)
button.click()
browser.switch_to.window(browser.window_handles[-1])
verification_code = None
while True:
    try:
        code = browser.find_element_by_class_name('email-excerpt').text
        print(code)
        if not code[-6:].isnumeric():
            raise Exception()
        print(code[-6:], 'the code')
        verification_code = code[-6:]
        break
    except:
        time.sleep(1)
browser.switch_to.window(browser.window_handles[0])
button = browser.find_element_by_id('code')
button.click()
time.sleep(2)
button.send_keys(verification_code)
time.sleep(2)
button = browser.find_element_by_xpath(
    '/html/body/div/main/main/div/div[2]/div/div[1]/div[2]/form/div/div/div[2]/button'
)
button.click()
print("Done,saving data...")

#save data to txt
saveData = open(f'{finalUserName}.txt', 'w')
saveData.write(f'User Name:{finalUserName} Password:{password}')
saveData.close()
print(mail, password, finalUserName)
print('Saving to file....')
time.sleep(3)
browser.find_element_by_xpath("/html/body/div[3]/dialog/div/footer/div/div/button[2]").click()

print("created, else you need to press manually on resent to verify")
