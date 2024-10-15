import yfinance as yf
import pandas as pd

companies_wikipedia: str = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

class Symbol:
    def __init__(
            self,
    ) -> None:
        ...

    def get_standard_and_poors(self) -> list[str]:
        df: pd.DataFrame = pd.read_html(companies_wikipedia)[0]
        return df['Symbol'].tolist()
