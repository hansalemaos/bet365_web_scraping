# pip install pandas selenium a_selenium2df PrettyColorPrinter
# imporant: seleniumbase must be installed like this:
# python.exe -m pip install -U seleniumbase
# https://www.youtube.com/watch?v=uVkT61OQTPs

from seleniumbase import Driver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from a_selenium2df import get_df
from PrettyColorPrinter import add_printer

add_printer(1)
driver = Driver(uc=True)
driver.get("https://www.bet365.com/#/AC/B1/C1/D1002/E88638566/G40/")
df = pd.DataFrame()
while df.empty:
    df = get_df(
        driver,
        By,
        WebDriverWait,
        expected_conditions,
        queryselector="*",
        with_methods=True,
    )

df.loc[df.aa_textContent.str.contains("^Aceitar$", regex=True, na=False)].iloc[
    0
].se_click()
dfteams = df.loc[
    df.aa_innerHTML.str.contains("rcl-ParticipantFixtureDetails_LhsContainer", na=False)
    & ~df.aa_offsetLeft.isna()
    & df.aa_textContent.str.contains(r"^\d+:\d\d", regex=True, na=False)
]
data = list(
    reversed(
        df.loc[
            df.aa_classList.str.contains(
                "gl-MarketGroupContainer", na=False, regex=False
            )
        ]
        .aa_innerText.iloc[0]
        .splitlines()
    )
)
data2 = [x for x in data if x not in ["1", "2", "X"]]
passos = len(dfteams)
df2 = pd.DataFrame(
    reversed(
        [list(reversed(data2[x : x + passos])) for x in range(0, len(data2), passos)][
            :4
        ]
    )
).T
df3 = dfteams.aa_innerText.str.split("\n", expand=True, regex=False)[[0, 1, 2]].rename(
    columns={0: "horario", 1: "team1", 2: "team2"}
)
df2 = df2.rename(columns={0: "vencedor1", 1: "empate", 2: "vencedor2", 3: "numero"})
dffinal = pd.concat([df2.reset_index(drop=True), df3.reset_index(drop=True)], axis=1)
print(dffinal)
