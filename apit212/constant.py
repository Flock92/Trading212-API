#POS SETUP ELEMENTS
POS_SETTINGS = '//*[@id="app"]/div[3]/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div/div[2]/div[3]/div/div/div'
POS_INSTRUMENT = '//*[@id="app"]/div[11]/div/div/div/div[1]/div/div/div/div/div[1]'
POS_NUM = '//*[@id="app"]/div[11]/div/div/div/div[1]/div/div/div/div/div[2]'
POS_QUANTITY = '//*[@id="app"]/div[11]/div/div/div/div[1]/div/div/div/div/div[3]'
POS_DIRECTION = '//*[@id="app"]/div[11]/div/div/div/div[1]/div/div/div/div/div[4]'
POS_PRICE = '//*[@id="app"]/div[11]/div/div/div/div[1]/div/div/div/div/div[5]'
POS_CURRENT_PRICE = '//*[@id="app"]/div[11]/div/div/div/div[1]/div/div/div/div/div[6]'
POS_TP = '//*[@id="app"]/div[11]/div/div/div/div[1]/div/div/div/div/div[7]'
POS_SL = '//*[@id="app"]/div[11]/div/div/div/div[1]/div/div/div/div/div[8]'
POS_TS = '//*[@id="app"]/div[11]/div/div/div/div[1]/div/div/div/div/div[9]'
POS_MARGIN = '//*[@id="app"]/div[11]/div/div/div/div[1]/div/div/div/div/div[10]'
POS_DATE_CREATED = '//*[@id="app"]/div[11]/div/div/div/div[1]/div/div/div/div/div[11]'
RESULT = '//*[@id="app"]/div[11]/div/div/div/div[1]/div/div/div/div/div[12]'
POS_DEFAULT = '//*[@id="app"]/div[11]/div/div/div/div[2]/div'
POS_RESIZE = '//*[@id="app"]/div[3]/div[2]/div[2]/div/div[2]/div[1]/div/div[2]'
ADJUST_POS = '//*[@id="app"]/div[3]/div[2]/div[2]/div/div[2]/div[1]' #110px 405px  width: auto; height: 165px; width: auto; height: 406px;

#MONITORING ELEMENTS
UNSUPPORTED = '//*[@id="app"]/div/div[2]/div[1]' #unsupported browser message
LOG_IN_EXPIRED = '//*[@id="app"]/div[4]/div/div[2]/div/div[2]' #log_in expired button
LOG_IN_EXPIRED_MSG = '//*[@id="app"]/div[4]/div/div[2]/div/div[1]/div/div/div' # value (Your login session has expired.)
#page expired
LOG_IN = '//*[@id="app"]/div[6]/div/div[2]/div/div[2]/div' #BUTTON
LOGIN_EXPIRED = '//*[@id="app"]/div[6]/div/div[2]/div/div[1]/div/div/div' #EXPIRED MESSAGE
#always present elements
LOCATION = "header-label" #Class
HOME = '//*[@id="app"]/div[5]/div[1]/div/div[1]/div[2]'
HOME3 = '//*[@id="app"]/div[3]/div[1]/div/div[1]/div[2]'
HOME4 = '//*[@id="app"]/div[4]/div[1]/div/div[1]/div[2]'
#header content buttons
ACCOUNT_STATUS = '//*[@id="app"]/div[3]/div[2]/div[2]/div/div[2]/div[2]/div[4]/div[4]/div/div/div/div' #Span
START_TRADING_NOW = '//*[@id="app"]/div[3]/div[1]/div/div[2]/div[2]'
DROP_MENU = '//*[@id="app"]/div[5]/div[1]/div/div[2]/div[3]' #XPATH type=dropdown
USER_NAME = '//*[@id="app"]/div[5]/div[1]/div/div[2]/div[3]/div/div[1]/div[1]'
TRADE_TYPE = '//*[@id="app"]/div[5]/div[1]/div/div[2]/div[3]/div/div[1]/div[2]'# example 'CFD - Real money'
#side_panel 
WATCH_LIST = 'with-tooltip sidepanel-tab home-tab stroked active selected'#class home button
SEARCH_BUTTON = 'with-tooltip sidepanel-tab search-tab stroked'#class search button
NOTIFICATIONS = 'with-tooltip sidepanel-tab notifications-tab stroked active'#class notifications
#status bar
LIVE_RESULTS = '//*[@id="app"]/div[3]/div[2]/div[2]/div/div[2]/div[2]/div[4]/div[1]/div[2]' #xpath
FREE_FUNDS = '//*[@id="app"]/div[3]/div[2]/div[2]/div/div[2]/div[2]/div[4]/div[2]/div[2]' #xpath
BLOCKED_FUNDS = '//*[@id="app"]/div[3]/div[2]/div[2]/div/div[2]/div[2]/div[4]/div[3]/div[2]' #xpath
MARGIN_INDICATORS = '//*[@id="app"]/div[5]/div[2]/div[2]/div/div[2]/div[2]/div[4]/div[4]/div/div/div/div' #xpath
#watch list
SCROLL_DOWN_BAR = '//*[@id="app"]/div[4]/div/div[2]/div/div[2]/div[2]/div[3]/div/div[2]/div/div[2]/div' #STYLE  height: 20px; top: 13.4645px;
OPEN_POSISTION_LIST = '//*[@id="app"]/div[3]/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div/div[3]/div'
ADD_TICKER_LAYOUT = '//*[@id="app"]/div[3]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[2]'
SPLIT_VIEW = '//*[@id="app"]/div[3]/div[2]/div[2]/div/div[1]/div[5]/div/div/div/div/div[1]/div[2]'
LAYOUT_AUTO = '//*[@id="app"]/div[3]/div[2]/div[2]/div/div[1]/div[6]/div/div/div/div/div[3]/div[1]/div/div/svg'
ADD_TICKER = '//*[@id="app"]/div[3]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div[1]'
ADD_TICKER2 = '//*[@id="app"]/div[3]/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[3]'
CLOSE_SEARCH = '//*[@id="app"]/div[4]/div/div[2]/div/div[1]/div[2]'
LAYOUT_MENU = '//*[@id="app"]/div[3]/div[2]/div[2]/div/div[1]/div[1]/div[2]/div'
CHART_TABS = '//*[@id="app"]/div[3]/div[2]/div[2]/div/div[1]/div[1]/div[1]/div[2]'
BUY_SCROLL_BAR = '//*[@id="app"]/div[4]/div/div[2]/div/div/div[4]/div[3]/div' #STYLE height: 198.032px; top: 0px;
#order positions
ACCESS_DENIED = '/html/body/div[2]/p[1]'
ACCESS_DENIED_REF = '/html/body/div[2]/p[3]'
ACCESS_DENIED_IP = '/html/body/div[2]/p[4]'
ACCESS_DENIED_MESSAGE = '/html/body/div[2]/p[2]'

#SETUP ELEMENTS
URL = "https://www.trading212.com/"
MEM_BUTTON = '//*[@id="__next"]/main/div[2]/div/div[2]/div/div[2]/div/form/div[4]/div[2]/input'
SUBMIT = '//*[@id="__next"]/main/div[2]/div/div[2]/div/div[2]/div/form/div[5]/input'
CLOSE = '//*[@id="app"]/div[6]/div/div[2]/div/div/div/div[2]/div/div[1]/div[3]/div/span/div'
CHECK_USER = '//*[@id="app"]/div[5]/div[1]/div/div[2]/div[3]/div/div[1]/div[1]'
COOKIES = '//*[@id="__next"]/main/div[2]/div/div[2]/div[2]/div[2]/div[1]'
LOGIN = '//*[@id="__next"]/header/div/div/div[2]/div[1]/div[2]/p'
#dropdown menu
PRACTICE = '//*[@id="app"]/div[11]/div/div/div/div/div/div/div[9]/div[1]'
#PRACTICE = '//*[@id="app"]/div[11]/div/div/div/div/div/div/div[9]/div[1]/div'
REAL = '//*[@id="app"]/div[11]/div/div/div/div/div/div/div[6]/div[1]/div'
ACCOUNT_PRACTICE = '//*[@id="app"]/div[11]/div/div/div/div/div/div/div[9]/div[1]/div' #class (real/practice) xpath=
SETTINGS = '//*[@id="app"]/div[11]/div/div/div/div/div/div/div[9]/div[2]/div[1]'
LOG_OUT = '//*[@id="app"]/div[11]/div/div/div/div/div/div/div[9]/div[2]/div[2]'

#TRADE ELEMENTS FOR CFD
#buttons for buy/sell
LIST0 = '//*[@id="app"]/div[4]/div/div[2]/div/div[2]/div[2]/div[3]/div/div[2]'
LIST = '//*[@id="app"]/div[4]/div/div[2]/div/div[2]/div[2]/div[3]/div/div[2]/div'
NEW_ORDER = '//*[@id="app"]/div[3]/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div/div[2]/div[1]' #xpath opens menu
CLOSE_TRADING_MENU = '//*[@id="app"]/div[4]/div/div[2]/div/div[1]/div[2]'#xpath to close trade menu (use to test elements)
SEARCH_INPUT_BAR = '//*[@id="app"]/div[4]/div/div[2]/div/div[2]/div[2]/div[1]/input'#xpath search bar to find stock
CHECK_FOR_OPTIONS = '//*[@id="app"]/div[4]/div/div[2]/div/div[2]/div[2]/div[3]/div/div[2]/div/div/div[1]/div/div' #xpath check to see if there are any options
INSTRUMENTS = '//*[@id="app"]/div[4]/div/div[2]/div/div[2]/div[2]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div'#class data-qa-code="search ticker"
SCROLLABLE_AREA = '//*[@id="app"]/div[4]/div/div[2]/div/div[2]/div[2]/div[3]/div/div[2]/div/div/div[1]/div'
#TRADE setup CFD (for market buys)
ORDER_COST = '//*[@id="app"]/div[4]/div/div[2]/div/div/div[4]/div/div/div[2]' #shows the value of the order
SELL_BUTTON = '//*[@id="app"]/div[4]/div/div[2]/div/div/div[2]/div[1]/div[1]'#class sell button
SELL_PRICE = 'price-sell' #class check the sell price on platform (from children get label class='formatted-price' children 1= currency symbol 2 & 3)
BUY_BUTTON = '//*[@id="app"]/div[4]/div/div[2]/div/div/div[2]/div[1]/div[2]'
BUY_PRICE = 'price-buy'
QUANTITY_SLIDER_RIGHT = '//*[@id="app"]/div[4]/div/div[2]/div/div/div[4]/div/div/div[3]/div[3]'
QUANTITY_SLIDER_LEFT = '//*[@id="app"]/div[4]/div/div[2]/div/div/div[4]/div/div/div[3]/div[1]'
QUANTITY_SLIDER = '//*[@id="app"]/div[4]/div/div[2]/div/div/div[4]/div/div/div[3]/div[2]/div[3]' #STYLE left: 290.82px; max
QUANTITY_BUTTON = '//*[@id="app"]/div[4]/div/div[2]/div/div/div[4]/div[1]/div/div[1]/div[2]/div[2]'
QUANTITY = '//*[@id="app"]/div[4]/div/div[2]/div/div/div[4]/div/div/div[1]/div[2]/div[2]/div[2]/input' #xpath span displays amouth of shares
QUANTITY2 = '//*[@id="app"]/div[4]/div/div[2]/div/div/div[4]/div/div/div[1]/div[2]/div[2]/div[1]/div/span[2]' #span needs to be cleared.
QUANTITY_SLIDER = '//*[@id="app"]/div[4]/div/div[2]/div/div/div[4]/div[1]/div/div[2]/div[2]/div[4]' #class
SCROLL_ORDER_MENU = '//*[@id="app"]/div[4]/div/div[2]/div/div/div[4]/div[4]' #top: 184.871px;
TP = '//*[@id="app"]/div[4]/div/div[2]/div/div/div[4]/div/div/div[4]/div/div[2]' #xpath toggle button
TP_RESULTS = '//*[@id="app"]/div[4]/div/div[2]/div/div/div[4]/div[2]/div/div[4]/div[2]/div[3]/div[2]/div[2]/input' #xpath change value to for take profit
SET_TP_AMMOUNT = '//*[@id="app"]/div[4]/div/div[2]/div/div/div[4]/div[2]/div/div[4]/div[2]/div[3]/div[2]/div[1]/div/span[2]'
SL = '//*[@id="app"]/div[4]/div/div[2]/div/div/div[4]/div/div/div[5]/div/div[2]' #xpath toggle button
SL_RESULTS = '//*[@id="app"]/div[4]/div/div[2]/div/div/div[4]/div[2]/div/div[5]/div[2]/div[3]/div[2]/div[2]/input' #xpath chnage value to stop loss
SET_SL_AMMOUNT = '//*[@id="app"]/div[4]/div/div[2]/div/div/div[4]/div[2]/div/div[5]/div[2]/div[3]/div[2]/div[1]/div/span[2]'
CONFIRM_ORDER = '//*[@id="app"]/div[4]/div/div[2]/div/div/div[5]/div' #xpath to confirm order
CHECK_ORDER_TYPE = '//*[@id="app"]/div[4]/div/div[2]/div/div/div[5]/div' #xpath to label that confirms order type (buy/sell)
#WATCH LIST
CURRENT_PRICE_INDICATOR = 'current-price-label current-sell-price-label' #class for current price indicator
#CLOSE POSITION
OPEN_POSISTION_LIST = '//*[@id="app"]/div[3]/div[2]/div[2]/div/div[2]/div[1]/div/div[1]/div/div[3]/div'
CLOSE_POSITION = '//*[@id="position-a645d758-d56a-403f-a51f-3ccec07a3dfc"]/div[3]/div/div' #CLASS data-table-content-column
CONFIRM_CLOSE = '//*[@id="app"]/div[4]/div/div[2]/div/div[3]/div[1]'
CLOSE_POSITION_CLASS = 'data-table-content-column'
OPEN_POSITION__CLASS = 'positions-table-item'
CLOSE_BUTTON_MENU = '//*[@id="app"]/div[7]/div/div/div[7]'
