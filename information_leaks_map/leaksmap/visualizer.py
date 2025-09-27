from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Title, FactorRange, Legend
from bokeh.embed import components
from bokeh.palettes import Category10
from bokeh.transform import factor_cmap
from .models import Breach
import pandas as pd
from datetime import datetime
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

def create_breach_visualization(user, data_type_filter: Optional[str] = None,
                                start_date: Optional[str] = None,
                                end_date: Optional[str] = None) -> Optional[str]:
    """
    Create a visualization of breaches using Bokeh with improved features.

    :param user: User object to filter breaches
    :param data_type_filter: Optional filter for data types
    :param start_date: Optional start date filter (YYYY-MM-DD)
    :param end_date: Optional end date filter (YYYY-MM-DD)
    :return: HTML string with visualization or None if no data
    """
    try:
        # Apply filters
        breaches = Breach.objects.filter(user=user)

        if data_type_filter:
            breaches = breaches.filter(data_type=data_type_filter)

        if start_date:
            try:
                start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                breaches = breaches.filter(breach_date__gte=start_dt)
            except ValueError:
                logger.warning(f"Invalid start_date format: {start_date}")

        if end_date:
            try:
                end_dt = datetime.strptime(end_date, "%Y-%m-%d")
                breaches = breaches.filter(breach_date__lte=end_dt)
            except ValueError:
                logger.warning(f"Invalid end_date format: {end_date}")

        if not breaches.exists():
            return None

        # Prepare data for visualization
        data = {
            'service_name': [breach.service_name for breach in breaches],
            'breach_date': [breach.breach_date for breach in breaches],
            'location': [breach.location for breach in breaches],
            'data_type': [breach.data_type for breach in breaches],
            'description': [breach.description for breach in breaches]
        }

        # Create a DataFrame
        df = pd.DataFrame(data)

        # Convert breach_date to datetime if needed
        try:
            df['breach_date'] = pd.to_datetime(df['breach_date'])
        except Exception as e:
            logger.error(f"Error converting breach_date to datetime: {str(e)}")
            return None

        # Create unique service names for categorical axis
        unique_services = sorted(df['service_name'].unique())
        service_factor = pd.Categorical(df['service_name'], categories=unique_services)

        # Create a ColumnDataSource
        source = ColumnDataSource(df.assign(service_factor=service_factor))

        # Create a figure with categorical y-axis
        p = figure(
            x_axis_type="datetime",
            y_range=FactorRange(factors=unique_services),
            height=500,
            width=900,
            tools="pan,wheel_zoom,box_zoom,reset,save"
        )

        # Set title
        title = Title()
        title.text = "Визуализация утечек данных"
        title.text_font_size = "18pt"
        p.title = title

        # Use different colors for different data types
        unique_data_types = df['data_type'].unique()
        color_map = factor_cmap(
            'data_type',
            palette=Category10[len(unique_data_types)],
            factors=sorted(unique_data_types)
        )

        # Add scatter plot with different colors by data type
        scatter = p.scatter(
            x='breach_date',
            y='service_factor',
            source=source,
            size=12,
            color=color_map,
            alpha=0.7,
            legend_field='data_type'
        )

        # Add HoverTool with improved formatting
        hover = HoverTool()
        hover.tooltips = [
            ("Сервис", "@service_name"),
            ("Дата", "@breach_date{%F}"),
            ("Локация", "@location"),
            ("Тип данных", "@data_type"),
            ("Описание", "@description")
        ]
        hover.formatters = {
            '@breach_date': 'datetime'
        }
        p.add_tools(hover)

        # Customize the plot
        p.xaxis.axis_label = "Дата утечки"
        p.yaxis.axis_label = "Сервис"
        p.ygrid.grid_line_color = None
        p.legend.location = "top_right"
        p.legend.orientation = "vertical"
        p.legend.click_policy = "hide"

        # Convert the plot to HTML
        script, div = components(p)
        return script + div

    except Exception as e:
        logger.error(f"Error creating visualization: {str(e)}")
        return None
