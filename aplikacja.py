import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.graph_objects as go
import openpyxl


# Ustawienia stylu aplikacji

st.set_page_config(
    page_title="Premier League",
    initial_sidebar_state="expanded"
)


######################### Zbiory danych #########################


@st.cache_data
def load_data():
    df = pd.read_excel(io='Premier_league_all_season1.xlsx', engine='openpyxl')
    carabao_cup = pd.read_excel(io='carabao_cup.xlsx', engine='openpyxl')
    fa_cup = pd.read_excel(io='fa_cup.xlsx', engine='openpyxl')
    premier_league = pd.read_excel(io='premier_league_winners.xlsx', engine='openpyxl')
    wartosci = pd.read_excel(io='wartosci_pieciu_lig.xlsx', engine='openpyxl')

    cup1 = pd.DataFrame(carabao_cup['Carabao_cup'].value_counts())
    cup2 = pd.DataFrame(fa_cup['Fa_cup'].value_counts())
    p_l = pd.DataFrame(premier_league['zwyciezca'].value_counts())
    unique_teams = df['HomeTeam'].unique().tolist()

    return df, carabao_cup, fa_cup, premier_league, wartosci, cup1, cup2, p_l, unique_teams


df, carabao_cup, fa_cup, premier_league, wartosci, cup1, cup2, p_l, unique_teams = load_data()

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
    'Burnley': {'BURGUNDY'.lower(): '#6C1D45', 'blue': '#99D6EA'},
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
    'Bradford': {'yellow': '#FFDF00','black': '#000000'},
    'Portsmouth': {'red': '#ff0000', 'black': '#000000'},
    'Sheffield United': {'red': '#ec2227', 'yellow': '#fcee23'},
    'Fullham': {'black': '#000000', 'red': '#CC0000'},
    'Charlton': {'red': '#d4021d', 'black': '#000000'},
    'Oldham': {'cyan': '#59777d'},
    'Sunderland': {'red': '#eb172b', 'gold': '#a68a26'}
}


######################### FUNKCJE PRZETWARZAJĄCE DANE #########################


def find_common_seasons(team1, team2, df):
    common_seasons = []
    for season in df['Season'].unique():
        teams_in_season = set(df[df['Season'] == season]['HomeTeam'].unique()) | \
                          set(df[df['Season'] == season]['AwayTeam'].unique())
        if team1 in teams_in_season and team2 in teams_in_season:
            common_seasons.append(season)
    return common_seasons


def return_opponents(df, team='Arsenal'):
    opponents = df[df['HomeTeam'] == team]['AwayTeam'].unique().tolist()
    return opponents


def head_to_head_results(df, home_team, away_team):

    subset = df[(df['HomeTeam'].isin([home_team, away_team])) &
                (df['AwayTeam'].isin([home_team, away_team]))]

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
    if team1 == team2:
        return {team1: list(color_dictionary[team1].values())[0]}
    if len(color_dictionary[team2].items()) == 1 and len(color_dictionary[team1]) != 1:
        if list(color_dictionary[team1].values())[0] == list(color_dictionary[team2].values())[0]:
            return {
                        team1: list(color_dictionary[team1].values())[1],
                        team2: list(color_dictionary[team2].values())[0]
            }
        else:
            return {
                        team1: list(color_dictionary[team1].values())[0],
                        team2: list(color_dictionary[team2].values())[0]
            }
    else:
        team1_color = color_dictionary.get(team1, {})
        team2_color = color_dictionary.get(team2, {})
        color1 = list(team1_color.keys())[0]
        for color2 in team2_color.keys():
            if color1 != color2:
                return {team1: team1_color[color1], team2: team2_color[color2]}


def calculate_lost_goals_by_half(df, team, season):
    first_half_goals_conceded = df[df['Season'] == season].groupby('HomeTeam')['HTAG'].sum().get(team) + \
                                df[df['Season'] == season].groupby('AwayTeam')['HTHG'].sum().get(team)
    second_half_goals_conceded = df[df['Season'] == season].groupby('HomeTeam')['SHTAG'].sum().get(team) + \
                                  df[df['Season'] == season].groupby('AwayTeam')['SHTHG'].sum().get(team)
    first_half_goals_scored = df[df['Season'] == season].groupby('HomeTeam')['HTHG'].sum().get(team) + \
                              df[df['Season'] == season].groupby('AwayTeam')['HTAG'].sum().get(team)
    second_half_goals_scored = df[df['Season'] == season].groupby('HomeTeam')['SHTHG'].sum().get(team) + \
                               df[df['Season'] == season].groupby('AwayTeam')['SHTAG'].sum().get(team)
    return pd.DataFrame(
        {
            'GSTWPP': [int(first_half_goals_conceded)],
            'GSTWDP': [int(second_half_goals_conceded)],
            'GSWPP': [int(first_half_goals_scored)],
            'GSWDP': [int(second_half_goals_scored)]
        }
    )

def calculate_home_away_points(df, season, team):
    result = {'Domowy': 0, 'Wyjazdowy': 0}
    filtered_df = df[
        (df["Season"] == season) & ((df["HomeTeam"] == team) | (df["AwayTeam"] == team))
    ][["HomeTeam", "AwayTeam", "FTR"]]
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

############################################################


streamlit_style = """
<style>
body {
    font-size: 20px;
}
</style>
"""

css = """
    <style>
    div[data-baseweb="select"] > div:first-child {
        font-size: 15px;
    }
    </style>
"""
st.markdown(css, unsafe_allow_html=True)

css = """
    <style>
        .stApp {
            margin-top: 30px;
        }
    </style>
"""

st.markdown(css, unsafe_allow_html=True)

st.markdown(streamlit_style, unsafe_allow_html=True)

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


# Wybór zakładki za pomocą option_menu

selected_tab = option_menu(
                   None,
                   ["Strona główna", "Premier League", "Porównywanie statystyk", "Transfery"],
                   icons=['house-fill', 'bar-chart-fill', 'house-fill', 'cash-stack'],
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
                            "color": "white"
                        },
                        "nav-link-selected": {"background-color": "red"},
                   }
              )


# Zawartość wybranej zakładki
if selected_tab == "Strona główna":
    st.markdown('---')
    st.title("Wstęp")
    st.markdown("<span style='font-size:20px'>Informacje o Premier League.</span>", unsafe_allow_html=True)

elif selected_tab == "Premier League":
    st.markdown('---')
    st.header('Liczba zawodników w Premier League')
    st.write('Tu coś będzie.')
    st.header('Liczba sukcesów w Europejskich pucharach')
    
    zwyciezcy_lm = ['Liverpool', 'Manchester United', 'Chelsea']
    zwyciezcy_le = ['Chelsea', 'Manchester United', 'Liverpool']

    liczebnosci_lm = [2, 2, 2]  # Liczebności dla zwycięzców LM
    liczebnosci_le = [2, 1, 1]  # Liczebności dla zwycięzców LE

    # Tworzenie figury i dodawanie danych dla słupków
    fig9 = go.Figure()
    fig9.add_trace(go.Bar(
        x=zwyciezcy_lm,
        y=liczebnosci_lm,
        text=liczebnosci_lm,
        textfont=dict(size=17, color='white'),
        hovertemplate="Zwycięstwa Ligi Mistrzów: <b>%{y}</b> <extra></extra>",
        name='Liga Mistrzów',
        marker_color='blue'
    ))
    fig9.add_trace(go.Bar(
        x=zwyciezcy_le,
        y=liczebnosci_le,
        text=liczebnosci_le,
        textfont=dict(size=17, color='black'),
        hovertemplate="Zwycięstwa Ligi Europy: <b>%{y}</b> <extra></extra>",
        name='Liga Europy',
        marker_color='orange'
    ))

    # Konfiguracja wykresu
    fig9.update_layout(
        xaxis_title='Klub',
        hovermode='x unified',
        yaxis_title='Liczba zwycięstw',
        barmode='group',
        plot_bgcolor='white'
    )

    fig9.update_layout(
        margin=dict(l=20, r=50, t=25, b=50),
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

    st.header('Liczba strzelonych bramek w sezonie')
    fig5 = go.Figure()
    season_goals = df.groupby('Season')[['FTHG', 'FTAG']].sum().sort_values(by='Season', ascending=False)
    season_total_goals = season_goals.sum(axis=1).reset_index(name='liczba bramek')
    sorted_seasons = [
        '92/93', '93/94', '94/95', '95/96', '96/97', '97/98', '98/99', '99/00', '00/01', '01/02',
        '02/03', '03/04', '04/05', '05/06', '06/07', '07/08', '08/09', '09/10', '10/11', '11/12',
        '12/13', '13/14', '14/15', '15/16', '16/17', '17/18', '18/19', '19/20', '20/21', '21/22'
    ]
    season_total_goals['Season'] = pd.Categorical(season_total_goals['Season'], sorted_seasons)
    season_total_goals = season_total_goals.sort_values('Season')
    fig5.add_trace(
        go.Bar(
            x=season_total_goals['Season'],
            y=season_total_goals['liczba bramek'],
            text=season_total_goals['liczba bramek'],
            textfont=dict(size=11, color='white'),
            hoverlabel=dict(font=dict(size=14, color='white'), bgcolor='blue'),
            hovertemplate='Liczba strzelonych bramek: <b>%{y}</b><extra></extra>'
        )
    )
    fig5.update_layout(
        margin=dict(l=20, r=20, t=25, b=50),
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
        width=1200,
    )
    st.plotly_chart(fig5, use_container_width=True)


    st.header('Wartość ligi na przestrzeni lat')
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
                hovertemplate=f'Wartość {replace_name.get(lig, lig)}: <b>%{{y:.2f}} mld</b> <extra></extra>',
                # hoverlabel=dict(
                #     font=dict(size=15),
                #     bgcolor=colors[i],
                #     font_color='white',
                # ),
                line=dict(color=colors[i]),
                showlegend=True
            )
        )
    fig0.update_layout(
        margin=dict(l=20, r=50, t=25, b=50),
        xaxis=dict(
            title='Sezon',
            range=[-0.5, 17.5],
            title_font=dict(size=25, color='black'),
            tickfont=dict(size=16, color='black'),
            showline=True
        ),
        yaxis=dict(
            title="Wartość ligi (mld euro)",
            title_font=dict(size=25, color='black'),
            range=[0, 11],
            tickfont=dict(size=16, color='black'),
            showgrid=True,
            gridwidth=1,
            gridcolor='gray',
            zerolinecolor='white'
        ),
        #hovermode='x',
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
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="right",
            x=1.20
        ),
    )
    st.plotly_chart(fig0, use_container_width=True)

    st.header('Zwycięzcy Premier League')
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=p_l.index,
            y=p_l['zwyciezca'],
            text=p_l['zwyciezca'],
            textfont=dict(size=12, color='white'),
            hoverlabel=dict(font=dict(size=14, color='white'), bgcolor='blue'),
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
    puchary = st.multiselect('Wybierz puchar :', ['Fa cup', 'Carabao cup'], default=['Fa cup'])
    fig1 = go.Figure()

    for puchar in puchary:
        if puchar == 'Fa cup':
            fig1.add_trace(
                go.Bar(
                    x=cup2.index,
                    y=cup2['Fa_cup'],
                    name='Fa Cup',
                    text=cup2['Fa_cup'],
                    hoverlabel=dict(font=dict(size=14, color='white'), bgcolor='red'),
                    hovertemplate='Liczba tytułów FA Cup: <b>%{y}</b><extra></extra>',
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
                    hoverlabel=dict(font=dict(size=14, color='white'), bgcolor='green'),
                    hovertemplate='Liczba tytułów Carabao Cup: <b>%{y}</b><extra></extra>',
                    textfont=dict(size=15, color='white'),
                    showlegend=True
                )
            )
    fig1.update_traces(selector=dict(type='bar', name='Fa Cup'), marker_color='red')
    fig1.update_traces(selector=dict(type='bar', name='Carabao Cup'), marker_color='green')

    fig1.update_layout(
        margin=dict(l=50, r=50, t=15, b=50),
        xaxis=dict(
            title='Nazwa drużyny',
            title_font=dict(size=25, color='black'),
            tickfont=dict(size=13, color='black')
        ),
        yaxis=dict(
            title='Liczba pucharów',
            title_font=dict(size=25, color='black'),
            range=[0, 10],
            tickfont=dict(size=13, color='black'),
            showgrid=True,
            gridwidth=1,
            gridcolor='gray',
            zeroline=False,
        ),
        height=500,
        width=1200,
        legend=dict(
            title=dict(text="Puchar", font=dict(size=25, color='black')),
            font=dict(size=20, color='black'),
            orientation="v",
            yanchor="top",
            y=0.98,
            xanchor="right",
            x=1.18,
        ),
    )
    st.plotly_chart(fig1, use_container_width=True)
    # st.header('Liczba rozegranych sezonów w podziale na przedziały')
    # fig6 = go.Figure()
    # seasons_count = st.selectbox("Wybierz przedział zamknięty :",
    #                             ["1-5", "6-10", "11-15", "16-20", "21-25", "26-30"]
    # )
    # x, y = map(lambda x: int(x), seasons_count.split('-'))
    # team_and_number_of_seasons = pd.DataFrame(
    #     df.groupby("Season")["AwayTeam"].unique().explode().value_counts()
    # )
    # team_and_number_of_seasons.rename(columns={'AwayTeam': 'Liczba sezonów'}, inplace=True)
    # df1 = team_and_number_of_seasons[team_and_number_of_seasons['Liczba sezonów'].between(x, y)]
    # fig6.add_traces(
    #     go.Bar(
    #         y=df1.index,
    #         x=df1['Liczba sezonów'],
    #         #text=df1['Liczba sezonów'],
    #         orientation='h',
    #         marker=dict(color='purple'),
    #         textfont=dict(size=16, color='white'),
    #         hoverlabel=dict(font=dict(size=14, color='white'), bgcolor='purple'),
    #         hovertemplate='Liczba rozegranych sezonów: <b>%{x}</b><extra></extra>',
    #         showlegend=False
    #     )
    # )
    # fig6.update_layout(
    #     margin=dict(l=50, r=50, t=20, b=50),
    #     xaxis=dict(
    #             title='Liczba sezonów w Premier league',
    #             showgrid=True,
    #             gridwidth=1,
    #             gridcolor='gray',
    #             title_font=dict(size=25, color='black'),
    #             tickfont=dict(size=14, color='black'),

    #     ),
    #     yaxis=dict(
    #         title='Nazwa drużyny',
    #         title_font=dict(size=25, color='black'),
    #         #range=[0, y + 1.5],
    #         tickfont=dict(size=14, color='black'),
    #         showgrid=False,
    #         gridwidth=0,
    #         gridcolor='gray',
    #         zeroline=False,
    #     ),
    #     height=500,
    #     width=1200,

    # )
    # st.plotly_chart(fig6, use_container_width=True)
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
        '2021': '21/22'
    }
    slider = st.slider('Wybierz przedział czasowy :', 1992, 2021, (1992, 2021), 1)
    selected_seasons = [season_dict[str(year)] for year in range(slider[0], slider[1] + 1)]
    team_and_number_of_seasons = pd.DataFrame(
        df[df['Season'].astype(str).isin(selected_seasons)]
        .groupby("Season")["AwayTeam"]
        .unique()
        .explode()
        .value_counts()
    )
    team_and_number_of_seasons.rename(columns={'AwayTeam': 'Liczba sezonów'}, inplace=True)
    team_and_number_of_seasons = team_and_number_of_seasons.reindex(unique_teams, fill_value=0)
    sorted_option = st.selectbox('Jak chcesz posortować?', ['Malejąco liczebnościami', 'Rosnąco liczebnościami', 'Malejąco alfabetycznie', 'Rosnąco alfabetycznie'])
    if sorted_option == 'Malejąco liczebnościami':
        team_and_number_of_seasons = team_and_number_of_seasons.sort_values(by='Liczba sezonów', ascending=True)
    elif sorted_option == 'Rosnąco liczebnościami':
        team_and_number_of_seasons = team_and_number_of_seasons.sort_values(by='Liczba sezonów', ascending=False)
    elif sorted_option == 'Malejąco alfabetycznie':
        team_and_number_of_seasons = team_and_number_of_seasons.sort_index(ascending=True)
    elif sorted_option == 'Rosnąco alfabetycznie':
        team_and_number_of_seasons = team_and_number_of_seasons.sort_index(ascending=False)
    
    fig10 = go.Figure()
    fig10.add_traces(
        go.Bar(
            y=team_and_number_of_seasons.index,
            x=team_and_number_of_seasons['Liczba sezonów'],
            #text=df1['Liczba sezonów'],
            orientation='h',
            marker=dict(color='purple'),
            textfont=dict(size=16, color='white'),
            hoverlabel=dict(font=dict(size=15, color='white'), bgcolor='purple'),
            hovertemplate='Liczba rozegranych sezonów: <b>%{x}</b><extra></extra>',
            showlegend=False
        )
    )
    fig10.update_layout(
        margin=dict(l=50, r=50, t=30, b=50),
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
            #range=[0, y + 1.5],
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
    st.write('Rok początkowy i końcowy odnosi się odpowiednio do początku i końca sezonu.\
             Przykładowo wybór przedziału 1992-2000, odpowiada sezonom od 1992/93 do 00/01 włącznie.'
    )

elif selected_tab == "Porównywanie statystyk":
    st.markdown('---')
    st.header('Liczba punktów ewoluująca w trakcie sezonu')
    comparison_type = st.radio("Co chcesz porównać?", ("Drużyny", "Drużynę i sezony"))

    if comparison_type == "Drużyny":
        selected_teams = st.multiselect(
                            "Wybierz drużyny :", unique_teams,
                            max_selections=2,
                            default=['Manchester City', 'Manchester United']
                        )
        if len(selected_teams) == 2:
            column1, column2 = st.columns(2)
            color_line = choose_color_for_teams(selected_teams[0], selected_teams[1])
            common_season1 = find_common_seasons(selected_teams[0], selected_teams[0], df)
            common_season2 = find_common_seasons(selected_teams[1], selected_teams[1], df)
            selected_season1 = column1.selectbox(f"Wybierz sezon dla {selected_teams[0]} :", common_season1)
            selected_season2 = column2.selectbox(f'Wybierz sezon dla {selected_teams[1]} : ', common_season2)
            club1 = calculate_points(df, selected_teams[0], selected_season1)
            club2 = calculate_points(df, selected_teams[1], selected_season2)
            club0 = pd.concat([club1, club2])
            max_value0 = club0['Punkty'].max()

            fig2 = go.Figure()
            fig2.add_trace(
                go.Scatter(
                    x=club1['Kolejka'],
                    y=club1['Punkty'],
                    mode='lines+markers',
                    marker=dict(color=color_line[selected_teams[0]]),
                    name=f'{selected_teams[0]} {selected_season1}',
                    #hoverlabel=dict(font=dict(size=14, color='white'), bgcolor='red'),
                    hovertext=[f"Punkty drużyny {selected_teams[0]}: <b>{points}</b>" for points in club1['Punkty']],
                    hovertemplate="%{hovertext}<extra></extra>"
                )
            )
            fig2.add_trace(
                go.Scatter(
                    x=club2['Kolejka'],
                    y=club2['Punkty'],
                    mode='lines+markers',
                    name=f'{selected_teams[1]} {selected_season2}',
                    marker=dict(color=color_line[selected_teams[1]]),
                    #hoverlabel=dict(font=dict(size=14, color='white'), bgcolor='red'),
                    hovertext=[f"Punkty drużyny {selected_teams[1]}: <b>{points}</b>" for points in club2['Punkty']],
                    hovertemplate="%{hovertext}<extra></extra>",
                )
            )
            fig2.update_layout(
                margin=dict(l=20, r=20, t=50, b=50),
                xaxis=dict(
                    title='Kolejka',
                    showline=True,
                    range=(
                        [-0.5, 43]
                        if any(season in selected_season1 + selected_season2 for season in ["92/93", "93/94", "94/95"])
                        else [-0.5, 39]
                    ),
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
                    title=dict(font=dict(size=25, color='black')),
                    font=dict(size=17, color='black'),
                    orientation="v",
                    yanchor="top",
                    y=0.98,
                    xanchor="right",
                    x=1.28
                ),
                height=500,
                width=1200,
                hovermode='x unified',
            )
            st.plotly_chart(fig2, use_container_width=True)
    if comparison_type == "Drużynę i sezony":
        club = st.selectbox("Wybierz klub :", unique_teams)
        seasons = find_common_seasons(club, club, df)
        selected_seasons = st.multiselect("Wybierz sezon :", seasons, default='00/01')
        fig3, max_value1 = go.Figure(), []
        for season in selected_seasons:
            chart_season = calculate_points(df, club, season)
            max_value1.append(chart_season['Punkty'].max())
            fig3.add_trace(
                go.Scatter(
                    x=chart_season['Kolejka'],
                    y=chart_season['Punkty'],
                    mode='lines+markers',
                    name=season,
                    showlegend=True,
                    #hoverlabel=dict(font=dict(size=14, color='white'), bgcolor='red'),
                    hovertext=[f"Punkty drużyny {club} w sezonie {season}: <b>{points}</b>" for points in chart_season['Punkty']],
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
                            "92/93" in selected_seasons
                            or "93/94" in selected_seasons
                            or "94/95" in selected_seasons
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
                    title=dict(text="Sezon", font=dict(size=25, color='black')),
                    font=dict(size=17, color='black'),
                    orientation="v",
                    yanchor="top",
                    y=0.96,
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
    team1 = st.selectbox("Wybierz pierwszą drużynę :", unique_teams)
    team2 = st.selectbox('Wybierz drugą drużynę :', return_opponents(df=df, team=team1))
    color = choose_color_for_teams(team1, team2)
    fig4 = go.Figure()
    wyniki = head_to_head_results(df, team1, team2)
    colors = [color[team1], '#cd7f32', color[team2]]
    fig4.add_traces(
        go.Bar(
            x=wyniki['result'],
            y=wyniki['count'],
            text=wyniki['count'],
            textfont=dict(size=17, color='white'),
            showlegend=False,
            marker=dict(color=colors),
            hoverlabel=dict(
                font=dict(size=15, color='white'),
                bgcolor=colors
            ),
            hovertemplate=[
                f'Liczba zwycięstw drużyny {team1}: <b>%{{y}}</b> <extra></extra><br>',
                f'Liczba remisów: <b>%{{y}}</b> <extra></extra><br>',
                f'Liczba zwycięstw drużyny {team2}: <b>%{{y}}</b> <extra></extra>'
            ]
        )
    )
    fig4.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(color=color[team1], size=10),
            name=f'Ilość zwycięstw drużyny {team1}'
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
            marker=dict(color=color[team2], size=10),
            name=f'Ilość zwycięstw drużyny {team2}'
        )
    )

    fig4.update_layout(
        margin=dict(l=50, r=50, t=15, b=50),
        xaxis=dict(
            title='Wyniki starcia',
            tickfont=dict(size=16, color='black'),
            title_font=dict(size=25, color='black')
        ),
        yaxis=dict(
            title="Liczba rezultatów",
            title_font=dict(size=25, color='black'),
            range=[0, int(max(wyniki['count'])) + (2 if max(wyniki['count']) > 7 else 0)],
            tickfont=dict(size=16, color='black'),
            showgrid=True,
            gridwidth=1,
            gridcolor='gray',
            zeroline=False,
        ),
        legend=dict(font=dict(size=16), y=0.95),
        height=500,
        width=1200,
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.header('Porównanie bramek strzelonych i straconych względem połów')
    seasons_to_remove = ['92/93', '93/94', '94/95']
    filtered_df = df[~df['Season'].isin(seasons_to_remove)]
    unique_home_teams = filtered_df['HomeTeam'].unique().tolist()
    column3, column4 = st.columns(2)
    column5, column6 = st.columns(2)
    club3 = column3.selectbox("Wybierz pierwszą drużynę :", unique_home_teams, key='x')
    club4 = column4.selectbox("Wybierz drugą drużynę :", unique_home_teams, key='y', index=1)
    seasons1 = find_common_seasons(club3, club3, df)
    seasons2 = find_common_seasons(club4, club4, df)
    excluded_seasons = ['92/93', '93/94', '94/95']
    season3 = column5.selectbox("Wybierz sezon dla pierwszego zespołu :", [season for season in seasons1 if season not in excluded_seasons])
    season4 = column6.selectbox("Wybierz sezon dla drugiego zespołu :", [season for season in seasons2 if season not in excluded_seasons])
    scored_or_conceded = st.selectbox("Wybierz statystykę : ",['Bramki strzelone', 'Bramki stracone'])
    df_c3 = calculate_lost_goals_by_half(df, club3, season3)
    df_c4 = calculate_lost_goals_by_half(df, club4, season4)
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
                textfont=dict(size=16, color='white'),
                hovertemplate=[
                    f'Liczba strzelonych bramek drużyny {club3}: <b>%{{y}}</b><extra></extra>',
                    f'Liczba strzelonych bramek drużyny {club3}: <b>%{{y}}</b><extra></extra>'
                ],

                marker=dict(color=color2[club3]),
                name=f'{club3} {season3}'
            ),
            go.Bar(
                x=['Pierwsza', 'Druga'],
                y=[df_c5['GSWPP'].iloc[1], df_c5['GSWDP'].iloc[1]],
                text=[df_c5['GSWPP'].iloc[1], df_c5['GSWDP'].iloc[1]],
                hovertemplate=[
                    f'Liczba strzelonych bramek drużyny {club4}: <b>%{{y}}</b><extra></extra>',
                    f'Liczba strzelonych bramek drużyny {club4}: <b>%{{y}}</b><extra></extra>'
                ],
                textfont=dict(size=16, color='white'),
                marker=dict(color=(color2[club4] if club4 != club3 else '#967bb6')),
                name=f'{club4} {season4}'
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
                font=dict(
                    size=17  # Rozmiar czcionki legendy
                ),
                y=0.98,
                x=1
            ),
            height=500,
            width=1200
        )
    if scored_or_conceded == 'Bramki stracone':
        fig7 = go.Figure()
        fig7.add_traces(data=[
            go.Bar(
                x=['Pierwsza połowa', 'Druga połowa'],
                y=[df_c5['GSTWPP'].iloc[0], df_c5['GSTWDP'].iloc[0]],
                text=[df_c5['GSTWPP'].iloc[0], df_c5['GSTWDP'].iloc[0]],
                textfont=dict(size=16, color='white'),
                hovertemplate=[
                    f'Liczba straconych bramek drużyny {club3}: <b>%{{y}}</b><extra></extra>',
                    f'Liczba straconych bramek drużyny {club3}: <b>%{{y}}</b><extra></extra>'
                ],
                marker=dict(color=color2[club3]),
                name=club3
            ),
            go.Bar(
                x=['Pierwsza połowa', 'Druga połowa'],
                y=[df_c5['GSTWPP'].iloc[1], df_c5['GSTWDP'].iloc[1]],
                text=[df_c5['GSTWPP'].iloc[1], df_c5['GSTWDP'].iloc[1]],
                hovertemplate=[
                    f'Liczba straconych bramek drużyny {club4}: <b>%{{y}}</b><extra></extra>',
                    f'Liczba straconych bramek drużyny {club4}: <b>%{{y}}</b><extra></extra>'
                ],
                textfont=dict(size=16, color='white'),
                marker=dict(color=(color2[club4] if club3 != club4 else '#967bb6')),
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
                font=dict(
                    size=17  # Rozmiar czcionki legendy
                ),
                y=0.98,
                x=1
            ),
            height=500,
            width=1200
        )
    st.plotly_chart(fig7, use_container_width=True)
    # abc = calculate_lost_goals_by_half(df, club3, season3)
    # fig7 = go.Figure()

    # fig7.add_traces(data=[
    #     go.Bar(
    #         x=['Bramki strzelone', 'Bramki stracone'],
    #         y=[abc['GSWPP'].iloc[0], abc['GSTWPP'].iloc[0]],
    #         text=[abc['GSWPP'].iloc[0], abc['GSTWPP'].iloc[0]],
    #         textfont=dict(size=17, color='white'),
    #         hoverlabel=dict(font=dict(size=15, color='black'), bgcolor='#E3A329'),
    #         hovertemplate=[
    #                         'Liczba strzelonych bramek w pierwszej połowie: <b>%{y}</b><extra></extra>',
    #                         'Liczba straconych bramek w pierwszej połowie: <b>%{y}</b><extra></extra>'
    #                       ],
    #         name='Pierwsza połowa',
    #         marker=dict(color='#E3A329')
    #     ),
    #     go.Bar(
    #         x=['Bramki strzelone', 'Bramki stracone'],
    #         y=[abc['GSWDP'].iloc[0], abc['GSTWDP'].iloc[0]],
    #         text=[abc['GSWDP'].iloc[0], abc['GSTWDP'].iloc[0]],
    #         textfont=dict(size=17, color='white'),
    #         hoverlabel=dict(font=dict(size=15, color='black'), bgcolor='#00CCFF'),
    #         hovertemplate=[
    #                         'Liczba strzelonych bramek w drugiej połowie: <b>%{y}</b><extra></extra>',
    #                         'Liczba straconych bramek w drugiej połowie: <b>%{y}</b><extra></extra>'
    #                       ],
    #         name='Druga połowa',
    #         marker=dict(color='#00CCFF')
    #     )
    #     ]
           # )
    # fig7.update_layout(
    #     barmode='group',
    #     margin=dict(l=50, r=50, t=50, b=50),
    #     showlegend=True,
    #     xaxis=dict(
    #         title='Rodzaj bramki',
    #         title_font=dict(size=25, color='black'),
    #         tickfont=dict(size=15, color='black')
    #     ),
    #     yaxis=dict(
    #         title='Liczba',
    #         title_font=dict(size=25, color='black'),
    #         tickfont=dict(size=15, color='black'),
    #         showgrid=True,
    #         gridwidth=1,
    #         gridcolor='gray',
    #         zeroline=False,
    #         zerolinewidth=0
    #     ),
    #     legend=dict(
    #         font=dict(
    #             size=17  # Rozmiar czcionki legendy
    #         ),
    #         y=1.02,
    #         x=1
    #     ),
    #     height=500,
    #     width=1200,
    # )
    # st.plotly_chart(fig7, use_container_width=True)
    st.header('Punktowanie w meczach domowych i wyjazdowych')
    fig8 = go.Figure()
    col1, col2 = st.columns(2)
    seasons_x = [
        '00/01', '01/02', '02/03', '03/04', '04/05', '05/06',
        '06/07', '07/08', '08/09', '09/10', '10/11', '11/12',
        '12/13', '13/14', '14/15', '15/16', '16/17', '17/18',
        '18/19', '19/20', '20/21', '21/22'
    ]
    unique_teams_for_calculate_points = df[df['Season'].isin(seasons_x)]
    team1 = col1.selectbox('Wybierz drużynę :', unique_teams_for_calculate_points['HomeTeam'].unique().tolist())
    season1 = col2.selectbox('Wybierz sezon: ', find_common_seasons(team1, team1, unique_teams_for_calculate_points))
    data_for_graph = calculate_home_away_points(df, season1, team1)
    
    fig8.add_trace(
        go.Bar(
            x=list(data_for_graph.keys()),
            y=list(data_for_graph.values()),
            text=list(data_for_graph.values()),
            textfont=dict(size=20, color='white'),
            hoverlabel=dict(font=dict(size=15, color='white'), bgcolor=['blue', 'red']),
            hovertemplate=[
                            'Liczba zdobytych punktów w spotkaniach domowych: <b>%{y}</b><extra></extra>',
                            'Liczba zdobytych punktów w spotkaniach wyjazdowych: <b>%{y}</b><extra></extra>'
            ],
            marker=dict(color=['blue', 'red']),
            showlegend=False
        )
    )  
    fig8.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(color='blue', size=10),
            name=f'Ilość punktów domowych'
        )
    )
    fig8.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(color='red', size=10),
            name='Ilość punktów wyjazdowych'
        )
    )
    fig8.update_layout(
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
                font=dict(
                    size=17  # Rozmiar czcionki legendy
                ),
                y=1.02,
                x=1
            ),
        )
    st.plotly_chart(fig8, use_container_width=True)
    st.header('Porównanie ')

elif selected_tab == "Transfery":
    st.markdown('---')
