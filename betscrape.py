import time
from LatinFixer import LatinFix
from pandasmemuc import MeMuc
from PrettyColorPrinter import add_printer  # optional
from a_pandas_ex_bs4df_lite import pd_add_bs4_to_df_lite
import pandas as pd
from a_pandas_ex_apply_ignore_exceptions import pd_add_apply_ignore_exceptions

pd_add_apply_ignore_exceptions()
add_printer(1)
pd_add_bs4_to_df_lite()
devices = MeMuc()


def wait_for_element_and_click(fu, deviceindex, timeout=60, click=True):
    df2 = pd.DataFrame()
    timeoutfinal = time.time() + timeout
    while df2.empty:
        try:
            if time.time().__gt__(timeoutfinal):
                raise TimeoutError("Timeout!!")
            uia = devices.get_ui_automator_df(deviceindex)
            df2 = uia.loc[fu(uia)]
        except AttributeError:
            continue
    if click:
        df2.iloc[0].ff_bb_tap_exact_center()


def get_mhtml_file(deviceindex):
    newest_archive = (
        [
            x
            for x in devices.iloc[
                deviceindex
            ].bb_adbtools.aa_execute_multiple_adb_shell_commands(
                "ls -t /sdcard/Download/"
            )
            if b"bet365" in x and b"mhtml" in x
        ][0]
        .decode("utf-8")
        .strip()
    )
    htmlcode = b"".join(
        devices.iloc[deviceindex].bb_adbtools.aa_execute_multiple_adb_shell_commands(
            [f'cat "/sdcard/Download/{newest_archive}"']
        )
    ).replace(b"\r\n", b"\n")
    return htmlcode


def download_data(
    link="https://www.bet365.com/#/AC/B1/C1/D1002/E88369731/G40/",
    deviceindex=5,
    timeout=60,
):

    devices.iloc[deviceindex].bb_adbtools.aa_open_website(link)

    wait_for_element_and_click(
        fu=lambda uia: uia.bb_content_desc == "More options",
        deviceindex=deviceindex,
        timeout=timeout,
    )
    wait_for_element_and_click(
        fu=lambda uia: uia.bb_content_desc == "Download",
        deviceindex=deviceindex,
        timeout=timeout,
    )
    wait_for_element_and_click(
        fu=lambda uia: uia.bb_resource_id == "com.android.chrome:id/positive_button",
        deviceindex=deviceindex,
        timeout=timeout,
    )
    wait_for_element_and_click(
        fu=lambda uia: (uia.bb_class == "android.widget.Button") & (uia.bb_text == "Open"),
        deviceindex=deviceindex,
        timeout=timeout,
        click=False,
    )

    htmlcode = get_mhtml_file(deviceindex)

    df = pd.Q_bs4_to_df_lite(htmlcode, parser="lxml")

    teams = (
        df.loc[df.aa_value == "rcl-ParticipantFixtureDetails_TeamNames"]
        .ds_apply_ignore(
            [pd.NA, pd.NA],
            lambda x: [
                LatinFix(x.aa_contents[0].text).apply_wrong_chars(),
                LatinFix(x.aa_contents[1].text).apply_wrong_chars(),
            ],
            axis=1,
            result_type="expand",
        )
        .rename(columns={0: "team1", 1: "team2"})
        .reset_index(drop=True)
    )

    bookcloses_cat = (
        df.loc[df.aa_value == "rcl-ParticipantFixtureDetails_Details"]
        .ds_apply_ignore(
            [
                pd.NA,
                pd.NA,
            ],
            lambda x: [y.text for y in x.aa_contents][:2],
            axis=1,
            result_type="expand",
        )
        .rename(columns={0: "book_closes", 1: "category_type"})
        .reset_index(drop=True)
    )
    betdata = pd.DataFrame(
        (
            df.loc[
                (df.aa_name == "span") & (df.aa_value == "sgl-ParticipantOddsOnly80_Odds")
            ].ds_apply_ignore(pd.NA, lambda x: float(x.aa_contents[0].text), axis=1)
        )
        .__array__()
        .reshape((3, len(teams)))
        .T,
        columns=["bet_1", "bet_x", "bet_2"],
    )
    return pd.concat([teams, bookcloses_cat, betdata], axis=1)



serie_a = download_data(
    link="https://www.bet365.com/#/AC/B1/C1/D1002/E88369731/G40/",
    deviceindex=5,
    timeout=60,
)
print(serie_a)
serie_b = download_data(
    link="https://www.bet365.com/#/AC/B1/C1/D1002/E88638566/G40/",
    deviceindex=5,
    timeout=60,
)
print(serie_b)