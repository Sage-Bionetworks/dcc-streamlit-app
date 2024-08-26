import random

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_unique_users_trend(unique_users_data, width=2000, height=400):

    # Group by PROJECT_ID and sum the DISTINCT_USER_COUNT
    grouped_df = (
        unique_users_data.groupby("PROJECT_ID")["DISTINCT_USER_COUNT"]
        .sum()
        .reset_index()
    )

    # Sort by DISTINCT_USER_COUNT in descending order and get the top 10
    top_projects = grouped_df.sort_values(
        by="DISTINCT_USER_COUNT", ascending=False
    ).head(10)
    
    fig = go.Figure()
    for i, project in zip(top_projects.index, top_projects["PROJECT_ID"]):

        # Extract the data for the current project
        filtered_df = unique_users_data[unique_users_data["PROJECT_ID"].isin([project])]
        months = pd.to_datetime(filtered_df["ACCESS_MONTH"])
        counts = filtered_df["DISTINCT_USER_COUNT"]
        project_name = filtered_df["NAME"].iloc[0]  # Assuming NAME is the same for each project

        # Scatter plot for the current project
        fig.add_trace(
            go.Scatter(
                x=months,
                y=list(counts),
                mode="lines+markers",
                name=project,
                line=dict(width=2),
                opacity=0.6,
                hoverinfo="x+y+name",
                hovertemplate="<b>Project Name</b>: " + project_name + "<br>"
                + "<b>Project ID</b>: " + str(project) + "<br>"
                + "<b>Date</b>: %{x}<br>"
                + "<b>Unique User Downloads</b>: %{y}<extra></extra>",
                showlegend=True,
                visible=True,
            )
        )
    # Calculate the median DISTINCT_USER_COUNT for each month
    median_monthly_counts = (
        unique_users_data.groupby("ACCESS_MONTH")["DISTINCT_USER_COUNT"]
        .median()
        .reset_index()
    )
    median_monthly_counts["ACCESS_MONTH"] = pd.to_datetime(
        median_monthly_counts["ACCESS_MONTH"]
    )

    fig.add_trace(
        go.Scatter(
            x=median_monthly_counts["ACCESS_MONTH"],
            y=median_monthly_counts["DISTINCT_USER_COUNT"],
            mode="lines+markers",
            name="Median",
            line=dict(color="black", width=4),
            hoverinfo="x+y+name",
            hovertemplate="<b>Date</b>: %{x}<br><b>Users</b>: %{y}<extra></extra>",
            visible=True,
        )
    )
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Unique User Downloads",
        title="Top 10 Projects by Unique User Downloads",
        width=width,
        height=height,
    )
    return fig


def plot_download_sizes(df, width=2000):
    # Convert project size from TiB to GiB for better comparison
    df["PROJECT_SIZE_IN_GIB"] = df["TOTAL_PROJECT_SIZE_IN_TIB"] 
    df["TOTAL_DOWNLOADS_GIB"] = df["ANNUAL_DOWNLOADS_IN_TIB"] 

    # Sort the DataFrame by total downloads for ordered display
    df = df.sort_values(by="TOTAL_DOWNLOADS_GIB")

    def truncate_name(name, max_length=20):
        return name if len(name) <= max_length else name[:max_length] + "..."

    # Create the bar chart using Plotly
    fig = go.Figure(
        data=[
            go.Bar(
                x=df["NAME"].apply(truncate_name),
                y=df["TOTAL_DOWNLOADS_GIB"],
                marker=dict(
                    color=df["PROJECT_SIZE_IN_GIB"],
                    colorscale="emrld",
                    colorbar=dict(title="Project Size (TiB)"),
                ),
                hovertemplate="<b>Project Name:</b> %{x}<br>"
                + "<b>Project ID:</b> %{customdata[0]}<br>"
                + "<b>Usage (Downloads):</b> %{y:.2f} TiB<br>"
                + "<b>Project Size:</b> %{marker.color:.2f} TiB<extra></extra>",
                customdata=df[["PROJECT_ID"]],
            )
        ]
    )

    # Update the layout of the plot
    fig.update_layout(
        xaxis_title="Project Name",
        yaxis_title="Usage (Downloads in TiB)",
        title="Project Size vs. Download Volumes (in TiB)",
        width=width,
    )
    
    return fig


def plot_popular_entities(popular_entities):
    popular_entities_df = pd.DataFrame(
        list(popular_entities.items()), columns=["Entity Type", "Details"]
    )
    popular_entities_df["Entity Name"] = popular_entities_df["Details"].apply(
        lambda x: x[0]
    )
    popular_entities_df["Unique Users"] = popular_entities_df["Details"].apply(
        lambda x: x[1]
    )
    popular_entities_df = popular_entities_df.drop(columns=["Details"])
    return popular_entities_df


def plot_entity_distribution(entity_distribution):
    entity_df = pd.DataFrame(
        list(entity_distribution.items()), columns=["Entity Type", "Count"]
    )
    fig = px.pie(
        entity_df, names="Entity Type", values="Count", title="Entity Distribution"
    )
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0), title=dict(text="Entity Distribution", x=0.5)
    )
    return fig


def plot_user_downloads_map(locations, width=10000):
    locations_df = pd.DataFrame.from_dict(locations, orient="index")
    locations_df.reset_index(inplace=True)
    locations_df.columns = ["Region", "Latitude", "Longitude", "Most Popular Project"]
    fig = px.scatter_geo(
        locations_df,
        lat="Latitude",
        lon="Longitude",
        text="Region",
        hover_name="Region",
        hover_data={
            "Latitude": False,
            "Longitude": False,
            "Most Popular Project": True,
        },
        size_max=10,
        color=locations_df["Most Popular Project"],
        color_continuous_scale=px.colors.sequential.Plasma,
    )
    fig.update_geos(
        showland=True,
        landcolor="rgb(217, 217, 217)",
        showocean=True,
        oceancolor="LightBlue",
        showcountries=True,
        countrycolor="Black",
        showcoastlines=True,
        coastlinecolor="Black",
    )
    fig.update_layout(
        title="User Downloads by Region",
        geo=dict(
            scope="world", projection=go.layout.geo.Projection(type="natural earth")
        ),
        width=width,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )
    return fig

def plot_citation_stats():

    data = {
    "Year": ["2022", "2023", "2024"],
    "Citations": [300, 360, 420]  # Adjusted citation numbers
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Convert Year column to string to avoid commas in axis labels
    df['Year'] = df['Year'].astype(str)

    # Plot the bar chart using Plotly
    fig = px.bar(df, x="Year", y="Citations", 
                labels={"Citations": "Number of Citations", "Year": "Year"},
                title=" ",
                color_discrete_sequence=["#0f5a5e"])

    # Update x-axis to remove commas
    fig.update_xaxes(tickformat='d')

    # Customize the chart (optional)
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Number of Citations",
        title_x=0.5  # Center the title
    )


    return fig

def plot_human_records():
    # Create a dummy dataset
    data = {
        'Year': [2022, 2023, 2024],
        'Number of Records': [500, 750, 900]
    }

    df = pd.DataFrame(data)

    # Convert Year column to string to avoid commas in axis labels
    df['Year'] = df['Year'].astype(str)

    # Create a bar chart
    fig = px.bar(df,
                 x="Year",
                 y="Number of Records",
                 title=" ",
                 color_discrete_sequence=["#0f5a5e"])
    
    # Update x-axis to remove commas
    fig.update_xaxes(tickformat='d')

    return fig

def plot_map():
    # Dummy data: Replace with your actual download data
    # Load a list of all countries using Plotly's built-in data
    country_list = px.data.gapminder()['country'].unique()

    # Generate random download numbers for each country
    data = {
        'Country': country_list,
        'Downloads': [random.randint(100, 5000) for _ in country_list]
    }

    df = pd.DataFrame(data)

    # Create a world map using Plotly
    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="Downloads",
        hover_name="Country",
        color_continuous_scale="emrld",
        title=" "
    )
    # Update layout to reduce the space between title and chart
    fig.update_layout(
        title_x=0.5,
        title_y=1.,  # Bring the title closer to the chart
        margin={"r":0,"t":100,"l":0,"b":0},  # Adjust margins to tighten layout
        coloraxis_colorbar={
            'title': 'Downloads',
            'lenmode': 'fraction',
            'len': 1.,  # Make the color bar 80% of the map's height
        }
    )

    return fig

