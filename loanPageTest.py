# used selenium IDE for easy aquisition of element xpaths/css/ID/etc
# used the most unique identifier for a UI element as possible, at places , as is good practice
# not running headless for debug reasons and for ease of use when checking my homework. 
# It would be resource efficient to run headless when in production


# prerequisites:
#   python 3.7.2+
#   selenium 3.141.0 for python
#   chromedriver in PATH (used chromedriver included) ((in general Selenium Grid is a very useful thing, but for simplicities sake, decided not to use it for this))


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time #time.sleep(1)-s added here and there for animations and stuff to catch up

def faultyTest(inSpot):
    print("execution error at: ", inSpot, ", fix or update test code")
    print("good place to make a screenshot, etc")

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging']) #less garbage being thrown from chromedriver this way
browser = webdriver.Chrome(options=options)
browser.get("https://www.swedbank.lt/private/credit/loans/home?language=ENG")

#767 pixels is the magic number for width, test works for both desktop and mobile versions

#assuming starting fresh each time as is good practice, accepting cookies
#another option would be to permanently save the cookies in the webdriver options/setup
if browser.find_element_by_xpath("//ui-cookie-consent[@id='cookie-consent']/ui-modal/div[2]/div/div/ui-views/ui-view/h2"): 
    browser.find_element_by_css_selector(".ui-cookie-consent__accept-all-button").click()

#Make sure co-applicant tickbox unticked
borrowersTicked=browser.find_element_by_id("borrowers2")
borrowersUnticked=browser.find_element_by_id("borrowers1")

if borrowersTicked.get_attribute("checked") == "true":
    print("borrowers ticked, bad")
    browser.find_element_by_xpath("//label[contains(.,'Applying with a co-applicant')]").click()
    if borrowersUnticked.get_attribute("checked") == "true":
        print("borrowers not ticked anymore, good")
    else:
        faultyTest("borrowers, can't get unticked")
        
elif borrowersUnticked.get_attribute("checked") == "true":
        print("borrowers not ticked, continue")
else:
    faultyTest("borrowers, Schroedingers tickbox")
    
time.sleep(1)
#the least the devs could have done is named them borrowersTrue and borrowersFalse
# and maybe instead of the checked property, use a different boolean, like visible or enabled?
#referring to:

#function(event) {
#  if (event.target.checked) document.getElementById("borrowers2").checked = true;
#  else {
#    document.getElementById("borrowers1").checked = true;
#    if (Swedbank.country === "LT") document.querySelector(".borrowersRow").hide()
#  }
#  Calculation()
#}

#after checking another page with a similar tickbox, I now realize, that this might be an elaborate test, in which case, nice

#browser.get("https://www.swedbank.ee/private/credit/loans/student?language=EST")
#if browser.find_element_by_xpath("//ui-cookie-consent[@id='cookie-consent']/ui-modal/div[2]/div/div/ui-views/ui-view/h2"): 
#    browser.find_element_by_css_selector(".ui-cookie-consent__accept-all-button").click()

#e=browser.find_element_by_id("payrest-check")
#a=e.get_attribute("checked")
#print(a)
#browser.find_element_by_xpath("//section[@id='student-loan-calculator']/div/div[2]/div/dl/dd[4]/label").click()
#time.sleep(1)
#a=e.get_attribute("checked")
#print(a)
#exit()


#Dependants, 2 or more
if browser.find_element_by_id("dependants0").get_attribute("checked") == "true":
    print("dependants unticked") #means unticked
    browser.find_element_by_xpath("//label[contains(.,'More than one dependant in family')]").click()
    if browser.find_element_by_id("dependants1").get_attribute("checked") == "true" or browser.find_element_by_id("dependants2").get_attribute("checked") == "true":
        print("dependants now ticked")
    else:
        faultyTest("dependants faulty click")
elif browser.find_element_by_id("dependants1").get_attribute("checked") == "true":
        print("already ticked")
else:
    faultyTest("dependants, Schroedingers tickbox")

browser.find_element_by_xpath("//label[contains(.,'2 or more')]").click()
if browser.find_element_by_id("dependants2").get_attribute("checked") == "true":
    print("2 or more dependants selected")
else:
    faultyTest("dependantes, not enough children")

time.sleep(1)
#No obligations
if browser.find_element_by_id("obligationsCheck").get_attribute("checked") == "true":
    print("obligations")
    browser.find_element_by_xpath("//label[contains(.,'I have existing loan obligations (incl. in Swedbank)')]").click()
    if browser.find_element_by_id("obligationsCheck").get_attribute("checked") == "true":
        faultyTest("forever in debt")
    else:
        print("no obligations anymore")
else:
    print("no obligations")
 
time.sleep(1)
#monthly income 1000
income=browser.find_element_by_id("income")
income.send_keys(Keys.DELETE+Keys.BACKSPACE)
income.send_keys("1000"+Keys.RETURN)
if browser.find_element_by_xpath('//*[@id="long"]').get_attribute("value") == "1000":
    print("income 1k")
else:
    faultyTest("income, possibly wrong amount")

#max loan amount
maxLoanAmount=browser.find_element_by_xpath("//ui-slider[@id='slider1']/div[3]/ui-hint[2]").text
print("The maximum loan available with 1k monthly, 2 kids, no obligations and no co-applicant is: ", maxLoanAmount)
 
time.sleep(1)
#loan amount 45 000
loanslider=browser.find_element_by_xpath("//ui-slider/div[2]/input")
loanslider.clear()
for n in range(1, 10): #quick and dirty, but works
    loanslider.send_keys(Keys.BACKSPACE+Keys.DELETE)
loanslider.send_keys("45000" + Keys.ENTER)
    #still false amount, interact with other element

time.sleep(1)
#loan term 11 years
yearslider=browser.find_element_by_xpath("(//input[@type='text'])[11]")
for n in range(1, 10): #quick and dirty, but works
    yearslider.send_keys(Keys.BACKSPACE+Keys.DELETE)
yearslider.send_keys("132") #12 months x 11 years = 132 months

#click on monthly to update
#get monthly payment
browser.find_element_by_id("month-payment").click()
time.sleep(1)
#have to update the element after calculations
monthlyPayback=browser.find_element_by_id("month-payment").text
print("The monthly payback for 45k over 11 years with 1k monthly, 2 kids, no obligations and no co-applicant is: ", monthlyPayback)


time.sleep(1)
browser.close()