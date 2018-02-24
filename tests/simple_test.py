# this is a simple script to test, whether the test environment is working

# create a browser object
from selenium import webdriver
browser=webdriver.Firefox()

# let the browser point to github
browser.get('https://github.com/')

# just test something we are sure to be there
assert 'GitHub' in browser.title

# ok fine, close things down again ..
browser.quit()
