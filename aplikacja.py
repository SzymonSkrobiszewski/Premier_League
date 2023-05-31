import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.graph_objects as go

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
    wartosci = pd.read_excel(io='wartosci_pieciu_lig.xlsx', engine='openpyxl')
    cup1 = pd.DataFrame(carabao_cup['Carabao_cup'].value_counts())
    cup2 = pd.DataFrame(fa_cup['Fa_cup'].value_counts())
    p_l = pd.DataFrame(premier_league['zwyciezca'].value_counts())
    unique_teams = df['HomeTeam'].unique().tolist()

    return (
        df,
        carabao_cup,
        fa_cup,
        premier_league,
        wartosci,
        cup1,
        cup2,
        p_l,
        unique_teams
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
) = load_data()

color_dictionary = {
    'Arsenal': {'red': '#EF0107', 'gold': '#9C824A'},
    'Nottingham Forest': {'red': '#DD0000'},
    'Chelsea': {'blue': '#034694', 'gold': '#DBA111'},
    'Coventry': {'blue': '#059DD9', 'gold': '#E54724'},
    'Crystal Palace': {'blue': '#1B458F', 'gray': '#A7A5A6', 'red': '#C4122E'},
    'Ipswich': {'blue': '#3a64a3', 'red': '#de2c37'},
    'Leeds': {'yellow': '#FFCD00', 'gold': '#AC944D'},
    'Liverpool': {'red': '#C8102E', 'green': '#00B2A9'},
    'Manchester United': {'red': '#DA291C', 'yellow': '#FBE122'},
    'Middlesbrough': {'blue': '#004494', 'black': '#000000'},
    'Sheffield Wednesday': {'blue': '#4681cf', 'yellow': '#e9b008'},
    'Manchester City': {'blue': '#6CABDD', 'gold': '#D4A12A'},
    'Southampton': {'black': '#130C0E', 'red': '#D71920'},
    'Tottenham': {'blue': '#132257'},
    'Aston Villa': {'claret': '#670E36', 'blue': '#95BFE5'},
    'Newcastle': {'black': '#241F20', 'blue': '#41B6E6'},
    'West Ham': {'maroon': '#7A263A', 'blue': '#1BB1E7'},
    'Swindon': {'gold': '#B48D00', 'red': '#DC161B'},
    'Leicester': {'blue': '#003090', 'gold': '#FDBE11'},
    'Brentford': {'orange': '#FFB400', 'red': '#D20000'},
    'Barnsley': {'red': '#D71921', 'blue': '#00B8F1'},
    'Birmingham': {'blue': '#0000FF', 'red': '#DC241F'},
    'Blackburn Rovers': {'green': '#009036', 'blue': '#009EE0'},
    'Blackpool': {'orange': '#F68712'},
    'Bolton': {'blue': '#263C7E', 'red': '#88111E'},
    'Bournemouth': {'black': '#000000', 'red': '#B50E12'},
    'Brighton': {'blue': '#0057B8', 'yellow': '#FDB913'},
    'Burnley': {'claret': '#6C1D45', 'blue': '#99D6EA'},
    'Derby': {'black': '#000000', 'blue': '#000040'},
    'Everton': {'blue': '#003399', 'pink': '#fa9bac'},
    'Huddersfield': {'blue': '#0E63AD', 'yellow': '#FDE43C'},
    'Wolves': {'black': '#231F20', 'yellow': '#FDB913'},
    'West Brom': {'blue': '#122F67', 'green': '#149557'},
    'Wimbledon': {'blue': '#2b4690', 'yellow': '#fff200'},
    'Wigan': {'green': '#123d0f', 'blue': '#1d59af'},
    'Norwich City': {'green': '#00A650', 'yellow': '#FFF200'},
    'Swansea': {'black': '#000000'},
    'Hull': {'orange': '#f5971d', 'black': '#101920'},
    'Reading': {'pink': '#dd1740 ', 'blue': '#004494'},
    'Watford': {'yellow': '#FBEE23', 'red': '#ED2127'},
    'Cardiff': {'blue': '#0070B5', 'red': '#D11524'},
    'QPR': {'blue': '#1d5ba4', 'pink': '#ff33cc'},
    'Stoke': {'red': '#E03A3E', 'blue': '#1B449C'},
    'Bradford': {'yellow': '#FFDF00', 'black': '#000000'},
    'Portsmouth': {'red': '#ff0000', 'black': '#000000'},
    'Sheffield United': {'red': '#ec2227', 'yellow': '#fcee23'},
    'Fulham': {'black': '#000000', 'red': '#CC0000'},
    'Charlton': {'red': '#d4021d', 'black': '#000000'},
    'Oldham': {'cyan': '#59777d'},
    'Sunderland': {'red': '#eb172b', 'gold': '#a68a26'}
}

# Funkcje przetwarzające dane


def find_common_seasons(team1, team2, df):
    common_seasons = df.query(
        "(HomeTeam == @team1 or AwayTeam == @team1) and \
            (HomeTeam == @team2 or AwayTeam == @team2)"
    )["Season"].unique()
    return common_seasons


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
    return pd.DataFrame(
        {
            "GSTWPP": [int(first_half_goals_conceded)],
            "GSTWDP": [int(second_half_goals_conceded)],
            "GSWPP": [int(first_half_goals_scored)],
            "GSWDP": [int(second_half_goals_scored)],
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


# Odległość granic od -----
streamlit_style = """
<style>
body {
    font-size: 25px;
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
    ["Strona główna", "Premier League", "Porównywanie statystyk", "Transfery"],
    icons=["house-fill", "bar-chart-fill", "house-fill", "cash-stack"],
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
    st.title("Wstęp")
    with open('strona_glowna.txt', 'r', encoding='utf-8') as file:
        file_content = file.read().split('\n')
    formatted_text = (
        f'<div style="text-align: justify; font-size: 25px;"> {file_content[0]} </div>'
    )
    formatted_text1 = (
        f'<div style="text-align: justify; font-size: 25px;"> {file_content[1]} </div>'
    )
    st.markdown(formatted_text, unsafe_allow_html=True)
    st.markdown(" ")
    st.markdown(formatted_text1, unsafe_allow_html=True)

elif selected_tab == "Premier League":
    st.markdown('---')
    premier_league1 = option_menu(
        None,
        [
            "Ogólne statystyki ligi",
            "Premier League na płaszczyźnie Europejskiej"
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
    if premier_league1 == "Premier League na płaszczyźnie Europejskiej":
        st.header('Porównanie wartości lig piłkarskich')
        liga = st.multiselect(
            "Wybierz ligę :",
            ["Ligue 1", "Bundesliga", "Premier league", "La liga", "Serie A"],
            default=["Premier league"],
        )
        fig0 = go.Figure()
        colors = ['red', 'green', 'blue', 'purple', 'black']
        replace_name = {'Bundesliga': 'Bundesligi', 'La liga': 'La ligi'}
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
                range=[-0.5, 17.5],
                title_font=dict(size=25, color='black'),
                tickfont=dict(size=16, color='black'),
                #showline=True
            ),
            yaxis=dict(
                title="Wartość ligi (mld euro)",
                title_font=dict(size=25, color='black'),
                range=[0, 11],
                tickfont=dict(size=16, color='black'),
                showgrid=True,
                gridwidth=1,
                gridcolor='gray',
                zerolinecolor='black'
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
        st.header(
            'Liczba zwycięstw klubów z Premier League \
                w Europejskich pucharach'
        )
        zwyciezcy_lm = ['Liverpool', 'Manchester United', 'Chelsea']
        zwyciezcy_le = ['Chelsea', 'Manchester United', 'Liverpool']
        liczebnosci_lm = [2, 2, 2]
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
            xaxis_title='Klub',
            hovermode='x unified',
            yaxis_title='Liczba zwycięstw',
            barmode='group',
            plot_bgcolor='white'
        )

        fig9.update_layout(
            margin=dict(l=20, r=50, t=35, b=50),
            barmode='group',
            xaxis=dict(
                title='Klub',
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
    else:
        st.header('Liczba zawodników w Premier League')
        st.write('Tu coś będzie.')
        st.header('Liczba strzelonych bramek')
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
                textfont=dict(size=11, color='white'),
                hoverlabel=dict(
                    font=dict(size=14, color='white'),
                    bgcolor='blue'
                ),
                hovertemplate="Liczba strzelonych bramek: <b>%{y}</b>"
                + "<extra></extra>"
            )
        )
        fig5.update_layout(
            margin=dict(l=0, r=0, t=25, b=0),
            xaxis=dict(
                title='Sezon',
                tickfont=dict(size=13, color='black'),
                title_font=dict(size=25, color='black')
            ),
            yaxis=dict(
                title="Liczba strzelonych bramek",
                title_font=dict(size=25, color='black'),
                range=[0, 1250],
                tickfont=dict(size=15, color='black'),
                showgrid=True,
                gridwidth=1,
                gridcolor='gray',
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
                textfont=dict(size=12, color='white'),
                hoverlabel=dict(
                    font=dict(size=14, color='white'),
                    bgcolor='blue'
                ),
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

        st.header('Podział pucharów krajowych')
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
                range=[0, 10.5],
                tickfont=dict(size=13, color='black'),
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
        st.header('Liczba rozegranych sezonów w Premier League według drużyn')
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


elif selected_tab == "Porównywanie statystyk":
    st.markdown('---')
    st.header('Porównanie liczby punktów ewoluującej w trakcie sezonu')
    comparison_type = st.radio(
        "Co chcesz porównać?",
        ("Drużyny", "Drużynę i sezon/y")
    )
    if comparison_type == "Drużyny":
        column1, column2 = st.columns(2)
        team1 = column1.selectbox('Wybierz pierwszą drużynę :', unique_teams)
        team2 = column2.selectbox(
            'Wybierz drugą drużynę :', return_opponents(df, team1)
        )
        if len([team1, team2]) == 2:
            color_line = choose_color_for_teams(team1, team2)
            common_season = find_common_seasons(team1, team2, df)
            selected_season = st.selectbox("Wybierz sezon :", common_season)
            club1 = calculate_points(df, team1, selected_season)
            club2 = calculate_points(df, team2, selected_season)
            club0 = pd.concat([club1, club2])
            max_value0 = club0['Punkty'].max()

            fig2 = go.Figure()
            fig2.add_trace(
                go.Scatter(
                    x=club1['Kolejka'],
                    y=club1['Punkty'],
                    mode='lines+markers',
                    marker=dict(color=color_line[team1]),
                    name=f'{team1}',
                    hovertext=[
                        f"Punkty drużyny {team1}: <b>{points}</b>" for points in club1['Punkty']
                    ],
                    hovertemplate="%{hovertext}<extra></extra>"
                )
            )
            fig2.add_trace(
                go.Scatter(
                    x=club2['Kolejka'],
                    y=club2['Punkty'],
                    mode='lines+markers',
                    name=f'{team2}',
                    marker=dict(color=color_line[team2]),
                    hovertext=[
                        f"Punkty drużyny {team2}: <b>{points}</b>" for points in club2['Punkty']
                    ],
                    hovertemplate="%{hovertext}<extra></extra>",
                )
            )
            fig2.update_layout(
                margin=dict(l=50, r=50, t=50, b=50),
                showlegend=True,
                xaxis=dict(
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
                    range=[-2, round(max_value0, -1) + 15],
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
    if comparison_type == "Drużynę i sezon/y":
        c1, c2 = st.columns(2)
        club = c1.selectbox("Wybierz klub :", unique_teams)
        seasons = find_common_seasons(club, club, df)
        selected_seasons1 = c2.multiselect(
            "Wybierz sezon/y :", seasons,
            default=seasons[0]
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
                    range=[-2, round(max(max_value1, default=0), -1) + 15],
                    tickfont=dict(size=17, color='black'),
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='gray',
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
            name=f'Ilość zwycięstw drużyny {team3}'
        )
    )
    fig4.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(color='#cd7f32', size=10),
            name='Ilość remisów'
        )
    )
    fig4.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(color=color[team4], size=10),
            name=f'Ilość zwycięstw drużyny {team4}'
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
            range=[
                0,
                int(max(result['count'])) + (2 if max(result['count']) > 7 else 0)
            ],
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
        ("Drużyny", "Drużynę i sezon/y"), key="comparison_type1"
    )
    seasons_to_remove = ['92/93', '93/94', '94/95']
    filtered_df = df[~df['Season'].isin(seasons_to_remove)]
    unique_home_teams = filtered_df['HomeTeam'].unique().tolist()
    if comparison_type1 == 'Drużyny':
        column3, column4 = st.columns(2)
        column5, column6 = st.columns(2)
        club3 = column3.selectbox(
            "Wybierz pierwszą drużynę :",
            sorted(unique_home_teams),
            key='x'
        )
        club4 = column4.selectbox(
            "Wybierz drugą drużynę :",
            return_opponents(df, club3),
            key='y',
            index=0
        )
        seasons1 = find_common_seasons(club3, club4, df)
        excluded_seasons = ['92/93', '93/94', '94/95']
        season3 = column5.selectbox(
            "Wybierz sezon :",
            [season5 for season5 in seasons1 if season5 not in excluded_seasons]
        )
        scored_or_conceded = column6.selectbox(
            "Wybierz statystykę : ",
            ['Bramki strzelone', 'Bramki stracone']
        )
        df_c3 = calculate_lost_goals_by_half(df, club3, season3)
        df_c4 = calculate_lost_goals_by_half(df, club4, season3)
        df_c5 = pd.concat([df_c3, df_c4])
        color2 = choose_color_for_teams(club3, club4)
        if scored_or_conceded == 'Bramki strzelone':
            maksimum = max(df_c5['GSWPP'].max(), df_c5['GSWDP'].max())
            fig7 = go.Figure()
            fig7.add_traces(data=[
                go.Bar(
                    x=['Pierwsza', 'Druga'],
                    y=[df_c5['GSWPP'].iloc[0], df_c5['GSWDP'].iloc[0]],
                    text=[df_c5['GSWPP'].iloc[0], df_c5['GSWDP'].iloc[0]],
                    textfont=dict(size=18, color='white'),
                    hovertemplate=[
                        f'Liczba strzelonych bramek drużyny {club3}: <b>%{{y}}</b>'
                        + '<extra></extra>',
                        f'Liczba strzelonych bramek drużyny {club3}: <b>%{{y}}</b>'
                        + '<extra></extra>'
                    ],
                    marker=dict(color=color2[club3]),
                    name=club3
                ),
                go.Bar(
                    x=['Pierwsza', 'Druga'],
                    y=[df_c5['GSWPP'].iloc[1], df_c5['GSWDP'].iloc[1]],
                    text=[df_c5['GSWPP'].iloc[1], df_c5['GSWDP'].iloc[1]],
                    hovertemplate=[
                        f'Liczba strzelonych bramek drużyny {club4}: <b>%{{y}}</b>'
                        + '<extra></extra>',
                        f'Liczba strzelonych bramek drużyny {club4}: <b>%{{y}}</b>'
                        + '<extra></extra>'
                    ],
                    textfont=dict(size=18, color='white'),
                    marker=dict(color=(color2[club4])),
                    name=club4
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
                    title='Połowa meczu',
                    title_font=dict(size=25, color='black'),
                    tickfont=dict(size=17, color='black')
                ),
                yaxis=dict(
                    range=[0, maksimum + 3],
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
            fig7.add_traces(data=[
                go.Bar(
                    x=['Pierwsza', 'Druga'],
                    y=[df_c5['GSTWPP'].iloc[0], df_c5['GSTWDP'].iloc[0]],
                    text=[df_c5['GSTWPP'].iloc[0], df_c5['GSTWDP'].iloc[0]],
                    textfont=dict(size=18, color='white'),
                    hovertemplate=[
                        f'Liczba straconych bramek drużyny {club3}: <b>%{{y}}</b>'
                        + '<extra></extra>',
                        f'Liczba straconych bramek drużyny {club3}: <b>%{{y}}</b>'
                        + '<extra></extra>'
                    ],
                    marker=dict(color=color2[club3]),
                    name=club3
                ),
                go.Bar(
                    x=['Pierwsza', 'Druga'],
                    y=[df_c5['GSTWPP'].iloc[1], df_c5['GSTWDP'].iloc[1]],
                    text=[df_c5['GSTWPP'].iloc[1], df_c5['GSTWDP'].iloc[1]],
                    hovertemplate=[
                        f'Liczba straconych bramek drużyny {club4}: <b>%{{y}}</b>'
                        + '<extra></extra>',
                        f'Liczba straconych bramek drużyny {club4}: <b>%{{y}}</b>'
                        + '<extra></extra>'
                    ],
                    textfont=dict(size=18, color='white'),
                    marker=dict(color=(color2[club4])),
                    name=club4
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
    if comparison_type1 == 'Drużynę i sezon/y':
        colors2 = ['#FFA500', '#FFC0CB', '#FFFF00', '#00FFFF', '#FF00FF']
        column6, column7 = st.columns(2)
        club3 = column6.selectbox(
            "Wybierz drużynę:",
            sorted(unique_home_teams),
            key='t'
        )
        seasons1 = find_common_seasons(club3, club3, df)
        excluded_seasons1 = ['92/93', '93/94', '94/95']
        season3 = column7.multiselect(
            "Wybierz sezon/y :",
            [season4 for season4 in seasons1 if season4 not in excluded_seasons1],
            default=seasons1[-2:],
            max_selections=5,
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
                        marker=dict(color=colors2[i]),
                        name=season
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
                        marker=dict(color=colors2[i])
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
    st.header('Punktowanie w meczach domowych i wyjazdowych')
    comparison_type2 = st.radio(
        "Co chcesz porównać?",
        ("Drużyny", "Drużynę i sezon/y"), key='ct2'
    )
    if comparison_type2 == 'Drużyny':
        fig8 = go.Figure()
        col1, col2 = st.columns(2)
        team1 = col1.selectbox('Wybierz drużynę :', unique_teams)
        team2 = col2.selectbox(
            'Wybierz drugą drużynę :',
            return_opponents(df, team1),
            key='punktowanie'
        )
        season1 = st.selectbox(
            'Wybierz sezon/y: ',
            find_common_seasons(team1, team2, df)
        )
        data_for_graph = calculate_home_away_points(df, season1, team1)
        data_for_graph1 = calculate_home_away_points(df, season1, team2)
        color1 = choose_color_for_teams(team1, team2)
        fig8.add_trace(
            go.Bar(
                x=list(data_for_graph.keys()),
                y=list(data_for_graph.values()),
                text=list(data_for_graph.values()),
                textfont=dict(size=18, color='white'),
                hovertemplate=[
                    f'Punkty domowe drużyny {team1}: <b>%{{y}}</b>'
                    + '<extra></extra>',
                    f'Punkty wyjazdowe drużyny {team1} : <b>%{{y}}</b>'
                    + '<extra></extra>'
                ],
                marker=dict(color=color1[team1]),
                name=team1,
            )
        )
        fig8.add_trace(
            go.Bar(
                x=list(data_for_graph1.keys()),
                y=list(data_for_graph1.values()),
                text=list(data_for_graph1.values()),
                textfont=dict(size=18, color='white'),
                hovertemplate=[
                    f'Punkty domowe drużyny {team2}: <b>%{{y}}</b>'
                    + '<extra></extra>',
                    f'Punkty wyjazdowe drużyny {team2}: <b>%{{y}}'
                    + '</b><extra></extra>'
                ],
                name=team2,
                marker=dict(color=color1[team2]),
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
    if comparison_type2 == 'Drużynę i sezon/y':
        kolory = ['#ea03ff', "#ADD8E6", "#90EE90", "#FFA500", "#FF0000"]
        fig8 = go.Figure()
        col1, col2 = st.columns(2)
        team1 = col1.selectbox('Wybierz drużynę :', unique_teams)
        seasons = find_common_seasons(team1, team1, df)
        selected_seasons = col2.multiselect(
            'Wybierz sezon/y :', seasons,
            default=seasons[:2],
            max_selections=5
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
                    marker=dict(color=kolory[i])
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
                        text="Sezon",
                        font=dict(size=25, color='black')
                    ),
                    font=dict(size=17),
                    y=1.02,
                    x=1.02
                ),
            )
        st.plotly_chart(fig8, use_container_width=True)
    st.header('Rozkład kar za faule')
    c1, c2 = st.columns(2)
    seasons_x = [
        '00/01', '01/02', '02/03', '03/04', '04/05', '05/06',
        '06/07', '07/08', '08/09', '09/10', '10/11', '11/12',
        '12/13', '13/14', '14/15', '15/16', '16/17', '17/18',
        '18/19', '19/20', '20/21', '21/22', '22/23'
    ]
    df2 = df[df['Season'].isin(seasons_x)]
    team1 = c1.selectbox(
        'Wybierz pierwszą drużynę :', unique_teams,
        key='faule'
    )
    team2 = c2.selectbox(
        'Wybierz drugą drużynę :', return_opponents(df2, team1),
        key='faule1'
    )
    season = st.selectbox(
        'Wybierz sezon :', find_common_seasons(team1, team2, df2),
        key='faule2'
    )
    fauls1 = calculate_fauls_yellow_and_red_cards(season, team1, df)
    fauls2 = calculate_fauls_yellow_and_red_cards(season, team2, df)
    with open('legenda.txt', 'r', encoding='utf-8') as file:
        file_content = file.read()
    st.markdown(file_content, unsafe_allow_html=True)
    k1, k2 = st.columns(2)
    labels1, values1 = zip(*fauls1.items())
    labels2, values2 = zip(*fauls2.items())
    with k1:
        fig11 = go.Figure(
            go.Pie(
                labels=labels1,
                sort=False,
                values=values1,
                textinfo="value+percent",
                marker=dict(colors=["black", "red", "yellow"]),
                direction="clockwise",
                hovertemplate="<b>%{label}</b><extra></extra>",
                hoverlabel=dict(font=dict(size=17, color="black")),
            )
        )
        fig11.update_layout(
            plot_bgcolor='white',
            title=dict(
                text=f'Drużyna - {team1}',
                font=dict(size=22),
                xanchor='left',
                yanchor='top',
            ),
            font=dict(size=18, color='Black'),
            separators=',',
            margin=dict(t=80, b=0, l=20, r=0),
            showlegend=False
        )
        st.plotly_chart(fig11, use_container_width=True)
    with k2:
        fig11 = go.Figure(
            go.Pie(
                labels=labels2,
                sort=False,
                values=values2,
                textinfo="value+percent",
                marker=dict(colors=["black", "red", "yellow"]),
                direction="clockwise",
                hovertemplate="<b>%{label}</b><extra></extra>",
                hoverlabel=dict(font=dict(size=17, color="black")),
            )
        )
        fig11.update_layout(
            plot_bgcolor='white',
            title=dict(
                text=f'Drużyna - {team2}',
                font=dict(size=22),
                xanchor='left',
                yanchor='top',
            ),
            font=dict(size=18, color='Black'),
            separators=',',
            margin=dict(t=80, b=0, l=20, r=0),
            showlegend=False
        )
        st.plotly_chart(fig11, use_container_width=True)
    st.markdown('''
        Powyższy wykres przedstawia sumy rozłączne. Oznacza to, \
        że jeśli zawodnik otrzyma drugą żółtą kartkę,\
        co skutkuje czerwoną kartką, wartość jest dodawana \
        tylko do **"czerwonych kartek"**.
        Przykładowo jeśli drużyna A dostała dwie żółte kartki, \
        po czym jeden z wcześniej ukaranych zawodników wylatuje z boiska,\
        to bilans kartek w meczu wynosi odpowiednio dwie żółte i \
        jedną czerwoną kartkę.
    ''')
elif selected_tab == "Transfery":
    st.markdown('---')
