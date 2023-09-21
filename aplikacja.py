import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.graph_objects as go
import re
import numpy as np
from collections import defaultdict

# Ustawienia stylu aplikacji

st.set_page_config(
    page_title="Premier League",
    initial_sidebar_state="expanded"
)

# Zbiory danych


@st.cache_data
def load_data():
    df = pd.read_excel(
        io='Premier_league_with2223.xlsx',
        sheet_name='pl',
        engine='openpyxl'
    )
    carabao_cup = pd.read_excel(
        io='puchary.xlsx',
        engine='openpyxl',
        sheet_name='Carabao_cup'
    )
    fa_cup = pd.read_excel(
        io='puchary.xlsx',
        engine='openpyxl',
        sheet_name='Fa_cup'
    )
    premier_league = pd.read_excel(
        io='puchary.xlsx',
        engine='openpyxl',
        sheet_name='Premier_league'
    )
    transfers_direction = pd.read_excel(
        io='transfers_directions.xlsx',
        engine='openpyxl'
    )
    wartosci = pd.read_excel(io='wartosci_pieciu_lig.xlsx', engine='openpyxl')
    cup1 = pd.DataFrame(carabao_cup['Carabao_cup'].value_counts())
    cup2 = pd.DataFrame(fa_cup['Fa_cup'].value_counts())
    p_l = pd.DataFrame(premier_league['zwyciezca'].value_counts())
    unique_teams = df['HomeTeam'].unique().tolist()
    uefa_ranking = pd.read_excel(
        io='UEFA.xlsx',
        engine='openpyxl',
        index_col=False
    )
    seasonal_league_financial = pd.read_excel(
        io='transfer_expenditures.xlsx',
        engine='openpyxl'
    )
    transfers = pd.read_excel(
        io='Premier_league_transfers.xlsx',
        engine='openpyxl'
    )
    stats = pd.read_excel(io='StatsOfClubs.xlsx', engine='openpyxl')
    players = pd.read_excel(io='players.xlsx', engine='openpyxl')
    transfers_direction_by_season = pd.read_excel(
        io='Transfers_directions_by_season.xlsx',
        engine='openpyxl'
    )
    return (
        df,
        carabao_cup,
        fa_cup,
        premier_league,
        wartosci,
        cup1,
        cup2,
        p_l,
        unique_teams,
        uefa_ranking,
        transfers,
        stats,
        players,
        transfers_direction,
        seasonal_league_financial,
        transfers_direction_by_season
    )


(
    df,
    carabao_cup,
    fa_cup,
    premier_league,
    wartosci,
    cup1,
    cup2,
    p_l,
    unique_teams,
    uefa_ranking,
    transfers,
    clubstats,
    players,
    transfer_directions,
    seasonal_league_financial,
    transfers_by_season
) = load_data()

color_dictionary = {
    'Arsenal': {'gred': '#EF0107', 'gold': '#9C824A'},
    'Nottingham Forest': {'gred': '#DD0000'},
    'Chelsea': {'zblue': '#034694', 'gold': '#DBA111'},
    'Coventry': {'0blue': '#059DD9', 'gold': '#E54724'},
    'Crystal Palace': {'zblue': '#1B458F', 'gray': '#A7A5A6', 'red': '#C4122E'},
    'Ipswich': {'7blue': '#3a64a3', 'red': '#de2c37'},
    'Leeds': {'2yellow': '#FFCD00', 'gold': '#AC944D'},
    'Liverpool': {'zred': '#C8102E', 'green': '#00B2A9'},
    'Manchester United': {'gred': '#DA291C', 'yellow': '#FBE122'},
    'Middlesbrough': {'zblue': '#004494', 'black': '#000000'},
    'Sheffield Wednesday': {'1blue': '#4681cf', 'yellow': '#e9b008'},
    'Manchester City': {'2blue': '#6CABDD', 'gold': '#D4A12A'},
    'Southampton': {'black': '#130C0E', 'red': '#D71920'},
    'Tottenham': {'3blue': '#132257'},
    'Aston Villa': {'1claret': '#670E36', 'blue': '#95BFE5'},
    'Newcastle': {'black': '#241F20', 'blue': '#41B6E6'},
    'West Ham': {'1maroon': '#7A263A', 'blue': '#1BB1E7'},
    'Swindon': {'gold': '#B48D00', 'red': '#DC161B'},
    'Leicester': {'cblue': '#003090', 'gold': '#FDBE11'},
    'Brentford': {'zorange': '#FFB400', 'red': '#D20000'},
    'Barnsley': {'gred': '#D71921', 'blue': '#00B8F1'},
    'Birmingham': {'4blue': '#0000FF', 'red': '#DC241F'},
    'Blackburn Rovers': {'green': '#009036', 'blue': '#009EE0'},
    'Blackpool': {'2orange': '#F68712'},
    'Bolton': {'cblue': '#263C7E', 'red': '#88111E'},
    'Bournemouth': {'1red': '#B50E12', 'black': '#000000'},
    'Brighton': {'zblue': '#0057B8', 'yellow': '#FDB913'},
    'Burnley': {'claret': '#6C1D45', 'blue': '#99D6EA'},
    'Derby': {'black': '#000000', 'blue': '#000040'},
    'Everton': {'5blue': '#003399', 'pink': '#fa9bac'},
    'Huddersfield': {'gblue': '#0E63AD', 'yellow': '#FDE43C'},
    'Wolves': {'zorange': '#FDB913', 'black': '#231F20', },
    'West Brom': {'6blue': '#122F67', 'green': '#149557'},
    'Wimbledon': {'cblue': '#2b4690', 'yellow': '#fff200'},
    'Wigan': {'green': '#123d0f', 'blue': '#1d59af'},
    'Norwich City': {'green': '#00A650', 'yellow': '#FFF200'},
    'Swansea': {'black': '#000000'},
    'Hull': {'1orange': '#f5971d', 'black': '#101920'},
    'Reading': {'pink': '#dd1740 ', 'blue': '#004494'},
    'Watford': {'1yellow': '#FBEE23', 'red': '#ED2127'},
    'Cardiff': {'gblue': '#0070B5', 'red': '#D11524'},
    'QPR': {'zblue': '#1d5ba4', 'pink': '#ff33cc'},
    'Stoke': {'zred': '#E03A3E', 'blue': '#1B449C'},
    'Bradford': {'1yellow': '#FFDF00', 'black': '#000000'},
    'Portsmouth': {'2red': '#ff0000', 'black': '#000000'},
    'Sheffield United': {'gred': '#ec2227', 'yellow': '#fcee23'},
    'Fulham': {'black': '#000000', 'red': '#CC0000'},
    'Charlton': {'gred': '#d4021d', 'black': '#000000'},
    'Oldham': {'cyan': '#59777d'},
    'Sunderland': {'gred': '#eb172b', 'gold': '#a68a26'}
}

new_color_dict = {
    team: {list(colors.keys())[0]: list(colors.values())[0]}
    for team, colors in color_dictionary.items()
}

# Funkcje przetwarzające dane


def find_common_seasons(team1, team2, df):
    common_seasons = df.query(
        "(HomeTeam == @team1 or AwayTeam == @team1) and \
            (HomeTeam == @team2 or AwayTeam == @team2)"
    )["Season"].unique()
    return common_seasons


def return_teams_for_season(season, df):
    return sorted(set(df[df['Season'] == season]['HomeTeam']))


def return_opponents(df, team='Arsenal'):
    opponents = df[df['HomeTeam'] == team]['AwayTeam'].unique().tolist()
    return sorted(opponents)


def head_to_head_results(df, home_team, away_team):
    subset = df[
        (df["HomeTeam"].isin([home_team, away_team]))
        & (df["AwayTeam"].isin([home_team, away_team]))
    ]
    results = {home_team: 0, 'Remis': 0, away_team: 0}

    for index, row in subset.iterrows():
        if row['HomeTeam'] == home_team:
            if row['FTR'] == 'H':
                results[home_team] += 1
            elif row['FTR'] == 'D':
                results['Remis'] += 1
            else:
                results[away_team] += 1
        elif row['AwayTeam'] == home_team:
            if row['FTR'] == 'A':
                results[home_team] += 1
            elif row['FTR'] == 'D':
                results['Remis'] += 1
            else:
                results[away_team] += 1

    df_results = pd.DataFrame.from_dict(results, orient='index').reset_index()
    df_results = df_results.rename(columns={'index': 'result', 0: 'count'})
    return df_results


def calculate_points(df, team_name, season):
    df = df[
        ((df["HomeTeam"] == team_name) | (df["AwayTeam"] == team_name))
        & (df["Season"] == season)
    ].reset_index(drop=True)
    points = 0
    points_by_matchweek = {0: 0}
    for index, row in df.iterrows():
        if row['HomeTeam'] == team_name:
            if row['FTR'] == 'H':
                points += 3
        elif row['AwayTeam'] == team_name:
            if row['FTR'] == 'A':
                points += 3
        if row['FTR'] == 'D':
            points += 1
        points_by_matchweek[index + 1] = points
    return pd.DataFrame(
        {
            "Kolejka": list(points_by_matchweek.keys()),
            "Punkty": list(points_by_matchweek.values()),
        }
    )


def choose_color_for_teams(team1, team2):
    sorted_teams = sorted([team1, team2])
    if (
        len(color_dictionary[sorted_teams[0]].items())
        + len(color_dictionary[sorted_teams[1]].items())
        == 2
    ):
        return {
            sorted_teams[0]: list(color_dictionary[sorted_teams[0]].values())[0],
            sorted_teams[1]: list(color_dictionary[sorted_teams[1]].values())[0],
        }
    elif len(color_dictionary[sorted_teams[0]].items()) > 1:
        color2 = list(color_dictionary[sorted_teams[1]].keys())[0]
        for color1 in color_dictionary[sorted_teams[0]].keys():
            if color1 != color2:
                return {
                    sorted_teams[0]: color_dictionary[sorted_teams[0]]
                    .get(color1),
                    sorted_teams[1]: color_dictionary[sorted_teams[1]]
                    .get(color2),
                }
    elif len(color_dictionary[sorted_teams[1]].items()) > 1:
        color1 = list(color_dictionary[sorted_teams[0]].keys())[0]
        for color2 in color_dictionary[sorted_teams[1]].keys():
            if color1 != color2:
                return {
                    sorted_teams[0]: color_dictionary[sorted_teams[0]]
                    .get(color1),
                    sorted_teams[1]: color_dictionary[sorted_teams[1]]
                    .get(color2),
                }


# def count_position(category, season, df):
#     position_mapping = {
#         'Left Winger': 'Lewy skrzydłowy',
#         'defence': 'Obrońca',
#         'Right-Back': 'Prawy obrońca',
#         'Goalkeeper': 'Bramkarz',
#         'Centre-Back': 'Środkowy obrońca',
#         'Right Winger': 'Prawy skrzydłowy',
#         'Centre-Forward': 'Środkowy napastnik',
#         'attack': 'Napastnik',
#         'Defensive Midfield': 'Defensywny pomocnik',
#         'Left Midfield': 'Lewy pomocnik',
#         'Attacking Midfield': 'Ofensywny pomocnik',
#         'Central Midfield': 'Środkowy pomocnik',
#         'midfield': 'Pomocnik',
#         'Right Midfield': 'Prawy pomocnik',
#         'Left-Back': 'Lewy obrońca',
#         'Second Striker': 'Drugi napastnik'
#     }
#     position_counts = df.query("season == @season and transfer_movement == @category")[
#         "position"
#     ].value_counts()
#     position_counts = position_counts.rename(position_mapping)
#     position_df = position_counts.to_frame().reset_index()
#     position_df.columns = ['position', 'count']
#     return position_df


def map_to_category(position):
    goalkeeper_positions = ['Goalkeeper']
    defense_positions = ['Centre-Back', 'Right-Back', 'Left-Back', 'defence', 'Defensive Midfield']
    offense_positions = [
        'Centre-Forward', 'Left Winger', 'Right Winger', 'Second Striker',
        'Attacking Midfield', 'midfield', 'Left Midfield', 'Right Midfield',
        'Central Midfield', 'attack']

    if position in goalkeeper_positions:
        return 'Bramkarz'
    elif position in defense_positions:
        return 'Zawodnik defensywny'
    elif position in offense_positions:
        return 'Zawodnik ofensywny'
    else:
        return 'Inna'


def count_position(category, season, df):
    df['season'] = df['season'].astype(str)
    df['new_position'] = df['position'].map(map_to_category)
    position_counts = df.query("season1 == @season and transfer_movement == @category")[
        "new_position"
    ].value_counts()
    print(position_counts)
    position_df = position_counts.to_frame().reset_index()
    position_df.columns = ['position', 'count']
    return position_df


def calculate_lost_goals_by_half(df, team, season):
    first_half_goals_conceded = df[df["Season"] == season].groupby("HomeTeam")[
        "HTAG"
    ].sum().get(team) + df[df["Season"] == season].groupby("AwayTeam")[
        "HTHG"
    ].sum().get(
        team
    )
    second_half_goals_conceded = df[df["Season"] == season].groupby("HomeTeam")[
        "SHTAG"
    ].sum().get(team) + df[df["Season"] == season].groupby("AwayTeam")[
        "SHTHG"
    ].sum().get(
        team
    )
    first_half_goals_scored = df[df["Season"] == season].groupby("HomeTeam")[
        "HTHG"
    ].sum().get(team) + df[df["Season"] == season].groupby("AwayTeam")[
        "HTAG"
    ].sum().get(
        team
    )
    second_half_goals_scored = df[df["Season"] == season].groupby("HomeTeam")[
        "SHTHG"
    ].sum().get(team) + df[df["Season"] == season].groupby("AwayTeam")[
        "SHTAG"
    ].sum().get(
        team
    )
    # total_goals_scored = first_half_goals_scored + second_half_goals_scored
    # total_goals_conceded = first_half_goals_conceded + second_half_goals_conceded
    return pd.DataFrame(
        {
            "GSTWPP": [int(first_half_goals_conceded)],
            "GSTWDP": [int(second_half_goals_conceded)],
            "GSWPP": [int(first_half_goals_scored)],
            "GSWDP": [int(second_half_goals_scored)],
            # "TotalGoalsScored": [total_goals_scored],
            # "TotalGoalsConceded": [total_goals_conceded],
        }
    )


def calculate_home_away_points(df, season, team):
    result = {'Domowy': 0, 'Wyjazdowy': 0}
    filtered_df = df.query(
        "Season == @season and (HomeTeam == @team or AwayTeam == @team)"
    )[["HomeTeam", "AwayTeam", "FTR"]]
    for _, row in filtered_df.iterrows():
        if row['HomeTeam'] == team:
            if row['FTR'] == 'H':
                result['Domowy'] += 3
            elif row['FTR'] == 'D':
                result['Domowy'] += 1
        else:
            if row['FTR'] == 'A':
                result['Wyjazdowy'] += 3
            elif row['FTR'] == 'D':
                result['Wyjazdowy'] += 1
    return result


def calculate_fauls_yellow_and_red_cards(season, team, df):
    filtered_df = df.query(
        "Season == @season and (HomeTeam == @team or AwayTeam == @team)"
    )
    home_fouls = filtered_df.query('HomeTeam == @team')['HF'].sum()
    away_fouls = filtered_df.query('HomeTeam == @team')['AF'].sum()
    fouls = home_fouls + away_fouls
    home_yellow_cards = filtered_df.query('HomeTeam == @team')['HY'].sum()
    away_yellow_cards = filtered_df.query('AwayTeam == @team')['AY'].sum()
    yellow_cards = home_yellow_cards + away_yellow_cards
    home_red_cards = filtered_df.query('HomeTeam == @team')['HR'].sum()
    away_red_cards = filtered_df.query('AwayTeam == @team')['AR'].sum()
    red_cards = home_red_cards + away_red_cards
    result = {
        'Faule bez kartki': int(fouls) - int(red_cards) - int(yellow_cards),
        'Czerwone kartki': int(red_cards),
        'Żółte kartki': int(yellow_cards)
    }
    return result


# def calculate_shots_stats(season, team, df):
#     filtered_df = df.query(
#         "Season == @season and (HomeTeam == @team or AwayTeam == @team)"
#     )
#     home_shots = filtered_df.query('HomeTeam == @team')['HS'].sum()
#     away_shots = filtered_df.query('AwayTeam == @team')['AS'].sum()
#     shots = home_shots + away_shots
#     home_shots_on_target = filtered_df.query('HomeTeam == @team')['HST'].sum()
#     away_shots_on_target = filtered_df.query('AwayTeam == @team')['AST'].sum()
#     shots_on_target = home_shots_on_target + away_shots_on_target
#     shots_off_target = shots - shots_on_target
#     result = {
#         'Strzały celne': int(shots_on_target),
#         'Strzały niecelne': int(shots_off_target)
#     }
#     return result

def calculate_shots_stats(season, team, df):
    filtered_df = df.query("season == @season and team == @team")
    on_target_shots = filtered_df['ontarget_scoring_att'].sum()
    total_shots = filtered_df['total_scoring_att'].sum()
    off_target_shots = total_shots - on_target_shots
    statistics = {
        'Strzały celne': on_target_shots,
        'Strzały niecelne': off_target_shots
    }
    return statistics


def get_top_10_by_season(data, season):
    filtered_data = data[data['season'] == season]
    sorted_data = filtered_data.sort_values(by='ranking', ascending=False)
    mapping = {
        'France': 'Francuska',
        'Czech Republic': 'Czeska',
        'Turkey': 'Turecka',
        'Belgium': 'Belgijska',
        'Norway': 'Norweska',
        'Germany': 'Niemiecka',
        'Romania': 'Rumuńska',
        'Russia': 'Rosyjska',
        'Greece': 'Grecka',
        'England': 'Angielska',
        'Portugal': 'Portugalska',
        'Spain': 'Hiszpańska',
        'Austria': 'Austriacka',
        'Italy': 'Włoska',
        'Ukraine': 'Ukraińska',
        'Scotland': 'Szkocka',
        'Netherlands': 'Holenderska'
    }
    # Wybierz top 10 wyników
    top_10 = sorted_data.head(10).reset_index(drop=True)
    top_10.loc[:, 'country'] = top_10['country'].map(mapping)
    return top_10


def get_seasons(df):
    return df['Season'].unique()


def return_most_valuable_transfers_for_season(category, season, df):
    df['season1'] = df['season1'].astype(str)
    df_filtered = df.query(
        'season1 == @season and transfer_movement == @category'
    )
    return_10 = df_filtered[
        ['player_name', 'fee_cleaned']
    ].sort_values(by='fee_cleaned', ascending=False)
    return return_10.iloc[:10]


# Odległość granic od -----
streamlit_style = """
<style>
body {
    font-size: 20px;
}
</style>
"""

# Zmienianie wysokości pasków wyborów i rozmiar tekstu
css = """
    <style>
    div[data-baseweb="select"] > div:first-child {
        font-size: 15px;
    }
    </style>
"""
st.markdown(css, unsafe_allow_html=True)

# Ustawienie odległości pierwszego elementu od górnej części strony
css = """
    <style>
        .stApp {
            margin-top: 30px;
        }
    </style>
"""

st.markdown(streamlit_style, unsafe_allow_html=True)

st.markdown(css, unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .appview-container .main .block-container {
        max-width: 1200px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

selected_tab = option_menu(
    None,
    ["Strona główna", "Premier League", "Drużyny", "Transfery"],
    icons=["house-fill", "bar-chart-fill", "bar-chart-fill", "cash-stack"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "green"},
        "icon": {"color": "white", "font-size": "20px"},
        "nav-link": {
            "font-size": "15px",
            "text-align": "left",
            "margin": "0px",
            "--hover-color": "red",
            "color": "white",
        },
        "nav-link-selected": {"background-color": "red"},
    },
)

if selected_tab == "Strona główna":
    st.markdown('---')
    st.title("Statystyki Premier League")
    with open('strona_glowna.txt', 'r', encoding='utf-8') as file:
        file_content = file.read().split('\n')

    formatted_text = re.sub(
        r'\[([^]]+)\]\(([^)]+)\)',
        r'<a href="\2">\1</a>',
        file_content[0]
    )
    formatted_text1 = re.sub(
        r'\[([^]]+)\]\(([^)]+)\)',
        r'<a href="\2">\1</a>',
        file_content[1]
    )

    st.markdown(
        f'<div style="text-align: justify; font-size: 25px;">{formatted_text}</div>',
        unsafe_allow_html=True
    )
    st.markdown(" ")
    st.write(
        f'<div style="text-align: justify; font-size: 25px;">{formatted_text1}</div>',
        unsafe_allow_html=True
    )

    transfermarkt = '1. <a href="https://www.transfermarkt.com/">Transfermarkt</a>, \
        dane z dnia 11 kwietnia 2023.'
    st.markdown(
        f'<div style="text-align: justify; font-size: 25px;">{transfermarkt}</div>',
        unsafe_allow_html=True
    )
    football_data = '2. <a href="https://www.football-data.co.uk/englandm.php/">football-data</a>, \
        dane z dnia 28 maja 2023.'
    st.markdown(
        f'<div style="text-align: justify; font-size: 25px;">{football_data}</div>',
        unsafe_allow_html=True
    )
    premier_league_website = '3. <a href="https://www.premierleague.com/">Oficjalna strona Premier League</a>, \
        dane z dnia 28 maja 2023.'
    st.markdown(
        f'<div style="text-align: justify; font-size: 25px;">{premier_league_website}</div>',
        unsafe_allow_html=True
    )

elif selected_tab == "Premier League":
    st.markdown('---')
    premier_league1 = option_menu(
        None,
        [
            "Ogólne statystyki ligi",
            "Premier League na płaszczyźnie europejskiej"
        ],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "green",
            },
            "icon": {"color": "white", "font-size": "20px"},
            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "red",
                "color": "white",
            },
            "nav-link-selected": {"background-color": "red"},
        },
    )
    if premier_league1 == "Premier League na płaszczyźnie europejskiej":
        st.header('Wartość lig piłkarskich')
        liga = st.multiselect(
            "Wybierz ligę :",
            ["Ligue 1", "Bundesliga", "Premier League", "La Liga", "Serie A"],
            default=["Premier League"],
        )
        fig0 = go.Figure()
        colors = ['red', 'green', 'blue', 'purple', 'black']
        replace_name = {'Bundesliga': 'Bundesligi', 'La Liga': 'La Ligi'}
        for i, lig in enumerate(liga):
            fig0.add_trace(
                go.Scatter(
                    x=wartosci['sezon'],
                    y=wartosci[lig]/1000,
                    name=lig,
                    mode='lines+markers',
                    hovertemplate=f"Wartość {replace_name.get(lig, lig)}: <b>%{{y:.2f}} mld</b>"
                    + "<extra></extra>",
                    line=dict(color=colors[i]),
                    showlegend=True
                )
            )
        fig0.update_layout(
            margin=dict(l=20, r=50, t=25, b=50),
            separators=',',
            xaxis=dict(
                title='Sezon',
                ticks="outside",
                ticklen=4,
                tickcolor='black',
                range=[-0.5, 18.5],
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=16, color='black'),
                showline=True,
            ),
            yaxis=dict(
                # position=0,
                title="Wartość ligi (mld euro)",
                title_font=dict(size=25, color='black'),
                range=[0, 11.5],
                tickfont=dict(size=16, color='black'),
                showgrid=True,
                gridwidth=1,
                gridcolor='black',
                zerolinecolor='white'
            ),
            hovermode="x unified",
            hoverlabel=dict(
                font=dict(
                    size=15,
                    color='black'
                )
            ),
            height=500,
            width=1200,
            legend=dict(
                title=dict(text="Liga", font=dict(size=25, color='black')),
                font=dict(size=20, color='black'),
                y=0.96,
                x=1.02
            ),
        )
        st.plotly_chart(fig0, use_container_width=True)
        st.header('10 najlepszych lig według UEFA')
        year_of_uefa_ranking = st.selectbox('Wybierz rok :', range(2023, 1996, -1))
        fig12 = go.Figure()
        uefa_rank = get_top_10_by_season(
            data=uefa_ranking,
            season=year_of_uefa_ranking
        )
        fig12.add_traces(
            go.Bar(
                x=uefa_rank['country'],
                y=uefa_rank['ranking'],
                text=uefa_rank['ranking'].apply(
                    lambda x: str(x).replace('.', ',')
                ),
                textfont=dict(size=17, color='white'),
                hovertemplate="Liczba punktów w rankingu UEFA: <b>%{y}</b>"
                + "<extra></extra>",
                name='Liga Mistrzów',
                hoverlabel=dict(
                    font=dict(size=14, color='white'),
                    bgcolor='blue'
                ),
                marker_color='blue'
            )
        )
        fig12.update_layout(
                separators=',',
                margin=dict(l=50, r=50, t=50, b=0),
                xaxis=dict(
                    title='Liga',
                    tickfont=dict(size=16, color='black'),
                    zeroline=False,
                    title_font=dict(size=25, color='black')
                ),
                yaxis=dict(
                    title="Liczba punktów UEFA",
                    title_font=dict(size=25, color='black'),
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='gray',
                    tickfont=dict(size=15, color='black'),
                ),
                height=500,
                width=1200,
            )
        st.plotly_chart(fig12, use_container_width=True)
        st.write('Rok odnosi się do końca sezonu, wybór roku 2020 odpowiada\
                  wybraniu rankingu z końca sezonu 2019/2020.')
        st.write('Ranking UEFA odgrywa kluczową rolę w piłce nożnej. \
                 Im wyższa pozycja w rankingu, tym więcej drużyn\
                  z danej ligi może powalczyć o udział w prestiżowych i dochodowych turniejach \
                 europejskich. Udział w tych turniejach przyciąga uwagę kibiców i\
                  generuje znaczące przychody. Dlatego ranking UEFA ma istotne \
                 znaczenie dla rozwoju i reputacji drużyn oraz lig.\
                 Dla zainteresowanych umieszczam \
                [link](https://www.uefa.com/nationalassociations/uefarankings/country/about/)\
                do oficjalnej strony UEFA.')
        st.header(
            'Zwycięstwa drużyn z Premier League w pucharach europejskich'
        )
        zwyciezcy_lm = ['Liverpool', 'Manchester United', 'Chelsea', 'Manchester City']
        zwyciezcy_le = ['Chelsea', 'Manchester United', 'Liverpool']
        liczebnosci_lm = [2, 2, 2, 1]
        liczebnosci_le = [2, 1, 1]
        fig9 = go.Figure()
        fig9.add_trace(go.Bar(
            x=zwyciezcy_lm,
            y=liczebnosci_lm,
            text=liczebnosci_lm,
            textfont=dict(size=17, color='white'),
            hovertemplate="Zwycięstwa Ligi Mistrzów: <b>%{y}</b>"
            + "<extra></extra>",
            name='Liga Mistrzów',
            marker_color='blue'
        ))
        fig9.add_trace(go.Bar(
            x=zwyciezcy_le,
            y=liczebnosci_le,
            text=liczebnosci_le,
            textfont=dict(size=17, color='black'),
            hovertemplate="Zwycięstwa Ligi Europy: <b>%{y}</b>"
            + "<extra></extra>",
            name='Liga Europy',
            marker_color='orange'
        ))

        fig9.update_layout(
            xaxis_title='Drużyna',
            hovermode='x unified',
            yaxis_title='Liczba zwycięstw',
            barmode='group',
            plot_bgcolor='white'
        )

        fig9.update_layout(
            margin=dict(l=20, r=50, t=35, b=50),
            barmode='group',
            xaxis=dict(
                title='Drużyna',
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=16, color='black'),
                showline=False
            ),
            yaxis=dict(
                title="Liczba zwycięstw",
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=16, color='black'),
                showgrid=True,
                gridwidth=1,
                gridcolor='gray',
                zerolinecolor='white'
            ),
            hovermode="x unified",
            hoverlabel=dict(
                font=dict(
                    size=15,
                    color='black'
                )
            ),
            height=500,
            width=1200,
            legend=dict(
                title=dict(text="Turniej", font=dict(size=25, color='black')),
                font=dict(size=20, color='black'),
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="right",
                x=1.20
            ),
        )
        st.plotly_chart(fig9, use_container_width=True)
        st.header('Liczba edycji pucharów europejskich, w których wystąpiły drużyny angielskie')
        wystepy_UCL = {
            'Manchester United': 25,
            'Arsenal': 19,
            'Chelsea': 19,
            'Liverpool': 15,
            'Manchester City': 12,
            'Tottenham': 6,
            'Newcastle United': 3,
            'Leeds': 2,
            'Blackburn Rovers': 1,
            'Leicester': 1
        }
        wystepy_ul = {
            'Liverpool': 11,
            'Tottenham': 11,
            'Arsenal': 8,
            'Manchester United': 8,
            'Aston Villa': 7,
            'Newcastle United': 7,
            'Blackburn Rovers': 6,
            'Everton': 6,
            'Chelsea': 5,
            'Leeds': 5,
            'Leicester': 4,
            'Manchester City': 4,
            'Fulham': 3,
            'West Ham': 3,
            'Bolton': 2,
            'Ipswich': 2,
            'Middlesbrough': 2,
            'Southampton': 2,
            'Birmingham': 1,
            'Millwall': 1,
            'Norwich City': 1,
            'Nottingham Forest': 1,
            'Portsmouth': 1,
            'Sheffield Wednesday': 1,
            'Stoke': 1,
            'Swansea': 1,
            'Wigan': 1,
            'Wolves': 1,
        }
        fig6 = go.Figure()
        tournament = st.selectbox('Wybór turnieju :', ['Liga Mistrzów', 'Liga Europy'])
        if tournament == 'Liga Mistrzów':
            fig6.add_trace(
                go.Bar(
                    x=list(wystepy_UCL.keys()),
                    y=list(wystepy_UCL.values()),
                    text=list(wystepy_UCL.values()),
                    textfont=dict(size=15, color='white'),
                    textposition='inside',
                    textangle=0,
                    # insidetextanchor='middle',
                    hoverlabel=dict(
                        font=dict(size=14, color='white'),
                        bgcolor='blue'
                    ),
                    marker_color='blue',
                    hovertemplate="Liczba edycji Ligi Mistrzów: <b>%{y}</b>"
                    + "<extra></extra>"
                )
            )
            fig6.update_layout(
                margin=dict(l=0, r=25, t=25, b=0),
                xaxis=dict(
                    title='Drużyna',
                    tickfont=dict(size=14, color='black'),
                    title_font=dict(size=25, color='black')
                ),
                yaxis=dict(
                    title="Liczba edycji",
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='gray',
                    zeroline=False,
                    title_font=dict(size=25, color='black'),
                    # range=[0, 25],
                    tickfont=dict(size=15, color='black'),
                ),
                height=550,
                width=1200,
            )
            st.plotly_chart(fig6, use_container_width=True)
        elif tournament == 'Liga Europy':
            fig6.add_trace(
                go.Bar(
                    # orientation='h',
                    x=list(wystepy_ul.keys()),
                    y=list(wystepy_ul.values()),
                    text=list(wystepy_ul.values()),
                    textfont=dict(size=13, color='white'),
                    textposition='inside',
                    marker=dict(color='orange'),
                    # insidetextanchor='middle',
                    hoverlabel=dict(
                        font=dict(size=14, color='black'),
                        bgcolor='orange'
                    ),
                    hovertemplate="Liczba edycji Ligi Europy: <b>%{y}</b>"
                    + "<extra></extra>"
                )
            )
            fig6.update_layout(
                margin=dict(l=0, r=0, t=25, b=0),
                xaxis=dict(
                    title='Drużyna',
                    tickfont=dict(size=12.5, color='black'),
                    title_font=dict(size=25, color='black')
                ),
                yaxis=dict(
                    title="Liczba edycji",
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='gray',
                    zeroline=False,
                    title_font=dict(size=25, color='black'),
                    # range=[0, 25],
                    tickfont=dict(size=15, color='black'),
                ),
                height=550,
                width=1300,
            )
            st.plotly_chart(fig6, use_container_width=True)
        st.write('Może wzbudzać pewnien niepokój fakt, że suma udziałów niektórych \
                 drużyn w turniejach przekracza liczbę sezonów, które miały miejsce \
                 od początku rozgrywek Premier League (31). \
                 Od pewnego czasu drużyny, które spadają z Ligi Mistrzów, mają \
                 możliwość kontynuowania swojej przygody w niższych rozgrywkach.'
        )
    else:
        st.header('Zawodnicy Premier League')
        choose_kind_of_players = st.multiselect(
            "Wybierz :",
            [
                'Anglicy',
                'cudzoziemcy'
            ],
            default='Anglicy'
        )
        fig16 = go.Figure()
        for category in choose_kind_of_players:
            if category == 'Anglicy':
                fig16.add_trace(
                    go.Scatter(
                        x=players['season'],
                        y=players['england'],
                        stackgroup='one',
                        marker=dict(color='green'),
                        name='Anglicy',
                        hovertemplate="Anglicy: <b>%{y}</b>"
                        + "<extra></extra>"
                    )
                )
            elif category == 'cudzoziemcy':
                fig16.add_trace(
                    go.Scatter(
                        x=players['season'],
                        y=players['foreigners'],
                        marker=dict(color='red'),
                        stackgroup='one',
                        name='cudzoziemcy',
                        hovertemplate="cudzoziemcy: <b>%{y}</b>"
                        + "<extra></extra>"
                    )
                )
        if len(choose_kind_of_players) == 2:
            fig16.add_trace(
                go.Scatter(
                    x=players['season'],
                    y=players['squad'],  # Suma piłkarzy
                    mode='markers',
                    marker=dict(color='rgba(0, 0, 0, 0)'),
                    hovertemplate="Wszyscy: <b>%{y}</b>"
                    + "<extra></extra>",
                    showlegend=False,  # Wyłączanie legendy
                )
            )
        fig16.update_layout(
            margin=dict(l=50, r=50, t=50, b=0),
            showlegend=True,
            xaxis=dict(
                tickangle=30,
                range=[0, 30],
                title='Sezon',
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=12, color='black'),
            ),
            yaxis=dict(
                range=[0, 850],
                title='Liczba zawodników',
                tickfont=dict(size=17, color='black'),
                title_font=dict(size=25, color='black'),
                showgrid=True,
                gridwidth=1,
                gridcolor='black',
                zerolinecolor='black'
            ),
            hoverlabel=dict(
                font=dict(
                    size=15,
                    color='black'
                )
            ),
            legend=dict(
                title=dict(
                    text='Narodowość',
                    font=dict(size=25, color='black')
                ),
                font=dict(size=17, color='black'),
                y=0.99,
                x=1.02
            ),
            height=500,
            width=1200,
            hovermode='x unified',
        )
        st.plotly_chart(fig16, use_container_width=True)
        st.markdown(
            """
            Piłkarz jest kwalifikowany jako zawodnik, jeśli spełnia co najmniej jeden z poniższych warunków:
            1. jest związany kontraktem z drużyną,
            2. rozegrał przynajmniej jeden mecz z drużyną (np. w pucharze).
            """
        )
        st.header('Strzelone bramki')
        fig5 = go.Figure()
        season_goals = (
            df.groupby("Season")[["FTHG", "FTAG"]]
            .sum()
            .sort_values(by="Season", ascending=False)
        )
        season_total_goals = season_goals.sum(axis=1).reset_index(
                                name='liczba bramek'
        )
        sorted_seasons = [
            '92/93', '93/94', '94/95', '95/96', '96/97',
            '97/98', '98/99', '99/00', '00/01', '01/02',
            '02/03', '03/04', '04/05', '05/06', '06/07',
            '07/08', '08/09', '09/10', '10/11', '11/12',
            '12/13', '13/14', '14/15', '15/16', '16/17',
            '17/18', '18/19', '19/20', '20/21', '21/22',
            '22/23'
        ]
        season_total_goals["Season"] = pd.Categorical(
            season_total_goals["Season"], sorted_seasons
        )
        season_total_goals = season_total_goals.sort_values('Season')
        fig5.add_trace(
            go.Bar(
                x=season_total_goals['Season'],
                y=season_total_goals['liczba bramek'],
                text=season_total_goals['liczba bramek'],
                textposition='outside',
                textfont=dict(size=13, color='black'),
                hoverlabel=dict(
                    font=dict(size=14, color='white'),
                    bgcolor='blue'
                ),
                marker_color='blue',
                hovertemplate="Liczba strzelonych bramek: <b>%{y}</b>"
                + "<extra></extra>"
            )
        )
        fig5.update_layout(
            margin=dict(l=25, r=0, t=25, b=0),
            xaxis=dict(
                range=[-0.5, 30.5],
                title='Sezon',
                tickfont=dict(size=13, color='black'),
                title_font=dict(size=25, color='black')
            ),
            yaxis=dict(
                title="Liczba strzelonych bramek",
                title_font=dict(size=25, color='black'),
                range=[0, 1300],
                tickfont=dict(size=15, color='black'),
                showgrid=True,
                gridwidth=0.5,
                gridcolor='rgba(211, 211, 211, 1)',
                zeroline=False,
            ),
            height=500,
            width=1400,
        )
        st.plotly_chart(fig5, use_container_width=True)
        st.header('Zwycięzcy Premier League')
        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                x=p_l.index,
                y=p_l['zwyciezca'],
                text=p_l['zwyciezca'],
                # x=p_l.index,
                # y=p_l['count'],
                # text=p_l['count'],
                textfont=dict(size=15, color='white'),
                textangle=0,
                hoverlabel=dict(
                    font=dict(size=14, color='white'),
                    bgcolor='blue'
                ),
                marker_color='blue',
                hovertemplate='Liczba tytułów: <b>%{y}</b><extra></extra>',
            )
        )
        fig.update_layout(
            margin=dict(l=50, r=50, t=15, b=50),
            xaxis=dict(
                title='Nazwa drużyny',
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=15, color='black')
            ),
            yaxis=dict(
                title='Liczba tytułów',
                title_font=dict(size=25, color='black'),
                range=[0, 15],
                tickfont=dict(size=15, color='black'),
                showgrid=True,
                gridwidth=1,
                gridcolor='gray',
                zeroline=False,
                zerolinewidth=0
            ),
            height=500,
            width=1200,
        )
        st.plotly_chart(fig, use_container_width=True)

        st.header('Zdobyte puchary krajowe')
        puchary = st.multiselect(
            'Wybierz puchar :', ['Fa cup', 'Carabao cup'],
            default=['Fa cup']
        )
        fig1 = go.Figure()

        for puchar in puchary:
            if puchar == 'Fa cup':
                fig1.add_trace(
                    go.Bar(
                        x=cup2.index,
                        y=cup2['Fa_cup'],
                        name='Fa Cup',
                        text=cup2['Fa_cup'],
                        # x=cup2.index,
                        # y=cup2['count'],
                        # name='Fa Cup',
                        # text=cup2['count'],
                        # hoverlabel=dict(font=dict(size=14, color='white'), bgcolor='red'),
                        hovertemplate='Liczba tytułów FA Cup: <b>%{y}</b>'
                        + '<extra></extra>',
                        textfont=dict(size=15, color='white'),
                        showlegend=True
                    )
                )
            elif puchar == 'Carabao cup':
                fig1.add_trace(
                    go.Bar(
                        x=cup1.index,
                        y=cup1['Carabao_cup'],
                        name='Carabao Cup',
                        text=cup1['Carabao_cup'],
                        # x=cup1.index,
                        # y=cup1['count'],
                        # name='Carabao Cup',
                        # text=cup1['count'],
                        # hoverlabel=dict(font=dict(size=14, color='white'), bgcolor='green'),
                        hovertemplate='Liczba tytułów Carabao Cup: <b>%{y}</b>'
                        + '<extra></extra>',
                        textfont=dict(size=15, color='white'),
                        showlegend=True
                    )
                )
        fig1.update_traces(
            selector=dict(type='bar', name='Fa Cup'),
            marker_color='red'
        )
        fig1.update_traces(
            selector=dict(type='bar', name='Carabao Cup'),
            marker_color='green'
        )
        fig1.update_layout(
            barmode='relative',
            margin=dict(l=50, r=50, t=35, b=50),
            hovermode='x unified',
            hoverlabel=dict(
                font=dict(
                    size=15,
                    color='black'
                )
            ),
            xaxis=dict(
                title='Nazwa drużyny',
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=13, color='black')
            ),
            yaxis=dict(
                title='Liczba pucharów',
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=15, color='black'),
                showgrid=True,
                gridwidth=1,
                gridcolor='gray',
                zeroline=False,
            ),
            height=500,
            width=1200,
            legend=dict(
                title=dict(
                    text="Puchar",
                    font=dict(size=25, color='black')
                ),
                font=dict(size=20, color='black'),
                y=1,
                x=1.02,
            )
        )
        st.plotly_chart(fig1, use_container_width=True)
        st.write('Powyższy wykres przedstawia zdobyte puchary od sezonu, \
                 w którym rozpoczęły się rozgrywki Premier League.')
        st.header('Liczba rozegranych sezonów w Premier League')
        season_dict = {
            '1992': '92/93',
            '1993': '93/94',
            '1994': '94/95',
            '1995': '95/96',
            '1996': '96/97',
            '1997': '97/98',
            '1998': '98/99',
            '1999': '99/00',
            '2000': '00/01',
            '2001': '01/02',
            '2002': '02/03',
            '2003': '03/04',
            '2004': '04/05',
            '2005': '05/06',
            '2006': '06/07',
            '2007': '07/08',
            '2008': '08/09',
            '2009': '09/10',
            '2010': '10/11',
            '2011': '11/12',
            '2012': '12/13',
            '2013': '13/14',
            '2014': '14/15',
            '2015': '15/16',
            '2016': '16/17',
            '2017': '17/18',
            '2018': '18/19',
            '2019': '19/20',
            '2020': '20/21',
            '2021': '21/22',
            '2022': '22/23'
        }
        slider = st.slider(
            'Wybierz przedział czasowy :', 1992, 2022, (1992, 2022), 1
        )
        selected_seasons = [
            season_dict[str(year)] for year in range(slider[0], slider[1] + 1)
        ]
        team_and_number_of_seasons = pd.DataFrame(
            df[df['Season'].astype(str).isin(selected_seasons)]
            .groupby("Season")["AwayTeam"]
            .unique()
            .explode()
            .value_counts()
        )
        team_and_number_of_seasons.rename(
            columns={'AwayTeam': 'Liczba sezonów'},
            inplace=True
        )
        team_and_number_of_seasons = team_and_number_of_seasons.reindex(
            unique_teams, fill_value=0
        )
        sorted_option = st.selectbox(
            'Jak chcesz posortować?',
            [
                'Malejąco liczebnościami',
                'Rosnąco liczebnościami',
                'Malejąco alfabetycznie',
                'Rosnąco alfabetycznie'
            ]
        )
        if sorted_option == 'Malejąco liczebnościami':
            team_and_number_of_seasons = team_and_number_of_seasons.sort_values(
                by='Liczba sezonów', ascending=True
            )
        elif sorted_option == 'Rosnąco liczebnościami':
            team_and_number_of_seasons = team_and_number_of_seasons.sort_values(
                by="Liczba sezonów", ascending=False
            )
        elif sorted_option == 'Malejąco alfabetycznie':
            team_and_number_of_seasons = team_and_number_of_seasons.sort_index(
                ascending=True
            )
        elif sorted_option == 'Rosnąco alfabetycznie':
            team_and_number_of_seasons = team_and_number_of_seasons.sort_index(
                ascending=False
            )
        fig10 = go.Figure()
        fig10.add_traces(
            go.Bar(
                y=team_and_number_of_seasons.index,
                x=team_and_number_of_seasons['Liczba sezonów'],
                # y=team_and_number_of_seasons.index,
                # x=team_and_number_of_seasons['count'],
                orientation='h',
                marker=dict(color='purple'),
                textfont=dict(size=16, color='white'),
                hoverlabel=dict(
                    font=dict(size=15, color='white'),
                    bgcolor='purple'
                ),
                hovertemplate='Liczba rozegranych sezonów: <b>%{x}</b>'
                + '<extra></extra>',
                showlegend=False
            )
        )
        fig10.update_layout(
            margin=dict(l=50, r=0, t=50, b=0),
            xaxis=dict(
                    title='Liczba sezonów w Premier League',
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='gray',
                    title_font=dict(size=25, color='black'),
                    tickfont=dict(size=14, color='black'),

            ),
            yaxis=dict(
                title='Nazwa drużyny',
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=12, color='black'),
                showgrid=False,
                gridwidth=0,
                gridcolor='gray',
                zeroline=False,
            ),
            height=850,
            width=1200,

        )
        st.plotly_chart(fig10, use_container_width=True)
        st.write(
            'Wybrany przedział lat odnosi się do początku sezonu. \
            Na przykład, jeśli wybierzesz przedział od 1992 do 1994,\
            obejmie to sezony począwszy od 1992/93 do 1994/95 (włącznie).'
        )


elif selected_tab == "Drużyny":
    st.markdown('---')
    st.header('Ewolucja liczby punktów w sezonie')
    comparison_type = st.radio(
        "Co chcesz porównać?",
        ("Drużyny", "Sezony")
    )
    if comparison_type == "Drużyny":
        column1, column2 = st.columns(2)
        selected_season = column1.selectbox("Wybierz sezon :", get_seasons(df)[::-1])
        teams1 = column2.multiselect(
            "Wybierz drużyny :",
            return_teams_for_season(selected_season, df),
            default=['Arsenal', 'Chelsea']
        )
        fig2 = go.Figure()
        max_value0 = 0
        symbols0 = [
            'circle', 'square',  'cross', 'x',
            'diamond', 'star-square', 'hexagram',
            'diamond-tall', 'star'
        ]
        number_of_colors_used0 = defaultdict(int)
        for team in teams1:
            club1 = calculate_points(df, team, selected_season)
            if club1['Punkty'].max() > max_value0:
                max_value0 = club1['Punkty'].max()
            color0, hex0 = [(i, j) for i, j in new_color_dict[team].items()][0]
            number_of_colors_used0[color0] += 1
            fig2.add_trace(
                go.Scatter(
                    x=club1['Kolejka'],
                    y=club1['Punkty'],
                    mode='lines+markers',
                    marker=dict(
                        color=hex0,
                        symbol=symbols0[number_of_colors_used0[color0] - 1],
                        line=dict(width=1.5)
                    ),
                    name=f'{team}',
                    hovertext=[
                        f"Punkty drużyny {team}: <b>{points}</b>" for points in club1['Punkty']
                    ],
                    hovertemplate="%{hovertext}<extra></extra>"
                )
            )
        fig2.update_layout(
                margin=dict(l=50, r=50, t=50, b=50),
                showlegend=True,
                xaxis=dict(
                    ticks="outside",
                    ticklen=4,
                    tickcolor='black',
                    range=(
                        [-0.5, 43]
                        if (
                            "92/93" in selected_season
                            or "93/94" in selected_season
                            or "94/95" in selected_season
                        )
                        else [-0.5, 39]
                    ),
                    title='Kolejka',
                    showline=True,
                    title_font=dict(size=25, color='black'),
                    tickfont=dict(size=17, color='black'),
                ),
                yaxis=dict(
                    title='Punkty',
                    range=[-2, round(max_value0, -1) + 7],
                    tickfont=dict(size=17, color='black'),
                    title_font=dict(size=25, color='black'),
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='gray',
                    zerolinecolor='white'
                ),
                hoverlabel=dict(
                    font=dict(
                        size=15,
                        color='black'
                    )
                ),
                legend=dict(
                    title=dict(
                        text='Drużyna',
                        font=dict(size=25, color='black')
                    ),
                    font=dict(size=17, color='black'),
                    y=0.99,
                    x=1.02
                ),
                height=500,
                width=1200,
                hovermode='x unified',
            )
        st.plotly_chart(fig2, use_container_width=True)
        st.write('Mecze w piłce nożnej czasem są przekładane ze względu na m.in inne rozgrywki (pucharowe).\
                 W tym celu u nas kolejka oznacza **numer meczu w sezonie** w celu zachowania ciągłości.')
    if comparison_type == "Sezony":
        c1, c2 = st.columns(2)
        club = c1.selectbox("Wybierz drużynę :", sorted(unique_teams))
        seasons = find_common_seasons(club, club, df)
        selected_seasons1 = c2.multiselect(
            "Wybierz sezony :", seasons[::-1],
            default=seasons[-2:][::-1]
        )
        fig3, max_value1 = go.Figure(), []
        for season2 in selected_seasons1:
            chart_season = calculate_points(df, club, season2)
            max_value1.append(chart_season['Punkty'].max())
            fig3.add_trace(
                go.Scatter(
                    x=chart_season['Kolejka'],
                    y=chart_season['Punkty'],
                    mode='lines+markers',
                    name=season2,
                    showlegend=True,
                    hovertext=[
                        f"Punkty drużyny {club} w sezonie {season2}: <b>{points}</b>"
                        for points in chart_season["Punkty"]
                    ],
                    hovertemplate="%{hovertext}<extra></extra>"
                )
            )
        fig3.update_layout(
                margin=dict(l=20, r=20, t=60, b=50),
                height=500,
                xaxis=dict(
                    ticks="outside",
                    ticklen=4,
                    tickcolor='black',
                    showline=True,
                    title='Kolejka',
                    title_font=dict(size=25, color='black'),
                    tickfont=dict(size=17, color='black'),
                    range=(
                        [-0.5, 43]
                        if (
                            "92/93" in selected_seasons1
                            or "93/94" in selected_seasons1
                            or "94/95" in selected_seasons1
                        )
                        else [-0.5, 39]
                    )
                ),
                yaxis=dict(
                    title='Kolejka',
                    title_font=dict(size=25, color='black'),
                    range=[-2, round(max(max_value1, default=0), -1) + 7],
                    tickfont=dict(size=17, color='black'),
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='black',
                    zerolinecolor='white'
                ),
                legend=dict(
                    title=dict(
                        text="Sezon",
                        font=dict(size=25, color='black')
                    ),
                    font=dict(size=20, color='black'),
                    orientation="v",
                    yanchor="top",
                    y=1,
                    xanchor="right",
                    x=1.11
                ),
                width=1200,
                hovermode='x unified',
                hoverlabel=dict(
                    font=dict(
                        size=15,
                        color='black'
                    )
                ),
        )
        st.plotly_chart(fig3, use_container_width=True)
    st.header('Rezultaty bezpośrednich starć dwóch drużyn')
    col1, col2 = st.columns(2)
    team3 = col1.selectbox(
        "Wybierz pierwszą drużynę :",
        unique_teams,
        key='rezultaty'
    )
    team4 = col2.selectbox(
        'Wybierz drugą drużynę :',
        return_opponents(df=df, team=team3),
        key='rezultaty1'
    )
    color = choose_color_for_teams(team3, team4)
    fig4 = go.Figure()
    result = head_to_head_results(df, team3, team4)
    colors1 = [color[team3], '#cd7f32', color[team4]]
    fig4.add_traces(
        go.Bar(
            x=result['result'],
            y=result['count'],
            text=result['count'],
            textfont=dict(size=17, color='white'),
            showlegend=False,
            marker=dict(color=colors1),
            hoverlabel=dict(
                font=dict(size=15, color='white'),
                bgcolor=colors1
            ),
            hovertemplate=[
                f'Liczba zwycięstw drużyny {team3}: <b>%{{y}}</b>'
                + '<extra></extra><br>',
                f'Liczba remisów: <b>%{{y}}</b> <extra></extra><br>',
                f'Liczba zwycięstw drużyny {team4}: <b>%{{y}}</b>'
                + '<extra></extra>'
            ]
        )
    )
    fig4.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(color=color[team3], size=10),
            name=f'Liczba zwycięstw drużyny {team3}'
        )
    )
    fig4.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(color='#cd7f32', size=10),
            name='Liczba remisów'
        )
    )
    fig4.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(color=color[team4], size=10),
            name=f'Liczba zwycięstw drużyny {team4}'
        )
    )

    fig4.update_layout(
        margin=dict(l=50, r=50, t=50, b=50),
        xaxis=dict(
            title='Wyniki starcia',
            tickfont=dict(size=16, color='black'),
            title_font=dict(size=25, color='black')
        ),
        yaxis=dict(
            title="Liczba rezultatów",
            title_font=dict(size=25, color='black'),
            # range=[
            #     0,
            #     int(max(result['count'])) + (2 if max(result['count']) > 7 else 0)
            # ],
            tickfont=dict(size=16, color='black'),
            showgrid=True,
            gridwidth=1,
            gridcolor='gray',
            zeroline=False,
        ),
        legend=dict(font=dict(size=16), y=1.03),
        height=500,
        width=1200,
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.header('Porównanie bramek strzelonych i straconych względem połowy meczu')
    comparison_type1 = st.radio(
        "Co chcesz porównać?",
        ("Drużyny", "Sezony"), key="comparison_type1"
    )
    seasons_to_remove = ['92/93', '93/94', '94/95']
    if comparison_type1 == 'Drużyny':
        column3, column4 = st.columns(2)
        scored_or_conceded = st.selectbox(
            "Wybierz statystykę : ",
            ['Bramki strzelone', 'Bramki stracone']
        )
        season3 = column3.selectbox(
            "Wybierz sezon :",
            [season5 for season5 in get_seasons(df) if season5 not in seasons_to_remove][::-1]
        )
        teams6 = column4.multiselect(
            "Wybierz drużyny :",
            return_teams_for_season(season3, df),
            default=['Chelsea', 'Arsenal']
        )
        fig7 = go.Figure()
        conceded_and_scored_goals = pd.DataFrame()
        for team in teams6:
            df_c3 = calculate_lost_goals_by_half(df, team, season3)
            conceded_and_scored_goals = pd.concat([conceded_and_scored_goals, df_c3])
        maksimum = max(
            conceded_and_scored_goals['GSWPP'].max(),
            conceded_and_scored_goals['GSWDP'].max(),
            #conceded_and_scored_goals['TotalGoalsScored'].max()
        )
        if scored_or_conceded == 'Bramki strzelone':
            symbols1 = ['', '/', '\\', 'x', '-', '|', '+', '.']
            number_of_colors_used1 = defaultdict(int)
            for i, name in enumerate(teams6):
                color1, hex1 = [(x, j) for x, j in new_color_dict[name].items()][0]
                number_of_colors_used1[color1] += 1
                fig7.add_traces(
                    data=[
                        go.Bar(
                            x=['Pierwsza', 'Druga'],
                            y=[
                                conceded_and_scored_goals['GSWPP'].iloc[i],
                                conceded_and_scored_goals['GSWDP'].iloc[i],
                            ],
                            marker=dict(
                                color='gray' if number_of_colors_used1[color1] > 1 else hex1,
                                pattern_shape=symbols1[number_of_colors_used1[color1] - 1],
                                pattern_bgcolor=hex1
                            ),
                            text=[
                                conceded_and_scored_goals['GSWPP'].iloc[i],
                                conceded_and_scored_goals['GSWDP'].iloc[i],
                            ],
                            textfont = (
                                dict(
                                    size=18,
                                    color="white" if "yellow" not in color1 and "orange" not in color1 else "black",
                                )
                            ),
                            hovertemplate=[
                                f'Liczba strzelonych bramek drużyny {name}: <b>%{{y}}</b>'
                                + '<extra></extra>',
                                f'Liczba strzelonych bramek drużyny {name}: <b>%{{y}}</b>'
                                + '<extra></extra>'
                            ],
                            name=name
                        )
                    ]
                )
            fig7.update_layout(
                barmode='group',
                hovermode="x unified",
                hoverlabel=dict(
                    font=dict(
                        size=15,
                        color='black'
                    )
                ),
                showlegend=True,
                margin=dict(l=25, r=25, t=25, b=25),
                #margin=dict(l=50, r=50, t=50, b=50),
                xaxis=dict(
                    title='Połowa meczu',
                    title_font=dict(size=25, color='black'),
                    tickfont=dict(size=17, color='black')
                ),
                yaxis=dict(
                    range=[0, maksimum + 6],
                    title='Liczba bramek strzelonych',
                    title_font=dict(size=25, color='black'),
                    tickfont=dict(size=17, color='black'),
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='gray',
                    zeroline=False,
                    zerolinewidth=0
                ),
                legend=dict(
                    title=dict(
                        text="Drużyna",
                        font=dict(size=25, color='black')
                    ),
                    font=dict(size=17),
                    y=1.05,
                    x=1.02
                ),
                height=500,
                width=1200
            )
        if scored_or_conceded == 'Bramki stracone':
            fig7 = go.Figure()
            symbols2 = ['', '/', '\\', 'x', '-', '|', '+', '.']
            number_of_colors_used2 = defaultdict(int)
            for i, name in enumerate(teams6):
                color2, hex2 = [(x, j) for x, j in new_color_dict[name].items()][0]
                number_of_colors_used2[color2] += 1
                fig7.add_traces(data=[
                    go.Bar(
                        x=['Pierwsza', 'Druga'],
                        y=[
                            conceded_and_scored_goals['GSTWPP'].iloc[i],
                            conceded_and_scored_goals['GSTWDP'].iloc[i]],
                        marker=dict(
                            color='gray' if number_of_colors_used2[color2] > 1 else hex2,
                            pattern_shape=symbols2[number_of_colors_used2[color2] - 1],
                            pattern_bgcolor=hex2
                        ),
                        text=[
                            conceded_and_scored_goals['GSTWPP'].iloc[i],
                            conceded_and_scored_goals['GSTWDP'].iloc[i]],
                        textfont=dict(size=18, color="white" if "yellow" not in color2 and "orange" not in color2 else "black",),
                        hovertemplate=[
                            f'Liczba straconych bramek drużyny {name}: <b>%{{y}}</b>'
                            + '<extra></extra>',
                            f'Liczba straconych bramek drużyny {name}: <b>%{{y}}</b>'
                            + '<extra></extra>'
                        ],
                        name=name
                    )]
                )
            fig7.update_layout(
                barmode='group',
                hovermode="x unified",
                hoverlabel=dict(
                    font=dict(
                        size=15,
                        color='black'
                    )
                ),
                showlegend=True,
                margin=dict(l=50, r=50, t=50, b=50),
                xaxis=dict(
                    title='Połowa',
                    title_font=dict(size=25, color='black'),
                    tickfont=dict(size=16, color='black')
                ),
                yaxis=dict(
                    title='Liczba bramek straconych',
                    title_font=dict(size=25, color='black'),
                    tickfont=dict(size=16, color='black'),
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='gray',
                    zeroline=False,
                    zerolinewidth=0
                ),
                legend=dict(
                    title=dict(
                        text="Drużyna",
                        font=dict(size=25, color='black')
                    ),
                    font=dict(size=17),
                    y=1.05,
                    x=1.02
                ),
                height=500,
                width=1200
            )
        st.plotly_chart(fig7, use_container_width=True)
    if comparison_type1 == 'Sezony':
        seasons_to_remove = ['92/93', '93/94', '94/95']
        filtered_df = df[~df['Season'].isin(seasons_to_remove)]
        unique_home_teams = filtered_df['HomeTeam'].unique().tolist()
        #colors2 = ['#FFA500', '#FFC0CB', '#FFFF00', '#00FFFF', '#FF00FF']
        column6, column7 = st.columns(2)
        club3 = column6.selectbox(
            "Wybierz drużynę :",
            sorted(unique_home_teams),
            key='t'
        )
        seasons1 = find_common_seasons(club3, club3, filtered_df)[::-1]
        #excluded_seasons1 = ['92/93', '93/94', '94/95']
        season3 = column7.multiselect(
            "Wybierz sezony :",
            seasons1,
            #[season4 for season4 in seasons1 if season4 not in excluded_seasons1][::-1],
            default=seasons1[:2],
        )
        scored_or_conceded = st.selectbox(
            "Wybierz statystykę : ",
            ['Bramki strzelone', 'Bramki stracone']
        )
        fig7 = go.Figure()
        if scored_or_conceded == 'Bramki strzelone':
            for i, season in enumerate(season3):
                df_c3 = calculate_lost_goals_by_half(df, club3, season)
                fig7.add_traces(data=[
                    go.Bar(
                        x=['Pierwsza', 'Druga'],
                        y=[df_c3['GSWPP'].iloc[0], df_c3['GSWDP'].iloc[0]],
                        text=[df_c3['GSWPP'].iloc[0], df_c3['GSWDP'].iloc[0]],
                        textfont=dict(size=18, color='black'),
                        hovertemplate=[
                            f'Liczba strzelonych bramek w sezonie {season}: <b>%{{y}}</b>'
                            + '<extra></extra>',
                            f'Liczba strzelonych bramek w sezonie {season}: <b>%{{y}}</b>'
                            + '<extra></extra>'
                        ],
                        #marker=dict(color=colors2[i]),
                        name=season
                    )]
                )
            fig7.update_layout(
                barmode='group',
                hovermode="x unified",
                hoverlabel=dict(
                    font=dict(
                        size=15,
                        color='white'
                    )
                ),
                showlegend=True,
                margin=dict(l=50, r=50, t=50, b=50),
                xaxis=dict(
                    title='Połowa meczu',
                    title_font=dict(size=25, color='black'),
                    tickfont=dict(size=17, color='black')
                ),
                yaxis=dict(
                    title='Liczba bramek strzelonych',
                    title_font=dict(size=25, color='black'),
                    tickfont=dict(size=17, color='black'),
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='gray',
                    zeroline=False,
                    zerolinewidth=0
                ),
                legend=dict(
                    title=dict(
                        text="Sezon",
                        font=dict(size=25, color='black')
                    ),
                    font=dict(size=17),
                    y=1.05,
                    x=1.02
                ),
                height=500,
                width=1200
            )
            st.plotly_chart(fig7, use_container_width=True)
        elif scored_or_conceded == 'Bramki stracone':
            for i, season in enumerate(season3):
                df_c3 = calculate_lost_goals_by_half(df, club3, season)
                fig7.add_traces(data=[
                    go.Bar(
                        x=['Pierwsza', 'Druga'],
                        y=[df_c3['GSTWPP'].iloc[0], df_c3['GSTWDP'].iloc[0]],
                        text=[df_c3['GSTWPP'].iloc[0], df_c3['GSTWDP'].iloc[0]],
                        textfont=dict(size=18, color='black'),
                        hovertemplate=[
                            f'Liczba straconych bramek w sezonie {season}: <b>%{{y}}</b>'
                            + '<extra></extra>',
                            f'Liczba straconych bramek w sezonie {season}: <b>%{{y}}</b>'
                            + '<extra></extra>'
                        ],
                        name=season,
                        #marker=dict(color=colors2[i])
                    )]
                )
            fig7.update_layout(
                barmode='group',
                hovermode="x unified",
                hoverlabel=dict(
                    font=dict(
                        size=15,
                        color='white'
                        )
                ),
                showlegend=True,
                margin=dict(l=50, r=50, t=50, b=50),
                xaxis=dict(
                    title='Połowa meczu',
                    title_font=dict(size=25, color='black'),
                    tickfont=dict(size=17, color='black')
                ),
                yaxis=dict(
                    title='Liczba bramek straconych',
                    title_font=dict(size=25, color='black'),
                    tickfont=dict(size=17, color='black'),
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='gray',
                    zeroline=False,
                    zerolinewidth=0
                ),
                legend=dict(
                    title=dict(
                        text="Sezon",
                        font=dict(size=25, color='black')
                    ),
                    font=dict(size=17),
                    y=1.05,
                    x=1.02
                ),
                height=500,
                width=1200
            )
            st.plotly_chart(fig7, use_container_width=True)
    st.header('Porównanie punktów zdobytych u siebie i na wyjeździe')
    comparison_type2 = st.radio(
        "Co chcesz porównać?",
        ("Drużyny", "Sezony"), key='ct2'
    )
    if comparison_type2 == 'Drużyny':
        fig8 = go.Figure()
        col1, col2 = st.columns(2)
        season0 = col1.selectbox(
            'Wybierz sezon :',
            get_seasons(df)[::-1],
            key='porównanie_pkt'
        )
        teams2 = col2.multiselect(
            "Wybierz drużyny :",
            return_teams_for_season(season0, df),
            default=['Chelsea', 'Arsenal'],
            key='porownanie_pkt1'
        )
        symbols3 = ['', '/', '\\', 'x', '-', '|', '+', '.']
        number_of_colors_used3 = defaultdict(int)
        for i, team in enumerate(teams2):
            color3, hex3 = [(x, j) for x, j in new_color_dict[team].items()][0]
            number_of_colors_used3[color3] += 1
            data_for_graph = calculate_home_away_points(df, season0, team)
            fig8.add_trace(
                go.Bar(
                    x=list(data_for_graph.keys()),
                    y=list(data_for_graph.values()),
                    marker=dict(
                        color='gray' if number_of_colors_used3[color3] > 1 else hex3,
                        pattern_shape=symbols3[number_of_colors_used3[color3] - 1],
                        pattern_bgcolor=hex3
                    ),
                    text=list(data_for_graph.values()),
                    textfont=dict(size=18, color="white" if "yellow" not in color3 and "orange" not in color3 else "black",),
                    hovertemplate=[
                        f'Punkty domowe drużyny {team}: <b>%{{y}}</b>'
                        + '<extra></extra>',
                        f'Punkty wyjazdowe drużyny {team} : <b>%{{y}}</b>'
                        + '<extra></extra>'
                    ],
                    name=team,
                )
            )
        fig8.update_layout(
                barmode='group',
                hovermode='x unified',
                showlegend=True,
                hoverlabel=dict(
                    font=dict(
                        size=15,
                        color='black'
                    )
                ),
                margin=dict(l=50, r=50, t=50, b=50),
                xaxis=dict(
                    title='Rodzaj meczu',
                    title_font=dict(size=25, color='black'),
                    tickfont=dict(size=16, color='black')
                ),
                yaxis=dict(
                    title='Liczba zdobytych punktów',
                    title_font=dict(size=25, color='black'),
                    tickfont=dict(size=16, color='black'),
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='gray',
                    zeroline=False,
                ),
                height=500,
                width=1200,
                legend=dict(
                    title=dict(
                        text="Drużyna",
                        font=dict(size=25, color='black')
                    ),
                    font=dict(size=17),
                    y=1.05,
                    x=1.02
                ),
            )
        st.plotly_chart(fig8, use_container_width=True)
    if comparison_type2 == 'Sezony':
        fig8 = go.Figure()
        col1, col2 = st.columns(2)
        team1 = col1.selectbox(
            'Wybierz drużynę :',
            sorted(unique_teams),
            key='Porównanie_pkt_u_siebie')
        seasons = find_common_seasons(team1, team1, df)
        selected_seasons = col2.multiselect(
            'Wybierz sezony :', seasons[::-1],
            default=seasons[-2:][::-1],
        )
        for i, season in enumerate(selected_seasons):
            data_for_graph = calculate_home_away_points(df, season, team1)
            fig8.add_trace(
                go.Bar(
                    x=list(data_for_graph.keys()),
                    y=list(data_for_graph.values()),
                    text=list(data_for_graph.values()),
                    textfont=dict(size=18, color='black'),
                    hovertemplate=[
                        f'Punkty domowe w sezonie {season}: <b>%{{y}}</b>'
                        + '<extra></extra>',
                        f'Punkty wyjazdowe w sezonie {season} : <b>%{{y}}</b>'
                        + '<extra></extra>'
                    ],
                    name=season,
                )
            )
        fig8.update_layout(
                barmode='group',
                hovermode='x unified',
                showlegend=True,
                hoverlabel=dict(
                    font=dict(
                        size=15,
                        color='white'
                    )
                ),
                margin=dict(l=50, r=50, t=50, b=50),
                xaxis=dict(
                    title='Rodzaj meczu',
                    title_font=dict(size=25, color='black'),
                    tickfont=dict(size=16, color='black')
                ),
                yaxis=dict(
                    title='Liczba zdobytych punktów',
                    title_font=dict(size=25, color='black'),
                    tickfont=dict(size=16, color='black'),
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='gray',
                    zeroline=False,
                ),
                height=500,
                width=1200,
                legend=dict(
                    title=dict(
                        text="Sezon",
                        font=dict(size=25, color='black')
                    ),
                    font=dict(size=17),
                    y=1.02,
                    x=1.02
                ),
            )
        st.plotly_chart(fig8, use_container_width=True)
    st.header('Porównanie drużyn pod względem kartek\
               czerwonych, żółtych i liczby fauli')
    c1, c2 = st.columns(2)
    seasons_x = [
        '00/01', '01/02', '02/03', '03/04', '04/05', '05/06',
        '06/07', '07/08', '08/09', '09/10', '10/11', '11/12',
        '12/13', '13/14', '14/15', '15/16', '16/17', '17/18',
        '18/19', '19/20', '20/21', '21/22', '22/23'
    ]
    df2 = df[df['Season'].isin(seasons_x)]
    comparison_type5 = st.radio(
        "Co chcesz porównać?",
        ("Drużyny", "Sezony"),
        key='kartki'
    )
    fig11 = go.Figure()
    if comparison_type5 == "Drużyny":
        col0, col3 = st.columns(2)
        season12 = col0.selectbox(
            "Wybierz sezon :",
            seasons_x[::-1]
        )
        teams3 = col3.multiselect(
            "Wybierz drużyny :",
            return_teams_for_season(season12, df2),
            default=['Arsenal', 'Chelsea'],
            key='Kartki, faule'
        )
        symbols4 = ['', '/', '\\', 'x', '-', '|', '+', '.']
        number_of_colors_used4 = defaultdict(int)
        for team in teams3:
            color4, hex4 = [(x, j) for x, j in new_color_dict[team].items()][0]
            number_of_colors_used4[color4] += 1
            fauls = calculate_fauls_yellow_and_red_cards(
                season12,
                team,
                df
            )
            fig11.add_traces(
                go.Bar(
                    x=list(fauls.keys()),
                    y=list(fauls.values()),
                    marker=dict(
                        color='gray' if number_of_colors_used4[color4] > 1 else hex4,
                        pattern_shape=symbols4[number_of_colors_used4[color4] - 1],
                        pattern_bgcolor=hex4
                    ),
                    text=list(fauls.values()),
                    textfont=dict(size=18, color='black'),
                    textposition='outside',
                    hovertemplate=[
                        f'Faule bez kartki drużyny {team}: <b>%{{y}}</b>'
                        + '<extra></extra>',
                        f'Czerwone kartki drużyny {team} : <b>%{{y}}</b>'
                        + '<extra></extra>',
                        f'Żółte kartki drużyny {team} : <b>%{{y}}</b>'
                        + '<extra></extra>'
                    ],
                    name=team,
                )
            )
        fig11.update_layout(
            barmode='group',
            hovermode='x unified',
            showlegend=True,
            hoverlabel=dict(
                font=dict(
                    size=15,
                    color='black'
                )
            ),
            margin=dict(l=0, r=25, t=30, b=25),
            xaxis=dict(
                title='Rodzaj',
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=16, color='black')
            ),
            yaxis=dict(
                title='Liczba',
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=16, color='black'),
                showgrid=True,
                gridwidth=0.5,
                gridcolor='rgba(211, 211, 211, 1)',
                zeroline=False,
            ),
            height=500,
            width=1200,
            legend=dict(
                title=dict(
                    text="Drużyna",
                    font=dict(size=25, color='black')
                ),
                font=dict(size=17),
                y=1.02,
                x=1.02
            ),
        )
        st.plotly_chart(fig11, use_container_width=True)
    else:
        col0, col3 = st.columns(2)
        team12 = col0.selectbox(
            "Wybierz drużynę :",
            sorted(df2['HomeTeam'].unique())
        )
        seasons2 = col3.multiselect(
            "Wybierz sezony :",
            find_common_seasons(team12, team12, df2)[::-1],
            default=find_common_seasons(team12, team12, df2)[-2:][::-1]
        )
        for season in seasons2:
            fauls = calculate_fauls_yellow_and_red_cards(
                season,
                team12,
                df
            )
            fig11.add_traces(
                go.Bar(
                    x=list(fauls.keys()),
                    y=list(fauls.values()),
                    text=list(fauls.values()),
                    textfont=dict(size=18, color='black'),
                    textposition='outside',
                    hovertemplate=[
                        f'Faule bez kartki w sezonie {season}: <b>%{{y}}</b>'
                        + '<extra></extra>',
                        f'Czerwone kartki w sezonie {season} : <b>%{{y}}</b>'
                        + '<extra></extra>',
                        f'Żółte kartki w sezonie {season} : <b>%{{y}}</b>'
                        + '<extra></extra>'
                    ],
                    name=season,
                )
            )
        fig11.update_layout(
            barmode='group',
            hovermode='x unified',
            showlegend=True,
            hoverlabel=dict(
                font=dict(
                    size=15,
                    color='black'
                )
            ),
            margin=dict(l=0, r=25, t=30, b=25),
            xaxis=dict(
                title='Rodzaj',
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=16, color='black')
            ),
            yaxis=dict(
                title='Liczba',
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=16, color='black'),
                showgrid=True,
                gridwidth=0.5,
                gridcolor='rgba(211, 211, 211, 1)',
                zeroline=False,
            ),
            height=500,
            width=1200,
            legend=dict(
                title=dict(
                    text="Sezon",
                    font=dict(size=25, color='black')
                ),
                font=dict(size=17),
                y=1.02,
                x=1.02
            ),
        )
        st.plotly_chart(fig11, use_container_width=True)
    st.write('Kartki w piłce nożnej nie zawsze są \
             wynikiem fauli, mogą zostać pokazane \
             również za zachowania nie fair play.\
             Do tego trzeba zwrócić uwagę, że jeśli zawodnik otrzyma\
             drugą żółtą kartkę, a co za tym idzie czerwoną, wartość\
             jest dodawana **tylko** do czerwonych kartek.\
            Przykładowo jeśli drużyna A dostała dwie żółte kartki, \
            po czym jeden z wcześniej ukaranych zawodników wylatuje z boiska,\
            to bilans kartek w meczu wynosi odpowiednio dwie żółte i \
            jedną czerwoną kartkę.')
    st.header('Porównanie efektywności strzałów')
    seasons_y = [
        '06/07', '07/08', '08/09', '09/10', '10/11', '11/12',
        '12/13', '13/14', '14/15', '15/16', '16/17', '17/18',
        '18/19', '19/20', '20/21', '21/22', '22/23'
    ][::-1]
    df3 = df[df['Season'].isin(seasons_y)]
    comparison_type3 = st.radio(
        "Co chcesz porównać?",
        ("Drużyny", "Sezony"),
        key='shoot4'
    )
    if comparison_type3 == 'Drużyny':
        fig14 = go.Figure()
        col8, col9 = st.columns(2)
        season10 = col8.selectbox(
            "Wybierz sezon :",
            seasons_y
        )
        teams7 = col9.multiselect(
            "Wybierz drużyny :",
            return_teams_for_season(season10, df),
            default=['Arsenal', 'Chelsea'],
            key='efektywność'
        )
        symbols5 = ['', '/', '\\', 'x', '-', '|', '+', '.']
        number_of_colors_used5 = defaultdict(int)
        for team in teams7:
            color5, hex5 = [(x, j) for x, j in new_color_dict[team].items()][0]
            number_of_colors_used5[color5] += 1
            shoot = calculate_shots_stats(season10, team, clubstats)
            fig14.add_trace(
                go.Bar(
                    x=list(shoot.keys()),
                    y=list(shoot.values()),
                    marker=dict(
                        color='gray' if number_of_colors_used5[color5] > 1 else hex5,
                        pattern_shape=symbols5[number_of_colors_used5[color5] - 1],
                        pattern_bgcolor=hex5
                    ),
                    text=list(shoot.values()),
                    textfont=dict(size=18, color="white" if "yellow" not in color5 and "orange" not in color5 else "black"),
                    hovertemplate=[
                        f'Strzały celne drużyny {team}: <b>%{{y}}</b>'
                        + '<extra></extra>',
                        f'Strzały niecelne drużyny {team} : <b>%{{y}}</b>'
                        + '<extra></extra>'
                    ],
                    name=team,
                )
            )
        fig14.update_layout(
            barmode='group',
            hovermode='x unified',
            showlegend=True,
            hoverlabel=dict(
                font=dict(
                    size=15,
                    color='black'
                )
            ),
            margin=dict(l=50, r=50, t=50, b=50),
            xaxis=dict(
                title='Rodzaj strzałów',
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=16, color='black')
            ),
            yaxis=dict(
                title='Liczba strzałów',
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=16, color='black'),
                showgrid=True,
                gridwidth=1,
                gridcolor='gray',
                zeroline=False,
            ),
            height=500,
            width=1200,
            legend=dict(
                title=dict(
                    text="Drużyna",
                    font=dict(size=25, color='black')
                ),
                font=dict(size=17),
                y=1.05,
                x=1.02
            ),
        )
        st.plotly_chart(fig14, use_container_width=True)
    else:
        col10, col11 = st.columns(2)
        team13 = col10.selectbox(
            'Wybierz drużynę :',
            sorted(df3['HomeTeam'].unique().tolist()),
            key='shoot'
        )
        seasons13 = col11.multiselect(
            'Wybierz sezony :',
            find_common_seasons(team13, team13, df3)[::-1],
            key='shootteam',
            default=find_common_seasons(team13, team13, df3)[-2:][::-1],
        )
        fig14 = go.Figure()
        for i, season in enumerate(seasons13):
            shoot5 = calculate_shots_stats(season, team13, clubstats)
            fig14.add_trace(
                go.Bar(
                    x=list(shoot5.keys()),
                    y=list(shoot5.values()),
                    text=list(shoot5.values()),
                    textfont=dict(size=18, color='white'),
                    hovertemplate=[
                        f'Strzały celne w sezonie {season}: <b>%{{y}}</b>'
                        + '<extra></extra>',
                        f'Strzały niecelne w sezonie {season} : <b>%{{y}}</b>'
                        + '<extra></extra>'
                    ],
                    name=season,
                )
            )
        fig14.update_layout(
            barmode='group',
            hovermode='x unified',
            showlegend=True,
            hoverlabel=dict(
                font=dict(
                    size=15,
                    color='black'
                )
            ),
            margin=dict(l=50, r=50, t=50, b=50),
            xaxis=dict(
                title='Rodzaj strzałów',
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=16, color='black')
            ),
            yaxis=dict(
                title='Liczba strzałów',
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=16, color='black'),
                showgrid=True,
                gridwidth=1,
                gridcolor='gray',
                zeroline=False,
            ),
            height=500,
            width=1200,
            legend=dict(
                title=dict(
                    text="Sezon",
                    font=dict(size=25, color='black')
                ),
                font=dict(size=17),
                y=1.05,
                x=1.02
            ),
        )
        st.plotly_chart(fig14, use_container_width=True)
    st.header('Porównanie zdobytych bramek według rodzaju strzału')
    comparison_type4 = st.radio(
        "Co chcesz porównać?",
        ("Drużyny", "Sezony"),
        key='rodzaj_bramki'
    )
    fig15 = go.Figure()
    if comparison_type4 == "Drużyny":
        col4, col5 = st.columns(2)
        season11 = col4.selectbox(
            "Wybierz sezon :",
            seasons_y,
            key='rozkład'
        )
        teams8 = col5.multiselect(
            "Wybierz drużyny :",
            return_teams_for_season(season11, df),
            default=['Arsenal', 'Chelsea'],
            key='rozkład1'
        )
        symbols6 = ['', '/', '\\', 'x', '-', '|', '+', '.']
        number_of_colors_used6 = defaultdict(int)
        for team in teams8:
            color6, hex6 = [(x, j) for x, j in new_color_dict[team].items()][0]
            number_of_colors_used6[color6] += 1
            df4 = clubstats.query('team == @team and season == @season11')
            labels = [
                'Głową',
                'Z rzutu karnego',
                'Z rzutu wolnego',
                'Z pola karnego',
                'Spoza pola karnego',
                'Z kontrataku'
            ]
            values_row = df4.iloc[:, 9:15].values.tolist()[0]
            values = list(np.array(values_row).flatten())
            fig15.add_trace(go.Bar(
                x=labels,
                y=values,
                marker=dict(
                    color='gray' if number_of_colors_used6[color6] > 1 else hex6,
                    pattern_shape=symbols6[number_of_colors_used6[color6] - 1],
                    pattern_bgcolor=hex6
                ),
                text=values,
                textposition='outside',
                textfont=dict(size=18, color='black'),
                hovertemplate=[
                    f'Liczba bramek zdobytych głową drużyny {team}: <b>%{{y}}</b>'
                    + '<extra></extra>',
                    f'Bramki zdobyte z rzutu karnego drużyny {team} : <b>%{{y}}</b>'
                    + '<extra></extra>',
                    f'Bramki zdobyte z rzutu wolnego druzyny {team}: <b>%{{y}}</b>'
                    + '<extra></extra>',
                    f'Bramki zdobyte z pola karnego drużyny {team} : <b>%{{y}}</b>'
                    + '<extra></extra>',
                    f'Bramki zdobyte spoza pola karnego drużyny {team} : <b>%{{y}}</b>'
                    + '<extra></extra>',
                    f'Bramki zdobyte z kontrataku drużyny {team} : <b>%{{y}}</b>'
                    + '<extra></extra>'
                ],
                name=team,
            ))
        fig15.update_layout(
            barmode='group',
            hovermode='x unified',
            showlegend=True,
            hoverlabel=dict(
                font=dict(
                    size=15,
                    color='black'
                )
            ),
            margin=dict(l=0, r=25, t=45, b=0),
            xaxis=dict(
                title='Rodzaj strzału',
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=16, color='black')
            ),
            yaxis=dict(
                title='Liczba bramek',
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=16, color='black'),
                showgrid=True,
                gridwidth=0.5,
                gridcolor='rgba(211, 211, 211, 1)',
                zeroline=False,
            ),
            height=500,
            width=1200,
            legend=dict(
                title=dict(
                    text="Drużyna",
                    font=dict(size=25, color='black')
                ),
                font=dict(size=17),
                y=1.05,
                x=1.02
                ),
            )
        st.plotly_chart(fig15, use_container_width=True)
    else:
        col4, col5 = st.columns(2)
        team7 = col4.selectbox(
            "Wybierz drużynę :",
            sorted(df3['HomeTeam'].unique().tolist()),
            key='Rodzaj_bramki1'
        )
        seasons11 = col5.multiselect(
            "Wybierz sezony :",
            find_common_seasons(team7, team7, df3)[::-1],
            default=find_common_seasons(team7, team7, df3)[-2:][::-1],
            key='rozkład'
        )
        for season in seasons11:
            df4 = clubstats.query('team == @team7 and season == @season')
            labels = [
                'Głową',
                'Z rzutu karnego',
                'Z rzutu wolnego',
                'Z pola karnego',
                'Spoza pola karnego',
                'Z kontrataku'
            ]
            values_row = df4.iloc[:, 9:15].values.tolist()[0]
            values = list(np.array(values_row).flatten())
            fig15.add_trace(go.Bar(
                x=labels,
                y=values,
                text=values,
                textposition='outside',
                textfont=dict(size=18, color='black'),
                hovertemplate=[
                    f'Liczba bramek zdobytych głową w sezonie {season}: <b>%{{y}}</b>'
                    + '<extra></extra>',
                    f'Bramki zdobyte z rzutu karnego w sezonie {season} : <b>%{{y}}</b>'
                    + '<extra></extra>',
                    f'Bramki zdobyte z rzutu wolnego w sezonie {season}: <b>%{{y}}</b>'
                    + '<extra></extra>',
                    f'Bramki zdobyte z pola karnego w sezonie {season} : <b>%{{y}}</b>'
                    + '<extra></extra>',
                    f'Bramki zdobyte spoza pola karnego w sezonie {season} : <b>%{{y}}</b>'
                    + '<extra></extra>',
                    f'Bramki zdobyte z kontrataku w sezonie {season} : <b>%{{y}}</b>'
                    + '<extra></extra>'
                ],
                name=season,
            ))
        fig15.update_layout(
            barmode='group',
            hovermode='x unified',
            showlegend=True,
            hoverlabel=dict(
                font=dict(
                    size=15,
                    color='black'
                )
            ),
            margin=dict(l=0, r=25, t=45, b=0),
            xaxis=dict(
                title='Rodzaj strzału',
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=16, color='black')
            ),
            yaxis=dict(
                title='Liczba bramek',
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=16, color='black'),
                showgrid=True,
                gridwidth=0.5,
                gridcolor='rgba(211, 211, 211, 1)',
                zeroline=False,
            ),
            height=500,
            width=1200,
            legend=dict(
                title=dict(
                    text="Sezon",
                    font=dict(size=25, color='black')
                ),
                font=dict(size=17),
                y=1.05,
                x=1.02
            ),
        )
        st.plotly_chart(fig15, use_container_width=True)
    st.write("Należy zwrócić szczególną uwagę na to, \
             że podane liczby nie sumują się do ogólnej \
             liczby bramek zdobytych w danym sezonie. Wynika \
             to z faktu, że niektóre bramki, np. te \
             zdobyte podczas kontrataków, mogą być uwzględnione \
             zarówno jako strzały spoza pola karnego, jak i z \
             pola karnego.")
elif selected_tab == "Transfery":
    st.markdown('---')
    transfers['season'] = transfers['season'].apply(
        lambda x: '/'.join(map(lambda y: y[2:], x.split('/')))
    )
    sorted_seasons = [
        '92/93', '93/94', '94/95', '95/96', '96/97',
        '97/98', '98/99', '99/00', '00/01', '01/02',
        '02/03', '03/04', '04/05', '05/06', '06/07',
        '07/08', '08/09', '09/10', '10/11', '11/12',
        '12/13', '13/14', '14/15', '15/16', '16/17',
        '17/18', '18/19', '19/20', '20/21', '21/22',
        '22/23'
    ]
    st.header('Wydatki i przychody transferowe Premier League')
    fig13 = go.Figure(data=[
        go.Scatter(
            x=seasonal_league_financial.season,
            y=seasonal_league_financial['in'],
            mode='lines+markers',
            hovertemplate=f"Transferowe wydatki drużyn: <b>%{{y:.3f}} mln</b>"
            + "<extra></extra>",
            marker=dict(color='red'),
            name='Wydatki'
        ),
        go.Scatter(
            x=seasonal_league_financial.season,
            hovertemplate=f"Transferowe przychody drużyn: <b>%{{y:.3f}} mln</b>"
            + "<extra></extra>",
            y=seasonal_league_financial['out'],
            mode='lines+markers',
            marker=dict(color='green'),
            name='Przychody'
        )
    ])
    fig13.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
        hovermode='x unified',
        hoverlabel=dict(
            font=dict(
                size=15,
                color='black'
            )
        ),
        xaxis=dict(
            range=[-0.5, 30.5],
            title='Sezon',
            title_font=dict(size=25, color='black'),
            tickfont=dict(size=12, color='black'),
            ticks="outside",
            ticklen=4,
            tickcolor='black',
            showline=True,
            tickangle=30
        ),
        yaxis=dict(
            range=[0, 3150],
            title='Bilans transferowy (mln)',
            title_font=dict(size=25, color='black'),
            tickfont=dict(size=16, color='black'),
            showgrid=True,
            gridwidth=1,
            gridcolor='gray',
            zerolinecolor='white',
        ),
        height=500,
        width=1200,
        legend=dict(
            title=dict(text="Kategoria", font=dict(size=20, color='black')),
            font=dict(size=18, color='black'),
            y=1.01,
            x=1.02
        ),
    )
    st.plotly_chart(fig13, use_container_width=True)
    st.header('Liczba transferów w sezonie według roli zawodników')
    col6, col7 = st.columns(2)
    choose_in_out = col6.selectbox(
        'Wybierz rodzaj transferów :',
        ['Przychodzący', 'Odchodzący']
    )
    season6 = col7.selectbox('Wybierz sezon :', sorted_seasons[::-1])
    fig17 = go.Figure()
    if choose_in_out == 'Przychodzący':
        positions_and_numbers = count_position('in', season6, transfers)
        fig17.add_traces(
            go.Bar(
                x=positions_and_numbers.position,
                y=positions_and_numbers['count'],
                text=positions_and_numbers['count'].astype(str),
                #textposition='outside',
                textfont=dict(size=15, color='white'),
                hovertemplate="Liczba trasnferów: <b>%{y}</b>"
                + "<extra></extra>",
                hoverlabel=dict(
                    font=dict(size=14, color='white'),
                    bgcolor='blue'
                ),
                marker_color='blue'
            )
        )
        fig17.update_layout(
            margin=dict(l=25, r=0, t=15, b=0),
            xaxis=dict(
                title='Rola na boisku',
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=15, color='black')
            ),
            yaxis=dict(
                title='Liczba transferów przychodzących',
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=15, color='black'),
                showgrid=True,
                gridwidth=0.5,
                gridcolor='rgba(211, 211, 211, 1)',
                #gridcolor='gray',
                zeroline=False,
                zerolinewidth=0
            ),
            height=550,
            width=1200,
        )
        st.plotly_chart(fig17, use_container_width=True)
    elif choose_in_out == 'Odchodzący':
        positions_and_numbers = count_position('out', season6, transfers)
        fig17.add_traces(
            go.Bar(
                x=positions_and_numbers.position,
                y=positions_and_numbers['count'],
                text=positions_and_numbers['count'].astype(str),
                textfont=dict(size=15, color='white'),
                #textposition='outside',
                hovertemplate="Liczba trasnferów: <b>%{y}</b>"
                + "<extra></extra>",
                hoverlabel=dict(
                    font=dict(size=14, color='white'),
                    bgcolor='blue'
                ),
                marker_color='blue'
            )
        )
        fig17.update_layout(
            margin=dict(l=50, r=0, t=15, b=50),
            xaxis=dict(
                title='Rola na boisku',
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=15, color='black')
            ),
            yaxis=dict(
                title='Liczba transferów odchodzących',
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=15, color='black'),
                showgrid=True,
                gridwidth=0.5,
                gridcolor='rgba(211, 211, 211, 1)',
                #gridcolor='gray',
                zeroline=False,
                zerolinewidth=0
            ),
            height=570,
            width=1200,
        )
        st.plotly_chart(fig17, use_container_width=True)
    st.write('Transfery dotyczą zarówno sprzedaży/kupna zawodnika jak i wypożyczeń zawodników. Podział ról jest następujący')
    st.markdown(
            """
            Klasyfikacja roli piłkarza następuje według poniższego wzorca:
            1. **Zawodnik defensywny** - jeśli zawodnik jest obrońcą, bądź pomocnikiem defensywnym,
            2. **Bramkarz** - jeśli zawodnik jest bramkarzem,
            3. **Zawodnik ofensywny** - w pozostałych przypadkach.
            """
        )
    st.header('Najdroższe transfery w sezonach')
    fig18 = go.Figure()
    col12, col13 = st.columns(2)
    choose_transfer_movement = col12.selectbox(
        'Wybierz rodzaj trasnferu :',
        ['Zawodnik przychodzący', 'Zawodnik odchodzący']
    )
    choose_season = col13.selectbox(
        'Wybierz sezon :',
        get_seasons(df)[::-1],
        key='Najdroższe'
    )
    if choose_transfer_movement == 'Zawodnik przychodzący':
        data_for_transfers = return_most_valuable_transfers_for_season(
            'in',
            choose_season,
            transfers
        )
        fig18.add_traces(
            go.Bar(
                x=data_for_transfers.index,
                y=data_for_transfers.fee_cleaned,
                text=data_for_transfers.fee_cleaned.apply(
                    lambda x: str(x).replace('.', ',')
                ),
                textfont=dict(size=17, color='white'),
                hovertemplate="Wartość transferu: <b>%{y} mln</b>"
                + "<extra></extra>",
                marker_color='blue',
                hoverlabel=dict(
                    font=dict(size=14, color='white'),
                    bgcolor='blue'
                )
            )
        )
        fig18.update_layout(
            xaxis={'type': 'category'},
            xaxis_tickvals=list(data_for_transfers.index),
            xaxis_ticktext=data_for_transfers.player_name.tolist()
        )
        fig18.update_layout(
                margin=dict(l=50, r=50, t=50, b=50),
                separators=',',
                xaxis=dict(
                    title='Zawodnik',
                    tickfont=dict(size=13, color='black'),
                    title_font=dict(size=25, color='black')
                ),
                yaxis=dict(
                    title="Wartość transferu (mln)",
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='gray',
                    zeroline=False,
                    title_font=dict(size=25, color='black'),
                    tickfont=dict(size=15, color='black'),
                ),
                height=500,
                width=1200,
            )
        st.plotly_chart(fig18, use_container_width=True)
    elif choose_transfer_movement == 'Zawodnik odchodzący':
        data_for_transfers = return_most_valuable_transfers_for_season(
            'out',
            choose_season,
            transfers
        )
        fig18.add_traces(
            go.Bar(
                x=data_for_transfers.index,
                y=data_for_transfers.fee_cleaned,
                text=data_for_transfers.fee_cleaned.apply(
                    lambda x: str(x).replace('.', ',')
                ),
                textfont=dict(size=17, color='white'),
                hovertemplate="Wartość transferu: <b>%{y} mln</b>"
                + "<extra></extra>",
                marker_color='blue',
                hoverlabel=dict(
                    font=dict(size=14, color='white'),
                    bgcolor='blue'
                )
            )
        )
        fig18.update_layout(
            xaxis={'type': 'category'},
            xaxis_tickvals=list(data_for_transfers.index),
            xaxis_ticktext=data_for_transfers.player_name.tolist()
        )
        fig18.update_layout(
                margin=dict(l=50, r=50, t=50, b=50),
                separators=',',
                xaxis=dict(
                    title='Zawodnik',
                    tickfont=dict(size=13, color='black'),
                    title_font=dict(size=25, color='black')
                ),
                yaxis=dict(
                    title="Wartość transferu (mln)",
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='gray',
                    zeroline=False,
                    title_font=dict(size=25, color='black'),
                    tickfont=dict(size=15, color='black'),
                ),
                height=500,
                width=1200,
            )
        st.plotly_chart(fig18, use_container_width=True)

    st.header('Transfery do najpopularniejszych lig piłkarskich')
    fig19 = go.Figure()
    transfers_by_season['season'] = transfers_by_season['season'].astype(str)
    col14, col15 = st.columns(2)
    direction = col14.selectbox(
        'Wybierz rodzaj transferów :',
        ['Transfery przychodzące', 'Transfery odchodzące']
    )
    season14 = col15.selectbox(
        'Wybierz sezon :',
        find_common_seasons('Arsenal', 'Arsenal', df)[::-1],
        key='kierunki_t'
    )
    if direction == 'Transfery przychodzące':
        df_directions = transfers_by_season.query(
            'season == @season14 and transfer_movement == "out"'
        )
        fig19.add_traces(
            go.Bar(
                x=df_directions['country'],
                y=df_directions['count_player'],
                text=df_directions['count_player'],
                textposition='outside',
                textfont=dict(size=17, color='black'),
                hovertemplate="Liczba transferów: <b>%{y}</b>"
                + "<extra></extra>",
                marker_color='blue',
                hoverlabel=dict(
                    font=dict(size=14, color='white'),
                    bgcolor='blue'
                )
            )
        )
        fig19.update_layout(
            margin=dict(l=25, r=25, t=25, b=25),
            separators=',',
            xaxis=dict(
                title='Liga',
                tickfont=dict(size=13, color='black'),
                title_font=dict(size=25, color='black')
            ),
            yaxis=dict(
                title="Liczba transferów",
                showgrid=True,
                gridwidth=0.5,
                #gridcolor='gray',
                gridcolor='rgba(211, 211, 211, 1)',
                zeroline=False,
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=15, color='black'),
            ),
            height=530,
            width=1210,
        )
        fig19.update_layout(xaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig19, use_container_width=True)
    else:
        df_directions = transfers_by_season.query(
            'season == @season14 and transfer_movement == "in"'
        )
        fig19.add_traces(
            go.Bar(
                x=df_directions['country'],
                y=df_directions['count_player'],
                text=df_directions['count_player'],
                textposition='outside',
                textfont=dict(size=17, color='black'),
                hovertemplate="Liczba transferów: <b>%{y}</b>"
                + "<extra></extra>",
                marker_color='blue',
                hoverlabel=dict(
                    font=dict(size=14, color='white'),
                    bgcolor='blue'
                )
            )
        )
        fig19.update_layout(
            margin=dict(l=25, r=25, t=25, b=25),
            separators=',',
            xaxis=dict(
                title='Liga',
                tickfont=dict(size=13, color='black'),
                title_font=dict(size=25, color='black')
            ),
            yaxis=dict(
                title="Liczba transferów",
                showgrid=True,
                gridwidth=0.5,
                #gridcolor='gray',
                gridcolor='rgba(211, 211, 211, 1)',
                zeroline=False,
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=15, color='black'),
            ),
            height=530,
            width=1210,
        )
        fig19.update_layout(xaxis={'categoryorder': 'total descending'})
        st.plotly_chart(fig19, use_container_width=True)
    st.write('Naturalnym jest, że w przypadku Premier League liczba transferów \
             odchodzących i przychodzących jest taka sama.')
    st.write('Dane dotyczące Championship zaczynają się począwszy od sezonu 2004/05.')
