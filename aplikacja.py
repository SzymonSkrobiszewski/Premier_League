import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.graph_objects as go
import openpyxl


# Ustawienia stylu aplikacji

st.set_page_config(
    page_title="Moja aplikacja",
    initial_sidebar_state="expanded"
)

@st.cache(allow_output_mutation=True)
def set_theme():
    st.set_option('theme', 'light')

set_theme()  # ustawienie motywu przy starcie aplikacji

######################### Zbiory danych #########################


@st.cache_data
def load_data():
    df = pd.read_excel(io='Premier_league_all_season.xlsx', engine='openpyxl')
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


######################### FUNKCJE PRZETWARZAJĄCE DANE #########################


def find_common_seasons(team1, team2, df):
    common_seasons = []
    for season in df['Season'].unique():
        teams_in_season = set(df[df['Season'] == season]['HomeTeam'].unique()) | \
                          set(df[df['Season'] == season]['AwayTeam'].unique())
        if team1 in teams_in_season and team2 in teams_in_season:
            common_seasons.append(season)
    return common_seasons


def return_opponents(df, selected_team='Arsenal'):
    opponents = df[df['HomeTeam'] == selected_team]['AwayTeam'].unique().tolist()
    return opponents


def head_to_head_results(df, home_team, away_team):

    subset = df[(df['HomeTeam'].isin([home_team, away_team])) & \
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
    df = df[((df['HomeTeam'] == team_name) | (df['AwayTeam'] == team_name)) & (df['Season'] == season)].reset_index(drop=True)
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
    return pd.DataFrame({'Kolejka': list(points_by_matchweek.keys()), 'Punkty': list(points_by_matchweek.values())})

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
        max-width: 1250px;
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
                            "font-size": "17px",
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
    st.header('Wartość ligi na przestrzeni lat')
    liga = st.multiselect('Wybierz ligę :', ['Ligue 1', 'Bundesliga', 'Premier league', 'La liga', 'Serie A'])
    fig0 = go.Figure()
    for lig in liga:
        fig0.add_trace(
            go.Scatter(
                x=wartosci['sezon'],
                y=wartosci[lig],
                name=lig,
                mode='lines+markers',
                hovertemplate='<br><b>Wartość ligi:</b> %{y}',
                showlegend=True
            )
        )
    fig0.update_layout(
        xaxis_title="Sezon",
        yaxis=dict(
            range=[0, 8000],
            tickfont=dict(size=13, color='black'),
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        ),
        hovermode='x',
        yaxis_title="Wartość ligi (mld euro)",
        yaxis_title_font=dict(size=25, color='black'),
        xaxis_title_font=dict(size=25, color='black'),
        height=500,
        width=1200,
        legend=dict(
            title=dict(text="Liga", font=dict(size=25, color='black')),
            font=dict(size=20, color='black'),
            orientation="v",
            yanchor="top",
            y=1.1,
            xanchor="right",
            x=1.17
        ),
        xaxis_tickfont=dict(size=13, color='black'),
        #font=dict(size=30, color='black')
    )
    st.plotly_chart(fig0, use_container_width=True)

    st.header('Zwycięzcy Premier League.')
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
        xaxis_title="Nazwa drużyny",
        margin=dict(l=50, r=50, t=15, b=50),
        yaxis=dict(
            range=[0, 15],
            tickfont=dict(size=13, color='black'),
            showgrid=True,
            gridwidth=2,
            gridcolor='lightgray'
        ),
        yaxis_title="Liczba tytułów",
        yaxis_title_font=dict(size=20, color='black'),
        xaxis_title_font=dict(size=20, color='black'),
        height=500,
        width=1200,
        xaxis_tickfont=dict(size=13, color='black'),
    )
    fig.update_yaxes(zeroline=False, zerolinewidth=0)
    st.plotly_chart(fig, use_container_width=True)

    st.header('Podział pucharów krajowych.')
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
        xaxis_title="Nazwa drużyny",
        margin=dict(l=50, r=50, t=15, b=50),
        yaxis=dict(
            range=[0, 11],
            tickfont=dict(size=13, color='black'),
            showgrid=True,
            gridwidth=2,
            gridcolor='lightgray'
        ),
        yaxis_title="Liczba pucharów",
        yaxis_title_font=dict(size=20, color='black'),
        xaxis_title_font=dict(size=20, color='black'),
        height=500,
        width=1200,
        legend=dict(
            title=dict(text="Puchar", font=dict(size=25, color='black')),
            font=dict(size=20, color='black'),
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="right",
            x=1.16,
        ),
        xaxis_tickfont=dict(size=13, color='black'),
        #font=dict(size=30, color='black')
    )
    fig1.update_yaxes(zeroline=False, zerolinewidth=0)
    st.plotly_chart(fig1, use_container_width=True)

elif selected_tab == "Porównywanie statystyk":
    st.markdown('---')
    st.header('Tekst')
    comparison_type = st.radio("Co chcesz porównać?", ("Drużyny", "Drużyna i sezon"))

    if comparison_type == "Drużyny":
        selected_teams = st.multiselect(
                            "Wybierz drużyny :", unique_teams,
                            max_selections=2,
                            default=['Manchester City', 'Manchester United']
                        )
        if len(selected_teams) == 2:
            common_seasons = find_common_seasons(selected_teams[0], selected_teams[1], df)
            selected_season = st.selectbox("Wybierz sezon :", common_seasons)
            club1 = calculate_points(df, selected_teams[0], selected_season)
            club2 = calculate_points(df, selected_teams[1], selected_season)
            club0 = pd.concat([club1, club2])
            max_value0 = club0['Punkty'].max()

            fig2 = go.Figure()

            fig2.add_trace(
                go.Scatter(
                    x=club1['Kolejka'],
                    y=club1['Punkty'],
                    mode='lines+markers',
                    name=selected_teams[0],
                    hoverlabel=dict(font=dict(size=14, color='white'), bgcolor='red'),
                    hovertext=[f"Punkty drużyny {selected_teams[0]}: <b>{points}</b>" for points in club1['Punkty']],
                    hovertemplate="%{hovertext}<extra></extra>"
                )
            )
            fig2.add_trace(
                go.Scatter(
                    x=club2['Kolejka'],
                    y=club2['Punkty'],
                    mode='lines+markers',
                    name=selected_teams[1],
                    hoverlabel=dict(font=dict(size=14, color='white'), bgcolor='red'),
                    hovertext=[f"Punkty drużyny {selected_teams[1]}: <b>{points}</b>" for points in club2['Punkty']],
                    hovertemplate="%{hovertext}<extra></extra>"
                )
            )
            fig2.update_layout(
                xaxis_title='Kolejka',
                yaxis_title='Punkty',
                xaxis=dict(
                    range = [-0.5, 43] if ("92/93" in selected_season or "93/94" in selected_season or "94/95" in selected_season) else [-0.5, 39]

                ),
                legend=dict(
                    title=dict(text="Drużyna", font=dict(size=25, color='black')),
                    font=dict(size=20, color='black'),
                    orientation="v",
                    yanchor="top",
                    y=1.1,
                    xanchor="right",
                    x=1.22
                ),
                height=500,
                width=1200,
                yaxis_title_font=dict(size=20, color='black'),
                xaxis_title_font=dict(size=20, color='black'),
                xaxis_tickfont=dict(size=15, color='black'),
                hovermode='x',
                yaxis=dict(
                    range=[-2, round(max_value0, -1) + 10],
                    tickfont=dict(size=15, color='black'),
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='lightgray'
                )
            )
            st.plotly_chart(fig2, use_container_width=True)
    if comparison_type == "Drużyna i sezon":
        club = st.selectbox("Wybierz klub", unique_teams)
        seasons = find_common_seasons(club, club, df)
        selected_seasons = st.multiselect("Wybierz sezon", seasons, default='00/01')
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
                    hoverlabel=dict(font=dict(size=14, color='white'), bgcolor='red'),
                    hovertext=[f"Punkty drużyny {club} w sezonie {season}: <b>{points}</b>" for points in chart_season['Punkty']],
                    hovertemplate="%{hovertext}<extra></extra>"
                )
            )
        fig3.update_layout(
                xaxis_title='Kolejka',
                yaxis_title='Punkty',
                height=500,
                xaxis=dict(
                    range = [-0.5, 43] if ("92/93" in selected_seasons or "93/94" in selected_seasons or "94/95" in selected_seasons) else [-0.5, 39]
                ),
                legend=dict(
                    title=dict(text="Sezon", font=dict(size=25, color='black')),
                    font=dict(size=20, color='black'),
                    orientation="v",
                    yanchor="top",
                    y=1.1,
                    xanchor="right",
                    x=1.1
                ),
                width=1200,
                yaxis_title_font=dict(size=20, color='black'),
                xaxis_title_font=dict(size=20, color='black'),
                xaxis_tickfont=dict(size=15, color='black'),
                hovermode='x',
                yaxis=dict(
                    range=[-2, round(max(max_value1, default=0), -1) + 10],
                    tickfont=dict(size=15, color='black'),
                    showgrid=True,
                    gridwidth=2,
                    gridcolor='lightgray'
                )
        )
        st.plotly_chart(fig3, use_container_width=True)
    st.header('Statystyki dotyczące bezpośrednich starć drużyn')
    team1 = st.selectbox("Wybierz pierwszą drużynę :", unique_teams)
    team2 = st.selectbox('Wybierz drugą drużynę', return_opponents(df=df, selected_team=team1))
    fig4 = go.Figure()
    wyniki = head_to_head_results(df, team1, team2)
    fig4.add_traces(
        go.Bar(
            x=wyniki['result'],
            y=wyniki['count'],
            text=wyniki['count'],
            textfont=dict(size=16, color='white'),
            showlegend=False,
            marker=dict(color=['blue', '#cd7f32', 'green']),
            hovertemplate='Liczba rezultatów: %{y} <extra></extra>',
            hoverlabel=dict(
                font=dict(size=14, color='white'),
                bgcolor=['blue', '#cd7f32', 'green']
            )
        )
    )
    fig4.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode='markers',
            marker=dict(color='blue', size=10),
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
            marker=dict(color='green', size=10),
            name=f'Ilość zwycięstw drużyny {team2}'
        )
    )

    fig4.update_layout(
        xaxis_title="Wyniki starcia",
        margin=dict(l=50, r=50, t=15, b=50),
        yaxis=dict(
            range=[0, int(max(wyniki['count'])) + (2 if max(wyniki['count']) > 7 else 0)],
            tickfont=dict(size=13, color='black'),
            showgrid=True,
            gridwidth=2,
            gridcolor='lightgray'
        ),
        legend=dict(font=dict(size=16)),
        yaxis_title="Liczba rezultatów",
        yaxis_title_font=dict(size=20, color='black'),
        xaxis_title_font=dict(size=20, color='black'),
        height=500,
        width=1200,
        xaxis_tickfont=dict(size=13, color='black')
    )
    fig4.update_yaxes(zeroline=False, zerolinewidth=0)
    st.plotly_chart(fig4, use_container_width=True)


elif selected_tab == "Transfery":
    st.markdown('---')
