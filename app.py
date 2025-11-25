import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# הגדרות עמוד
st.set_page_config(
    page_title="Crypto Signals Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS מתקדם - בהשראת הדוגמאות
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main background */
    .stApp {
        background: #0A0E1A !important;
    }
    
    .main .block-container {
        padding: 2rem 3rem !important;
        max-width: 1800px !important;
    }
    
    /* Sidebar - Icon only */
    [data-testid="stSidebar"] {
        background: #0F1419 !important;
        width: 80px !important;
        min-width: 80px !important;
        max-width: 80px !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        padding: 2rem 0 !important;
    }
    
    [data-testid="stSidebar"] > div {
        width: 80px !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1.5rem;
    }
    
    /* Header section */
    .dashboard-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    h1 {
        font-size: 1.875rem !important;
        font-weight: 600 !important;
        color: #FFFFFF !important;
        margin: 0 !important;
        letter-spacing: -0.02em !important;
    }
    
    .last-update {
        font-size: 0.875rem !important;
        color: #6B7280 !important;
        font-weight: 400 !important;
    }
    
    h2 {
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        color: #6B7280 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        margin: 2rem 0 1rem 0 !important;
    }
    
    /* Stats cards - BIG */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #151B2B 0%, #0F1419 100%) !important;
        padding: 2rem 1.75rem !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    [data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #3B82F6, #06B6D4);
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    [data-testid="stMetric"]:hover {
        border-color: rgba(59, 130, 246, 0.3) !important;
        transform: translateY(-4px) !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4) !important;
    }
    
    [data-testid="stMetric"]:hover::before {
        opacity: 1;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.6875rem !important;
        font-weight: 700 !important;
        color: #6B7280 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        margin-bottom: 0.875rem !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        line-height: 1.1 !important;
        margin: 0.75rem 0 !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        margin-top: 0.625rem !important;
    }
    
    /* Charts container */
    .chart-container {
        background: linear-gradient(135deg, #151B2B 0%, #0F1419 100%) !important;
        border-radius: 16px !important;
        padding: 1.75rem !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
        margin-bottom: 1.5rem;
    }
    
    .js-plotly-plot {
        background: transparent !important;
        border-radius: 12px !important;
    }
    
    /* Dataframes */
    .stDataFrame {
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        background: #151B2B !important;
    }
    
    .stDataFrame thead tr th {
        background: #0F1419 !important;
        color: #6B7280 !important;
        font-weight: 700 !important;
        font-size: 0.6875rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        padding: 1rem !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
    }
    
    .stDataFrame tbody tr {
        background: #151B2B !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.03) !important;
        transition: background 0.2s;
    }
    
    .stDataFrame tbody tr:hover {
        background: #1A2032 !important;
    }
    
    .stDataFrame tbody tr td {
        color: #E5E7EB !important;
        padding: 0.875rem 1rem !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: #151B2B !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
        font-size: 0.875rem !important;
    }
    
    /* Info boxes */
    .stInfo {
        background: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 10px !important;
        color: #E5E7EB !important;
    }
    
    /* Divider */
    hr {
        border: none !important;
        height: 1px !important;
        background: rgba(255, 255, 255, 0.05) !important;
        margin: 3rem 0 !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0A0E1A;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #1F2937;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #374151;
    }
    
    /* Grid layout for cards */
    .metric-row {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 1.25rem;
        margin-bottom: 2rem;
    }
    
    /* Chart titles */
    .chart-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 1rem;
        letter-spacing: -0.01em;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data(ttl=300)
def load_data():
    try:
        sheet_url = st.secrets.get("GOOGLE_SHEET_URL", None)
        if sheet_url:
            if "/edit" in sheet_url:
                sheet_url = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")
                sheet_url = sheet_url.replace("/edit?usp=sharing", "/export?format=csv")
            df = pd.read_csv(sheet_url)
        else:
            df = pd.read_csv('Signals_Log_-_Sheet1.csv')
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.stop()
    
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Check_Date'] = pd.to_datetime(df['Check_Date'], errors='coerce')
    df['P&L_%'] = pd.to_numeric(df['P&L_%'], errors='coerce')
    df['Actual_RR'] = pd.to_numeric(df['Actual_RR'], errors='coerce')
    df['Confidence'] = pd.to_numeric(df['Confidence'], errors='coerce')
    return df

df = load_data()

# Sidebar minimal
st.sidebar.markdown("🏠")
st.sidebar.markdown("📊")
st.sidebar.markdown("💰")
st.sidebar.markdown("⚙️")

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("# Dashboard")
with col2:
    last_update = df['Timestamp'].max()
    st.markdown(f"<p class='last-update'>Updated {last_update.strftime('%H:%M')}</p>", unsafe_allow_html=True)

# Filters (compact)
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    date_range = st.date_input(
        "Date Range",
        value=(df['Timestamp'].min().date(), df['Timestamp'].max().date()),
        label_visibility="collapsed"
    )
with col2:
    side_filter = st.multiselect("Direction", ['ALL'] + list(df['Side'].unique()), default=['ALL'], label_visibility="collapsed")
with col3:
    result_filter = st.multiselect("Status", ['ALL'] + list(df['Result'].dropna().unique()), default=['ALL'], label_visibility="collapsed")

# Apply filters
df_filtered = df.copy()
if len(date_range) == 2:
    df_filtered = df_filtered[(df_filtered['Timestamp'].dt.date >= date_range[0]) & (df_filtered['Timestamp'].dt.date <= date_range[1])]
if 'ALL' not in side_filter and side_filter:
    df_filtered = df_filtered[df_filtered['Side'].isin(side_filter)]
if 'ALL' not in result_filter and result_filter:
    df_filtered = df_filtered[df_filtered['Result'].isin(result_filter)]

# Calculate metrics
completed = df_filtered[df_filtered['Result'].isin(['TP1_HIT', 'TP2_HIT', 'SL_HIT'])]
total = len(df_filtered)
completed_count = len(completed)
pending = len(df_filtered[df_filtered['Result'] == 'PENDING'])
expired = len(df_filtered[df_filtered['Result'] == 'EXPIRED'])
wins = len(completed[completed['Result'].isin(['TP1_HIT', 'TP2_HIT'])])
losses = len(completed[completed['Result'] == 'SL_HIT'])
win_rate = (wins / completed_count * 100) if completed_count > 0 else 0
avg_pnl = completed['P&L_%'].mean() if not completed.empty else 0
total_pnl = completed['P&L_%'].sum() if not completed.empty else 0

st.markdown("<br>", unsafe_allow_html=True)

# Metrics row
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Win Rate", f"{win_rate:.1f}%", f"{wins}W / {losses}L")
with col2:
    st.metric("Avg P&L", f"{avg_pnl:.2f}%", f"{total_pnl:+.1f}% total")
with col3:
    st.metric("Total Signals", f"{total:,}", f"{completed_count} done")
with col4:
    st.metric("Pending", f"{pending:,}", f"{(pending/total*100):.1f}%" if total > 0 else "0%")
with col5:
    st.metric("Expired", f"{expired:,}", f"{(expired/total*100):.1f}%" if total > 0 else "0%")

st.markdown("<br>", unsafe_allow_html=True)

# Charts row
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.markdown("<p class='chart-title'>Results Distribution</p>", unsafe_allow_html=True)
    
    result_counts = df_filtered['Result'].value_counts()
    fig_donut = go.Figure(data=[go.Pie(
        labels=result_counts.index,
        values=result_counts.values,
        hole=0.6,
        marker=dict(
            colors=['#3B82F6', '#10B981', '#EF4444', '#F59E0B', '#8B5CF6'],
            line=dict(color='#0A0E1A', width=3)
        ),
        textfont=dict(size=14, color='white', family='Inter', weight=600),
        textposition='outside',
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>%{value} signals<br>%{percent}<extra></extra>'
    )])
    
    fig_donut.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E5E7EB', family='Inter', size=13),
        margin=dict(t=10, b=10, l=10, r=10),
        height=280,
        annotations=[dict(
            text=f'{total}<br><span style="font-size:14px; color:#6B7280;">signals</span>',
            x=0.5, y=0.5,
            font_size=32,
            font_color='#FFFFFF',
            font_weight=700,
            showarrow=False
        )]
    )
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.markdown("<p class='chart-title'>Long vs Short Performance</p>", unsafe_allow_html=True)
    
    side_stats = df_filtered.groupby('Side').agg({'Result': 'count', 'P&L_%': 'mean'}).reset_index()
    side_stats.columns = ['Side', 'Count', 'Avg_PnL']
    
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=side_stats['Side'],
        y=side_stats['Count'],
        name='Signals',
        marker=dict(
            color=['#3B82F6', '#8B5CF6'],
            line=dict(color='#0A0E1A', width=2)
        ),
        text=side_stats['Count'],
        textposition='outside',
        textfont=dict(size=14, color='#E5E7EB', weight=600),
        yaxis='y'
    ))
    
    fig_bar.add_trace(go.Scatter(
        x=side_stats['Side'],
        y=side_stats['Avg_PnL'],
        name='Avg P&L',
        mode='lines+markers',
        marker=dict(size=12, color='#10B981', line=dict(color='#FFFFFF', width=2)),
        line=dict(width=3, color='#10B981'),
        yaxis='y2'
    ))
    
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E5E7EB', family='Inter', size=13),
        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.05)', showgrid=True),
        yaxis2=dict(overlaying='y', side='right', gridcolor='rgba(255, 255, 255, 0.03)'),
        margin=dict(t=10, b=10, l=10, r=10),
        height=280,
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            bgcolor='rgba(0,0,0,0)',
            font=dict(size=12)
        )
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Performance timeline
st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
st.markdown("<p class='chart-title'>Cumulative Performance</p>", unsafe_allow_html=True)

if not completed.empty:
    daily_pnl = completed.groupby(completed['Check_Date'].dt.date)['P&L_%'].sum().reset_index()
    daily_pnl.columns = ['Date', 'PnL']
    daily_pnl['Cumulative'] = daily_pnl['PnL'].cumsum()
    
    fig_area = go.Figure()
    fig_area.add_trace(go.Scatter(
        x=daily_pnl['Date'],
        y=daily_pnl['Cumulative'],
        mode='lines',
        fill='tozeroy',
        line=dict(color='#3B82F6', width=2.5),
        fillcolor='rgba(59, 130, 246, 0.15)',
        name='P&L',
        hovertemplate='<b>%{x}</b><br>Cumulative: %{y:.2f}%<extra></extra>'
    ))
    
    fig_area.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E5E7EB', family='Inter', size=13),
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.05)', showgrid=True),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.05)',
            showgrid=True,
            zeroline=True,
            zerolinecolor='rgba(239, 68, 68, 0.3)',
            zerolinewidth=2
        ),
        margin=dict(t=10, b=10, l=10, r=10),
        height=280,
        hovermode='x unified'
    )
    st.plotly_chart(fig_area, use_container_width=True)
else:
    st.info("No completed signals")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Top performers
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.markdown("<p class='chart-title'>Top Winners</p>", unsafe_allow_html=True)
    if not completed.empty:
        winners = completed.nlargest(10, 'P&L_%')[['Timestamp', 'Symbol', 'Side', 'P&L_%']]
        winners['Time'] = winners['Timestamp'].dt.strftime('%b %d')
        winners['P&L'] = winners['P&L_%'].apply(lambda x: f"+{x:.2f}%")
        st.dataframe(
            winners[['Time', 'Symbol', 'Side', 'P&L']],
            use_container_width=True,
            hide_index=True,
            height=320
        )
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.markdown("<p class='chart-title'>Top Losers</p>", unsafe_allow_html=True)
    if not completed.empty:
        losers = completed.nsmallest(10, 'P&L_%')[['Timestamp', 'Symbol', 'Side', 'P&L_%']]
        losers['Time'] = losers['Timestamp'].dt.strftime('%b %d')
        losers['P&L'] = losers['P&L_%'].apply(lambda x: f"{x:.2f}%")
        st.dataframe(
            losers[['Time', 'Symbol', 'Side', 'P&L']],
            use_container_width=True,
            hide_index=True,
            height=320
        )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Symbol performance
st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
st.markdown("<p class='chart-title'>Top Performing Symbols</p>", unsafe_allow_html=True)

if not completed.empty:
    symbols = completed.groupby('Symbol').agg({
        'P&L_%': ['sum', 'count'],
        'Result': lambda x: (x.isin(['TP1_HIT', 'TP2_HIT'])).sum()
    }).reset_index()
    symbols.columns = ['Symbol', 'Total', 'Count', 'Wins']
    symbols['WR'] = (symbols['Wins'] / symbols['Count'] * 100).round(0)
    symbols = symbols.sort_values('Total', ascending=False).head(12)
    
    colors = ['#10B981' if x > 0 else '#EF4444' for x in symbols['Total']]
    
    fig_symbols = go.Figure()
    fig_symbols.add_trace(go.Bar(
        x=symbols['Symbol'],
        y=symbols['Total'],
        marker=dict(color=colors, line=dict(color='#0A0E1A', width=2)),
        text=symbols['WR'].apply(lambda x: f"{x:.0f}%"),
        textposition='outside',
        textfont=dict(size=12, color='#6B7280', weight=600),
        hovertemplate='<b>%{x}</b><br>P&L: %{y:.2f}%<br>Win Rate: %{text}<extra></extra>'
    ))
    
    fig_symbols.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E5E7EB', family='Inter', size=13),
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.05)'),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.05)',
            zeroline=True,
            zerolinecolor='rgba(255, 255, 255, 0.1)',
            zerolinewidth=1
        ),
        margin=dict(t=30, b=10, l=10, r=10),
        height=300,
        showlegend=False
    )
    st.plotly_chart(fig_symbols, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Recent signals
st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
st.markdown("<p class='chart-title'>Recent Signals</p>", unsafe_allow_html=True)

recent = df_filtered.sort_values('Timestamp', ascending=False).head(12)
recent_display = recent[['Timestamp', 'Symbol', 'Side', 'Entry', 'Confidence', 'Result', 'P&L_%']].copy()
recent_display['Time'] = recent_display['Timestamp'].dt.strftime('%b %d, %H:%M')
recent_display['Conf'] = recent_display['Confidence'].apply(lambda x: f"{x:.0f}%" if pd.notna(x) else "—")
recent_display['P&L'] = recent_display['P&L_%'].apply(lambda x: f"{x:+.2f}%" if pd.notna(x) else "—")

st.dataframe(
    recent_display[['Time', 'Symbol', 'Side', 'Entry', 'Conf', 'Result', 'P&L']],
    use_container_width=True,
    hide_index=True,
    height=360
)

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; color: #4B5563; font-size: 0.8125rem;'>FlowBot Automation © 2025</p>",
    unsafe_allow_html=True
)
