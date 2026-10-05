import os

os.makedirs("visualizations", exist_ok=True)

print("Folder ready")

import matplotlib.pyplot as plt

# Calculate return rate by payment method
return_rate = (
    orders_clean.groupby("payment_method")["returned"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)

print(return_rate)

plt.figure(figsize=(8, 5))

bars = plt.bar(
    return_rate.index,
    return_rate.values
)

# Add exact percentage labels
for bar, rate in zip(bars, return_rate.values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{rate:.1f}%",
        ha="center",
        va="bottom"
    )

plt.xlabel("Payment Method")
plt.ylabel("Return Rate (%)")
plt.title("COD Returns at 44.4% — 3x Card")

plt.tight_layout()

plt.savefig(
    "visualizations/return_rate_by_payment.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

import os

os.makedirs("visualizations", exist_ok=True)

import matplotlib.pyplot as plt

# Use the outlier-corrected monthly revenue from Task 10
months = monthly_corrected.index.astype(str)
revenue = monthly_corrected.values

# Find the actual peak month
peak_month = monthly_corrected.idxmax()
peak_revenue = monthly_corrected.max()

# Create line chart
plt.figure(figsize=(9, 5))

plt.plot(
    months,
    revenue,
    marker="o"
)

# Add exact revenue labels
for month, value in zip(months, revenue):
    plt.text(
        month,
        value,
        f"₹{value:,.2f}",
        ha="center",
        va="bottom"
    )

plt.xlabel("Month")
plt.ylabel("Revenue (₹)")

plt.title(
    f"Outlier-Corrected Monthly Revenue — Peak: {peak_month}"
)

plt.xticks(rotation=45)

plt.tight_layout()

# Save the chart
plt.savefig(
    "visualizations/monthly_revenue_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print(f"Peak month: {peak_month}")
print(f"Peak revenue: ₹{peak_revenue:,.2f}")

import os

print(os.listdir("visualizations"))

from google.colab import files

files.download("visualizations/return_rate_by_payment.png")
files.download("visualizations/monthly_revenue_trend.png")
