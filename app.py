import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Crypto Signals", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

# CSS with 3D Effects & Lighter Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Main background - LIGHTER */
    .stApp {
        background: linear-gradient(135deg, #1a2332 0%, #253447 100%) !important;
    }
    
    .main .block-container {
        padding: 2.5rem 3.5rem !important;
        max-width: 1800px !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(30, 41, 59, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        width: 80px !important;
        min-width: 80px !important;
        border-right: 1px solid rgba(148, 163, 184, 0.2) !important;
        box-shadow: 2px 0 10px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Headers */
    h1 {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        margin: 0 0 0.5rem 0 !important;
        letter-spacing: -0.02em !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
    }
    
    h2 {
        font-size: 0.8125rem !important;
        font-weight: 600 !important;
        color: #CBD5E1 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        margin: 2.5rem 0 1.25rem 0 !important;
    }
    
    /* Metric cards - 3D EFFECT */
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #2d3e52 0%, #1e2a3a 100%) !important;
        padding: 2rem 1.75rem !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 
            0 10px 30px rgba(0, 0, 0, 0.5),
            0 1px 0 rgba(255, 255, 255, 0.1) inset,
            0 -1px 0 rgba(0, 0, 0, 0.3) inset !important;
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
        height: 3px;
        background: linear-gradient(90deg, #3B82F6, #06B6D4, #10B981);
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: 
            0 20px 50px rgba(0, 0, 0, 0.6),
            0 2px 0 rgba(255, 255, 255, 0.15) inset,
            0 0 30px rgba(59, 130, 246, 0.3) !important;
        border-color: rgba(59, 130, 246, 0.5) !important;
    }
    
    [data-testid="stMetric"]:hover::before {
        opacity: 1;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.6875rem !important;
        font-weight: 700 !important;
        color: #94A3B8 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        margin-bottom: 0.875rem !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
        line-height: 1.1 !important;
        text-shadow: 
            0 2px 4px rgba(0, 0, 0, 0.4),
            0 0 20px rgba(59, 130, 246, 0.3) !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        margin-top: 0.625rem !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Chart containers - GLASSMORPHISM + 3D */
    .chart-box {
        background: linear-gradient(145deg, rgba(45, 62, 82, 0.9) 0%, rgba(30, 42, 58, 0.9) 100%) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 
            0 10px 30px rgba(0, 0, 0, 0.5),
            0 1px 0 rgba(255, 255, 255, 0.1) inset !important;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    
    .chart-box::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
        pointer-events: none;
    }
    
    .chart-title {
        font-size: 1rem;
        font-weight: 600;
        color: #F8FAFC;
        margin-bottom: 1.25rem;
        letter-spacing: -0.01em;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .js-plotly-plot {
        background: transparent !important;
    }
    
    /* Dataframes - 3D EFFECT */
    .stDataFrame {
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        background: linear-gradient(145deg, rgba(45, 62, 82, 0.9) 0%, rgba(30, 42, 58, 0.9) 100%) !important;
        box-shadow: 
            0 8px 20px rgba(0, 0, 0, 0.4),
            0 1px 0 rgba(255, 255, 255, 0.1) inset !important;
        overflow: hidden !important;
    }
    
    .stDataFrame thead tr th {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
        color: #CBD5E1 !important;
        font-weight: 700 !important;
        font-size: 0.6875rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        padding: 1rem !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5) !important;
    }
    
    .stDataFrame tbody tr {
        background: rgba(30, 42, 58, 0.5) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        transition: all 0.2s ease !important;
    }
    
    .stDataFrame tbody tr:hover {
        background: rgba(45, 62, 82, 0.8) !important;
        transform: translateX(2px) !important;
    }
    
    .stDataFrame tbody tr td {
        color: #F8FAFC !important;
        padding: 0.875rem 1rem !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
    }
    
    /* Buttons - 3D RAISED */
    .stButton button {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        box-shadow: 
            0 6px 20px rgba(59, 130, 246, 0.4),
            0 1px 0 rgba(255, 255, 255, 0.2) inset !important;
        transition: all 0.2s ease !important;
        position: relative !important;
    }
    
    .stButton button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 
            0 10px 30px rgba(59, 130, 246, 0.5),
            0 1px 0 rgba(255, 255, 255, 0.3) inset !important;
    }
    
    .stButton button:active {
        transform: translateY(-1px) !important;
        box-shadow: 
            0 4px 15px rgba(59, 130, 246, 0.4),
            0 1px 0 rgba(255, 255, 255, 0.2) inset !important;
    }
    
    /* Select boxes - ELEVATED */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: linear-gradient(145deg, rgba(45, 62, 82, 0.9) 0%, rgba(30, 42, 58, 0.9) 100%) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        color: #F8FAFC !important;
        box-shadow: 
            0 4px 15px rgba(0, 0, 0, 0.3),
            0 1px 0 rgba(255, 255, 255, 0.1) inset !important;
    }
    
    /* Info boxes - GLASS EFFECT */
    .stInfo {
        background: rgba(59, 130, 246, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 12px !important;
        color: #F8FAFC !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Divider - GLOWING */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(
            90deg, 
            transparent, 
            rgba(59, 130, 246, 0.5) 20%,
            rgba(59, 130, 246, 0.8) 50%,
            rgba(59, 130, 246, 0.5) 80%,
            transparent
        ) !important;
        margin: 3rem 0 !important;
        box-shadow: 0 0 10px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Scrollbar - MODERN */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #3B82F6, #2563EB);
        border-radius: 10px;
        border: 2px solid rgba(30, 41, 59, 0.5);
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #2563EB, #1D4ED8);
    }
    
    /* Floating animation for metrics */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    /* Gradient text for numbers */
    [data-testid="stMetricValue"] {
        background: linear-gradient(135deg, #FFFFFF 0%, #E0E7FF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
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
    st.markdown(f"<p style='color: #CBD5E1; font-size: 0.875rem; text-align: right;'>Updated {last.strftime('%H:%M')}</p>", unsafe_allow_html=True)

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
            line=dict(color='#1a2332', width=3)
        ),
        textfont=dict(size=14, color='white', family='Inter', weight=600),
        textposition='outside',
        textinfo='label+percent'
    )])
    
    fig.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC', family='Inter'),
        margin=dict(t=10, b=10, l=10, r=10),
        height=280,
        annotations=[dict(
            text=f'{total}<br><span style="font-size:14px; color:#CBD5E1;">signals</span>',
            x=0.5, y=0.5,
            font_size=32,
            font_color='#F8FAFC',
            font_family='Inter',
            font_weight=700,
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
        marker=dict(color=['#3B82F6', '#06B6D4'], line=dict(color='#1a2332', width=2)),
        text=side_stats['Count'],
        textposition='outside',
        textfont=dict(size=14, color='#F8FAFC', weight=600),
        yaxis='y'
    ))
    
    fig2.add_trace(go.Scatter(
        x=side_stats['Side'],
        y=side_stats['Avg_PnL'],
        mode='lines+markers',
        marker=dict(size=12, color='#10B981', line=dict(color='#F8FAFC', width=2)),
        line=dict(width=3, color='#10B981'),
        yaxis='y2'
    ))
    
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC', family='Inter'),
        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)', showgrid=True),
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
        line=dict(color='#3B82F6', width=3),
        fillcolor='rgba(59, 130, 246, 0.2)'
    ))
    
    fig3.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC', family='Inter'),
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)', showgrid=True),
        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)', showgrid=True, zeroline=True, zerolinecolor='rgba(239, 68, 68, 0.5)'),
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
        marker=dict(color=colors, line=dict(color='#1a2332', width=2)),
        text=symbols['WR'].apply(lambda x: f"{x:.0f}%"),
        textposition='outside',
        textfont=dict(size=12, color='#CBD5E1', weight=600)
    ))
    
    fig4.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC', family='Inter'),
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)', zeroline=True, zerolinecolor='rgba(255, 255, 255, 0.2)'),
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
st.markdown("<p style='text-align: center; color: #CBD5E1; font-size: 0.8125rem;'>FlowBot Automation © 2025</p>", unsafe_allow_html=True)
