#!/usr/bin/env python3

import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# SETTINGS
# ============================================================

STRC_TICKER = "STRC"
MSTR_TICKER = "MSTR"
BTC_TICKER = "BTC-USD"

TARGET_PRICE = 100.00
DEFAULT_LOWER_BOUND = 95.00

VOLATILITY_WINDOW = 20


# ============================================================
# DOWNLOAD PRICE HISTORY
# ============================================================

def get_history(ticker):
    df = yf.Ticker(ticker).history(
        period="max",
        interval="1d",
        auto_adjust=False
    )

    if df.empty:
        raise RuntimeError(f"No data returned for {ticker}")

    df = df.dropna(subset=["Close"]).copy()

    # Remove timezone information for easier comparison
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)

    df.index = df.index.normalize()

    return df


# ============================================================
# ASK USER FOR LOWER BOUND
# ============================================================

print("=" * 60)
print("STRC Historical Closing Price Analysis")
print("=" * 60)

lower_input = input(
    f"\nEnter lower bound "
    f"[press Enter for ${DEFAULT_LOWER_BOUND:.2f}]: "
).strip()

if lower_input == "":
    lower_bound = DEFAULT_LOWER_BOUND
else:
    try:
        lower_bound = float(lower_input)
    except ValueError:
        print(
            f"Invalid input. Using default "
            f"${DEFAULT_LOWER_BOUND:.2f}."
        )
        lower_bound = DEFAULT_LOWER_BOUND


range_name = (
    f"${TARGET_PRICE:.0f} - ${lower_bound:.0f} target range"
)


# ============================================================
# DOWNLOAD STRC
# ============================================================

print("\nDownloading STRC price history...")

strc = get_history(STRC_TICKER)
close = strc["Close"]

first_date = close.index[0]
last_date = close.index[-1]

first_close = close.iloc[0]
latest_close = close.iloc[-1]

total_days = len(close)


# ============================================================
# TARGET RANGE
# ============================================================

# Anything at or above the selected lower bound counts
# as within the target range.
#
# Prices slightly above $100 are also included.

within_target = close >= lower_bound
outside_target = close < lower_bound

within_days = int(within_target.sum())
outside_days = int(outside_target.sum())

within_pct = within_days / total_days * 100
outside_pct = outside_days / total_days * 100


# ============================================================
# PRICE STATISTICS
# ============================================================

highest_close = close.max()
highest_date = close.idxmax()

lowest_close = close.min()
lowest_date = close.idxmin()

average_close = close.mean()

average_distance = (
    close - TARGET_PRICE
).abs().mean()


# ============================================================
# FIND LONGEST CONSECUTIVE PERIOD BELOW LOWER BOUND
# ============================================================

below = close < lower_bound

excursions = []

start_position = None

for i in range(len(close)):

    if below.iloc[i] and start_position is None:
        start_position = i

    elif not below.iloc[i] and start_position is not None:

        end_position = i - 1
        recovery_position = i

        excursion_prices = close.iloc[
            start_position:end_position + 1
        ]

        excursions.append({
            "start": start_position,
            "end": end_position,
            "recovery": recovery_position,
            "days": end_position - start_position + 1,
            "lowest_price": excursion_prices.min(),
            "lowest_date": excursion_prices.idxmin(),
            "recovered": True
        })

        start_position = None


# Handle an excursion still underway
if start_position is not None:

    end_position = len(close) - 1

    excursion_prices = close.iloc[
        start_position:end_position + 1
    ]

    excursions.append({
        "start": start_position,
        "end": end_position,
        "recovery": None,
        "days": end_position - start_position + 1,
        "lowest_price": excursion_prices.min(),
        "lowest_date": excursion_prices.idxmin(),
        "recovered": False
    })


if excursions:

    longest = max(
        excursions,
        key=lambda x: x["days"]
    )

else:
    longest = None


# ============================================================
# CLEAN REPORT
# ============================================================

print("\n")
print("=" * 60)
print("STRC HISTORICAL CLOSING PRICE ANALYSIS")
print("=" * 60)

print(f"\nTarget range: {range_name}")

print(
    f"Prices above ${TARGET_PRICE:.0f} are included "
    f"as within the target range."
)


print("\nDATA")
print("-" * 60)

print(f"First trading day:  {first_date.date()}")
print(f"Latest trading day: {last_date.date()}")
print(f"Total trading days: {total_days:,}")


print(f"\n{range_name.upper()}")
print("-" * 60)

print(
    f"Days within {range_name}: "
    f"{within_days:,} ({within_pct:.2f}%)"
)

print(
    f"Days outside {range_name}: "
    f"{outside_days:,} ({outside_pct:.2f}%)"
)


print("\nPRICE EXTREMES")
print("-" * 60)

print(
    f"Highest closing price: "
    f"${highest_close:.2f} "
    f"on {highest_date.date()}"
)

print(
    f"Lowest closing price:  "
    f"${lowest_close:.2f} "
    f"on {lowest_date.date()}"
)


print("\nAVERAGES")
print("-" * 60)

print(
    f"Average closing price:      "
    f"${average_close:.2f}"
)

print(
    f"Average distance from $100: "
    f"${average_distance:.2f}"
)


print("\nLONGEST PERIOD OUTSIDE TARGET RANGE")
print("-" * 60)

if longest is None:

    print(
        f"STRC has never closed below "
        f"${lower_bound:.2f}."
    )

else:

    start_date = close.index[longest["start"]]
    end_date = close.index[longest["end"]]

    print(
        f"Longest consecutive period below "
        f"${lower_bound:.2f}: {longest['days']} trading days"
    )

    print(
        f"Period: {start_date.date()} "
        f"to {end_date.date()}"
    )

    print(
        f"Lowest close during period: "
        f"${longest['lowest_price']:.2f} "
        f"on {longest['lowest_date'].date()}"
    )

    if longest["recovered"]:

        recovery_date = close.index[
            longest["recovery"]
        ]

        recovery_close = close.iloc[
            longest["recovery"]
        ]

        print(
            f"Recovered into target range: "
            f"{recovery_date.date()} "
            f"at ${recovery_close:.2f}"
        )

    else:

        print(
            "Status: Still outside target range"
        )


print("\nFIRST / LATEST CLOSE")
print("-" * 60)

print(
    f"First close:  "
    f"${first_close:.2f} "
    f"on {first_date.date()}"
)

print(
    f"Latest close: "
    f"${latest_close:.2f} "
    f"on {last_date.date()}"
)

print("\n" + "=" * 60)


# ============================================================
# DOWNLOAD MSTR AND BTC FOR CHART ONLY
# ============================================================

print("\nGenerating STRC / MSTR / BTC comparison chart...")

mstr = get_history(MSTR_TICKER)
btc = get_history(BTC_TICKER)


# Only use the period that STRC has existed
mstr = mstr[
    (mstr.index >= first_date) &
    (mstr.index <= last_date)
]

btc = btc[
    (btc.index >= first_date) &
    (btc.index <= last_date)
]


# ============================================================
# NORMALISED PRICE
#
# Each asset starts at 100.
#
# 120 = up 20%
# 80  = down 20%
# ============================================================

strc_indexed = (
    close / close.iloc[0] * 100
)

mstr_indexed = (
    mstr["Close"] /
    mstr["Close"].iloc[0] * 100
)

btc_indexed = (
    btc["Close"] /
    btc["Close"].iloc[0] * 100
)


# ============================================================
# 20-DAY ROLLING VOLATILITY
# ============================================================

strc_returns = close.pct_change(fill_method=None)

mstr_returns = mstr["Close"].pct_change(
    fill_method=None
)

btc_returns = btc["Close"].pct_change(
    fill_method=None
)


strc_vol = (
    strc_returns
    .rolling(VOLATILITY_WINDOW)
    .std()
    * np.sqrt(252)
    * 100
)

mstr_vol = (
    mstr_returns
    .rolling(VOLATILITY_WINDOW)
    .std()
    * np.sqrt(252)
    * 100
)

btc_vol = (
    btc_returns
    .rolling(VOLATILITY_WINDOW)
    .std()
    * np.sqrt(365)
    * 100
)


# ============================================================
# CHART
# ============================================================

fig, (ax1, ax2) = plt.subplots(
    2,
    1,
    figsize=(14, 10),
    sharex=True
)


# Normalised price chart
ax1.plot(
    strc_indexed.index,
    strc_indexed,
    label="STRC"
)

ax1.plot(
    mstr_indexed.index,
    mstr_indexed,
    label="MSTR"
)

ax1.plot(
    btc_indexed.index,
    btc_indexed,
    label="Bitcoin"
)

ax1.axhline(
    100,
    linestyle="--",
    alpha=0.5
)

ax1.set_title(
    "STRC vs MSTR vs Bitcoin — Since STRC Began Trading"
)

ax1.set_ylabel(
    "Indexed price (start = 100)"
)

ax1.legend()

ax1.grid(
    True,
    alpha=0.25
)


# Volatility chart
ax2.plot(
    strc_vol.index,
    strc_vol,
    label="STRC"
)

ax2.plot(
    mstr_vol.index,
    mstr_vol,
    label="MSTR"
)

ax2.plot(
    btc_vol.index,
    btc_vol,
    label="Bitcoin"
)

ax2.set_title(
    f"{VOLATILITY_WINDOW}-Day Rolling Annualised Volatility"
)

ax2.set_ylabel(
    "Volatility (%)"
)

ax2.set_xlabel(
    "Date"
)

ax2.legend()

ax2.grid(
    True,
    alpha=0.25
)


plt.tight_layout()

chart_filename = "STRC_MSTR_BTC_volatility.png"

plt.savefig(
    chart_filename,
    dpi=160,
    bbox_inches="tight"
)

plt.show()
