# PV Calc

A simple script to parse Solar Assistant solar data.

Usage:

1. Go to SolarAssistant Charts tab.
2. Select filter, for example Last 30 days.
3. Go to PV power chart, click on title, select Inspect.
4. Click Download CSV.
5. Then parse the downloaded file:

```
python3 pv_calc.py ~/Downloads/PV\ power-data-2024-10-30\ 18_00_35.csv
```

