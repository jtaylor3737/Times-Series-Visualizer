import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import numpy as np

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")
# Clean data
df = df[
    (
        (df["value"] >= df["value"].quantile(0.025))
        & (df["value"] <= df["value"].quantile(0.975))
    )
]


def draw_line_plot():
    sns.set(font_scale=1)
    # Draw line plot
    fig, ax = plt.subplots()
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    sns.lineplot(data=df, legend=False)
    # Save image and return fig (don't change this part)
    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot():
    sns.set(font_scale=3)
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar["Years"] = df_bar.index.year
    df_bar["Months"] = df_bar.index.strftime("%B")
    month_order = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    df_bar = pd.DataFrame(
        df_bar.groupby(["Years", "Months"])["value"].mean().astype(int)
    )
    df_bar = df_bar.rename(columns={"value": "Average Page Views"})

    # Draw bar plot

    fig, ax = plt.subplots()
    ax.set_title("Daily freeCodeCamp Forum Average Page Views per Month")
    # Using seaborn for this will cause a unit test fail because of the higher child count. Oh well.

    sns.barplot(
        data=df_bar,
        x="Years",
        y="Average Page Views",
        hue="Months",
        hue_order=month_order,
        palette="Greens_d",
    )
    plt.legend(fontsize=20)
    fig.set_figheight(20)
    fig.set_figwidth(20)
    # Save image and return fig (don't change this part)
    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot():
    sns.set(font_scale=2)
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box["year"] = df_box.index.year
    df_box["month"] = df_box.index.strftime("%b")

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(2, 1)
    fig.set_figheight(20)
    fig.set_figwidth(20)

    # Yearly boxplot

    sns.boxplot(data=df_box, x="year", y="value", ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")
    axes[0].set_yticklabels(np.arange(0, 200001, step=20000))

    # Monthly boxplot
    month_order = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    sns.boxplot(data=df_box, x="month", y="value", order=month_order, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")
    axes[1].set_yticklabels(np.arange(0, 200001, step=20000))

    # Save image and return fig (don't change this part)
    fig.savefig("box_plot.png")
    return fig
