<h1>Python Selenium Page Object Wrapper</h1>

This project offers an selenium wrapper with enhanced page object design : 

**1. Finding of locators with ExplicitWait are wrapped under the library.**
* No use of webdriver.find_element nor explicit wait on the code. cleaner code
* Expected conditions and time-out value are pass as class instantiation arguments. No use of time.sleep on the code.
* Resulting in much better readable and maintainable scripts.
* Example :
<br></br>
  With Framework:
  ```
  #define locator
  username = HTMLElement(id_='UserUsername',expected_condition = 'visible', timeout=10)
  #call locator
  username.send_keys("admin")
  ```
  Without Framework (native way)
  ```
  loc_username = 'UserUsername
  username_ele = WebDriverWait(webdriver, 10).until(EC.visibility_of_element_located((By.ID,self.loc_username)))
  username_ele.send_keys("admin")
  ```
**2. Webelement gets looked up each time the locator is used.**
* Define locator once, but it does search for the locator everytime the webelement is called. (find element on the fly for every calls)
* Helps to prevent StaleElementReferenceExceptions where element no longer attached to DOM.
* Example:
<br></br>
  With Framework:
  ```
  state = HTMLElement(id_='state')
  state.get_attribute('value')
  # refresh page to reload the state
  webdriver.refresh
  # get the state without refinding the element
  state.get_attribute('value')
  ```
  Wihtout the Framework:
  ```
  # for simplicity , not using the webdriverwait in this examples.
  loc_state = 'state'
  state_ele = webdriver_find_by_id(loc_state)
  state_ele. get_attribute('value')
  webdriver.refresh
  # need to refind the webelement after refresh
  state_ele = webdriver_find_by_id(loc_state)
  state_ele. get_attribute('value')
  ```
**3. Wraps the standard selenium methods/properties for better error handling and retries.**
* Standard selenium webelement actions/methods that fails are retried. Example, when click fails due to the “webdriver exceptions, the click will be received by different element”. The framework will retry the click for x number of times before throwing an exception. 
* No try catch code on the scripts. Clean code.

**4. Allow parent-child node by defining the HTMLElement/HTMLElementList(child) as attributes of another HTMLElement/HTMLElementList(parents).**
 * Ability to define collection of web elements as a class and to reuse on multiple pages. Less boilerplate code. 
 * locating elements easier as its search scope will limited to the nested elements of the fragment only.
 * easier code management as the complex pages or large functinal areas can be break into smaller multiple class objects.

<h3>PageObject</h3>

* PageObject represents a webpage.
* Defines all the HTMLElement, HTMLElementList as class attributes.
* Functionality and the service offered by the page are defined as methods. 
* Test scripts calls the attributes and the methods which makes the test script human readable (like psudocode).
* Instantiate with selenium webdriver instance.

<h3>HTMLElement</h3>

* Represents each html element on a webpage (PageObject). Represents the DOM element. 
* A wrapper class that encapsulates the standard functionality of the Selenium WebElement class for better error handling. The actions will be retried for x (defaults to 3) times before raising an Timeout exception.
* Locates the element on the fly (in other words, the webdriver does a find_element every time this object is called in the script. helps to avoid StaleElementReference exceptions and cleaner code).
* Finds a Selenium WebElement instance for the locator specified in its constructor with an explicit wait(webdriverwait) automatically.
* Locators, Expected Conditions and WaitTimeout are specified as instantiation arguments.
* Locators can be any from the following table. The values maps to the Selenium Webdriver’s locator strategies.
  
  | Keyword Arg   | selenium.webdriver.common.by   |
  | ------------- |:------------------------------|
  | id\_          | By.ID  |  
  | css           | By.CSS_SELECTOR    |
  | name          | By.NAME    |
  | class_name    |  By.CLASS_NAME|
  | tag_name      |  By.TAG_NAME     | 
  | link_text     |  By.LINK_TEXT    |
  | partial_link_text |  By.PARTIAL_LINK_TEXT     |  
  | xpath         |  By.XPATH    |
    
* Expected Conditions can be any from the following table. The Values maps to Selenium Webdriver’s Expected Conditions.

    For HTMLElement:
    

    | Keyword Arg   | selenium.webdriver.support   |
    | ------------- |:------------------------------|
    | presence       | expected_conditions.presence_of_element_located  |  
    | visible           | expected_conditions.visibility_of_element_located    |
    | frame_available          | expected_conditions.frame_to_be_available_and_switch_to_it    |
    | invisible    |  expected_conditions.invisibility_of_element_located|
    | clickable     |  expected_conditions.element_to_be_clickable   |
    | selected |  expected_conditions.element_located_to_be_selected     |
    
    For HTMLElementList:
    
 
    | Keyword Arg   | selenium.webdriver.support   |
    | ------------- |:------------------------------|
    | presence       | expected_conditions.presence_of_all_elements_located  |  
    | visible           | expected_conditions.visibility_of_any_elements_located    |
    
* Expected condition and WaitTimeout is optional arguments which are default to "visible" and 10 seconds. 
* Available methods (Standard Selenium WebElement actions) that will be retried on failures.
  - Click()
  - Send_keys()
  - Clear()
  - Text
  - Get_attributes()
  - Is_displayed()
  - Is_selected()
  - Submit()
  - Is_enable()
* All the available find_element\* methods found under the selenium webelement are not wrapped under this for the error handling and retries.
* Instantiated under
  - PageObject
  - HTMLElement (where this instance acts as a parent)
* Parent-Child Hierachy
  - HTMLElement acts as a child node when they are defined as attributes of another HTMLElement class.
  - Search scope of the attributes will be limited to the Parent element.
  - When to use?
    - A collection of elements or fragment of a page is being reused. For an example, tables, widgets, menus, footers, search bars etc.
    - To break down the functionality of the page for a better code management and readability.
* native_weblement property returns the selenium webelement instance.


<h3>HTMLElementList</h3>

* Represents list of webelements on a webpage.
* Constructed same way as HTMLElement. 
* Locating elements works same way as HTMLElement.

<h3>Extended Elements</h3>

* Todo .. Coming Soon.

<h3>Simple Examples</h3>

<h5>1. PageObject & HTMLElement</h5>

lets take a simple login page.

```
<div class="form">
   <form class="login-form">
     <input type="text" id='UserUserName' placeholder="username"/>
     <input type="password" id='UserPassword' placeholder="password"/>
     <button id='loginbutton'>login</button>
     <p class="message">Not registered? <a href="#">Create an account</a></p>
   </form>
</div>
```

The PageObject Class :

``` python
class LoginPage(PageObject):
	username = HTMLElement(id_='UserUserName')
	password = HTMLElement(id_='UserPassword')
	login_button = HTMLElement(id_='loginbutton', expected_condition='clickable')
	
	# service offered by the page are defined as methods
	def login(username, password);
		self.username = username # can do it this way too, its the same: self.username.send_keys(username)
		self.password = password
		self.login_button.click() # since the expected_condition is set as clickable,
```

There is 2 ways to login from the test script

```python
webdriver = webdriver.Firefox()
login_page = LoginPage(webdriver)

# method 1 : use the attributes directly
login_page.username = 'SomeUserName' # can do it this way too, its the same :  login_page.username.send_keys('SomeUserName')
login_page.password = 'SomePassword'
login_page.login_button.click()

# method 2 : use the predefined method for login
login_page.login(username='SomeUserName', password='SomePassword')

```

<h5>2. PageObject with HTMLElementList</h5>

lets take a simple nav menu example

```
<nav>
  <ul id="Menu">
    <li class="Menus">
      <a>Home</a>
    </li>
    <li class="Menus">
      <a>Features</a>
    </li>
    <li class="Menus">
      <a>Explore</a>
    </li>
    <li class="Menus">
      <a>About</a>
    </li>
    <li class="Menus">
      <a>Contact</a>
    </li>
  </ul>
</nav>
```

The PageObject:

``` python
class SomePage(PageObject):
	nav_list = HTMLElementList(class_name='Menus')
```
To click the Explore menu at test script:

``` python
webdriver = webdriver.Firefox()
some_page = SomePage(webdriver)
some_page.nav_list[2].click()
```

<h5>3. PageObject with HTMLElement</h5>

Let's take a search box that appears on 2 different page. 

Snipet of Page A html

```
<div class='PageA'>
  <div id='search-box'> 
    <form> 
      <input name='q' placeholder='Search' type='text'/> 
      <button type='submit'> 
        <span>Search</span> 
      </button> 
    </form> 
  </div>
</div>
```

Snippet of Page B html

```
<div class='PageB'>
  <div> 
    <form> 
      <input name='q' placeholder='Search' type='text'/> 
      <button type='submit'> 
        <span>Search</span> 
      </button> 
    </form> 
  </div>
</div>
```

SearchBox HTMLElement class :

```python
class SearchBox(HTMLElement):
  # locators/attributes defined under HTMLElement is searched withtin the context of the element declared during the declaration of this HTMLElement
  
  search_text = HTMLElement(xpath="./form/input")
  search_button = HTMLElement(xpath="./form/button", expected_condition="clickable")
  
  # methods (operations that can be done on this collection of elements)
  def search(query):
    self.seach_text = query
    self.search_button.click()
```

Respective Page A and Page B PageObject: 

```python
class PageA(PageObject):

	search_box = SearchBox(id_="search-box")
	
class PageB(PageObject):
	
	seach_box = SearchBox(xpath="//div[@class='PageB'/div")
```

<h5>4. PageObject with HTMLElementList</h5>

Good example for this would be the google search results. Please look at the [test/google](./test/google) directory.
