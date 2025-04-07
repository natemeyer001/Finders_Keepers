import streamlit as st
import pandas as pd


# Function to apply row-wise styling
def highlight_rows(row):
    # Eligibles
    if(row['Keeper Status'] == 'Eligible to be kept'):
        return ['background-color: lightgreen'] * len(row)
    elif(row['Keeper Status'] == 'Eligible - non first rounder only kept once'):
        return ['background-color: orange'] * len(row)
    elif('Free Agent' in row['Keeper Status']):
        return ['background-color: teal'] * len(row)
    
    # Ineligibles
    elif(row['Keeper Status'] == 'Ineligible - off roster'):
        return ['background-color: darkgray'] * len(row)
    elif(row['Keeper Status'] == 'Ineligible - first rounder already kept'):
        return ['background-color: pink'] * len(row)
    elif(row['Keeper Status'] == 'Ineligible - non first rounder already kept twice'):
        return ['background-color: pink'] * len(row)
    # Default
    else:
        return [''] * len(row)


# # Create Tabs
tab1, tab2 = st.tabs(["Keeper Options", "Ineligible Draft List"])
# # , tab3, tab4 = , "League Luck", "Nate Analysis"])

# # Add tab that shows distribution of scores for the league (bin size of 1pt?)


# Keepers df used for the first 2 tabs
keepers_df = pd.read_csv('keepers.csv')


# Content for Tab 1 (Keeper Options)
with tab1:
    st.write("These are the keeper options, including Free Agents")
    st.title("League Keeper Options")
    
    # Filter by Owner
    owners = keepers_df["Owner"].unique()
    selected_owner = st.selectbox("Select an Owner:", ["All"] + list(owners))

    # Filter DataFrame
    if selected_owner != "All":
        filtered_df = keepers_df[keepers_df["Owner"] == selected_owner]
        filtered_df.reset_index(drop=True, inplace=True)
    else:
        filtered_df = keepers_df

    # Display styled DF
    styled_df = filtered_df.style.apply(highlight_rows, axis=1)
    st.dataframe(styled_df, use_container_width=True)


# Content for Tab 2 (Ineligible Draft List)
with tab2:
    st.write("This is the ineligible draft list")

    # Ineligible Draft List
    ineligible_df = keepers_df[
        keepers_df["Keeper Status"].str.contains("ineligible", case=False, na=False) &
        keepers_df["Keeper Status"].str.contains("kept", case=False, na=False)]
    ineligible_df.reset_index(drop=True, inplace=True)

    # Filter by Owner
    inel_owners = ineligible_df["Owner"].unique()
    selected_owner = st.selectbox("Select an Owner:", ["All"] + list(inel_owners))

    # Filter DataFrame
    if selected_owner != "All":
        filtered_df = ineligible_df[ineligible_df["Owner"] == selected_owner]
        filtered_df.reset_index(drop=True, inplace=True)
    else:
        filtered_df = ineligible_df

    # Display styled DF
    styled_df = filtered_df.style.apply(highlight_rows, axis=1)
    st.dataframe(styled_df, use_container_width=True)



# # Content for Tab 3 (League Luck)
# with tab3:
#     st.write("This is the luck analysis")

#     # import Luck_Analysis/final_team_standings.csv
#     luck_path = os.path.join(parent_dir, 'Luck_Analysis/data', 'final_team_standings.csv')
#     luck_df = pd.read_csv(luck_path)
#     luck_df = luck_df.sort_values(by='yearly_luck', ascending=False)
#     luck_df.reset_index(drop=True, inplace=True) 
#     st.dataframe(luck_df, use_container_width=True)


#     # Show graphs of luck below


#     # Include table for luckiest/unluckiest matchups for the year
#     st.write("The following 2 tables are based on season")

#     matchup_luck = pd.read_csv("Luck_Analysis/data/matchup_luck.csv")
#     melted_df = matchup_luck.melt(id_vars="Week", var_name="Owner", value_name="Luck")
#     sorted_df = melted_df.sort_values(by='Luck', ascending=True).reset_index(drop=True)

#     most_luck = sorted_df.tail(25).sort_values(by='Luck', ascending=False).reset_index(drop=True)
#     least_luck = sorted_df.head(25).reset_index(drop=True)
    
#     # Add score of matchups
#     st.write("Here are the 25 luckiest wins for the year")
#     st.write(most_luck)
#     st.write("Here are the 25 unluckiest losses of the year")
#     st.write(least_luck)
    