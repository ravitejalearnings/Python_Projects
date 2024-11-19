import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def display_data_info(df):
    st.write("----")
    st.write("### View Sample Data")
    st.write(df.head())
    st.write("----")
    st.write("### Data Characteristics")
    st.write(f"- **Number of Rows**: {df.shape[0]}")
    st.write(f"- **Number of Columns**: {df.shape[1]}")
    st.write(f"- **Is duplicated**: {df.duplicated().sum()}")
    st.write(f"- **Column Names**: {df.columns.tolist()}")
    st.write("----")

    # columns datatype
    st.write("### Data Types:")
    datatype_df = pd.DataFrame(df.dtypes).reset_index()
    datatype_df.rename(columns={'index': 'Column_name', 0: 'dtypes'}, inplace=True)
    st.write(datatype_df)
    st.write("----")

    # Check of Null values
    st.write("### Check for nulls:")
    isnull_df = pd.DataFrame(df.isnull().sum()).reset_index()
    isnull_df.rename(columns={'index': 'Column_name', 0: 'Null count'}, inplace=True)
    isnull_df['Null Perc'] = round((isnull_df['Null count'] * 100 / df.shape[0]),2)
    st.write(isnull_df)
    st.write("----")

    # Check of Memory Usage
    st.write("### Memory Usage:")
    Memory_usage_df = pd.DataFrame(df.memory_usage()).reset_index()
    Memory_usage_df.rename(columns={'index': 'Column_name', 0: 'Memory Usage'}, inplace=True)
    st.write(Memory_usage_df)
    st.write("----")

    # Check for Duplicate Records
    st.write("### Check for duplicates records:")
    st.write(df[df.duplicated()])
    st.write(f"Number of Duplicate Records: {df.duplicated().sum()}")
    st.write("----")

    # Status for Numerical Features
    st.write("### Statistical Information for Continuous variables:")
    st.write(df.describe(include=['float64','int64','int32']).round(0))
    st.write("----")

    # Status for Categorical Features
    st.write("### Statistical Information for Categorical variables:")
    st.write(df.describe(include='object').loc[['unique','count']])
    st.write("----")

    # Distribution plots
    numerical_cols = df.select_dtypes(include='number').columns
    st.write("### Distribution of Numerical Columns")
    len_cols = len(numerical_cols)
    ncols = 3
    nrows = (len_cols // ncols)+1 if len_cols >=2 else 0
    figplotsize = (16, 4) if len(df[numerical_cols].columns) <= 10 else (20, 25)

    fig1, axes = plt.subplots(nrows, ncols, figsize=figplotsize)
    axes = axes.flatten()
    for ax, col in zip(axes, numerical_cols):
        sns.histplot(data=df, x=col, kde=True, ax=ax)
        ax.set_title(f"Distribution of {col}")

    for ax in axes[len(numerical_cols):]:
        ax.set_visible(False)
    plt.tight_layout()
    st.pyplot(fig1)
    st.write("----")

    # Distribution plots
    categorical_cols = df.select_dtypes(include='object').columns
    st.write("### Distribution of Categorical Columns")
    len_cols = len(categorical_cols)
    ncols = 3 if len_cols >= 2 else 2
    nrows = (len_cols // ncols) + 1 if len_cols >= 2 else 0
    figplotsize = (16, 4) if len(df[categorical_cols].columns) <= 10 else (20, 20)
    fig2, axes = plt.subplots(nrows, ncols, figsize=figplotsize)
    axes = axes.flatten()
    for ax, col in zip(axes, categorical_cols):
        sns.histplot(data=df, x=col, kde=True, ax=ax)
        ax.set_title(f"Distribution of {col}")
    for ax in axes[len(categorical_cols):]:
        ax.set_visible(False)
    plt.tight_layout()
    st.pyplot(fig2)
    st.write("----")

    # Correlation Matrix
    figplotsize = (16, 4) if len(df.columns) <= 10 else (20, 20)
    fig3 = plt.figure(figsize=figplotsize)
    df1 = df.select_dtypes(include='number')
    st.write("### Correlation Matrix")
    cm = df1.corr()
    sns.heatmap(data=cm, annot=True)
    plt.tight_layout()
    st.pyplot(fig3)
    st.write("----")

    # Covariance Matrix
    figplotsize = (16, 4) if len(df.columns) <= 10 else (20, 20)
    fig3 = plt.figure(figsize=figplotsize)
    df1 = df.select_dtypes(include='number')
    st.write("### Covariance Matrix")
    cm = df1.cov()
    sns.heatmap(data=cm, annot=True)
    plt.tight_layout()
    st.pyplot(fig3)
    st.write("----")

    # Outlier detection
    numerical_cols = df.select_dtypes(include='number').columns
    st.write("### Box Plots for Outlier Detection")
    len_cols = len(numerical_cols)
    ncols = 3 if len_cols >= 2 else 2
    nrows = (len_cols // ncols) + 1 if len_cols >= 2 else 0
    figplotsize = (16, 4) if len(df[numerical_cols].columns) <= 10 else (20, 20)
    fig4, axes = plt.subplots(nrows, ncols, figsize=figplotsize)
    axes = axes.flatten()
    for ax, col in zip(axes, numerical_cols):
        sns.boxplot(data=df, y=col, ax=ax)
        ax.set_title(f"{col}")
    for ax in axes[len(numerical_cols):]:
        ax.set_visible(False)
    plt.tight_layout()
    st.pyplot(fig4)
    st.write("----")

    # Skewness and Kurtosis
    st.write("### Skewness and Kurtosis for Numerical Columns")
    skew_kurt_df = pd.DataFrame({
        "Skewness": df[numerical_cols].skew(),
        "Kurtosis": df[numerical_cols].kurt()
    }).reset_index().rename(columns={"index": "Column"})
    st.write(skew_kurt_df)

    st.write("### Missing Data Heatmap")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(df.isnull(), cbar=False, cmap="viridis", ax=ax)
    st.pyplot(fig)