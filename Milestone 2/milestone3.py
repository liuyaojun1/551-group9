import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt
import warnings

# 1. DISABLE ALTAIR ROW LIMIT
alt.data_transformers.disable_max_rows()
warnings.filterwarnings("ignore")

# =============================================================================
# 2. DATA LOADING
# =============================================================================
try:
    impacts = pd.read_csv("database.csv", low_memory=False)
except FileNotFoundError:
    impacts = pd.DataFrame()

# --- Pre-Process Data ---
required_cols = ['Incident Year', 'Species Name', 'Aircraft Damage', 
                 'Injuries', 'Fatalities', 'Flight Phase', 'State', 'Time of Day', 'Aircraft Type']

for col in required_cols:
    if col not in impacts.columns:
        impacts[col] = 'Unknown'

impacts = impacts[required_cols].copy()

# Fill NAs
impacts["Flight Phase"] = impacts["Flight Phase"].fillna("UNKNOWN")
impacts["Species Name"] = impacts["Species Name"].fillna("UNKNOWN BIRD")
impacts["State"] = impacts["State"].fillna("Unknown")
impacts["Time of Day"] = impacts["Time of Day"].fillna("Unknown")
impacts['Incident Year'] = pd.to_numeric(impacts['Incident Year'], errors='coerce')
impacts['Aircraft Damage'] = pd.to_numeric(impacts['Aircraft Damage'], errors='coerce').fillna(0)
impacts["Fatalities"] = pd.to_numeric(impacts["Fatalities"], errors='coerce').fillna(0)
impacts["Injuries"] = pd.to_numeric(impacts["Injuries"], errors='coerce').fillna(0)

# Filter out "Unknown" species globally
impacts = impacts[~impacts['Species Name'].str.contains('UNKNOWN', case=False, na=False)]

# =============================================================================
# 3. APP SETUP
# =============================================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Wildlife Strikes Dashboard"

app.layout = dbc.Container([
    html.H1("FAA Aircraft Wildlife Strikes", className="display-5 text-center my-3"),
    html.Hr(),

    dbc.Row([
        # --- Sidebar ---
        dbc.Col([
            # 1. Statistics Card (EXPANDED)
            html.Div([
                html.H5("Key Statistics", className="card-title text-primary"),
                html.Hr(),
                
                # Use a simple grid layout for stats
                dbc.Row([
                    dbc.Col([
                        html.Small("Total Incidents", className="text-muted"),
                        html.H4(id='stat-incidents', className="fw-bold")
                    ], width=6),
                    dbc.Col([
                        html.Small("Unique Species", className="text-muted"),
                        html.H4(id='stat-species', className="fw-bold")
                    ], width=6),
                ], className="mb-3"),

                dbc.Row([
                    dbc.Col([
                        html.Small("States Affected", className="text-muted"),
                        html.H4(id='stat-states', className="fw-bold")
                    ], width=6),
                    dbc.Col([
                        html.Small("Reports w/ Damage", className="text-muted"),
                        html.H4(id='stat-damage', className="fw-bold")
                    ], width=6),
                ], className="mb-3"),

                dbc.Row([
                    dbc.Col([
                        html.Small("Total Injuries", className="text-muted"),
                        html.H4(id='stat-injuries', className="text-warning")
                    ], width=6),
                    dbc.Col([
                        html.Small("Total Fatalities", className="text-muted"),
                        html.H4(id='stat-fatalities', className="text-danger")
                    ], width=6),
                ]),
                
            ], className="card p-3 bg-white shadow-sm mb-4 border-primary"),

            # 2. Filters Card
            html.Div([
                html.H5("Filters", className="card-title"),
                html.Label("Outcome Scope:", className="fw-bold mt-2"),
                dcc.Dropdown(
                    id='outcome-filter',
                    options=[
                        {'label': 'All Impacts', 'value': 'all'},
                        {'label': 'Damage', 'value': 'damage'},
                        {'label': 'Injuries', 'value': 'injury'},
                        {'label': 'Death', 'value': 'death'}
                    ],
                    value='all',
                    clearable=False
                ),
                html.Label("Year Range:", className="mt-3 fw-bold"),
                dcc.RangeSlider(
                    id='year-slider',
                    min=1990, max=2015, step=1,
                    value=[2000, 2015],
                    marks={y: str(y) for y in range(1990, 2016, 10)}
                ),
                html.Hr(),
                html.Label("Panel D Breakdown:", className="fw-bold"),
                dcc.Dropdown(
                    id='breakdown-filter',
                    options=[
                        {'label': 'Flight Phase', 'value': 'Flight Phase'},
                        {'label': 'Time of Day', 'value': 'Time of Day'},
                        {'label': 'Aircraft Type', 'value': 'Aircraft Type'}
                    ],
                    value='Flight Phase',
                    clearable=False
                ),
            ], className="card p-3 bg-light shadow-sm")
        ], width=3),

        # --- Main Charts Area ---
        dbc.Col([
            html.Div([
                html.H5("Top 10 Analysis (Interactive)", className="text-center mb-3"),
                html.Iframe(
                    id='main-plot',
                    style={'border-width': '0', 'width': '100%', 'height': '900px'}
                )
            ])
        ], width=9)
    ])
], fluid=True)

# =============================================================================
# 4. CALLBACKS
# =============================================================================
@app.callback(
    [Output('main-plot', 'srcDoc'),
     Output('stat-incidents', 'children'),
     Output('stat-species', 'children'),
     Output('stat-states', 'children'),
     Output('stat-damage', 'children'),
     Output('stat-injuries', 'children'),
     Output('stat-fatalities', 'children')],
    [Input('outcome-filter', 'value'),
     Input('year-slider', 'value'),
     Input('breakdown-filter', 'value')]
)
def update_dashboard(outcome, years, breakdown_col):
    # 1. Global Filter
    df = impacts[
        (impacts['Incident Year'] >= years[0]) & 
        (impacts['Incident Year'] <= years[1])
    ]
    
    if outcome == 'damage':
        df = df[df['Aircraft Damage'] == 1]
    elif outcome == 'injury':
        df = df[df['Injuries'] > 0]
    elif outcome == 'death':
        df = df[df['Fatalities'] > 0]

    # 2. CALCULATE EXPANDED STATS
    stat_incidents = f"{len(df):,}"
    stat_species = f"{df['Species Name'].nunique():,}"
    stat_states = f"{df['State'].nunique()}"
    stat_damage = f"{df[df['Aircraft Damage'] == 1].shape[0]:,}"
    stat_injuries = f"{int(df['Injuries'].sum()):,}"
    stat_fatalities = f"{int(df['Fatalities'].sum())}"

    # 3. Top 10 Filter (For Charts Only)
    top_species = df['Species Name'].value_counts().head(10).index.tolist()
    df_chart = df[df['Species Name'].isin(top_species)]
    
    if len(df_chart) == 0:
        return "<h3>No data available.</h3>", stat_incidents, stat_species, stat_states, stat_damage, stat_injuries, stat_fatalities

    # 4. Altair Charts
    selector = alt.selection_point(fields=['Species Name'], empty='all')
    color_scale = alt.condition(selector, alt.value('steelblue'), alt.value('lightgray'))
    base = alt.Chart(df_chart).add_params(selector)

    # Panel A: Top 10 Species
    chart_a = base.mark_bar().encode(
        y=alt.Y('Species Name', sort='-x', title='Species'),
        x=alt.X('count()', title='Count'),
        color=color_scale,
        tooltip=['Species Name', 'count()']
    ).properties(title='Panel A: Top 10 Species', width=350, height=350)

    # Panel B: Trend
    chart_b = base.mark_line(point=True).encode(
        x=alt.X('Incident Year:O', title='Year'),
        y=alt.Y('count()', title='Incidents'),
        color=alt.value('firebrick'),
        tooltip=['Incident Year', 'count()']
    ).transform_filter(selector).properties(title='Panel B: Trend', width=350, height=350)

    # Panel C: Top 10 States
    chart_c = base.mark_bar().encode(
        x=alt.X('count:Q', title='Incidents'),
        y=alt.Y('State:N', sort='-x'),
        color=alt.value('seagreen'),
        tooltip=['State', 'count:Q']
    ).transform_filter(selector).transform_aggregate(
        count='count()',
        groupby=['State']
    ).transform_window(
        rank='rank(count)',
        sort=[alt.SortField('count', order='descending')]
    ).transform_filter(alt.datum.rank <= 10).properties(title='Panel C: Top 10 States', width=350, height=350)

    # Panel D: Breakdown
    chart_d = base.mark_bar().encode(
        x=alt.X('count:Q', title='Incidents'),
        y=alt.Y(breakdown_col, sort='-x'),
        color=alt.value('orange'),
        tooltip=[breakdown_col, 'count:Q']
    ).transform_filter(selector).transform_aggregate(
        count='count()',
        groupby=[breakdown_col]
    ).transform_window(
        rank='rank(count)',
        sort=[alt.SortField('count', order='descending')]
    ).transform_filter(alt.datum.rank <= 10).properties(title=f'Panel D: Top 10 {breakdown_col}', width=350, height=350)

    final_chart = (chart_a | chart_b) & (chart_c | chart_d)
    
    return final_chart.to_html(), stat_incidents, stat_species, stat_states, stat_damage, stat_injuries, stat_fatalities

if __name__ == '__main__':
    app.run(debug=False)