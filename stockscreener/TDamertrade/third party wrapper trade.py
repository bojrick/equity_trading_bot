# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import requests
import config
from tda import auth, client
import json
import pandas as pd

# %%
try:
    c = auth.client_from_token_file(config.token_path, config.api_key)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome(executable_path='C://Users//bojri//OneDrive//Desktop//Trading//stockscreener//TDamertrade//chromedriver.exe') as driver:
        c = auth.client_from_login_flow(
            driver, config.api_key, config.redirect_url, config.token_path)

r = c.get_price_history('AAPL',
        period_type=client.Client.PriceHistory.PeriodType.YEAR,
        period=client.Client.PriceHistory.Period.FIVE_DAYS,
        frequency_type=client.Client.PriceHistory.FrequencyType.DAILY,
        frequency=client.Client.PriceHistory.Frequency.DAILY)
        
#json.dumps(, indent=4))

# %%
oc = c.get_option_chain('BNGO',
                        contract_type=client.Client.Options.ContractType.CALL,
                        strike_count=10,
                        include_quotes=True,
                        strategy=client.Client.Options.Strategy.COVERED)


assert oc.status_code == 200, oc.raise_for_status()
print(oc.json().keys())#json.dumps(, indent=4))
print(oc.json()['underlying'])

temp_df = pd.DataFrame(oc.json()['monthlyStrategyList'][1]['optionStrategyList'])
print(pd.DataFrame.from_records(temp_df['primaryLeg'].values))


# %%
