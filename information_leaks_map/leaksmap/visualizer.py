from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, HoverTool, TapTool, OpenURL
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import CustomJS
from bokeh.transform import factor_cmap
from .models import Breach
import pandas as pd

def create_breach_visualization():
    # Fetch data from the database
    breaches = Breach.objects.all()
    data = {
        'service_name': [breach.service_name for breach in breaches],
        'breach_date': [breach.breach_date for breach in breaches],
        'location': [breach.location for breach in breaches],
        'data_type': [breach.data_type for breach in breaches],
        'description': [breach.description for breach in breaches]
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Create a ColumnDataSource
    source = ColumnDataSource(df)

    # Create a figure
    p = figure(title="Breach Visualization", x_axis_type="datetime", height=400, width=800)

    # Add a line plot for breach dates
    p.line(x='breach_date', y='service_name', source=source, line_width=2, line_alpha=0.6)

    # Add circles for each breach
    p.circle(x='breach_date', y='service_name', source=source, size=10, color='navy', alpha=0.5)

    # Add HoverTool
    hover = HoverTool()
    hover.tooltips = [
        ("Service", "@service_name"),
        ("Date", "@breach_date{%F}"),
        ("Location", "@location"),
        ("Data Type", "@data_type"),
        ("Description", "@description")
    ]
    p.add_tools(hover)

    # Add TapTool to open a URL or show more details
    tap = TapTool()
    tap.callback = OpenURL(url="http://example.com/breach/@service_name")
    p.add_tools(tap)

    # Set output file and show the result
    output_file("breach_visualization.html")
    show(p)

    return p

# Add the visualization to the current document
curdoc().add_root(column(create_breach_visualization()))
