import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import altair as alt

# =============================================================================
# 1. DATA LOADING & CLEANING
# =============================================================================
try:
    print("Loading database.csv...")
    impacts = pd.read_csv("database.csv", low_memory=False)
except FileNotFoundError:
    print("Error: database.csv not found. Please ensure the file is in the same directory.")
    # Fallback empty dataframe to prevent immediate crash if file is missing
    impacts = pd.DataFrame(columns=['Incident Year', 'Species Name', 'Aircraft Damage', 'Injuries', 'Fatalities', 'Flight Phase'])

# --- Handling Null Values & Mapping ---
drop_cols = ["Engine1 Position", "Engine2 Position", "Engine3 Position", "Engine4 Position",
             "Engine Make", "Engine Model", "Engine Type", "Aircraft Make", "Aircraft Model",
             "Aircraft Mass", "Warning Issued", "Airport", "Distance", "Species ID", 
             "Record ID", "Operator ID"]
# Only drop if they exist
impacts = impacts.drop(columns=[c for c in drop_cols if c in impacts.columns], axis=1)

# Standardize aircraft type if column exists
typeMap = {"A": "Airplane", "B": "Helicopter", "J": "Other"}
if "Aircraft Type" in impacts.columns:
    impacts["Aircraft Type"] = impacts["Aircraft Type"].map(typeMap).fillna("Unknown")

# Fill missing values
impacts["Flight Phase"] = impacts["Flight Phase"].fillna("UNKNOWN")
impacts["Species Name"] = impacts["Species Name"].fillna("UNKNOWN BIRD")
impacts["Fatalities"] = impacts["Fatalities"].fillna(0)
impacts["Injuries"] = impacts["Injuries"].fillna(0)

# Ensure numeric columns are strictly numeric for filtering logic
impacts['Incident Year'] = pd.to_numeric(impacts['Incident Year'], errors='coerce')
impacts['Aircraft Damage'] = pd.to_numeric(impacts['Aircraft Damage'], errors='coerce').fillna(0)

# =============================================================================
# 2. APP SETUP
# =============================================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Wildlife Strikes Dashboard"

# =============================================================================
# 3. APP LAYOUT
# =============================================================================
app.layout = dbc.Container([
    # --- Header ---
    html.H1("Flight–Animal Impact Dashboard", className="display-5 text-center my-4"),
    html.Hr(),

    dbc.Row([
        # --- Sidebar / Controls ---
        dbc.Col([
            html.Div([
                html.H5("Filter Controls", className="card-title"),
                
                # Control 1: Outcome Scope
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
                
                # Control 2: Year Range
                html.Label("Year Range:", className="mt-4"),
                dcc.RangeSlider(
                    id='year-slider',
                    min=1990, max=2015, step=1,
                    value=[1990, 2015],
                    marks={year: str(year) for year in range(1990, 2016, 5)},
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
                
                html.P("Adjust filters to analyze specific risk factors.", className="text-muted mt-4 small")
            ], className="card p-3 bg-light")
        ], width=3),

        # --- Main Visualizations Area ---
        dbc.Col([
            # Row 1: Panel A (Species Ranking)
            dbc.Row([
                dbc.Col([
                    html.H5("Panel A: Top Species by Incident Count"),
                    html.Iframe(id='plot-species', style={'border-width': '0', 'width': '100%', 'height': '400px'})
                ], width=12)
            ], className="mb-4"),

            # Row 2: Panel B (Time Trend) & Panel D (Breakdown)
            dbc.Row([
                dbc.Col([
                    html.H5("Panel B: Incidents Over Time"),
                    html.Iframe(id='plot-trend', style={'border-width': '0', 'width': '100%', 'height': '350px'})
                ], width=6),
                
                dbc.Col([
                    html.H5("Panel D: Incidents by Flight Phase"),
                    html.Iframe(id='plot-phase', style={'border-width': '0', 'width': '100%', 'height': '350px'})
                ], width=6)
            ])
        ], width=9)
    ])
], fluid=True)

# =============================================================================
# 4. CALLBACKS (LOGIC)
# =============================================================================
@app.callback(
    [Output('plot-species', 'srcDoc'),
     Output('plot-trend', 'srcDoc'),
     Output('plot-phase', 'srcDoc')],
    [Input('outcome-filter', 'value'),
     Input('year-slider', 'value')]
)
def update_dashboard(outcome, years):
    # 1. Filter Data by Year
    df_filtered = impacts[
        (impacts['Incident Year'] >= years[0]) & 
        (impacts['Incident Year'] <= years[1])
    ]
    
    # 2. Filter Data by Outcome Scope
    if outcome == 'damage':
        df_filtered = df_filtered[df_filtered['Aircraft Damage'] == 1]
    elif outcome == 'injury':
        df_filtered = df_filtered[df_filtered['Injuries'] > 0]
    elif outcome == 'death':
        df_filtered = df_filtered[df_filtered['Fatalities'] > 0]
    
    # 3. Create Plots
    # --- Plot A: Top Species (Bar Chart) ---
    species_counts = df_filtered['Species Name'].value_counts().reset_index()
    species_counts.columns = ['Species', 'Count']
    species_counts = species_counts.head(20) # Top 20 species

    chart_a = alt.Chart(species_counts).mark_bar().encode(
        x=alt.X('Count', title='Number of Incidents'),
        y=alt.Y('Species', sort='-x', title=''),
        tooltip=['Species', 'Count'],
        color=alt.value('steelblue')
    ).interactive()

    # --- Plot B: Time Trend (Line Chart) ---
    trend_data = df_filtered.groupby('Incident Year').size().reset_index(name='Count')
    
    chart_b = alt.Chart(trend_data).mark_line(point=True).encode(
        x=alt.X('Incident Year', axis=alt.Axis(format='d'), title='Year'),
        y=alt.Y('Count', title='Incidents'),
        tooltip=['Incident Year', 'Count']
    ).interactive()

    # --- Plot D: Flight Phase (Bar Chart) ---
    phase_data = df_filtered['Flight Phase'].value_counts().reset_index()
    phase_data.columns = ['Phase', 'Count']
    
    chart_d = alt.Chart(phase_data).mark_bar().encode(
        x=alt.X('Count', title='Incidents'),
        y=alt.Y('Phase', sort='-x', title=''),
        color=alt.Color('Phase', legend=None),
        tooltip=['Phase', 'Count']
    ).interactive()

    return chart_a.to_html(), chart_b.to_html(), chart_d.to_html()

if __name__ == '__main__':
    app.run(debug=False)