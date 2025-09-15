
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

st.title("Math Performance Correlation Dashboard")

# Load data
df = pd.read_csv("StudentPerformance.csv")
df.columns = df.columns.str.strip()

# Compute Math Average
df_math = df[[col for col in df.columns if col.startswith("Math")]]
df_math = df_math.apply(pd.to_numeric, errors='coerce')
df['Math_Avg'] = df_math.mean(axis=1)

# Select relevant columns
cols = ['Math_Avg',
        'PreACT Composite Percentile PreACT',
        'PreACT Math Percentile PreACT',
        'PSAT Percentile Total',
        'PSAT Math Percentile']

data = df[cols].dropna()
data.columns = ['Math_Avg', 'PreACT_Composite', 'PreACT_Math', 'PSAT_Total', 'PSAT_Math']

# Filters
st.sidebar.header("Filters")
math_range = st.sidebar.slider("Math Average Range", float(data['Math_Avg'].min()), float(data['Math_Avg'].max()), (float(data['Math_Avg'].min()), float(data['Math_Avg'].max())))
preact_comp_range = st.sidebar.slider("PreACT Composite Percentile Range", float(data['PreACT_Composite'].min()), float(data['PreACT_Composite'].max()), (float(data['PreACT_Composite'].min()), float(data['PreACT_Composite'].max())))
preact_math_range = st.sidebar.slider("PreACT Math Percentile Range", float(data['PreACT_Math'].min()), float(data['PreACT_Math'].max()), (float(data['PreACT_Math'].min()), float(data['PreACT_Math'].max())))
psat_total_range = st.sidebar.slider("PSAT Total Percentile Range", float(data['PSAT_Total'].min()), float(data['PSAT_Total'].max()), (float(data['PSAT_Total'].min()), float(data['PSAT_Total'].max())))
psat_math_range = st.sidebar.slider("PSAT Math Percentile Range", float(data['PSAT_Math'].min()), float(data['PSAT_Math'].max()), (float(data['PSAT_Math'].min()), float(data['PSAT_Math'].max())))

# Apply filters
filtered_data = data[
    (data['Math_Avg'] >= math_range[0]) & (data['Math_Avg'] <= math_range[1]) &
    (data['PreACT_Composite'] >= preact_comp_range[0]) & (data['PreACT_Composite'] <= preact_comp_range[1]) &
    (data['PreACT_Math'] >= preact_math_range[0]) & (data['PreACT_Math'] <= preact_math_range[1]) &
    (data['PSAT_Total'] >= psat_total_range[0]) & (data['PSAT_Total'] <= psat_total_range[1]) &
    (data['PSAT_Math'] >= psat_math_range[0]) & (data['PSAT_Math'] <= psat_math_range[1])
]

# Correlation heatmap
st.subheader("Correlation Heatmap")
corr_matrix = filtered_data.corr()
fig = ff.create_annotated_heatmap(
    z=corr_matrix.values,
    x=corr_matrix.columns.tolist(),
    y=corr_matrix.index.tolist(),
    colorscale='Viridis',
    showscale=True
)
st.plotly_chart(fig)

# Scatter plots
st.subheader("Scatter Plots with Regression Lines")
for col in ['PreACT_Composite', 'PreACT_Math', 'PSAT_Total', 'PSAT_Math']:
    fig = px.scatter(filtered_data, x=col, y='Math_Avg', trendline="ols",
                     title=f"Math Average vs {col}")
    st.plotly_chart(fig)
