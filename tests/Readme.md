# Steps to install a test evvironment
## Obeing the test Goat!
I suggest the very instructiv and easy to read/follow book [Test-Driven Development with Python](https://www.obeythetestinggoat.com/)

## Tools to install
### [Geckodriver](https://github.com/mozilla/geckodriver/releases)
Download and install approriate version like so:  
`wget https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz`

check the path of your system: `echo $PATH`

unpack the geckodriver into one of the folders listed with the above commend:  

`tar xvfz geckodriver-v0.19.1-linux64.tar.gz -C ~/bin`

test it:  
`geckodriver`  
This should present some version information.

### Selenium
Selenium together with geckodriver will be used to create browser based tests.

**Important!!** before you install selenium, you have to activate the virtualenv into which to install it!  
`workon  bridgebuilder`  
then:  
`pip install selenium`

## A simple script to test whether all is in place

