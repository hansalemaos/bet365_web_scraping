import re
from kthread_sleep import sleep
from seleniumbase import Driver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from a_selenium2df import get_df
from PrettyColorPrinter import add_printer
add_printer(1)

def obter_dataframe(query='*'):
    df = pd.DataFrame()
    while df.empty:
        df = get_df(
            driver,
            By,
            WebDriverWait,
            expected_conditions,
            queryselector=query,
            with_methods=True,
        )
    return df



driver = Driver(uc=True)
driver.get("https://www.bet365.com/#/IP/B1")
df = obter_dataframe()
df.loc[df.aa_classList.str.contains(
    'iip-IntroductoryPopup_Cross', regex=False, na=False)].se_click.iloc[0]()
sleep(2)
df.loc[df.aa_classList.str.contains(
    'ccm-CookieConsentPopup_Accept', regex=False, na=False)].se_click.iloc[0]()
df3 = obter_dataframe(query='div.ovm-Fixture_Container')
df3.loc[df3.aa_innerText.str.split('\n').str[2:].apply(
    lambda x: True if re.match(r'^[\d:]+Ç\d+Ç\d+Ç\d+Ç[\d.]+Ç[\d.]', 'Ç'.join(x)) else False)
].aa_innerText.str.split(
    '\n').apply(pd.Series).reset_index(drop=True).to_excel('c:\\testbet365_3.xlsx')
