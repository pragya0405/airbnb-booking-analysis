import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Airbnb NYC Analytics",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────
# Design System & Styling
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --primary: #FF385C;
    --primary-light: #FFF1F3;
    --teal: #00BFA6;
    --amber: #FFD23F;
    --purple: #6C5CE7;
    --cyan: #00CEC9;
    --pink: #FD79A8;
    --dark: #2D2D2D;
    --gray: #717171;
    --light-gray: #F7F7F7;
    --border: #EBEBEB;
    --white: #FFFFFF;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: var(--dark);
}

/* Main content area */
.main .block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

/* Header */
.app-header {
    text-align: center;
    padding: 0.5rem 0 2rem;
}
.app-title {
    font-size: 2.25rem;
    font-weight: 800;
    color: var(--dark);
    letter-spacing: -0.5px;
    margin: 0;
}
.app-title .accent {
    color: var(--primary);
}
.app-subtitle {
    font-size: 0.95rem;
    color: var(--gray);
    margin-top: 0.5rem;
    font-weight: 400;
}

/* Metric / Insight cards */
.metric-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.1rem 1.3rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: box-shadow 0.2s ease;
}
.metric-card:hover {
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
}
.metric-card .accent-bar {
    width: 100%;
    height: 4px;
    border-radius: 2px;
    margin-bottom: 0.7rem;
}
.metric-card .label {
    font-size: 0.72rem;
    color: var(--gray);
    text-transform: uppercase;
    letter-spacing: 0.6px;
    font-weight: 600;
    margin-bottom: 0.35rem;
}
.metric-card .value {
    font-size: 1.45rem;
    font-weight: 700;
    color: var(--dark);
    margin: 0;
    line-height: 1.2;
}
.metric-card .subtext {
    font-size: 0.78rem;
    color: var(--gray);
    margin-top: 0.25rem;
}

/* Section headers */
.section-header {
    font-size: 1rem;
    font-weight: 700;
    color: var(--dark);
    margin: 0 0 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--border);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--white);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .stMarkdown h3,
section[data-testid="stSidebar"] .stMarkdown h4 {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: var(--gray);
    font-weight: 600;
}
.sidebar-brand {
    text-align: center;
    padding: 0.8rem 0 0.3rem;
}
.sidebar-brand .logo {
    font-size: 1.4rem;
    font-weight: 800;
    color: var(--primary);
    letter-spacing: -0.5px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: var(--light-gray);
    border-radius: 10px;
    padding: 4px;
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-weight: 500;
    font-size: 0.85rem;
    padding: 0.5rem 1.3rem;
    color: var(--gray);
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #FFF5F6, #FFFFFF) !important;
    box-shadow: 0 2px 8px rgba(255,56,92,0.15);
    font-weight: 600;
    color: #FF385C !important;
}
.stTabs [data-baseweb="tab-highlight"] {
    background-color: var(--primary);
    height: 0;
}
.stTabs [data-baseweb="tab-border"] {
    display: none;
}

/* Footer */
.app-footer {
    text-align: center;
    padding: 2.5rem 0 1rem;
    border-top: 1px solid var(--border);
    margin-top: 2.5rem;
}
.app-footer p {
    font-size: 0.8rem;
    color: var(--gray);
    margin: 0.25rem 0;
}

/* Data table styling */
.stDataFrame {
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
}

/* Plotly chart container */
.stPlotlyChart {
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.5rem;
    background: var(--white);
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────
PALETTE = ['#FF385C', '#00BFA6', '#FFD23F', '#6C5CE7', '#00CEC9', '#FD79A8',
           '#E17055', '#55EFC4']


def style_chart(fig, height=420, show_legend=False):
    """Apply consistent professional styling to a Plotly figure."""
    fig.update_layout(
        font=dict(family="Inter, sans-serif", size=12, color="#2D2D2D"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=50, r=20, t=40, b=40),
        height=height,
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=11),
        ),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, tickfont=dict(size=11))
    fig.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor="#EBEBEB",
        zeroline=False, tickfont=dict(size=11),
    )
    return fig


# ─────────────────────────────────────────────────────────────────────
# Data Loading
# ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/Airbnb NYC 2019.csv")
    df = df.dropna(subset=['price', 'neighbourhood_group', 'room_type'])
    df = df[df['price'] > 0]
    return df


df = load_data()

# ─────────────────────────────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <p class="app-title">Airbnb NYC <span class="accent">Analytics</span></p>
    <p class="app-subtitle">Pricing insights and booking trends across New York City neighborhoods</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# Sidebar — Filters
# ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand">
            <span class="logo">airbnb</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### Filters")

    boroughs = ['All'] + sorted(df['neighbourhood_group'].unique().tolist())
    selected_borough = st.multiselect("Borough", boroughs, default=['All'])

    room_types = ['All'] + sorted(df['room_type'].unique().tolist())
    selected_room_type = st.multiselect("Room Type", room_types, default=['All'])

    min_price = int(df['price'].min())
    max_price = int(df['price'].quantile(0.95))
    price_range = st.slider("Price Range ($)", min_price, max_price, (min_price, max_price))

# ─────────────────────────────────────────────────────────────────────
# Apply Filters
# ─────────────────────────────────────────────────────────────────────
filtered_df = df.copy()

if 'All' not in selected_borough and len(selected_borough) > 0:
    filtered_df = filtered_df[filtered_df['neighbourhood_group'].isin(selected_borough)]
if 'All' not in selected_room_type and len(selected_room_type) > 0:
    filtered_df = filtered_df[filtered_df['room_type'].isin(selected_room_type)]

filtered_df = filtered_df[
    (filtered_df['price'] >= price_range[0]) & (filtered_df['price'] <= price_range[1])
]

# Guard against empty data after aggressive filtering
if filtered_df.empty:
    st.warning(
        "No listings match your current filters. "
        "Try widening the price range or selecting different boroughs."
    )
    st.stop()

# ─────────────────────────────────────────────────────────────────────
# Sidebar — Quick Stats
# ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("---")
    st.markdown("### Quick Stats")
    c1, c2 = st.columns(2)
    c1.metric("Listings", f"{len(filtered_df):,}")
    c2.metric("Avg Price", f"${filtered_df['price'].mean():.0f}")
    c3, c4 = st.columns(2)
    c3.metric("Min Price", f"${filtered_df['price'].min():.0f}")
    c4.metric("Max Price", f"${filtered_df['price'].max():.0f}")

# ─────────────────────────────────────────────────────────────────────
# Key Insight Cards
# ─────────────────────────────────────────────────────────────────────
borough_prices = filtered_df.groupby('neighbourhood_group')['price'].mean()

st.markdown('<p class="section-header">Key Insights</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    most_exp = borough_prices.idxmax()
    st.markdown(f"""
    <div class="metric-card" style="background: #FFF5F6; border-color: #FFD0D8;">
        <div class="accent-bar" style="background: linear-gradient(90deg, #FF385C, #FF6B9D);"></div>
        <div class="label">Most Expensive</div>
        <div class="value">{most_exp}</div>
        <div class="subtext">Avg ${borough_prices.max():.0f}/night</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    most_aff = borough_prices.idxmin()
    st.markdown(f"""
    <div class="metric-card" style="background: #F0FFFB; border-color: #B2F2E8;">
        <div class="accent-bar" style="background: linear-gradient(90deg, #00BFA6, #00CEC9);"></div>
        <div class="label">Most Affordable</div>
        <div class="value">{most_aff}</div>
        <div class="subtext">Avg ${borough_prices.min():.0f}/night</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    popular = filtered_df['room_type'].mode()[0]
    st.markdown(f"""
    <div class="metric-card" style="background: #FFFDF0; border-color: #FFF0B3;">
        <div class="accent-bar" style="background: linear-gradient(90deg, #FFD23F, #FFB400);"></div>
        <div class="label">Most Common Room</div>
        <div class="value">{popular}</div>
        <div class="subtext">{(filtered_df['room_type'] == popular).sum():,} listings</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    avg_reviews = filtered_df['number_of_reviews'].mean()
    st.markdown(f"""
    <div class="metric-card" style="background: #F5F3FF; border-color: #D5D0FF;">
        <div class="accent-bar" style="background: linear-gradient(90deg, #6C5CE7, #A29BFE);"></div>
        <div class="label">Avg Reviews</div>
        <div class="value">{avg_reviews:.0f}</div>
        <div class="subtext">per listing</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top:1.5rem'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# Tabs
# ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "Price Analysis",
    "Geographic Insights",
    "Correlations",
    "Advanced Analytics",
])

# ── Tab 1: Price Analysis ─────────────────────────────────────────────
with tab1:
    st.markdown('<p class="section-header">Average Price by Borough</p>',
                unsafe_allow_html=True)
    a, b = st.columns(2)

    with a:
        avg_borough = (filtered_df.groupby('neighbourhood_group')['price']
                        .mean().sort_values(ascending=False).reset_index())
        fig1 = px.bar(
            avg_borough, x='neighbourhood_group', y='price',
            color='price', color_continuous_scale='Plasma',
            labels={'neighbourhood_group': 'Borough', 'price': 'Avg Price ($)'},
            text='price',
        )
        fig1.update_traces(
            texttemplate='$%{text:,.0f}', textposition='outside',
            textfont=dict(size=11),
        )
        fig1.update_coloraxes(showscale=False)
        fig1 = style_chart(fig1)
        st.plotly_chart(fig1, use_container_width=True)

    with b:
        st.markdown('<p class="section-header">Average Price by Room Type</p>',
                    unsafe_allow_html=True)
        avg_room = (filtered_df.groupby('room_type')['price']
                    .mean().sort_values(ascending=False).reset_index())
        fig2 = px.bar(
            avg_room, x='room_type', y='price',
            color='price', color_continuous_scale='Inferno',
            labels={'room_type': 'Room Type', 'price': 'Avg Price ($)'},
            text='price',
        )
        fig2.update_traces(
            texttemplate='$%{text:,.0f}', textposition='outside',
            textfont=dict(size=11),
        )
        fig2.update_coloraxes(showscale=False)
        fig2 = style_chart(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    c, d = st.columns(2)

    with c:
        st.markdown('<p class="section-header">Price Distribution</p>',
                    unsafe_allow_html=True)
        fig3 = px.histogram(
            filtered_df, x='price', nbins=60,
            labels={'price': 'Price ($)', 'count': 'Frequency'},
            color_discrete_sequence=['#FF385C'],
        )
        mean_price = filtered_df['price'].mean()
        fig3.add_vline(
            x=mean_price, line_dash="dash", line_color="#2D2D2D",
            annotation_text=f"Mean ${mean_price:,.0f}",
            annotation_font=dict(size=11, color="#2D2D2D"),
        )
        fig3 = style_chart(fig3)
        st.plotly_chart(fig3, use_container_width=True)

    with d:
        st.markdown('<p class="section-header">Price vs Availability</p>',
                    unsafe_allow_html=True)
        fig4 = px.scatter(
            filtered_df, x='availability_365', y='price',
            color='neighbourhood_group', opacity=0.45,
            labels={'availability_365': 'Availability (days/yr)',
                    'price': 'Price ($)'},
            color_discrete_sequence=PALETTE,
        )
        fig4 = style_chart(fig4, show_legend=True)
        st.plotly_chart(fig4, use_container_width=True)

# ── Tab 2: Geographic Insights ───────────────────────────────────────
with tab2:
    st.markdown('<p class="section-header">Listing Locations Across NYC</p>',
                unsafe_allow_html=True)
    map_df = filtered_df[
        ['latitude', 'longitude', 'price',
         'neighbourhood_group', 'room_type']
    ].dropna()

    fig_map = px.scatter_map(
        map_df, lat='latitude', lon='longitude',
        color='neighbourhood_group', size='price',
        hover_data={'price': True, 'room_type': True,
                    'latitude': False, 'longitude': False},
        zoom=9.5, height=480,
        color_discrete_sequence=PALETTE,
        size_max=12,
    )
    fig_map.update_layout(
        map_style="carto-positron",
        margin=dict(r=0, t=0, l=0, b=0),
        font=dict(family="Inter, sans-serif", size=12),
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.02,
            xanchor="center", x=0.5, font=dict(size=11),
        ),
    )
    st.plotly_chart(fig_map, use_container_width=True)

    e, f = st.columns(2)

    with e:
        st.markdown('<p class="section-header">Top 10 Most Expensive</p>',
                    unsafe_allow_html=True)
        top_nb = (filtered_df.groupby('neighbourhood')['price']
                  .mean().sort_values(ascending=False).head(10).reset_index())
        fig5 = px.bar(
            top_nb, y='neighbourhood', x='price', orientation='h',
            color='price', color_continuous_scale='Sunset',
            labels={'neighbourhood': '', 'price': 'Avg Price ($)'},
            text='price',
        )
        fig5.update_traces(
            texttemplate='$%{text:,.0f}', textposition='outside',
            textfont=dict(size=10),
        )
        fig5.update_coloraxes(showscale=False)
        fig5.update_yaxes(autorange="reversed")
        fig5 = style_chart(fig5, height=450)
        st.plotly_chart(fig5, use_container_width=True)

    with f:
        st.markdown('<p class="section-header">Top 10 Most Affordable</p>',
                    unsafe_allow_html=True)
        bot_nb = (filtered_df.groupby('neighbourhood')['price']
                  .mean().sort_values().head(10).reset_index())
        fig6 = px.bar(
            bot_nb, y='neighbourhood', x='price', orientation='h',
            color='price', color_continuous_scale='Tealgrn',
            labels={'neighbourhood': '', 'price': 'Avg Price ($)'},
            text='price',
        )
        fig6.update_traces(
            texttemplate='$%{text:,.0f}', textposition='outside',
            textfont=dict(size=10),
        )
        fig6.update_coloraxes(showscale=False)
        fig6.update_yaxes(autorange="reversed")
        fig6 = style_chart(fig6, height=450)
        st.plotly_chart(fig6, use_container_width=True)

# ── Tab 3: Correlations ──────────────────────────────────────────────
with tab3:
    g, h = st.columns([3, 2])

    with g:
        st.markdown('<p class="section-header">Feature Correlation Matrix</p>',
                    unsafe_allow_html=True)
        numeric_cols = filtered_df.select_dtypes(
            include=['float64', 'int64']
        ).columns
        corr = filtered_df[numeric_cols].corr()

        fig7 = px.imshow(
            corr, text_auto='.2f', aspect='auto',
            color_continuous_scale='RdBu_r', zmin=-1, zmax=1,
            labels=dict(color='Correlation'),
        )
        fig7.update_layout(
            font=dict(family="Inter, sans-serif", size=11),
            paper_bgcolor="white",
            plot_bgcolor="white",
            margin=dict(l=40, r=20, t=20, b=20),
            height=480,
            coloraxis_colorbar=dict(
                title="Correlation", thickness=12, len=0.7,
                tickfont=dict(size=10),
            ),
        )
        st.plotly_chart(fig7, use_container_width=True)

    with h:
        st.markdown('<p class="section-header">Statistical Summary</p>',
                    unsafe_allow_html=True)
        summary_cols = ['price', 'number_of_reviews',
                        'availability_365', 'reviews_per_month']
        available_cols = [c for c in summary_cols if c in filtered_df.columns]
        st.dataframe(
            filtered_df[available_cols].describe().round(2),
            use_container_width=True, height=480,
        )

# ── Tab 4: Advanced Analytics ─────────────────────────────────────────
with tab4:
    i, j = st.columns(2)

    with i:
        st.markdown('<p class="section-header">Listings by Borough</p>',
                    unsafe_allow_html=True)
        bc = filtered_df['neighbourhood_group'].value_counts().reset_index()
        bc.columns = ['Borough', 'Count']
        fig8 = px.pie(
            bc, values='Count', names='Borough', hole=0.45,
            color_discrete_sequence=PALETTE,
        )
        fig8.update_traces(
            textposition='inside', textinfo='percent+label',
            textfont=dict(size=11),
        )
        fig8.update_layout(
            font=dict(family="Inter, sans-serif", size=12),
            paper_bgcolor="white",
            margin=dict(l=20, r=20, t=20, b=20),
            height=400,
            showlegend=False,
        )
        st.plotly_chart(fig8, use_container_width=True)

    with j:
        st.markdown('<p class="section-header">Room Type Distribution</p>',
                    unsafe_allow_html=True)
        rc = filtered_df['room_type'].value_counts().reset_index()
        rc.columns = ['Room Type', 'Count']
        fig9 = px.pie(
            rc, values='Count', names='Room Type', hole=0.45,
            color_discrete_sequence=['#FF385C', '#00BFA6', '#FFD23F'],
        )
        fig9.update_traces(
            textposition='inside', textinfo='percent+label',
            textfont=dict(size=11),
        )
        fig9.update_layout(
            font=dict(family="Inter, sans-serif", size=12),
            paper_bgcolor="white",
            margin=dict(l=20, r=20, t=20, b=20),
            height=400,
            showlegend=False,
        )
        st.plotly_chart(fig9, use_container_width=True)

    st.markdown('<p class="section-header">'
                'Price Distribution by Borough and Room Type</p>',
                unsafe_allow_html=True)
    fig10 = px.box(
        filtered_df, x='neighbourhood_group', y='price', color='room_type',
        labels={'neighbourhood_group': 'Borough', 'price': 'Price ($)',
                'room_type': 'Room Type'},
        color_discrete_sequence=PALETTE,
    )
    fig10 = style_chart(fig10, height=450, show_legend=True)
    st.plotly_chart(fig10, use_container_width=True)

    st.markdown('<p class="section-header">Reviews vs Price</p>',
                unsafe_allow_html=True)
    fig11 = px.scatter(
        filtered_df, x='number_of_reviews', y='price',
        color='neighbourhood_group', size='availability_365',
        hover_data=['room_type'],
        labels={'number_of_reviews': 'Number of Reviews',
                'price': 'Price ($)'},
        color_discrete_sequence=PALETTE,
        opacity=0.6,
    )
    fig11 = style_chart(fig11, height=450, show_legend=True)
    st.plotly_chart(fig11, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-footer">
    <p>Data Source: Airbnb NYC 2019 Dataset &nbsp;|&nbsp; Built with Streamlit & Plotly</p>
    <p>Pragya &nbsp;|&nbsp; <a href="https://github.com/pragya0405" style="color:#717171;">github.com/pragya0405</a></p>
</div>
""", unsafe_allow_html=True)
