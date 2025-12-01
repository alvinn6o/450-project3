#CECS 450 Project 3 - Option A - ILS Approach Visualization#

[Quick Demo Video](https://youtu.be/TXTqFz7CSM8)

##About the Dataset#
- Two datasets (Collapsed and Expanded)
  - Contains pilot eye-movement pattern sequences 
- Collected during an Instrument Landing System Approach
- Sequences capture pilot gaze shifts across Areas of Interest (AOIs), with each AOI representing a flight instrument and displayed as a letter (A-H).
- Spreadsheets showed:
  - Rows representing a Pattern Sequence
  - Rows had frequency values
    - How many times the pattern occurs in the dataset
  - Rows had “Sequence Support” (shows proportion)
    - Percentage of how many pilots used the pattern during flight
- The data is separated into two groups with each having sheets with and without the A AOI:
  - Successful
  - Unsuccessful pilots

##Visualization Idea + Features##
**Sequential Index Plot**
- Visualize prominent gaze behavior patterns across pilot groups by encoding AOI sequences as color-coded index plots.

**Features**
- Dual plots for comparative analysis (One for each pilot group).
- Ranking of Top 3 most-viewed AOIs
- AOI Sequence mapping
  - Rows = Full gaze patterns
  - Columns = Indexes
  - Cells = AOI at that point in the sequence
  - Color-Coded AOIs by category
  - Legend shows AOI letter and full label with corresponding color mapping
  - Interactive Hover Tooltips
- Pattern String and Rank
  - AOI Name 
  - Index Position within sequence
  - Raw Frequency
  - Overall percentage of appearance across all AOIs
  - Percentage of appearance at specific index
- Dynamic Filtering (Update both plots simultaneously)
  - Pattern type (Collapsed vs. Expanded)
  - AOI A Filtering (Include or Exclude “No AOI”)
  - Ranking Metrics (Frequency or Sequence Support)
  - Top-K Selection (Top 5-100 patterns or all patterns)

##Data Cleanup Methodology##
1. Standardized Inputs
- Load from both Excel files (Collapsed / Expanded patterns)
- Auto-select sheets by group + AOI-A filter
- Correct misspelled group labels (“Successful” / “Unsuccessful”)
  
2. Normalize Pattern Data
- Convert pattern strings to consistent format
- Trimmed whitespace and validated AOI Letters (A-H)
  
3. Sequence Alignment
- Calculated max pattern length per dataset
- Padded shorter sequences with NaN uniform heatmap alignment

4. Filtering and Ranking
- Sorted by Frequency or Sequence Support
- Applied Top-K cutoff (5-100) with “Show All” override
  
5. AOI Metadata Enrichment
- Mapped AOI letters to Full Names
- Added AOI color legend and enhanced tooltip Information
  
6. Statistical Preprocessing
- Computed AOI overall percentages
- Computed per-index AOI percentages for deeper insight

##Libraries Used##
- Pandas: Loading, cleaning, and transforming the dataset
- Numpy: Numeric operations and adding jitter to dense data points for enhanced readability
- Plotly Express: Building interactive Sequence Index Plot with color coded AOIs and hover tooltips
- Dash: Creating layouts and dropdowns as well as handling dynamic visual update via callbacks

##Setup and Run Instructions##
- Install dependencies: pip install pandas plotly dash numpy
- Make sure all files are in same folder as main.py
- Run the app: python main.py
- Open in your browser Visit: http://127.0.0.1:8050/ (Should appear in your console window)

