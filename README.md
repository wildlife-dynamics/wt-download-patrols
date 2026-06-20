# Patrol Download Workflow

## Introduction

This workflow helps you to download, process, and visualize patrol data from EarthRanger.

**What this workflow does:**
- Downloads patrol observations and associated events from EarthRanger
- Builds patrol trajectories and filters both trajectories and events by a single shared set of location and segment filters
- Lets you refine the downloaded trajectory data with a custom SQL query
- Exports data in multiple formats (CSV, Parquet)
- Creates an interactive map showing patrol trajectories and event locations

**Who should use this:**
- Conservation managers monitoring patrol activities and field operations
- Researchers analyzing patrol patterns and coverage
- Anyone needing to export and visualize patrol tracks and events stored in EarthRanger

## Prerequisites

Before using this workflow, you need:

1. **Ecoscope Desktop** installed on your computer
   - If you haven't installed it yet, please follow the installation instructions for Ecoscope Desktop

2. **EarthRanger Data Source** configured in Ecoscope Desktop
   - You must have already set up a connection to your EarthRanger server
   - Your data source should be configured with proper authentication credentials
   - You'll need to know the name of your configured data source (e.g., `"mep_dev"`)

3. **Patrol Data** set up in EarthRanger
   - You need to have patrols configured in your EarthRanger system
   - You should know the patrol types you want to analyze
   - You can find them in your EarthRanger Admin site under Activity → Patrol Types

## Installation

1. Open Ecoscope Desktop
2. Select "Workflow Templates"
3. Click "+ Add Template"
4. Copy and paste this URL https://github.com/wildlife-dynamics/wt-download-patrols and wait for the workflow template to be downloaded and initialized
5. The template will now appear in your available template list

## Configuration Guide

The configuration form is organized into chapters, shown in this order: **Workflow Details**,
**Data Source**, **Time Range**, **Patrol and Event Types**, **Filter Data**, **Group Data**,
**Refine Patrol Data**, **Patrol Track Download File Format**, **Event Download File Format**,
**Trajectory Category**, and **Generate Maps**.

### Basic Configuration

#### 1. Workflow Details
Add information that will help to differentiate this workflow from another.

- **Workflow Name** (required): Give your workflow a descriptive name
  - Example: `"Patrol Tracks Events Workflow"`
- **Workflow Description** (optional): Add additional context
  - Example: `"Process and visualize patrol observations and events."`

#### 2. Data Source
Select one of your configured data sources.

- **Data Source** (required): Choose your EarthRanger connection
  - Example: `"mep_dev"`

#### 3. Time Range
Choose the period of time to analyze.

- **Since** (required): The start time
  - Example: `2015-01-10T00:00:00`
- **Until** (required): The end time
  - Example: `2015-02-28T23:59:59`
- **Timezone** (required): Select your timezone for time display
  - Example: `Africa/Nairobi (UTC+03:00)`
  - Note: If not specified, times will be displayed in UTC

#### 4. Patrol and Event Types
Specify which patrols and events to download.

- **Patrol Types** (optional): Specify the patrol type(s) to download. Leave this section empty to download all patrol types.
  - Example: `["ecoscope_patrol"]`
  - Help: If you are on Ecoscope Desktop, "Patrol Type" values can be found in your EarthRanger Admin site under Activity → Patrol Types
- **Event Types** (optional): Specify the event type(s) to download. Leave this section empty to download all event types.
  - Example: `["arrest_rep", "snare_rep", "poacher_camp_rep"]`
  - Help: If you are on Ecoscope Desktop, "Event Type" values can be found in your EarthRanger Admin site under Activity → Event Types
- **Include events without a location** (optional): Events without coordinates (point or area) will still appear in your download
  - Default: `true`

#### 5. Filter Data
One filter section that drives **both** the patrol trajectories and the patrol events. All
fields are optional and live under the advanced settings.

- **Bounding Box**: Only include patrol observations and events whose coordinates fall inside this bounding box. Applies to BOTH the patrol trajectories and the patrol events.
  - Default: Min Lon: `-180.0`, Max Lon: `180.0`, Min Lat: `-90.0`, Max Lat: `90.0`
- **Filter Exact Point Coordinates**: Exclude observations and events recorded at these exact coordinates (e.g. known bad GPS fixes). Applies to BOTH the patrol trajectories and the patrol events.
  - Example: `[{x: 180.0, y: 90.0}, {x: 0.0, y: 0.0}, {x: 1.0, y: 1.0}]`
- **Trajectory Filter**: Drop trajectory segments outside these length / time / speed bounds (e.g. to remove implausible jumps). Applies to the patrol trajectories only. See [Trajectory Filter](#trajectory-filter) under Advanced Configuration for the individual bounds.

#### 6. Group Data
Configure how patrols and events are grouped and split into per-group datasets for export and mapping.

- **Group Data** (optional): Choose grouping options
  - Leave empty to show all data in a single view
  - Temporal options: `Year`, `Month`, `Year and Month`, `Day of the year`, `Day of the month`, `Day of the week`, `Hour`, `Date`
  - Category options: `Patrol Serial Number`, `Patrol Type`, `Patrol Subject`

#### 7. Refine Patrol Data
Reshape and organize your patrol trajectory data before downloading.

- **Remove Columns** (optional): Columns listed here will be left out of both the generated map and your download. Leave empty to keep all columns.
  - Note: If you're not sure which columns exist, try running the workflow first to see all available columns.
- **SQL Query** (optional): Write a SQL query to filter or transform your patrol trajectory data. Leave blank to skip this step.
  - Use `df` as the table name
  - Example: `SELECT * FROM df WHERE speed_kmhr > 5`
  - Note: Complex columns are sanitized to JSON strings automatically, so any column can be queried. The query applies only to your downloaded files, **not** the generated map.

#### 8. Patrol Track Download File Format
Choose output formats for patrol trajectory data.

- **Filetypes** (required): Select one or more output formats
  - Options: `csv`, `parquet`
  - Default: `["parquet"]`

#### 9. Event Download File Format
Choose output formats for patrol event data.

- **Filetypes** (required): Select one or more output formats
  - Options: `csv`, `parquet`
  - Default: `["parquet"]`

#### 10. Trajectory Category
Differentiate tracks by color using the selected category.

- **Category** (required): Select the patrol observation attribute to use for categorizing and coloring patrol trajectories on the generated maps.
  - Options: `Patrol Type`, `Patrol Status`, `Patrol Subject`, `Patrol Serial Number`
  - Default: `Patrol Subject`

#### 11. Generate Maps
Control whether maps are generated in the dashboard.

- **Generate maps in dashboard** (optional): When checked, the workflow renders the patrol trajectories and events map in the dashboard.
  - Default: checked (`true`)
  - Help: Not recommended for large datasets to improve performance — uncheck to skip map generation.

### Advanced Configuration

These optional settings provide additional control over your workflow:

#### Patrol and Event Types
- **Patrol Status**: Choose to analyze patrols with a certain status. If left empty, patrols of all status will be analyzed.
  - Example: `["done"]`
  - Options: `active`, `overdue`, `done`, `cancelled`
  - Default: `["done"]`

#### Trajectory Filter
Filter track data by setting limits on track segment length, duration, and speed. These bounds
live on the **Filter Data** card.

- **Minimum Segment Length (Meters)**:
  - Example: `0.001`
- **Maximum Segment Length (Meters)**:
  - Example: `10000.0`
- **Minimum Segment Duration (Seconds)**:
  - Example: `1.0`
- **Maximum Segment Duration (Seconds)**:
  - Example: `3600.0` (1 hour)
- **Minimum Segment Speed (Kilometers per Hour)**:
  - Example: `0.01`
- **Maximum Segment Speed (Kilometers per Hour)**:
  - Example: `120.0`

#### Filename Prefixes
Customize the names of your output files.

- **Patrol Track Download File Format - Filename Prefix**: Custom prefix for trajectory files
  - Default: `"patrol_trajectories"`
  - Example: `"my_patrols"` will create files like `my_patrols_abc123.csv`
- **Event Download File Format - Filename Prefix**: Custom prefix for event files
  - Default: `"patrol_events"`
  - Example: `"patrol_incidents"` will create files like `patrol_incidents_xyz789.csv`

#### Map Base Layers
Select tile layers to use as base layers in map outputs.

- **Map Base Layers**: Choose base map layers
  - Default: World Topo Map and World Imagery
  - Options: Open Street Map, Roadmap, Satellite, Terrain, LandDx, USGS Hillshade, Custom Layer, etc.
  - Note: The first layer in the list will be the bottommost layer displayed
  - You can adjust opacity for each layer from 0 (hidden) to 1 (fully visible)

## Running the Workflow

Once you've configured all the settings:

1. **Review your configuration**
   - Double-check your time range, data source, and patrol types

2. **Save and run**
   - Click the "Submit" button and the workflow will show up in "My Workflows" table
   - Click on "Run" and the workflow will begin processing

3. **Monitor progress and wait for completion**
   - You'll see status updates as the workflow runs
   - Processing time depends on:
     - The size of your date range
     - Number of patrols
     - Number of observations in the system
   - The workflow completes with status "Success" or "Failed"

## Understanding Your Results

After the workflow completes successfully, you'll find your outputs in the designated output folder.

### Data Outputs

Your patrol data will be saved in the format(s) you selected:

#### Patrol Trajectory Data

- **File formats**: CSV, Parquet (based on your selection)
- **Opens in**: Microsoft Excel, Google Sheets (CSV), Python/R (Parquet)
- **Best for**:
  - CSV: Quick data review and analysis
  - Parquet: Large datasets, programmatic analysis
- **Reflects**: the **SQL query** from Refine Patrol Data (if you set one) — this fork is downloads-only
- **Contents**: Trajectory segments with movement information
  - `patrol_serial_number`: Unique identifier for each patrol
  - `patrol_type`: Type of patrol conducted
  - `patrol_subject`: Subject/person conducting the patrol
  - `segment_start`: Start time of the trajectory segment
  - `timespan_seconds`: Duration of the segment in seconds
  - `speed_kmhr`: Speed during the segment in km/h
  - `dist_meters`: Distance covered in the segment
  - `geometry`: Line geometry of the trajectory segment

#### Patrol Event Data

- **File formats**: CSV, Parquet (based on your selection)
- **Opens in**: Microsoft Excel, Google Sheets (CSV), Python/R (Parquet)
- **Best for**:
  - CSV: Quick data review and analysis
  - Parquet: Large datasets, programmatic analysis
- **Contents**: Events recorded during patrols
  - `patrol_serial_number`: Unique identifier for the associated patrol
  - `event_type`: Type of event recorded
  - `time`: Time when the event occurred
  - `geometry`: Point geometry of the event location

### Visual Outputs (Dashboard)

The workflow creates an interactive dashboard with a map visualization (unless you unchecked
"Generate maps in dashboard"):

#### Patrol Trajectories and Events Map

- **Format**: Interactive map
- **Features**:
  - Patrol trajectories displayed as colored polylines
  - Events displayed as colored points
  - Color coding of trajectories based on your selected **Trajectory Category** (patrol subject, type, status, or serial number)
  - Interactive hover: Shows patrol details when you mouse over trajectories or events
  - Legend: Shows category colors and labels
  - Zoom and pan: Navigate the map to explore different areas
  - Multiple base layers: Switch between terrain, satellite, and other views
- **Note**: The map reflects your **Remove Columns** choices but **not** the SQL query (which applies to downloads only).

### Grouped Outputs

If you selected grouping options in **Group Data**, your data and visualizations will be organized into separate views:

- **Temporal grouping**: Data split by time periods (e.g., separate views for each month)
- **Category grouping**: Data split by categories (e.g., separate views for each patrol type or subject)
- Each group will have its own data files and map view
- Navigate between groups using the dashboard interface

## Common Use Cases & Examples

Here are some typical scenarios and how to configure the workflow for each:

### Example 1: Monthly Patrol Summary

**Goal**: Download all patrols for a specific time period, grouped by month for monthly reporting

**Configuration**:
- **Time Range**:
  - Since: `2015-01-10T00:00:00`
  - Until: `2015-02-28T23:59:59`
  - Timezone: `Africa/Nairobi (UTC+03:00)`
- **Patrol Types**: `["ecoscope_patrol"]`
- **Patrol Status**: `["done"]`
- **Group Data**: `Month` (`"%B"`)
- **Trajectory Category**: `Patrol Subject`
- **Patrol Track Download File Format**: `["parquet", "csv"]`
- **Event Download File Format**: `["parquet", "csv"]`
- **Generate maps in dashboard**: checked

**Result**:
- Separate CSV and Parquet files for each month
- Separate map views for each month showing patrol trajectories colored by patrol subject
- Event locations overlaid on each map

---

### Example 2: Patrol Coverage Analysis by Type

**Goal**: Analyze patrol coverage by different patrol types

**Configuration**:
- **Time Range**:
  - Since: `2026-01-01T00:00:00`
  - Until: `2026-01-07T23:59:59`
  - Timezone: `Africa/Nairobi (UTC+03:00)`
- **Patrol Types**: `[]` (all types)
- **Patrol Status**: `["done"]`
- **Group Data**: `Patrol Type`
- **Trajectory Category**: `Patrol Type`
- **Patrol Track Download File Format**: `["parquet", "csv"]`
- **Event Download File Format**: `["parquet"]`

**Result**:
- Separate files for each patrol type
- Separate map views for each patrol type
- Easy comparison of coverage between different patrol types

---

### Example 3: Fast Movement Analysis (downloads-only SQL)

**Goal**: Keep only fast-moving trajectory segments in the downloaded files

**Configuration**:
- **Time Range**:
  - Since: `2015-01-10T00:00:00`
  - Until: `2015-02-28T23:59:59`
  - Timezone: `Africa/Nairobi (UTC+03:00)`
- **Patrol Types**: `["ecoscope_patrol"]`
- **Refine Patrol Data → SQL Query**: `SELECT * FROM df WHERE speed_kmhr > 5.0`
- **Trajectory Category**: `Patrol Subject`
- **Patrol Track Download File Format**: `["csv"]`

**Result**:
- Downloaded trajectory files contain only segments faster than 5 km/h
- The map still shows the full (unfiltered) trajectories — the SQL query applies to downloads only
- No `columns` whitelist is needed; complex columns are sanitized automatically

---

### Example 4: Event-Focused Analysis (maps off)

**Goal**: Export patrol data without generating maps for a large dataset

**Configuration**:
- **Time Range**:
  - Since: `2015-01-01T00:00:00`
  - Until: `2015-12-31T23:59:59`
  - Timezone: `Africa/Nairobi (UTC+03:00)`
- **Patrol Types**: `[]` (all types)
- **Event Types**: `[]` (all event types)
- **Patrol Status**: `["done"]`
- **Generate maps in dashboard**: unchecked
- **Patrol Track Download File Format**: `["parquet", "csv"]`
- **Event Download File Format**: `["parquet", "csv"]`

**Result**:
- Faster processing for large datasets by skipping map generation
- Trajectory and event files in both CSV and Parquet
- No map visualizations (to improve performance)

## Troubleshooting

### Common Issues and Solutions

#### Workflow fails to start

**Problem**: The workflow fails immediately when you try to run it

**Solutions**:
- Check that your EarthRanger data source is properly configured in Ecoscope Desktop
- Verify that you have network connectivity to your EarthRanger server
- Ensure your authentication credentials are valid and not expired
- Try reconnecting your data source in Ecoscope Desktop settings

#### No patrols or events returned

**Problem**: The workflow completes but returns empty data files

**Solutions**:
- Verify your time range covers a period with patrol data in EarthRanger
- Check that the patrol types you specified exist in your EarthRanger system (Admin → Activity → Patrol Types)
- Ensure the patrol status filter includes patrols in your system (try all statuses: `["active", "overdue", "done", "cancelled"]`)
- Check if your **Filter Data** settings (bounding box / excluded points) are too restrictive and excluding all data

#### Workflow runs very slowly

**Problem**: The workflow takes a very long time to complete

**Solutions**:
- Reduce your time range to analyze smaller periods
- Uncheck "Generate maps in dashboard" for large datasets to improve performance
- Use more restrictive filters (patrol types, status) to reduce data volume
- Consider grouping by shorter time periods (e.g., by month instead of by year)
- Note: The first run may be slower as EarthRanger "warms up" the data query. Subsequent runs with similar parameters may be faster.

#### Authentication errors

**Problem**: Workflow fails with authentication or permission errors

**Solutions**:
- Verify your EarthRanger user account has permission to access patrol data
- Check that your API token or credentials haven't expired
- Reconnect your EarthRanger data source in Ecoscope Desktop
- Contact your EarthRanger administrator to verify your account permissions

#### Maps not showing trajectories or events

**Problem**: Maps are generated but appear empty or incomplete

**Solutions**:
- Check that "Generate maps in dashboard" is checked
- Check that your patrol data includes valid GPS coordinates
- Try adjusting the **Filter Data** bounding box / excluded points to ensure data isn't being excluded
- Check that your trajectory filter bounds aren't too restrictive

#### SQL query returns no rows / errors

**Problem**: The downloaded trajectory files are empty or the SQL step fails

**Solutions**:
- Use `df` as the table name (e.g. `SELECT * FROM df WHERE speed_kmhr > 5`)
- Remember the query runs per group, after data is split — overly strict conditions can empty a group
- You do **not** need a `columns` whitelist; complex columns are sanitized automatically
- Leave the SQL Query blank to skip this step entirely

#### File export errors

**Problem**: Workflow fails when trying to export data files

**Solutions**:
- Ensure you have write permissions to the output directory
- Check that you have sufficient disk space for the output files
- Try exporting to a single format first (e.g., just CSV) to isolate the issue
