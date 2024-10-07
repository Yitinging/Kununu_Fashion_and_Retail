import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from math import pi
# Read the data
df = pd.read_csv('kununu_competitors.csv')

# List of scores to calculate
columns_to_average = [
    'employer_atmosphere_score', 'employer_communication_score',
    'employer_teamwork_score', 'employer_work_life_score', 'employer_leadership_score',
    'employer_tasks_score', 'employer_equality_score', 'employer_old_colleagues_score',
    'employer_work_conditions_score', 'employer_environment_score', 
    'employer_salary_score', 'employer_image_score', 'employer_career_score'
]



# Remove 'employer_' and '_score' from the columns in the DataFrame
new_columns = {col: col.replace('employer_', '').replace('_score', '') for col in columns_to_average}
df.rename(columns=new_columns, inplace=True)


# Now columns_to_average uses the modified column names
columns_to_average_new = list(new_columns.values())

# Calculate the average scores for each company
grouped_df = df.groupby('company_name_short')[columns_to_average_new].mean().round(1).reset_index()
grouped_df['total_score'] = grouped_df[columns_to_average_new].mean(axis=1).round(1)
grouped_df.sort_values(by='total_score', ascending=False, inplace=True)

# Sidebar to select view option
view_option = st.sidebar.radio("Select View", ["Compare", "Ranking"])

if view_option == "Compare":
    # Dropdown to select a company for the radar chart
    selected_company = st.sidebar.selectbox("Select a company", grouped_df['company_name_short'])

    # Get data for the selected company and Hugo Boss
    company_data = grouped_df[grouped_df['company_name_short'] == selected_company].iloc[0]
    hugo_boss_data = grouped_df[grouped_df['company_name_short'] == 'Hugo Boss'].iloc[0]

    # Prepare data for radar chart
    categories = columns_to_average_new
    selected_company_values = company_data[columns_to_average_new].tolist()
    hugo_boss_values = hugo_boss_data[columns_to_average_new].tolist()

    # Add first value to close the radar chart
    selected_company_values += selected_company_values[:1]
    hugo_boss_values += hugo_boss_values[:1]
    categories += categories[:1]

    # Create radar chart
    fig = go.Figure()

    # Add selected company's data to radar chart
    fig.add_trace(go.Scatterpolar(
        r=selected_company_values,
        theta=categories,
        fill='toself',
        name=selected_company
    ))

    # Add Hugo Boss data to radar chart
    fig.add_trace(go.Scatterpolar(
        r=hugo_boss_values,
        theta=categories,
        fill='toself',
        name='Hugo Boss'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 5])
        ),
        showlegend=True,
        title=f"Radar Chart: {selected_company} vs Hugo Boss"
    )

# After the radar chart, let's add the new bar chart for significant differences

# Function to perform statistical tests and return significance
    def calculate_significance(df, company1, company2, columns):
        significate = []
        for score_col in columns:
            company1_scores = df[df['company_name_short'] == company1][score_col]
            company2_scores = df[df['company_name_short'] == company2][score_col]
            
            # Shapiro-Wilk Test for Normality
            stat1, p1 = stats.shapiro(company1_scores)
            stat2, p2 = stats.shapiro(company2_scores)
            
            alpha = 0.05
            if p1 > alpha and p2 > alpha:
                # Perform Independent T-Test
                t_stat, t_p_value = stats.ttest_ind(company1_scores, company2_scores)
                if t_p_value < alpha:
                    significate.append(True)
                else:
                    significate.append(False)
            else:
                # Mann-Whitney U Test for non-normal distributions
                u_stat, u_p_value = stats.mannwhitneyu(company1_scores, company2_scores)
                if u_p_value < alpha:
                    significate.append(True)
                else:
                    significate.append(False)
        
        return significate

    # Generate significance information
    significate = calculate_significance(df, selected_company, 'Hugo Boss', columns_to_average_new)

    # Bar chart visualization with red for significant and gray for non-significant
    bar_colors = ['red' if sig else 'gray' for sig in significate]
    score_diff =  hugo_boss_data[columns_to_average_new] - company_data[columns_to_average_new] 

    bar_fig = go.Figure(go.Bar(
        x=columns_to_average_new,
        y=score_diff,
        marker=dict(color=bar_colors)
    ))

    bar_fig.update_layout(
        title=f'Comparison of {selected_company} vs Hugo Boss (Red = Significant)',
        xaxis_title='Score Categories',
        yaxis_title='Mean Difference',
        xaxis_tickangle=-45
    )

    # Display the bar chart in Streamlit

    # Display radar chart and bar chart in Streamlit
    st.plotly_chart(fig)
    st.plotly_chart(bar_fig)

elif view_option == "Ranking":
    # Dropdown to select ranking dimension
    ranking_option = st.sidebar.selectbox("Select Ranking Dimension", columns_to_average_new + ['total_score'])

    # Sort companies by the selected ranking dimension
    sorted_df = grouped_df.sort_values(by=ranking_option, ascending=False)

    # Prepare data for horizontal bar chart
    x_values = sorted_df[ranking_option]
    y_values = sorted_df['company_name_short']

    # Highlight Hugo Boss
    colors = ['lightskyblue' if company != 'Hugo Boss' else 'indianred' for company in y_values]

    # Create horizontal bar chart
    ranking_fig = go.Figure(go.Bar(
        x=x_values,
        y=y_values,
        orientation='h',
        marker_color=colors
    ))

    ranking_fig.update_layout(
        title=f"Company Ranking: {ranking_option}",
        xaxis_title=f"{ranking_option} Score",
        yaxis_title="Company",
        yaxis=dict(autorange='reversed')  # Ensure highest score is on top
    )

    # Display ranking chart in Streamlit
    st.plotly_chart(ranking_fig)
    
    # Calculate Hugo Boss's rank across all score dimensions
    hugo_boss_rankings = grouped_df[columns_to_average_new + ['total_score']].rank(ascending=False)
    hugo_boss_rankings = hugo_boss_rankings[grouped_df['company_name_short'] == 'Hugo Boss'].iloc[0]

    # Sort Hugo Boss's rankings from high to low
    sorted_rankings = hugo_boss_rankings.sort_values()

    # Display Hugo Boss's rankings in a compact format (3 scores per row), sorted by rank
    st.write("**Hugo Boss Rankings across all score dimensions (sorted by rank):**")

    # Create columns for compact display (3 scores per row)
    num_columns = 3  # Number of columns per row
    columns = st.columns(num_columns)

    for i, (score_dimension, rank) in enumerate(sorted_rankings.items()):
        with columns[i % num_columns]:
            st.write(f"{score_dimension}: {int(rank)}")
