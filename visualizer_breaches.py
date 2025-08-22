import networkx as nx
from bokeh.models import MultiLine, Scatter, LabelSet, ColumnDataSource, HoverTool
from bokeh.plotting import figure, from_networkx, show, output_file
from bokeh.models import CustomJS, Div
from bokeh.layouts import row
from recommendations import print_recommendations_for_breaches, generate_recommendations
from typing import List, Dict

def visualize_breaches_with_info(breaches: List[Dict[str, str]]) -> None:
    """
    Builds a graph of breaches between services and displays text next to the graph.

    :param breaches: List of dictionaries with breach information.
    """
    # Check if there are any breaches
    if not breaches:
        print("No breaches detected.")
        return

    # Create a graph and dictionary to store node information
    G = nx.Graph()
    info_dict = {}

    # Populate the graph and gather node information
    for breach in breaches:
        name = breach.get('service', 'Unknown')
        date = breach.get('breach_date', 'Unknown')
        desc = breach.get('description', 'No description')

        if name not in G:
            G.add_node(name, label=f'{name}\n{date}\n{desc}')
            info_dict[name] = {'dates': [], 'descs': []}

        info_dict[name]['dates'].append(date)
        info_dict[name]['descs'].append(desc)

    # Add edges between nodes
    for i in range(len(breaches)):
        for j in range(i + 1, len(breaches)):
            name_i = breaches[i].get('service', 'Unknown')
            name_j = breaches[j].get('service', 'Unknown')
            if name_i != name_j:
                G.add_edge(name_i, name_j)

    # Create a figure for the graph
    plot = figure(
        max_height=900,
        max_width=1000,
        x_range=(-1.4, 1.4),
        y_range=(-1.4, 1.4),
        x_axis_location=None,
        y_axis_location=None,
        toolbar_location="right",
        tools='tap,pan,wheel_zoom,reset,box_zoom',
        title="Карта информационной уязвимости",
    )

    # Remove grid lines
    plot.grid.grid_line_color = None

    # Create graph layout and renderer
    graph_layout = nx.spring_layout(G, scale=1, center=(0, 0))
    graph_renderer = from_networkx(G, graph_layout)

    # Configure nodes and edges
    graph_renderer.node_renderer.glyph = Scatter(size=15, fill_color="lightblue")
    graph_renderer.edge_renderer.glyph = MultiLine(line_color="black", line_alpha=1, line_width=2)

    # Add graph renderer to the figure
    plot.renderers.append(graph_renderer)

    # Add service name labels
    # Get node coordinates and names
    x, y = zip(*graph_layout.values())
    node_names = list(G.nodes())

    # Create data source for nodes
    source = ColumnDataSource(data=dict(x=x, y=y, name=node_names))
    graph_renderer.node_renderer.data_source.data['name'] = node_names

    # Add labels to nodes
    labels = LabelSet(
        x='x', y='y', text='name', source=source,
        background_fill_color='white', text_align='center',
        text_baseline='middle', x_offset=0, y_offset=10
    )

    # Add labels to the figure
    plot.add_layout(labels)

    # Add text with breach information
    # Prepare information for hover tooltips
    hover_info = []
    for node in node_names:
        dates = ','.join(info_dict[node]['dates'])
        descs = '|'.join(info_dict[node]['descs'])
        info_str = f'Breach Dates: {dates}\nDescription: {descs}'

        hover_info.append(info_str)
    # Add information for hover tooltips
    graph_renderer.node_renderer.data_source.data['info'] = hover_info

    # Add hover tool
    hover_tool = HoverTool(
        tooltips=[
            ('Service', '@name'),
            ('Details', '@info')
        ],
        renderers=[graph_renderer.node_renderer]
    )
    plot.add_tools(hover_tool)

    # Add div for displaying recommendations
    div = Div(
        width=300, height=400,
        styles={
            'border': '1px solid black',
            'padding': '10px',
            'overflow-y': 'auto',
            'white-space': 'pre-wrap',
            'background-color': '#f9f9f9',  # Added background for better readability
            'border-radius': '5px'  # Added rounded corners for better appearance
        },
        text="Нажми на утечку для просмотра рекомендаций"
    )

    # Create dictionary of recommendations in Python (key - node name, value - HTML string with recommendations)
    recs_dict = {}
    for node in node_names:
        recs_ru = generate_recommendations(node, "Russian")
        # Form a string from recommendations with line breaks and HTML markup (br)
        if recs_ru:
            recs_html_ru = f"<b>Recommendations for service {node}:</b><br>" + "<br>".join(recs_ru)
        else:
            recs_html_ru = f"<b>General recommendations:</b><br>" + "<br>".join(generate_recommendations("General", "Russian"))
        recs_dict[node] = recs_html_ru

    # Pass the dictionary of recommendations directly to CustomJS
    recs = recs_dict

    # Pass JSON string to JS and parse it
    callback = CustomJS(args=dict(div=div, source=graph_renderer.node_renderer.data_source, recs=recs), code="""
    const selected_indices = source.selected.indices;
    if (selected_indices.length > 0 && selected_indices[0] !== undefined) {
        const idx = selected_indices[0];
        if (idx >= 0 && idx < source.data['name'].length) {
            const node_name = source.data['name'][idx];
            const recommendations = recs[node_name];
            if (recommendations) {
                div.text = recommendations;
            } else {
                div.text = "No recommendations available.";
            }
        } else {
            div.text = "Invalid selected node index.";
        }
    } else {
        div.text = "Nothing selected.";
    }
    """)
    graph_renderer.node_renderer.data_source.selected.js_on_change('indices', callback)

    # Display graph and Div side by side
    layout = row(plot, div)

    output_file('main.html', title='Карта утечек')
    show(layout)

    # Optimize visualization for large datasets
    if len(breaches) > 100:
        plot.x_range.start = -2
        plot.x_range.end = 2
        plot.y_range.start = -2
        plot.y_range.end = 2
        graph_renderer.node_renderer.glyph.size = 10

    return G
