import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Crypto Signals", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

# CSS with Navy Blue theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    .stApp {
        background: #0F1729 !important;
    }
    
    .main .block-container {
        padding: 2.5rem 3.5rem !important;
        max-width: 1800px !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #1A2332 !important;
        width: 80px !important;
        min-width: 80px !important;
        border-right: 1px solid rgba(148, 163, 184, 0.1) !important;
    }
    
    /* Headers */
    h1 {
        font-size: 2rem !important;
        font-weight: 600 !important;
        color: #FFFFFF !important;
        margin: 0 0 0.5rem 0 !important;
        letter-spacing: -0.02em !important;
    }
    
    h2 {
        font-size: 0.8125rem !important;
        font-weight: 600 !important;
        color: #94A3B8 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        margin: 2.5rem 0 1.25rem 0 !important;
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background: #1E2A3A !important;
        padding: 2rem 1.75rem !important;
        border-radius: 16px !important;
        border: 1px solid rgba(148, 163, 184, 0.1) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    
    [data-testid="stMetric"]:hover {
        border-color: rgba(59, 130, 246, 0.4) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4) !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.6875rem !important;
        font-weight: 700 !important;
        color: #94A3B8 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        margin-bottom: 0.875rem !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        line-height: 1.1 !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        margin-top: 0.625rem !important;
    }
    
    /* Chart containers */
    .chart-box {
        background: #1E2A3A !important;
        border-radius: 16px !important;
        padding: 1.75rem !important;
        border: 1px solid rgba(148, 163, 184, 0.1) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
        margin-bottom: 1.5rem;
    }
    
    .chart-title {
        font-size: 0.9375rem;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 1.25rem;
        letter-spacing: -0.01em;
    }
    
    .js-plotly-plot {
        background: transparent !important;
    }
    
    /* Dataframes */
    .stDataFrame {
        border: 1px solid rgba(148, 163, 184, 0.1) !important;
        border-radius: 12px !important;
        background: #1E2A3A !important;
    }
    
    .stDataFrame thead tr th {
        background: #1A2332 !important;
        color: #94A3B8 !important;
        font-weight: 700 !important;
        font-size: 0.6875rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        padding: 1rem !important;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1) !important;
    }
    
    .stDataFrame tbody tr {
        background: #1E2A3A !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.03) !important;
    }
    
    .stDataFrame tbody tr:hover {
        background: #1A2332 !important;
    }
    
    .stDataFrame tbody tr td {
        color: #FFFFFF !important;
        padding: 0.875rem 1rem !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #3B82F6 0%, #06B6D4 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: #1E2A3A !important;
        border: 1px solid rgba(148, 163, 184, 0.1) !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
    }
    
    /* Info */
    .stInfo {
        background: rgba(59, 130, 246, 0.2) !important;
        border: 1px solid rgba(59, 130, 246, 0.4) !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
    }
    
    /* Divider */
    hr {
        border: none !important;
        height: 1px !important;
        background: rgba(148, 163, 184, 0.1) !important;
        margin: 3rem 0 !important;
    }
    
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0F1729;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #1E2A3A;
        border-radius: 4px;
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

# Sidebar
st.sidebar.markdown("🏠")
st.sidebar.markdown("📊")
st.sidebar.markdown("💰")

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("# Dashboard")
with col2:
    last = df['Timestamp'].max()
    st.markdown(f"<p style='color: #94A3B8; font-size: 0.875rem; text-align: right;'>Updated {last.strftime('%H:%M')}</p>", unsafe_allow_html=True)

# Filters
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    date_range = st.date_input("Date Range", value=(df['Timestamp'].min().date(), df['Timestamp'].max().date()), label_visibility="collapsed")
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

# Metrics
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

# KPIs
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

# Charts
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='chart-box'>", unsafe_allow_html=True)
    st.markdown("<p class='chart-title'>Results Distribution</p>", unsafe_allow_html=True)
    
    result_counts = df_filtered['Result'].value_counts()
    fig = go.Figure(data=[go.Pie(
        labels=result_counts.index,
        values=result_counts.values,
        hole=0.6,
        marker=dict(
            colors=['#3B82F6', '#10B981', '#EF4444', '#F59E0B', '#8B5CF6'],
            line=dict(color='#0F1729', width=3)
        ),
        textfont=dict(size=14, color='white', family='Inter'),
        textposition='outside',
        textinfo='label+percent'
    )])
    
    fig.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF', family='Inter'),
        margin=dict(t=10, b=10, l=10, r=10),
        height=280,
        annotations=[dict(
            text=f'{total}<br><span style="font-size:14px; color:#94A3B8;">signals</span>',
            x=0.5, y=0.5,
            font_size=32,
            font_color='#FFFFFF',
            showarrow=False
        )]
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='chart-box'>", unsafe_allow_html=True)
    st.markdown("<p class='chart-title'>Long vs Short Performance</p>", unsafe_allow_html=True)
    
    side_stats = df_filtered.groupby('Side').agg({'Result': 'count', 'P&L_%': 'mean'}).reset_index()
    side_stats.columns = ['Side', 'Count', 'Avg_PnL']
    
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=side_stats['Side'],
        y=side_stats['Count'],
        marker=dict(color=['#3B82F6', '#06B6D4'], line=dict(color='#0F1729', width=2)),
        text=side_stats['Count'],
        textposition='outside',
        textfont=dict(size=14, color='#FFFFFF'),
        yaxis='y'
    ))
    
    fig2.add_trace(go.Scatter(
        x=side_stats['Side'],
        y=side_stats['Avg_PnL'],
        mode='lines+markers',
        marker=dict(size=12, color='#10B981', line=dict(color='#FFFFFF', width=2)),
        line=dict(width=3, color='#10B981'),
        yaxis='y2'
    ))
    
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF', family='Inter'),
        yaxis=dict(gridcolor='rgba(148, 163, 184, 0.1)', showgrid=True),
        yaxis2=dict(overlaying='y', side='right'),
        margin=dict(t=10, b=10, l=10, r=10),
        height=280,
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Timeline
st.markdown("<div class='chart-box'>", unsafe_allow_html=True)
st.markdown("<p class='chart-title'>Cumulative Performance</p>", unsafe_allow_html=True)

if not completed.empty:
    daily = completed.groupby(completed['Check_Date'].dt.date)['P&L_%'].sum().reset_index()
    daily.columns = ['Date', 'PnL']
    daily['Cumulative'] = daily['PnL'].cumsum()
    
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=daily['Date'],
        y=daily['Cumulative'],
        mode='lines',
        fill='tozeroy',
        line=dict(color='#3B82F6', width=2.5),
        fillcolor='rgba(59, 130, 246, 0.25)'
    ))
    
    fig3.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF', family='Inter'),
        xaxis=dict(gridcolor='rgba(148, 163, 184, 0.1)', showgrid=True),
        yaxis=dict(gridcolor='rgba(148, 163, 184, 0.1)', showgrid=True, zeroline=True, zerolinecolor='rgba(239, 68, 68, 0.4)'),
        margin=dict(t=10, b=10, l=10, r=10),
        height=280
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("No data")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Top performers
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='chart-box'>", unsafe_allow_html=True)
    st.markdown("<p class='chart-title'>Top Winners</p>", unsafe_allow_html=True)
    if not completed.empty:
        winners = completed.nlargest(8, 'P&L_%')[['Timestamp', 'Symbol', 'Side', 'P&L_%']]
        winners['Time'] = winners['Timestamp'].dt.strftime('%b %d')
        winners['P&L'] = winners['P&L_%'].apply(lambda x: f"+{x:.2f}%")
        st.dataframe(winners[['Time', 'Symbol', 'Side', 'P&L']], use_container_width=True, hide_index=True, height=280)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='chart-box'>", unsafe_allow_html=True)
    st.markdown("<p class='chart-title'>Top Losers</p>", unsafe_allow_html=True)
    if not completed.empty:
        losers = completed.nsmallest(8, 'P&L_%')[['Timestamp', 'Symbol', 'Side', 'P&L_%']]
        losers['Time'] = losers['Timestamp'].dt.strftime('%b %d')
        losers['P&L'] = losers['P&L_%'].apply(lambda x: f"{x:.2f}%")
        st.dataframe(losers[['Time', 'Symbol', 'Side', 'P&L']], use_container_width=True, hide_index=True, height=280)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Symbols
st.markdown("<div class='chart-box'>", unsafe_allow_html=True)
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
    
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(
        x=symbols['Symbol'],
        y=symbols['Total'],
        marker=dict(color=colors, line=dict(color='#0F1729', width=2)),
        text=symbols['WR'].apply(lambda x: f"{x:.0f}%"),
        textposition='outside',
        textfont=dict(size=12, color='#94A3B8')
    ))
    
    fig4.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FFFFFF', family='Inter'),
        xaxis=dict(gridcolor='rgba(148, 163, 184, 0.1)'),
        yaxis=dict(gridcolor='rgba(148, 163, 184, 0.1)', zeroline=True, zerolinecolor='rgba(148, 163, 184, 0.2)'),
        margin=dict(t=30, b=10, l=10, r=10),
        height=300,
        showlegend=False
    )
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Recent
st.markdown("<div class='chart-box'>", unsafe_allow_html=True)
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

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.8125rem;'>FlowBot Automation © 2025</p>", unsafe_allow_html=True)
