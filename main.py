
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import datetime

from datetime import datetime, date, timedelta
# from format import format
from blackScholes import BlackScholes
from qbstyles import mpl_style


st.set_page_config(page_title="Black-Scholes",
                   page_icon="📈", layout="wide") 

# format()
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

st.title("📈 Black Scholes Option Pricer")

with st.sidebar:
    st.write("Author:")
    github_url = "https://ismaeldjimenez.github.io"
    st.markdown(f'<a href="{github_url}" target="_blank" style="text-decoration: none; color: inherit;"><i class="fi fi-brands-github" width="25" height="25" style="vertical-align: middle; margin-right: 10px;"></i>`Ismael Jimenez`</a>', unsafe_allow_html=True)
    # st.markdown(f'<a href="{github_url}" target="_blank" style="text-decoration: none; color: inherit;"> <img class="fi fi-brands-github" src="https://cdn-uicons.flaticon.com/2.6.0/uicons-brands/css/uicons-brands.css/" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Ismael Jimenez`</a>', unsafe_allow_html=True)
    linkedin_url = "https://www.linkedin.com/in/ismael-jimenez-nyu-data"
    st.markdown(f'<a href="{linkedin_url}" target="_blank" style="text-decoration: none; color: inherit;"><img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="25" height="25" style="vertical-align: middle; margin-right: 10px;">`Ismael Jimenez`</a>', unsafe_allow_html=True)

    st.subheader("Option Details")
    excercise_style = st.selectbox("Excercise Style", ['European', 'American'])
    spot_price = st.number_input("Spot/Current Asset Price (S)", value=90.00)
    strike_price = st.number_input("Strike/Exercise Price (X)", value=100.00)

    today = date.today()
    default_date_tomorrow = today + timedelta(days=30)
    settlement_date = st.date_input("Settlement Date", format="YYYY-MM-DD")
    str_settlement_date = str(settlement_date)
    expiration_date = st.date_input("Expiration Date", format="YYYY-MM-DD", value= default_date_tomorrow)
    str_expiration_date = str(expiration_date)

    risk_free_rate = st.number_input("Risk-Free Interest Rate (r)", value=0.04)
    dividend_rate = st.number_input("Dividend Rate (d)")
    call_sigma = st.number_input("Call Volatility (\u03C3c)", value=0.25)
    put_sigma = st.number_input("Put Volatility (\u03C3p)", value=0.25)

    st.divider()

    st.subheader("Volatility Heatmap")
    spot_min = st.number_input("Min Spot Price", value=max(spot_price-10, 0))
    spot_max = st.number_input("Max Spot Price", value=spot_price+10)
    call_sigma_min = st.slider("Call Min Volatility for Heatmap", min_value=0.0, max_value=1.0, value=max(call_sigma-0.1,0.0), step= 0.01)
    call_sigma_max = st.slider("Call Max Volatility for Heatmap", min_value=0.0, max_value=1.0, value=min(call_sigma+0.1,1.0), step= 0.01)
    put_sigma_min = st.slider("Put Min Volatility for Heatmap", min_value=0.0, max_value=1.0, value=max(put_sigma-0.1,0.0), step= 0.01)
    put_sigma_max = st.slider("Put Max Volatility for Heatmap", min_value=0.0, max_value=1.0, value=min(put_sigma+0.1,1.0), step= 0.01)

# Calculate the difference in days and convert it to years
settlement_date = datetime.combine(settlement_date, datetime.min.time())
expiration_date = datetime.combine(expiration_date, datetime.min.time())
date_difference = (expiration_date - settlement_date).days
time_to_mature = round(date_difference / 365.25, 3)


spot_price_col, strike_price_col, time_to_mature_col, interest_rate_col, dividend_col, call_vol_col, put_vol_col = st.columns([1,1,1,1,1,1,1])

with spot_price_col:
    with st.container():
        st.markdown(f'<p class="price_text">Spot Price (S)<br></p><p class="price_details">${spot_price}</p>', unsafe_allow_html = True)
with strike_price_col:
    with st.container():
        st.markdown(f'<p class="price_text">Strike Price (X)<br></p><p class="price_details">${strike_price}</p>', unsafe_allow_html = True)
with time_to_mature_col:
    with st.container():
        st.markdown(f'<p class="rate_text">Tenor in years (t)<br></p><p class="price_details">{time_to_mature}</p>', unsafe_allow_html = True)

with interest_rate_col:
    with st.container():
        st.markdown(f'<p class="rate_text">Risk-Free Interest Rate (r)<br></p><p class="price_details">{risk_free_rate}</p>', unsafe_allow_html = True)

with dividend_col:
    with st.container():
        st.markdown(f'<p class="rate_text">Dividend Rate (d)<br></p><p class="price_details">{dividend_rate}</p>', unsafe_allow_html = True)

with call_vol_col:
    with st.container():
        st.markdown(f'<p class="call_vol_text">Call Implied Volatility (\u03C3c)<br></p><p class="price_details">{call_sigma}</p>', unsafe_allow_html = True)

with put_vol_col:
    with st.container():
        st.markdown(f'<p class="put_vol_text">Put Implied Volatility (\u03C3p)<br></p><p class="price_details">{put_sigma}</p>', unsafe_allow_html = True)


# pd.options.display.float_format = "{:,.2f}".format
# df = pd.DataFrame([['$'+' '+str(spot_price),'$' + str(strike_price),time_to_mature,risk_free_rate, dividend_rate, call_sigma, put_sigma]], 
#     columns=(
#     "Spot Price (S)", 
#     "Exercise Price (X)",
#     "Time to Maturity in Years (t)",
#     "Risk-Free Interest Rate (r)",
#     "Dividend Rate (d)",
#     "Call Implied Volatility (\u03C3c)",
#     "Put Implied Volatility (\u03C3p)"))
# df.style.format(precision=2) 
# st.dataframe(df.style.format("{:.2%}"))
# st.table(df)        
# df.reset_index(drop=True, inplace=True)
# st.write((df))

col1, col2 = st.columns(2)

bs = BlackScholes()
spotPrices = np.round(np.linspace(spot_min,spot_max, 9), 2)
call_volatilities = np.round(np.linspace(call_sigma_min,call_sigma_max, 9), 2)
put_volatilities = np.round(np.linspace(put_sigma_min,put_sigma_max, 9), 2)


#CALL
call_bs_price, call_eu_prices, call_am_prices = bs.get_bs_price('call', str_settlement_date, str_expiration_date,
                              spot_price, strike_price, call_sigma,
                              risk_free_rate, dividend_rate)
steps = np.linspace(5, 200, 195)
# call_prices = pd.DataFrame(np.array([steps, call_eu_prices, call_am_prices]).T, columns=['steps','eu','am'])
# st.write(call_prices)
# sns.set_style("darkgrid")


with col1:
    # Using the custom class for CALL value
    st.markdown(f"""
        <div class="metric-container metric-call">
            <div>
                <div class="metric-label">CALL Value</div>
                <div class="metric-value">${call_bs_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

col1.divider()
# plt.style.use('dark_background') 
mpl_style(dark=True, minor_ticks=False,)
fig0, ax0 = plt.subplots()

ax0.set_title('Black Scholes Call Option Price')
ax0.set_xlabel('Binomial Steps')
ax0.set_ylabel('Option Price')
# ax0.set_xlim([steps[0], steps[-1]])
# ax0.set_ylim()
ax0 = plt.plot(steps, call_eu_prices, color='g', label= 'Binomial') if excercise_style == 'European' else plt.plot(range(5,200), call_am_prices, color='g', label=' Binomial')
ax0 = plt.axhline(y=call_bs_price, color='b', linestyle='--', label='Black Scholes')
ax0 = plt.legend()
# ax0 = sns.lineplot(data=call_prices, x='steps', y='eu')
# ax0 = plt.axis('off')
col1.pyplot(fig0)

col1.divider()

col1.subheader("Call Volatility-Price Heatmap")
call_grid = np.empty((len(call_volatilities),len(spotPrices)))
for i, vol in enumerate(call_volatilities):
    for j, spot in enumerate(spotPrices):
        call_grid[i][j] = bs.get_bs_price('call', str_settlement_date, str_expiration_date,
                              spot, strike_price, vol,
                              risk_free_rate, dividend_rate, binomial=False)


fig1, ax1 = plt.subplots()
ax1 = sns.heatmap(call_grid, annot=True, cmap='RdYlGn_r', fmt=".2f",
            xticklabels=spotPrices, yticklabels=call_volatilities,cbar=False)
ax1.set(xlabel="Spot Prices (S)", ylabel="Volatilities (\u03C3c)")

ax1.set_title("CALL")
col1.pyplot(fig1)


# PUT
put_bs_price, put_eu_prices, put_am_prices = bs.get_bs_price('put', str_settlement_date, str_expiration_date,
                              spot_price, strike_price, put_sigma,
                              risk_free_rate, dividend_rate)
with col2:
    # Using the custom class for PUT value
    st.markdown(f"""
        <div class="metric-container metric-put">
            <div>
                <div class="metric-label">PUT Value</div>
                <div class="metric-value">${put_bs_price:.2f}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

col2.divider()

fig2, ax2 = plt.subplots()
ax2.set_title('Black Scholes Put Option Price')
ax2.set_xlabel('Binomial Steps')
ax2.set_ylabel('Option Price')
ax2 = plt.plot(steps, put_eu_prices, label='Binomial') if excercise_style == 'European' else plt.plot(steps, put_am_prices, label='Binomial')
ax2 = plt.axhline(y=put_bs_price, color='b', linestyle='--', label='Black Scholes')
ax2 = plt.legend()
# ax0 = sns.lineplot(data=call_prices, x='steps', y='eu')
col2.pyplot(fig2)

col2.divider()

col2.subheader("Put Volatitily-Price Heatmap")

put_grid = np.empty((len(put_volatilities),len(spotPrices)))
for i, vol in enumerate(put_volatilities):
    for j, spot in enumerate(spotPrices):
        put_grid[i][j] = bs.get_bs_price('put', str_settlement_date, str_expiration_date,
                              spot, strike_price, vol,
                              risk_free_rate, dividend_rate, binomial=False)

fig3, ax3 = plt.subplots()
ax3 = sns.heatmap(put_grid, annot=True, cmap='RdYlGn_r', fmt=".2f",
            xticklabels=spotPrices, yticklabels=put_volatilities, cbar=False)
ax3.set(xlabel="Spot Prices (S)", ylabel="Volatilities (\u03C3p)")
ax3.set_title("PUT")
col2.pyplot(fig3)