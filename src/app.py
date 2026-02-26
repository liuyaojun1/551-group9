import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt
import warnings


warnings.filterwarnings("ignore", category=DeprecationWarning)
alt.data_transformers.disable_max_rows()

# =============================================================================
# DATA LOADING & CLEANING
# =============================================================================
try:
    print("Loading database.csv...")
    impacts = pd.read_csv("database.csv", low_memory=False)
except FileNotFoundError:
    print("Error: database.csv not found.")
    impacts = pd.DataFrame(columns=['Incident Year', 'Species Name', 'Aircraft Damage', 'Injuries', 'Fatalities', 'Flight Phase'])

drop_cols = ["Engine1 Position", "Engine2 Position", "Engine3 Position", "Engine4 Position",
             "Engine Make", "Engine Model", "Engine Type", "Aircraft Make", "Aircraft Model",
             "Aircraft Mass", "Warning Issued", "Airport", "Distance", "Species ID", 
             "Record ID", "Operator ID"]
impacts = impacts.drop(columns=[c for c in drop_cols if c in impacts.columns])

typeMap = {"A": "Airplane", "B": "Helicopter", "J": "Other"}
if "Aircraft Type" in impacts.columns:
    impacts["Aircraft Type"] = impacts["Aircraft Type"].map(typeMap).fillna("Unknown")

impacts["Flight Phase"] = impacts["Flight Phase"].fillna("UNKNOWN")
impacts["Species Name"] = impacts["Species Name"].fillna("UNKNOWN BIRD")
impacts["Fatalities"] = impacts["Fatalities"].fillna(0)
impacts["Injuries"] = impacts["Injuries"].fillna(0)
impacts['Incident Year'] = pd.to_numeric(impacts['Incident Year'], errors='coerce').fillna(0).astype(int)
impacts['Aircraft Damage'] = pd.to_numeric(impacts['Aircraft Damage'], errors='coerce').fillna(0)

# =============================================================================
# APP SETUP & LAYOUT
# =============================================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Interactive Wildlife Strikes"

app.layout = dbc.Container([
    html.H1("Flight–Animal Impact Dashboard", className="display-5 text-center my-4"),
    html.Hr(),

    dbc.Row([
        # --- Sidebar ---
        dbc.Col([
            html.Div([
                html.H5("Filter Controls", className="card-title"),
                html.Label("Outcome Scope:", className="mt-2"),
                dcc.Dropdown(
                    id='outcome-filter',
                    options=[
                        {'label': 'All Impacts', 'value': 'all'},
                        {'label': 'Damage to Aircraft', 'value': 'damage'},
                        {'label': 'Injuries Reported', 'value': 'injury'},
                        {'label': 'Fatalities Reported', 'value': 'death'}
                    ],
                    value='all',
                    clearable=False
                ),
                html.Label("Year Range:", className="mt-4"),
                dcc.RangeSlider(
                    id='year-slider',
                    min=1990, max=2015, step=1,
                    value=[1990, 2015],
                    marks={year: str(year) for year in range(1990, 2016, 5)},
                ),
                html.Hr(),
                html.H6("Interactivity Guide:"),
                html.Ul([
                    html.Li("Click bars to filter species/phase."),
                    html.Li("Drag across timeline to zoom years."),
                    html.Li("Double-click anywhere to reset.")
                ], className="small text-muted")
            ], className="card p-3 bg-light")
        ], width=3),

        # --- Main Visualizations Area ---
        dbc.Col([
            html.Iframe(id='combined-plot', style={'border-width': '0', 'width': '100%', 'height': '1000px'})
        ], width=9)
    ])
], fluid=True)

# =============================================================================
# CALLBACKS (Interactive Logic)
# =============================================================================
@app.callback(
    Output('combined-plot', 'srcDoc'),
    [Input('outcome-filter', 'value'),
     Input('year-slider', 'value')]
)
def update_dashboard(outcome, years):
    df = impacts[(impacts['Incident Year'] >= years[0]) & (impacts['Incident Year'] <= years[1])].copy()
    
    if outcome == 'damage':
        df = df[df['Aircraft Damage'] == 1]
    elif outcome == 'injury':
        df = df[df['Injuries'] > 0]
    elif outcome == 'death':
        df = df[df['Fatalities'] > 0]

    # SELECTIONS
    click_species = alt.selection_point(fields=['Species Name'])
    click_phase = alt.selection_point(fields=['Flight Phase'])
    brush_time = alt.selection_interval(encodings=['x'])

    # --- Plot A: Top Species ---
    chart_a = alt.Chart(df).mark_bar().encode(
        x=alt.X('count_incidents:Q', title='Number of Incidents'),
        y=alt.Y('Species Name:N', sort=alt.EncodingSortField(field='count_incidents', order='descending'), title=''),
        color=alt.condition(click_species, alt.value('steelblue'), alt.value('lightgray')),
        tooltip=['Species Name:N', 'count_incidents:Q']
    ).transform_filter(brush_time).transform_filter(click_phase).transform_aggregate(
        count_incidents='count()', groupby=['Species Name']
    ).transform_window(
        rank='rank(count_incidents)', sort=[alt.SortField('count_incidents', order='descending')]
    ).transform_filter(alt.datum.rank <= 15).add_params(click_species).properties(
        width=380, height=350, title="Panel A: Top Species by Incident Count"
    )

    # --- Plot B: Time Trend ---
    chart_b = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('Incident Year:O', title='Year'),
        y=alt.Y('count():Q', title='Incidents'),
        color=alt.condition(brush_time, alt.value('steelblue'), alt.value('lightgray')),
        tooltip=['Incident Year:O', 'count():Q']
    ).transform_filter(click_species).transform_filter(click_phase).add_params(brush_time).properties(
        width=380, height=300, title="Panel B: Incidents Over Time"
    )

    # --- Plot D: Flight Phase ---
    chart_d = alt.Chart(df).mark_bar().encode(
        x=alt.X('count():Q', title='Incidents'),
        y=alt.Y('Flight Phase:N', sort='-x', title=''),
        color=alt.condition(click_phase, alt.Color('Flight Phase:N', legend=None), alt.value('lightgray')),
        tooltip=['Flight Phase:N', 'count():Q']
    ).transform_filter(brush_time).transform_filter(click_species).add_params(click_phase).properties(
        width=380, height=300, title="Panel D: Incidents by Flight Phase"
    )

    # --- Placeholder for Panel C ---
    chart_c_placeholder = alt.Chart(pd.DataFrame({'x': [1]})).mark_text(
        text="Panel C (Coming Soon)", color="lightgray", size=16
    ).encode(
        x=alt.value(190), y=alt.value(175)
    ).properties(
        width=380, height=350
    )

    # --- BUILD THE 2x2 GRID ---
    # Top Row: Panel A on left, Placeholder C on right
    top_row = alt.hconcat(chart_a, chart_c_placeholder, spacing=60)
    
    # Bottom Row: Panel B on left, Panel D on right
    bottom_row = alt.hconcat(chart_b, chart_d, spacing=60).resolve_scale(color='independent')

    # Stack them vertically
    dashboard = alt.vconcat(top_row, bottom_row, spacing=40).configure_view(strokeWidth=0)

    return dashboard.to_html()

if __name__ == '__main__':
    app.run(debug=False)