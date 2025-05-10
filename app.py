import streamlit as st
import pandas as pd
import matplotlib .pyplot as plt



st.set_page_config(page_title="Pakistan E-Commerce Data Analysis", layout="wide")


@st.cache_data
def load_data():
  file_path = "data/cleaned_Pakistan_data.csv"

    return pd.read_csv(file_path, encoding='iso-8859-1')

df = load_data()


st.title("Pakistan E-Commerce Data Analysis")
st.markdown("""
The dataset has already been uploaded automatically.  
From this point on, we will begin analyzing the data to uncover valuable insights and identify key trends and patterns.
""")

col1, col2, col3 = st.columns(3)
col4, col5, _ = st.columns(3)

with col1:
    st.metric(label="💰 Total Revenue", value="1,237,970,009 PKR")

with col2:
    st.metric(label="📦 Number of Orders", value="268,420")

with col3:
    st.metric(label="💵 Average Order Value (AOV)", value="6,469 PKR")

with col4:
    st.metric(label="👥 Unique Customers", value="55,451")

with col5:
    st.metric(label="📈 Average Revenue per Customer", value="22,325 PKR")


st.dataframe(df.head(20))



# --- גרף Top 10 Payment Methods ---
st.subheader("💳 Top 10 Payment Methods")
top_methods = df['payment_method'].value_counts().head(10)

fig, ax = plt.subplots(figsize=(10, 6))
top_methods.plot(kind='bar', color='blue', ax=ax)
ax.set_title('Top 10 Payment Methods')
ax.set_xlabel('Payment Method')
ax.set_ylabel('Number of Transactions')
ax.set_xticklabels(top_methods.index, rotation=45)
ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

st.markdown("""
**Explanation:**  
This chart shows the 10 most commonly used payment methods in the dataset.  
It helps to understand customer preferences when completing transactions.
""")

# --- גרף Sales by Product Category ---
st.subheader("🛍️ Sales by Product Category")
df = df.dropna(subset=['category_name_1', 'new_grand_total'])
df['new_grand_total'] = pd.to_numeric(df['new_grand_total'], errors='coerce')
sales_by_category = df.groupby('category_name_1')['new_grand_total'].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(sales_by_category.index, sales_by_category.values, color='lightblue')
ax.set_title('Sales by Product Category')
ax.set_xlabel('Product Category')
ax.set_ylabel('Total Sales (PKR)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig)

st.markdown("""
**Explanation:**  
This chart shows the total revenue generated from each product category based on the 'NEW GRAND TOTAL'.  
It helps identify which product types are driving the most revenue.
""")

# --- גרף Monthly Orders Trend ---
df = df.dropna(subset=['Working Date', 'qty_ordered'])
df['Working Date'] = pd.to_datetime(df['Working Date'], errors='coerce')
df['qty_ordered'] = pd.to_numeric(df['qty_ordered'], errors='coerce')
df = df.dropna(subset=['Working Date', 'qty_ordered'])
df['Month'] = df['Working Date'].dt.to_period('M').astype(str)
monthly_orders = df.groupby('Month')['qty_ordered'].sum().reset_index()

st.subheader("📦 Monthly Orders Trend")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(monthly_orders['Month'], monthly_orders['qty_ordered'], marker='o', color='red')
ax.set_title('Monthly Orders Trend')
ax.set_xlabel('Month')
ax.set_ylabel('Total Quantity Ordered')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
st.pyplot(fig)

st.markdown("""
**Explanation:**  
This line chart displays how the total number of items ordered changes month by month.  
It helps track demand trends over time.
""")

# --- סיכום מדדים ---
st.markdown("""
## **Key Business Metrics:**
- **Total Revenue:** PKR 1,237,970,009  
- **Number of Orders:** 268,420  
- **Average Order Value (AOV):** PKR 6,469  
- **Unique Customers:** 55,451  
- **Average Revenue per Customer:** PKR 22,325  
""")

# --- תובנות והמלצות ---
st.markdown("""
## **Key Insights:**

1. **Top Payment Methods**  
   - The most frequently used payment methods are clearly highlighted, with one or two dominating the transaction volume.  
   - This suggests customers trust and prefer these methods, making them essential to maintain and optimize.

2. **Sales by Product Category**  
   - Certain product categories significantly outperform others in terms of total sales.  
   - These categories represent high-demand areas and are crucial to business growth.

3. **Monthly Sales Trend**  
   - A clear seasonality is observed with sales peaking in specific months.  
   - This pattern may reflect marketing campaigns, holidays, or customer buying behavior.

## **Business Recommendations:**

1. **Enhance Preferred Payment Methods**  
   - Ensure the most used payment methods are reliable, visible, and easy to use.  
   - Consider offering discounts or loyalty points for using preferred methods.

2. **Focus on High-Selling Categories**  
   - Allocate more inventory and marketing resources to top-performing product categories.  
   - Consider expanding product lines in those categories to meet growing demand.

3. **Prepare for Sales Seasonality**  
   - Use the monthly trend data to prepare inventory and marketing ahead of peak periods.  
   - Launch targeted campaigns in months with traditionally low sales.

4. **Increase AOV & Customer Retention**  
   - Upsell and cross-sell related products to increase order value.  
   - Introduce customer loyalty programs or discounts for repeat purchases.

5. **Monitor Customer Metrics**  
   - Use the number of unique customers and revenue per customer as KPIs for growth.  
   - Analyze behavior of top customers to replicate success.
""")
