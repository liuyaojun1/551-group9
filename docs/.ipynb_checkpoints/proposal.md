# **Flight–Animal Impact Dashboard Proposal**

## **Motivation and Purpose**

**Our role:** Data science consultancy firm    
**Target audience:** Airport administrators  

Although flying is a safe mode of transportation, wildlife strikes can still lead to costly outcomes, including aircraft damage, injuries, and (rarely) fatalities. Airport administrators benefit from understanding which species and operating conditions are most associated with severe outcomes, so that mitigation and monitoring efforts can be prioritized.

This dashboard uses the FAA Aircraft Wildlife Strikes dataset (1990–2015) to support two practical tasks:    
1\) Rank species by frequency under different outcome severities, and    
2\) Explain the conditions under which higher-severity outcomes concentrate.

Users begin by selecting an outcome scope from four options: (i) all impacts, (ii) impacts that caused aircraft damage, (iii) impacts that caused injury, or (iv) impacts that caused death. This allows direct comparison between “most frequent” species and species associated with more serious consequences. Users can further narrow the data with filters such as year range, species search, airport/state, and aircraft type. The interface is organized into coordinated panels so that selecting a species in the ranking view updates the remaining panels. A time-trend panel also supports selecting a date range to filter the other panels, enabling investigation of specific time windows.

## **Description of the Data**

We use the FAA Aircraft Wildlife Strikes dataset, which records wildlife strike incidents between 1990-01-01 and 2015-09-30. The dataset contains approximately 174,000 events, where each record represents a single wildlife strike incident. The data include aircraft characteristics, wildlife species, environmental conditions, and reported outcomes.

The dashboard defines severity using three outcome variables:

\- Aircraft Damage (binary indicator)    
\- Number of Injuries    
\- Number of Fatalities  

Severe outcomes are rare compared with total impacts, which motivates allowing users to switch between severity scopes rather than relying only on overall frequency.

Key explanatory variables used in the dashboard include:

\- Species Name    
\- Incident Date and Incident Year    
\- Height of strike    
\- Flight Phase    
\- Impact location on aircraft (e.g., engine, wing, windshield)    
\- Environmental indicators such as visibility or precipitation  

Limited data preparation will be applied to ensure consistent visualization and grouping:

\- Converting height and speed units for interpretability    
\- Standardizing missing categorical values as explicit “unknown” categories    
\- Reconstructing incident dates from year, month, and day fields    
\- Preserving strike and damage location fields for grouping in visualizations  

These steps maintain interpretability while ensuring that filters and groupings operate on consistent variables.

## **Research Questions and Usage Scenarios**

### **Research Questions**

The dashboard is designed to help airport administrators explore the following questions:

1\. Where do higher-severity impacts occur?    
   Are severe incidents more concentrated at runway level or during specific phases of flight?

2\. Which species and conditions are most associated with severe outcomes?    
   Do species rankings change when moving from all impacts to damage, injury, or fatal events?

3\. Which aircraft components are most vulnerable during severe incidents?    
   Are engines, windshields, or other parts more frequently involved in higher-severity outcomes?

4\. Are severe outcomes changing over time?    
   Do trends over the study period suggest improvement or deterioration in operational risk?

### **Usage Scenario**

Consider an airport wildlife management coordinator responsible for reducing aircraft damage. The coordinator begins by selecting the “aircraft damage” severity scope to focus only on incidents with operational impact. A ranking view highlights species most frequently associated with damage events. After selecting a species of interest, the coordinator examines yearly trends to determine whether incidents involving that species are increasing or decreasing.

Next, the coordinator groups incidents by flight phase or impact location to understand when and where damage is most likely to occur. If damage events cluster during takeoff or landing, or frequently involve engines, mitigation strategies such as habitat management or monitoring schedules can be adjusted. By switching between severity levels and adjusting filters, the coordinator can move from broad exploration to focused operational insights.

## **Summary of Planned Interface**

The dashboard will consist of four coordinated panels designed for interactive exploration:

**Panel A:** Species ranking bar chart and sortable table under the selected severity scope and filters. Selecting a species updates the remaining panels.    
**Panel B:** Yearly time-trend visualization for the selected species, with optional date-range filtering that updates other views.    
**Panel C:**  Geographic summary showing the distribution of incidents under the current filters.    
**Panel D:** Grouped breakdown using controls such as flight phase or impact location to reveal how risk concentrates within the filtered dataset.

Users will be able to filter by severity level, year range, species, aircraft type, and location. The coordinated panel design allows administrators to compare frequency and severity while investigating how operational conditions relate to higher-impact events. The scope of the interface is intentionally limited to ensure the dashboard remains feasible to implement within the timeline of the course.

