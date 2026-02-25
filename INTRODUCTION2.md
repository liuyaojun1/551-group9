# Milestone 2 Submission Introduction

## App Name
**Flight–Animal Impacts Explorer** (FAA Wildlife Strikes Dashboard)

## Overview
This project builds an interactive dashboard on the **FAA Aircraft Wildlife Strikes dataset (1990–2015)** to help users explore which bird species are associated with the **most frequent** and **most severe** outcomes of wildlife strikes. The app is designed to support fast exploratory analysis through coordinated views: users select an outcome scope, apply filters, and then investigate how risk varies over time, across geography, and across flight/impact conditions. :contentReference[oaicite:0]{index=0}

## Problem Statement
Wildlife strikes can lead to operational disruption and, in rare cases, serious consequences such as aircraft damage, injury, or death. However, identifying **which species** are most associated with severe outcomes—and under what conditions incidents concentrate—requires navigating multiple dimensions (time, location, aircraft type, flight phase, etc.). Raw tables make this difficult. Our dashboard addresses this by providing linked visual panels that support both **ranking** and **explanation**. :contentReference[oaicite:1]{index=1}

## Target Audience
The app is intended for users who need to explore wildlife strike risk patterns, including:
- aviation safety analysts and researchers
- airport/airline operations stakeholders
- students learning exploratory data analysis and interactive visualization

## Milestone 2 Scope (Prototype)
Milestone 2 focuses on delivering a **functional prototype** that demonstrates the core workflow and interaction design:
1. Choose an **outcome scope** (severity level)
2. Apply filters (e.g., year range, species search, airport/state, aircraft type)
3. Explore coordinated panels that update based on selections :contentReference[oaicite:2]{index=2}

## Core User Workflow and Coordinated Panels
The interface is organized into **four coordinated panels**: :contentReference[oaicite:3]{index=3}

- **Panel A — Species Ranking**
  - Ranks species for the selected outcome scope and filters
  - Uses a bar chart and a small sortable table for exact counts/values
  - Selecting a species drives updates in Panels B–D

- **Panel B — Time Trend**
  - Shows a year-by-year trend for the selected species
  - Helps determine whether the selected outcome is increasing or decreasing over 1990–2015

- **Panel C — Geographic Summary**
  - Summarizes where incidents occur geographically (e.g., state-level map or equivalent summary)

- **Panel D — Deeper Breakdown (“Group by”)**
  - Provides a deeper breakdown controlled by a “group by” selector with three options:
    - time of day
    - impact location on the aircraft
    - flight phase
  - Displays a comparison plot (e.g., grouped/stacked bars or heatmap) to show where risk concentrates

## What Is Planned for Future Milestones
Future milestones will focus on usability polish, richer interactions, performance improvements, and incorporating user feedback, while completing deployment and final documentation.

## Links
- **GitHub Repository:** https://github.com/liuyaojun1/Flight-Animal-Impacts :contentReference[oaicite:4]{index=4}
- **Deployed App:** *(add deployment link here if available)*

## Team Notes
This Milestone 2 submission emphasizes a working prototype that demonstrates the end-to-end exploratory workflow and the linked multi-panel design, aligned with the initial app concept and sketch.

