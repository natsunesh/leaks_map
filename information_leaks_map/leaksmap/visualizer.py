from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Title, FactorRange, Legend
from bokeh.embed import components
from bokeh.palettes import Category10
from bokeh.transform import factor_cmap
from .models import Breach
import pandas as pd
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple
import logging
import random

logger = logging.getLogger(__name__)

def create_breach_map(breaches: List[Dict[str, Any]]) -> Optional[str]:
    """
    Create a map visualization of breaches using Bokeh.

    :param breaches: List of breach dictionaries from API
    :return: HTML string with map visualization or None if no data
    """
    try:
        if not breaches:
            logger.warning("No breaches provided for map visualization")
            return None

        # Prepare data for map visualization
        locations = []
        for breach in breaches:
            location = breach.get('location', 'Unknown')
            if location != 'Unknown':
                locations.append(location)

        if not locations:
            logger.warning("No valid locations found for map visualization")
            return None

        # Geocode locations to get latitude and longitude
        lats, lons = geocode_locations(locations)

        source = ColumnDataSource(data=dict(
            lat=lats,
            lon=lons,
            location=locations
        ))

        # Create the map plot
        p = figure(
            height=500,
            width=900,
            tools="pan,wheel_zoom,box_zoom,reset,save"
        )

        p.circle(
            x='lon',
            y='lat',
            source=source,
            color='red',
            alpha=0.7
        )

        hover = HoverTool()
        hover.tooltips = [("Location", "@location")]
        p.add_tools(hover)

        title = Title()
        title.text = "Карта утечек данных"
        title.text_font_size = "18pt"
        p.title = title

        script, div = components(p)
        return script + div

    except Exception as e:
        logger.error(f"Error creating map visualization: {str(e)}")
        return None

def geocode_locations(locations: List[str]) -> Tuple[List[float], List[float]]:
    """
    Geocode locations to get latitude and longitude.
    This is a placeholder function. Replace with actual geocoding logic.
    """
    lats = [random.uniform(-90, 90) for _ in locations]
    lons = [random.uniform(-180, 180) for _ in locations]
    return lats, lons

def create_breach_visualization_from_api(breaches: List[Dict[str, Any]]) -> Optional[str]:
    """
    Create a visualization of breaches using Bokeh with data from API.

    :param breaches: List of breach dictionaries from API
    :return: HTML string with visualization or None if no data
    """
    try:
        if not breaches:
            logger.warning("No breaches provided for visualization")
            return None

        # Prepare data for visualization
        data = {
            'service_name': [breach.get('service_name', 'Unknown') for breach in breaches],
            'breach_date': [breach.get('breach_date', '2000-01-01') for breach in breaches],
            'location': [breach.get('location', 'Unknown') for breach in breaches],
            'data_type': [breach.get('data_type', 'Unknown') for breach in breaches],
            'description': [breach.get('description', 'No description') for breach in breaches]
        }

        # Create a DataFrame
        df = pd.DataFrame(data)

        # Convert breach_date to datetime if needed
        try:
            df['breach_date'] = pd.to_datetime(df['breach_date'], errors='coerce')
            # Drop rows with NaT (Not a Time) values
            df = df.dropna(subset=['breach_date'])
            if df.empty:
                logger.warning("No valid breach dates found")
                return None
        except Exception as e:
            logger.error(f"Error converting breach_date to datetime: {str(e)}")
            return None

        # Create unique service names for categorical axis
        unique_services = sorted(df['service_name'].unique())
        service_factor = pd.Categorical(df['service_name'], categories=unique_services)

        # Create a ColumnDataSource
        source = ColumnDataSource(df.assign(service_factor=service_factor.codes))

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
        num_types = len(unique_data_types)
        if num_types == 0:
            num_types = 1
        # Category10 supports up to 10 colors, use max to avoid index errors
        palette_size = min(num_types, 10)
        color_map = factor_cmap(
            'data_type',
            palette=Category10[palette_size] if palette_size > 0 else Category10[1],
            factors=sorted(unique_data_types) if len(unique_data_types) > 0 else ['Unknown']
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

def create_breach_visualization(user, data_type_filter: Optional[str] = None,
                                start_date: Optional[str] = None,
                                end_date: Optional[str] = None,
                                email: Optional[str] = None) -> Optional[str]:
    """
    Create a visualization of breaches using Bokeh with improved features.

    :param user: User object to filter breaches
    :param data_type_filter: Optional filter for data types
    :param start_date: Optional start date filter (YYYY-MM-DD)
    :param end_date: Optional end date filter (YYYY-MM-DD)
    :param email: Optional email filter
    :return: HTML string with visualization or None if no data
    """
    try:
        # Apply filters
        breaches = Breach.objects.filter(user=user)

        if email:
            breaches = breaches.filter(user__email=email)
        else:
            # If no email is provided, use the user's email
            breaches = breaches.filter(user__email=user.email)

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
            logger.warning("No breaches found for the given filters")
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
            df['breach_date'] = pd.to_datetime(df['breach_date'], errors='coerce')
            # Drop rows with NaT (Not a Time) values
            df = df.dropna(subset=['breach_date'])
            if df.empty:
                logger.warning("No valid breach dates found")
                return None
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
        num_types = len(unique_data_types)
        if num_types == 0:
            num_types = 1
        # Category10 supports up to 10 colors, use max to avoid index errors
        palette_size = min(num_types, 10)
        color_map = factor_cmap(
            'data_type',
            palette=Category10[palette_size] if palette_size > 0 else Category10[1],
            factors=sorted(unique_data_types) if len(unique_data_types) > 0 else ['Unknown']
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
