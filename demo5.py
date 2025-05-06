# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 01:56:41 2025

@author: HP V15 (493178410)
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df_players = pd.read_csv('cleaned_Players_Info_2024.csv')
df_matches = pd.read_csv('year_team_performance.csv')

st.set_page_config(page_title="IPL CricSphere", page_icon="🏏")
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Opening Screen"

# Welcome Screen
if st.session_state.current_page == "Opening Screen":
    st.title("🏏 Welcome to IPL CricSphere")
    st.write("""
    Explore detailed information about IPL players, analyze team and player stats, or dive into match analysis. 
    Choose what you'd like to do below!
    """)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("Player Information", use_container_width=True):
            st.session_state.current_page = "Player Information"
    with col2:
        if st.button("Team/Player Stats", use_container_width=True):
            st.session_state.current_page = "Team/Player Stats"
    with col3:
        if st.button("Match Analysis", use_container_width=True):
            st.session_state.current_page = "Match Analysis"
    if st.button("Win Predictor", key="win_predictor_button", use_container_width=True):
        st.session_state.current_page = "Win Predictor"
    st.subheader("Aarohi Saran")
    st.write("Roll No: A044")
    st.write("Sap ID: 86032400045")

# Player Information Section
if st.session_state.current_page == "Player Information":
    st.header("Player Information")
    st.write("Select a team and player to learn more about them.")
    st.sidebar.header("Filter Players")
    sorted_teams = sorted(df_players['Team Name'].unique())
    selected_team = st.sidebar.selectbox("Select a Team", sorted_teams)
    team_players = df_players[df_players['Team Name'] == selected_team]
    sorted_players = sorted(team_players['Player Name'].unique())
    if sorted_players:
        selected_player = st.sidebar.selectbox("Select a Player", sorted_players)
        search_button = st.sidebar.button("Search")
        if search_button:
            st.header(f"Player Information: {selected_player}")
            st.write("---")
            player_info = team_players[team_players['Player Name'] == selected_player].iloc[0]
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Basic Details")
                st.write(f"**Team:** {player_info['Team Name']}")
                st.write(f"**Nationality:** {player_info['Player Nationality']}")
                st.write(f"**Date of Birth:** {player_info['Date of Birth']}")
                st.write(f"**Role:** {player_info['Player Role']}")
                st.write(f"**IPL Debut:** {player_info['IPL Debut']}")
            with col2:
                st.subheader("Playing Style")
                st.write(f"**Batting Style:** {player_info['Batting Style']}")
                st.write(f"**Bowling Style:** {player_info['Bowling Style']}")
                st.write(f"**Salary:** {player_info['Player Salary']}")
            st.subheader("About the Player")
            st.write(player_info['About'])
        else:
            st.info("Please click the 'Search' button to display player information.")
    else:
        st.warning("No players found for the selected team.")

# Team/Player Stats Section
elif st.session_state.current_page == "Team/Player Stats":
    st.header("Team and Player Stats")
    st.write("Analyze team and player statistics using interactive visualizations.")
    stats_option = st.radio("What would you like to analyze?", ("Team Stats", "Player Stats"))
    if stats_option == "Team Stats":
        st.subheader("Team Statistics")
        selected_year = st.slider("Select Year", 2008, 2024, 2020)
        filtered_df = df_matches[df_matches['Year'] == selected_year]

        # Bar Chart for Match Winners
        st.write("### Match Winners in Selected Year")
        match_winners = filtered_df['Match_Winner'].value_counts()
        plt.figure(figsize=(10, 6))
        sns.barplot(x=match_winners.index, y=match_winners.values, palette="viridis")
        plt.xticks(rotation=45)
        plt.xlabel("Team")
        plt.ylabel("Number of Matches Won")
        plt.title(f"Match Winners in {selected_year}")
        st.pyplot(plt)

    elif stats_option == "Player Stats":
        st.subheader("Player Statistics")

        #Pie Chart
        plt.figure(figsize=(10, 8)) 
        threshold = 5  
        role_counts = df_players['Player Role'].value_counts()
        small_categories = role_counts[role_counts/role_counts.sum()*100 < threshold]
        if len(small_categories) > 0:
            role_counts['Other'] = small_categories.sum()
            role_counts = role_counts.drop(small_categories.index)
        patches, texts, autotexts = plt.pie(
            role_counts,
            labels=role_counts.index,
            autopct='%1.1f%%',
            startangle=140,
            colors=sns.color_palette("pastel"),
            pctdistance=0.85,
            textprops={'fontsize': 12}
        )
        plt.setp(autotexts, size=10, weight="bold")
        plt.setp(texts, size=10)
        plt.axis('equal')
        plt.title("Distribution of Player Roles", fontsize=16, pad=20)
        plt.legend(
            title="Player Roles",
            loc="center right",
            bbox_to_anchor=(1.1, 0.5),
            fontsize=10
        )
        plt.tight_layout()
        st.pyplot(plt)


        #Top 10 highest-paid players
        st.write("### Top 10 Highest-Paid Players")
        df_players['Cleaned Salary'] = pd.to_numeric(df_players['Cleaned Salary'], errors='coerce')  
        top_players = df_players.nlargest(10, 'Cleaned Salary')[['Player Name', 'Team Name', 'Cleaned Salary']]
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Player Name', y='Cleaned Salary', data=top_players, palette="rocket")
        plt.xticks(rotation=45)
        plt.xlabel("Player Name")
        plt.ylabel("Salary")
        plt.title("Top 10 Highest-Paid Players")
        st.pyplot(plt)

# Match Analysis Section
elif st.session_state.current_page == "Match Analysis":
    st.header("Match Analysis")
    st.write("Analyze IPL match data using interactive visualizations.")
    st.subheader("Win Type and Toss Decision")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Win Type Distribution")
        win_type_counts = df_matches['Win_Type'].value_counts()
        plt.figure(figsize=(6, 6))
        plt.pie(win_type_counts, labels=win_type_counts.index, autopct='%1.1f%%', startangle=90, colors=['#A6CEE3', '#B2DF8A'])
        plt.title("Win Type Distribution", fontsize=14, fontweight='bold')
        plt.tight_layout()
        st.pyplot(plt)
    with col2:
        st.write("### Toss Decision Distribution")
        toss_decision_counts = df_matches['Toss_Decision'].value_counts()
        plt.figure(figsize=(6, 6))
        plt.pie(toss_decision_counts, labels=toss_decision_counts.index, autopct='%1.1f%%', startangle=90, colors=['#FDBF6F', '#FB9A99'])
        plt.title("Toss Decision Distribution", fontsize=14, fontweight='bold')
        plt.tight_layout()
        st.pyplot(plt)

    # Line Graph for Scores by Match Phase
    st.subheader("Scores by Match Phase")
    match_phase_scores = df_matches[['Powerplay_Scores', 'Middle_Overs_Scores', 'Death_Overs_Scores']].mean()
    plt.figure(figsize=(10, 6))
    plt.plot(match_phase_scores.index, match_phase_scores.values, marker='o', linestyle='-', color='b', label='Line Graph')
    plt.bar(match_phase_scores.index, match_phase_scores.values, color='pink', alpha=0.5, label='Bar Graph')
    plt.xlabel("Match Phase")
    plt.ylabel("Average Score")
    plt.title("Average Scores by Match Phase")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    st.pyplot(plt)
    
elif st.session_state.current_page == "Win Predictor":
    st.header("Win Predictor")
    st.write("Select two teams to predict the winner and view their previous match stats.")
    team_list = sorted(df_matches['Team1'].unique())
    team_list_2 = sorted(df_matches['Team2'].unique())
    col1, col2 = st.columns(2)
    with col1:
        team1 = st.selectbox("Select Team 1", team_list)
    with col2:
        team2 = st.selectbox("Select Team 2", team_list_2)
    if st.button("Search", key="search_button", use_container_width=True):
        if team1 == team2:
            st.warning("Please select two different teams.")
        else:
            if team1 == team2:
                st.warning("Please select two different teams.")
            else:
                matches_between_teams = df_matches[(df_matches['Team1'].str.contains(team1)) & (df_matches['Team2'].str.contains(team2))]
                if not matches_between_teams.empty:
                    st.subheader(f"Previous Matches Between {team1} and {team2}")
                    total_matches = matches_between_teams.shape[0]
                    team1_wins = matches_between_teams[matches_between_teams['Match_Winner'] == team1].shape[0]
                    team2_wins = matches_between_teams[matches_between_teams['Match_Winner'] == team2].shape[0]
                    draw_matches = total_matches - (team1_wins + team2_wins)

                    st.write(f"**Total Matches Played:** {total_matches}")
                    st.write(f"**{team1} Wins:** {team1_wins}")
                    st.write(f"**{team2} Wins:** {team2_wins}")
                    st.write(f"**Draws/Ties:** {draw_matches}")
                    
                    fig, ax = plt.subplots(figsize=(8, 4), subplot_kw=dict(polar=True))
                    #gauge chart
                    wins = [team1_wins, team2_wins]
                    max_wins = max(wins)
                    angles = np.linspace(0, 2 * np.pi, 2, endpoint=False)
                    colors = ['#1f77b4', '#e377c2']  
                    for i, (win, color) in enumerate(zip(wins, colors)):
                        ax.bar(angles[i], win, width=0.5, color=color, alpha=0.7, label=f"{[team1, team2][i]}: {win} Wins")
                    ax.set_theta_zero_location('N')
                    ax.set_theta_direction(-1)
                    ax.set_ylim(0, max_wins + 1)
                    ax.set_xticks(angles)
                    ax.set_xticklabels([team1, team2], fontsize=12, fontweight='bold')
                    ax.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))
                    ax.set_title("Number of Wins Comparison", fontsize=14, fontweight='bold', pad=20)
                    plt.tight_layout()
                    st.pyplot(fig)

                    if team1_wins > team2_wins:
                        st.success(f"Prediction: **{team1}** is more likely to win based on previous matches.")
                    elif team2_wins > team1_wins:
                        st.success(f"Prediction: **{team2}** is more likely to win based on previous matches.")
                    elif team1_wins == team2_wins:
                        st.info("Both teams have an equal number of wins in previous matches. It's a 50/50!")
                    else:
                        st.warning(f"No previous matches found between {team1} and {team2}.")
    
if st.session_state.current_page != "Opening Screen":
    if st.button("Back to Home"):
        st.session_state.current_page = "Opening Screen"
        st.rerun()