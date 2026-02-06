# Patrol Download Workflow

## Introduction

This workflow helps you to download, process, and visualize patrol data from EarthRanger.

**What this workflow does:**
- Downloads patrol observations and associated events from EarthRanger
- Processes patrol trajectories and events with filtering and trajectory segment analysis
- Exports data in multiple formats (CSV, GeoParquet, GPKG)
- Creates interactive maps showing patrol trajectories and event locations

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
   - You'll need to know the name of your configured data source (e.g., "mep_dev")

3. **Patrol Data** set up in EarthRanger
   - You need to have patrols configured in your EarthRanger system
   - You should know the patrol types you want to analyze
   - You can find them at https://<your-site>.pamdas.org/admin/activity/patrol/

## Installation

1. Open Ecoscope Desktop
2. Select "Workflow Templates"
3. Click "+ Add Template"
4. Copy and paste this URL https://github.com/wildlife-dynamics/wt-download-patrols and wait for the workflow template to be downloaded and initialized
5. The template will now appear in your available template list

## Configuration Guide

### Basic Configuration

#### 1. Workflow Details
Add information that will help to differentiate this workflow from another.

- **Workflow Name** (required): Give your workflow a descriptive name
  - Example: `"Patrol Tracks Events Workflow"`
- **Workflow Description** (optional): Add additional context
  - Example: `"Process and visualize patrol observations and events."`

#### 2. Time Range
Choose the period of time to analyze.

- **Since** (required): The start time
  - Example: `2015-01-10T00:00:00`
- **Until** (required): The end time
  - Example: `2015-02-28T23:59:59`
- **Timezone** (required): Select your timezone for time display
  - Example: `Africa/Nairobi (UTC+03:00)`
  - Note: If not specified, times will be displayed in UTC

#### 3. Data Source
Select one of your configured data sources.

- **Data Source** (required): Choose your EarthRanger connection
  - Example: `"mep_dev"`

#### 4. Patrol and Event Types
Specify which patrols and events to analyze.

- **Patrol Types** (optional): Specify the patrol type(s) to analyze (optional). Leave empty to analyze all patrol types.
  - Example: `["ecoscope_patrol"]`
  - Note: Leave empty (`[]`) to include all patrol types
- **Event Types** (optional): Specify the event type(s) to analyze (optional). Leave this section empty to analyze all event types.
  - Example: `[]` (for all event types)
- **Include Events Without a Geometry** (optional): Include events that don't have a point or polygon location
  - Default: `true`

#### 5. Process Patrol Observations

- **Group Data** (optional): Choose grouping options
  - Leave empty to show all data in a single view
  - Temporal options: `Year`, `Month`, `Year and Month`, `Day of the year`, `Day of the month`, `Day of the week`, `Hour`, `Date`
  - Category options: `Patrol Serial Number`, `Patrol Type`, `Patrol Subject`
- **Style Trajectory By Category** (required): Select the patrol observation attribute to use for categorizing and coloring patrol trajectories on the generated maps.
  - Options: `Patrol Type`, `Patrol Status`, `Patrol Subject`, `Patrol Serial Number`
  - Default: `Patrol Subject`

#### 6. Persist Patrol Trajectories
Choose output formats for patrol trajectory data.

- **Filetypes** (required): Select one or more output formats
  - Options: `csv`, `gpkg`, `geoparquet`
  - Default: `["csv"]`

#### 7. Persist Patrol Events
Choose output formats for patrol event data.

- **Filetypes** (required): Select one or more output formats
  - Options: `csv`, `gpkg`, `geoparquet`
  - Default: `["csv"]`

#### 8. Skip Map Generation
Control whether maps are generated.

- **Skip** (required): Skip generating maps for patrol trajectories and events. Recommended for large datasets to improve performance.
  - Default: `false`

### Advanced Configuration

These optional settings provide additional control over your workflow:

#### Patrol and Event Types
- **Patrol Status** : Choose to analyze patrols with a certain status. If left empty, patrols of all status will be analyzed
  - Example: `["done"]`
  - Options: `active`, `overdue`, `done`, `cancelled`
  - Default: `["done"]`


#### Trajectory Segment Filter
Filter track data by setting limits on track segment length, duration, and speed.

- **Minimum Segment Length (Meters)**:
  - Default: `0.001`
  - Example: `0.001`
- **Maximum Segment Length (Meters)**:
  - Default: `100000`
  - Example: `10000.0`
- **Minimum Segment Duration (Seconds)**: 
  - Default: `1`
  - Example: `1.0`
- **Maximum Segment Duration (Seconds)**:
  - Default: `172800` (2 days)
  - Example: `3600.0` (1 hour)
- **Minimum Segment Speed (Kilometers per Hour)**:
  - Default: `0.01`
  - Example: `0.01`
- **Maximum Segment Speed (Kilometers per Hour)**:
  - Default: `500`
  - Example: `120.0`

#### Process Columns
Customize the columns in your trajectory output.

- **Drop Columns**: List of columns to drop from the output
  - Default includes common internal/system columns: `location`, `end_time`, `message`, `provenance`, `priority`, `priority_label`, `attributes`, `comment`, `patrol_segments`, `updated_at`, `state`, `is_contained_in`, `sort_at`, `icon_id`, `url`, `image_url`, `geojson`, `related_subjects`, `patrols`, `reported_by`
  - Modify the list based on your requirements - add columns you want to hide or remove columns you want to keep

#### Apply SQL Query
Apply custom SQL queries for advanced filtering.

- **Query**: SQL query string to apply to the DataFrame. Use 'df' as the table name in the query.
  - Default: `""`
  - Example: `"SELECT * FROM df WHERE speed_kmhr > 5"`
- **Columns**: Optional list of column names to include in the SQL query context
  - Default: `null`
  - Note: Use this to exclude columns with unsupported data types (list, dict)

#### Apply Coordinate Filter to Patrol Events
Filter patrol events by location.

- **Bounding Box**: Filter coordinates to be inside these bounding coordinates
  - Default: Min Lat: `-90.0`, Max Lat: `90.0`, Min Lon: `-180.0`, Max Lon: `180.0`
  - Example: Set custom boundaries to limit your area of interest
- **Filter Exact Point Coordinates**: Exclude events recorded at specific coordinates
  - Default: `[]`
  - Example: `[{"Latitude ": 0.0, "Longitude": 0.0}, {"Latitude": 1.0, "Longitude": 1.0}]`
  - Note: Useful for filtering out test points or known invalid locations

#### Filename Prefixes
Customize the names of your output files.

- **Persist Patrol Trajectories - Filename Prefix**: Custom prefix for trajectory files
  - Default: `"patrol_trajectories"`
  - Example: `"my_patrols"` will create files like `my_patrols_abc123.csv`
- **Persist Patrol Events - Filename Prefix**: Custom prefix for event files
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

- **File formats**: CSV, GeoParquet, and/or GPKG (based on your selection)
- **Opens in**: Microsoft Excel, Google Sheets (CSV), Python/R (GeoParquet), QGIS/ArcGIS (GPKG)
- **Best for**:
  - CSV: Quick data review and analysis
  - GeoParquet: Large datasets, programmatic analysis
  - GPKG: Spatial analysis in GIS software
- **Contents**: Trajectory segments with movement information
  - `patrol_serial_number`: Unique identifier for each patrol
  - `patrol_type`: Type of patrol conducted
  - `patrol_subject`: Subject/person conducting the patrol
  - `patrol_status`: Status of the patrol (active, done, cancelled, overdue)
  - `segment_start`: Start time of the trajectory segment
  - `timespan_seconds`: Duration of the segment in seconds
  - `speed_kmhr`: Speed during the segment in km/h
  - `dist_meters`: Distance covered in the segment
  - `geometry`: Line geometry of the trajectory segment

#### Patrol Event Data

- **File formats**: CSV, GeoParquet, and/or GPKG (based on your selection)
- **Opens in**: Microsoft Excel, Google Sheets (CSV), Python/R (GeoParquet), QGIS/ArcGIS (GPKG)
- **Best for**:
  - CSV: Quick data review and analysis
  - GeoParquet: Large datasets, programmatic analysis
  - GPKG: Spatial analysis in GIS software
- **Contents**: Events recorded during patrols with normalized event details (coded values are automatically mapped to human-readable display titles)
  - `id`: Unique identifier for the event
  - `patrol_serial_number`: Unique identifier for the associated patrol
  - `event_type`: Type of event recorded
  - `event_time`: Time when the event occurred
  - `geometry`: Point geometry of the event location
  - Additional event details are automatically expanded into separate columns

### Visual Outputs (Dashboard)

The workflow creates an interactive dashboard with map visualizations:

#### Patrol Trajectories and Events Map

- **Format**: Interactive map
- **Features**:
  - Patrol trajectories displayed as colored polylines
  - Events displayed as colored points
  - Color coding based on your selected category (patrol subject, type, status, or serial number)
  - Interactive hover: Shows patrol details when you mouse over trajectories or events
  - Legend: Shows category colors and labels
  - Zoom and pan: Navigate the map to explore different areas
  - Multiple base layers: Switch between terrain, satellite, and other views

### Grouped Outputs

If you selected grouping options, your data and visualizations will be organized into separate views:

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
- **Group Data**: `["%B"]` (group by month)
- **Style Trajectory By Category**: `patrol_subject`
- **Persist Patrol Trajectories**: `["geoparquet", "csv"]`
- **Persist Patrol Events**: `["geoparquet", "csv"]`
- **Skip Map Generation**: `false`

**Result**:
- Separate CSV and GeoParquet files for each month
- Separate map views for each month showing patrol trajectories colored by patrol subject
- Event locations overlaid on each map

---

### Example 2: Patrol Coverage Analysis by Type

**Goal**: Analyze patrol coverage by different patrol types

**Configuration**:
- **Time Range**:
  - Since: `2024-01-01T00:00:00`
  - Until: `2024-12-31T23:59:59`
  - Timezone: `UTC (UTC+00:00)`
- **Patrol Types**: `[]` (all types)
- **Patrol Status**: `["done"]`
- **Group Data**: `["patrol_type"]` (group by patrol type)
- **Style Trajectory By Category**: `patrol_type`
- **Persist Patrol Trajectories**: `["csv"]`
- **Persist Patrol Events**: `["csv"]`

**Result**:
- Separate CSV files for each patrol type
- Separate map views for each patrol type
- Easy comparison of coverage between different patrol types

---

### Example 3: Fast Movement Analysis

**Goal**: Identify fast-moving patrol segments for vehicle patrols

**Configuration**:
- **Time Range**:
  - Since: `2024-06-01T00:00:00`
  - Until: `2024-06-30T23:59:59`
  - Timezone: `Africa/Nairobi (UTC+03:00)`
- **Patrol Types**: `["vehicle_patrol"]`
- **Trajectory Segment Filter**:
  - Minimum Speed: `5.0` km/h
  - Maximum Speed: `60.0` km/h
- **Apply SQL Query**: `"SELECT * FROM df WHERE speed_kmhr > 10"`
- **Style Trajectory By Category**: `patrol_subject`
- **Persist Patrol Trajectories**: `["csv", "gpkg"]`

**Result**:
- Filtered trajectory data showing only fast-moving segments
- GPKG file suitable for GIS analysis
- Map visualization of vehicle patrol routes

---

### Example 4: Event-Focused Analysis

**Goal**: Export patrol events without generating maps for a large dataset

**Configuration**:
- **Time Range**:
  - Since: `2023-01-01T00:00:00`
  - Until: `2024-12-31T23:59:59`
  - Timezone: `UTC (UTC+00:00)`
- **Patrol Types**: `[]` (all types)
- **Event Types**: `[]` (all event types)
- **Patrol Status**: `["done"]`
- **Skip Map Generation**: `true`
- **Persist Patrol Trajectories**: `["csv"]`
- **Persist Patrol Events**: `["geoparquet"]`

**Result**:
- Fast processing for large datasets by skipping map generation
- Lightweight CSV file for trajectory data
- Efficient GeoParquet file for large event datasets
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
- Check that the patrol types you specified exist in your EarthRanger system
  - Visit https://<your-site>.pamdas.org/admin/activity/patrol/ to see available patrol types
- Ensure the patrol status filter includes patrols in your system (try using all statuses: `["active", "overdue", "done", "cancelled"]`)
- Verify that the patrols in your time range have observations and events recorded
- Check if your coordinate filters are too restrictive and excluding all data

#### Workflow runs very slowly

**Problem**: The workflow takes a very long time to complete

**Solutions**:
- Reduce your time range to analyze smaller periods
- Enable "Skip Map Generation" for large datasets to improve performance
- Use more restrictive filters (patrol types, status) to reduce data volume
- Consider grouping by shorter time periods (e.g., by week instead of by year)
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
- Check that your patrol data includes valid GPS coordinates
- Verify that the geometry data is not null for your patrols
- Ensure "Include Events Without a Geometry" is set appropriately for your data
- Try adjusting the coordinate filters to ensure data isn't being excluded
- Check that your trajectory segment filters aren't too restrictive

#### Missing trajectory segments

**Problem**: Some patrol tracks appear incomplete or have gaps

**Solutions**:
- Review your trajectory segment filter settings
- Increase the maximum time between segments (max_time_secs) if patrols have long stationary periods
- Adjust minimum and maximum speed filters to match your patrol activities
- Check the source patrol data in EarthRanger for GPS data gaps
- Verify that observations are being recorded during patrols

#### File export errors

**Problem**: Workflow fails when trying to export data files

**Solutions**:
- Ensure you have write permissions to the output directory
- Check that you have sufficient disk space for the output files
- Try exporting to a single format first (e.g., just CSV) to isolate the issue
- Verify that the data doesn't contain characters that cause file naming conflicts
