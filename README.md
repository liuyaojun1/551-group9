# Flight–Animal Impacts Explorer
*FAA Aircraft Wildlife Strikes Dashboard (1990–2015)*

## Project Overview
This project builds an interactive dashboard using the **FAA Aircraft Wildlife Strikes dataset (1990–2015)** to help users identify which bird species are associated with the **most frequent** and **most severe** wildlife strike outcomes.

Users begin by selecting an **outcome scope** (e.g., *all impacts*, *damage*, *injury*, or *fatality*), then refine the view using filters such as **year range**, **species search**, **airport/state**, and **aircraft type**. The dashboard supports exploratory analysis through **linked, coordinated panels** that help users both **rank** high-risk species and **explain** when/where risks concentrate.

## Problem Statement
Wildlife strikes can cause operational disruption and, in rare cases, serious consequences such as aircraft damage, injury, or death. Identifying which species and conditions drive risk requires navigating multiple dimensions (time, location, aircraft type, flight phase, etc.). Raw tables make this difficult; this dashboard provides linked visual views to make these patterns easier to explore and compare.

## Target Audience
- Aviation safety analysts and researchers  
- Airport/airline operations stakeholders  
- Students learning exploratory data analysis and interactive visualization

## App Design (Coordinated Panels)
The interface is organized into **four coordinated panels**:

- **Panel A — Species Ranking**
  - Ranks species for the selected outcome scope and filters (bar chart + sortable table for exact values)
  - Selecting a species updates the remaining panels
- **Panel B — Time Trend**
  - Shows a year-by-year trend for the selected species (1990–2015)
- **Panel C — Geographic Summary**
  - Summarizes where incidents occur geographically (e.g., state-level map or summary)
- **Panel D — Deeper Breakdown (“Group by”)**
  - Breaks down the filtered data by one of:
    - time of day
    - impact location on the aircraft
    - flight phase
  - Displays a comparison plot (e.g., grouped/stacked bars or heatmap)

### App Sketch (Milestone 1)
![App sketch](img/app_sketch.png)

---

## Milestone 1 (Design & Planning)
### Required Files
1. **Submission Instruction:** Since canvas-submission.md is no longer required, instead, we uploaded our dataset [here](Milestone%201/database.csv).
2. **Proposal:** [proposal.md](Milestone%201/proposal.md)
3. **Description of your app & sketch:** [README.md](README.md)
4. **Team work contract and collaborative documentation**:
   - [Team work contract](team-contract.md)
   - [Code of Conduct](CODE_OF_CONDUCT.md)
   - [Contribution guidelines](CONTRIBUTING.md)
5. **Start developing your app:** [master-plotter.ipynb](Milestone%201/master-plotter.ipynb)

---

## Milestone 2 (Prototype)
### Scope (Prototype)
Milestone 2 focuses on delivering a **functional prototype** that demonstrates the core workflow and interaction design:
1. Choose an **outcome scope** (severity level)
2. Apply filters (e.g., year range, species search, airport/state, aircraft type)
3. Explore coordinated panels that update based on selections

### What Is Planned for Future Milestones
Future milestones will focus on usability polish, richer interactions, performance improvements, and incorporating user feedback, while completing deployment and final documentation.

### Prototype Screenshot
<img width="1536" height="1024" alt="prototype" src="https://github.com/user-attachments/assets/38893b28-ea6e-41fe-84e5-fa4435f7e956" />

---

## Links
- **GitHub Repository:** https://github.com/liuyaojun1/Flight-Animal-Impacts
- **Deployed App:** *(add deployment link here if available)*
