import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# הגדרות עמוד
st.set_page_config(
    page_title="🚀 Crypto Signals Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS מתקדם מאוד - Dark Mode עם Neon/Glow Effects
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Reset and global */
    * {
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* FORCE dark background */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: #0a0e27 !important;
    }
    
    .main .block-container {
        background: linear-gradient(135deg, #0a0e27 0%, #16213e 100%) !important;
        padding: 2rem 3rem !important;
    }
    
    /* Header - FORCE gradient text */
    h1 {
        font-size: 2.8rem !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, #00d4ff 0%, #0099ff 50%, #7b2ff7 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin-bottom: 1rem !important;
        filter: drop-shadow(0 0 20px rgba(0, 212, 255, 0.5)) !important;
    }
    
    /* Subheaders */
    h2, h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        text-shadow: 0 0 15px rgba(0, 212, 255, 0.3) !important;
    }
    
    /* METRIC CARDS - Complete override */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1a1f3a 0%, #2d3561 100%) !important;
        padding: 2rem 1.5rem !important;
        border-radius: 20px !important;
        border: 2px solid rgba(0, 212, 255, 0.3) !important;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.6),
            inset 0 1px 0 rgba(255, 255, 255, 0.1),
            0 0 40px rgba(0, 212, 255, 0.15) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-8px) scale(1.02) !important;
        border-color: rgba(0, 212, 255, 0.8) !important;
        box-shadow: 
            0 12px 48px rgba(0, 0, 0, 0.8),
            0 0 60px rgba(0, 212, 255, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.75rem !important;
        color: #00d4ff !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.8) !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        color: #00d4ff !important;
        text-shadow: 
            0 0 30px rgba(0, 212, 255, 0.8),
            0 0 60px rgba(0, 212, 255, 0.4) !important;
        margin: 0.5rem 0 !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        color: #10b981 !important;
        text-shadow: 0 0 10px rgba(16, 185, 129, 0.5) !important;
    }
    
    /* Sidebar - Dark theme */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0e27 0%, #16213e 100%) !important;
        border-right: 2px solid rgba(0, 212, 255, 0.2) !important;
    }
    
    [data-testid="stSidebar"] > div {
        background: transparent !important;
    }
    
    [data-testid="stSidebar"] h2 {
        color: #00d4ff !important;
        font-weight: 800 !important;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.6) !important;
        font-size: 1.5rem !important;
    }
    
    /* Sidebar elements */
    [data-testid="stSidebar"] label {
        color: #00d4ff !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #00d4ff 0%, #0099ff 100%) !important;
        color: #0a0e27 !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 0.8rem 2.5rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        box-shadow: 
            0 6px 20px rgba(0, 212, 255, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #0099ff 0%, #00d4ff 100%) !important;
        transform: translateY(-3px) !important;
        box-shadow: 
            0 8px 30px rgba(0, 212, 255, 0.7),
            inset 0 1px 0 rgba(255, 255, 255, 0.4) !important;
    }
    
    /* Select boxes */
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background-color: #1a1f3a !important;
        border: 2px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }
    
    /* Multi-select */
    [data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
        background-color: #1a1f3a !important;
        border: 2px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 12px !important;
    }
    
    /* Date input */
    [data-testid="stDateInput"] input {
        background-color: #1a1f3a !important;
        border: 2px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }
    
    /* Dataframes */
    [data-testid="stDataFrame"] {
        background: #1a1f3a !important;
        border-radius: 15px !important;
        border: 2px solid rgba(0, 212, 255, 0.2) !important;
        overflow: hidden !important;
    }
    
    /* Dataframe headers */
    .stDataFrame thead tr th {
        background: linear-gradient(135deg, #00d4ff 0%, #0099ff 100%) !important;
        color: #0a0e27 !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        padding: 1rem !important;
    }
    
    /* Dataframe cells */
    .stDataFrame tbody tr {
        background: #1a1f3a !important;
        border-bottom: 1px solid rgba(0, 212, 255, 0.1) !important;
    }
    
    .stDataFrame tbody tr:hover {
        background: #2d3561 !important;
    }
    
    .stDataFrame tbody tr td {
        color: #ffffff !important;
        padding: 0.8rem !important;
    }
    
    /* Plotly charts */
    .js-plotly-plot {
        background: linear-gradient(135deg, #1a1f3a 0%, #2d3561 100%) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        border: 2px solid rgba(0, 212, 255, 0.2) !important;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.6),
            0 0 40px rgba(0, 212, 255, 0.1) !important;
    }
    
    /* Divider */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(0, 212, 255, 0.6) 20%, 
            rgba(0, 212, 255, 0.8) 50%,
            rgba(0, 212, 255, 0.6) 80%,
            transparent) !important;
        margin: 3rem 0 !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.4) !important;
    }
    
    /* Info/Success boxes */
    .stInfo, .stSuccess {
        background: linear-gradient(135deg, #1a1f3a 0%, #2d3561 100%) !important;
        border-left: 4px solid #00d4ff !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* Text colors */
    p, span, label {
        color: #e2e8f0 !important;
    }
    
    /* Last update */
    .main p:first-of-type {
        color: #00d4ff !important;
        font-weight: 600 !important;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.5) !important;
    }
    
    /* Animations */
    @keyframes glow {
        0%, 100% { 
            box-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
        }
        50% { 
            box-shadow: 0 0 40px rgba(0, 212, 255, 0.8);
        }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0e27;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00d4ff 0%, #0099ff 100%);
        border-radius: 10px;
        border: 2px solid #0a0e27;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #0099ff 0%, #00d4ff 100%);
    }
</style>
""", unsafe_allow_html=True)

# טעינת הדאטה
@st.cache_data(ttl=300)
def load_data():
    try:
        sheet_url = st.secrets.get("GOOGLE_SHEET_URL", None)
        
        if sheet_url:
            if "/edit" in sheet_url:
                sheet_url = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")
                sheet_url = sheet_url.replace("/edit?usp=sharing", "/export?format=csv")
            
            df = pd.read_csv(sheet_url)
            st.sidebar.success("✅ Connected to Google Sheets")
        else:
            df = pd.read_csv('Signals_Log_-_Sheet1.csv')
            st.sidebar.info("📁 Reading from local file")
    
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()
    
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Check_Date'] = pd.to_datetime(df['Check_Date'], errors='coerce')
    df['P&L_%'] = pd.to_numeric(df['P&L_%'], errors='coerce')
    df['Actual_RR'] = pd.to_numeric(df['Actual_RR'], errors='coerce')
    df['Confidence'] = pd.to_numeric(df['Confidence'], errors='coerce')
    
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Cannot load data")
    st.stop()

# Header
st.markdown('# 🚀 Crypto Trading Signals Dashboard')

# Last update
last_update = df['Timestamp'].max()
st.markdown(f"**🕐 Last Update:** {last_update.strftime('%d/%m/%Y %H:%M')}")

# Sidebar
st.sidebar.markdown("## ⚙️ Filters")

date_range = st.sidebar.date_input(
    "📅 Date Range",
    value=(df['Timestamp'].min().date(), df['Timestamp'].max().date()),
    min_value=df['Timestamp'].min().date(),
    max_value=df['Timestamp'].max().date()
)

side_filter = st.sidebar.multiselect(
    "📊 Direction",
    options=['ALL'] + list(df['Side'].unique()),
    default=['ALL']
)

result_filter = st.sidebar.multiselect(
    "✅ Result",
    options=['ALL'] + list(df['Result'].dropna().unique()),
    default=['ALL']
)

# Apply filters
df_filtered = df.copy()

if len(date_range) == 2:
    df_filtered = df_filtered[
        (df_filtered['Timestamp'].dt.date >= date_range[0]) & 
        (df_filtered['Timestamp'].dt.date <= date_range[1])
    ]

if 'ALL' not in side_filter and side_filter:
    df_filtered = df_filtered[df_filtered['Side'].isin(side_filter)]

if 'ALL' not in result_filter and result_filter:
    df_filtered = df_filtered[df_filtered['Result'].isin(result_filter)]

# Metrics
completed_signals = df_filtered[df_filtered['Result'].isin(['TP1_HIT', 'TP2_HIT', 'SL_HIT'])]
total_signals = len(df_filtered)
completed_count = len(completed_signals)
pending_count = len(df_filtered[df_filtered['Result'] == 'PENDING'])
expired_count = len(df_filtered[df_filtered['Result'] == 'EXPIRED'])

wins = len(completed_signals[completed_signals['Result'].isin(['TP1_HIT', 'TP2_HIT'])])
losses = len(completed_signals[completed_signals['Result'] == 'SL_HIT'])
win_rate = (wins / completed_count * 100) if completed_count > 0 else 0

avg_pnl = completed_signals['P&L_%'].mean() if not completed_signals.empty else 0
total_pnl = completed_signals['P&L_%'].sum() if not completed_signals.empty else 0

# KPIs
st.markdown("## 📊 Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("🎯 WIN RATE", f"{win_rate:.1f}%", f"{wins}W / {losses}L")

with col2:
    st.metric("💰 AVG P&L", f"{avg_pnl:.2f}%", f"Total: {total_pnl:.2f}%")

with col3:
    st.metric("📈 TOTAL SIGNALS", total_signals, f"Completed: {completed_count}")

with col4:
    st.metric("⏳ PENDING", pending_count, f"{(pending_count/total_signals*100):.1f}%" if total_signals > 0 else "0%")

with col5:
    st.metric("⌛ EXPIRED", expired_count, f"{(expired_count/total_signals*100):.1f}%" if total_signals > 0 else "0%")

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.markdown("## 📊 Results Distribution")
    result_counts = df_filtered['Result'].value_counts()
    
    fig_results = go.Figure(data=[go.Pie(
        labels=result_counts.index,
        values=result_counts.values,
        hole=0.65,
        marker=dict(
            colors=['#00d4ff', '#10b981', '#ef4444', '#f59e0b', '#8b5cf6'],
            line=dict(color='#0a0e27', width=3)
        ),
        textfont=dict(size=16, color='white', family='Poppins'),
        textposition='outside'
    )])
    
    fig_results.update_layout(
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Poppins', size=14),
        margin=dict(t=10, b=10, l=10, r=10),
        legend=dict(
            bgcolor='rgba(26, 31, 58, 0.9)',
            bordercolor='rgba(0, 212, 255, 0.3)',
            borderwidth=2,
            font=dict(size=12)
        ),
        height=400
    )
    
    st.plotly_chart(fig_results, use_container_width=True)

with col2:
    st.markdown("## 📈 LONG vs SHORT")
    side_stats = df_filtered.groupby('Side').agg({
        'Result': 'count',
        'P&L_%': 'mean'
    }).reset_index()
    side_stats.columns = ['Side', 'Count', 'Avg_PnL']
    
    fig_side = go.Figure()
    
    fig_side.add_trace(go.Bar(
        name='Count',
        x=side_stats['Side'],
        y=side_stats['Count'],
        marker=dict(
            color=['#00d4ff', '#7b2ff7'],
            line=dict(color='#ffffff', width=2)
        ),
        text=side_stats['Count'],
        textposition='outside',
        textfont=dict(size=16, color='#00d4ff'),
        yaxis='y'
    ))
    
    fig_side.add_trace(go.Scatter(
        name='Avg P&L',
        x=side_stats['Side'],
        y=side_stats['Avg_PnL'],
        mode='lines+markers',
        marker=dict(size=18, color='#10b981', line=dict(color='#ffffff', width=3)),
        line=dict(width=4, color='#10b981'),
        yaxis='y2'
    ))
    
    fig_side.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Poppins', size=14),
        yaxis=dict(
            title='Count',
            gridcolor='rgba(0, 212, 255, 0.15)',
            title_font=dict(color='#00d4ff')
        ),
        yaxis2=dict(
            title='Avg P&L %',
            overlaying='y',
            side='right',
            gridcolor='rgba(16, 185, 129, 0.15)',
            title_font=dict(color='#10b981')
        ),
        hovermode='x unified',
        margin=dict(t=10, b=10, l=10, r=10),
        height=400,
        legend=dict(
            bgcolor='rgba(26, 31, 58, 0.9)',
            bordercolor='rgba(0, 212, 255, 0.3)',
            borderwidth=2
        )
    )
    
    st.plotly_chart(fig_side, use_container_width=True)

st.markdown("---")

# Performance timeline
st.markdown("## 📅 Cumulative Performance")
if not completed_signals.empty:
    daily_pnl = completed_signals.groupby(completed_signals['Check_Date'].dt.date)['P&L_%'].sum().reset_index()
    daily_pnl.columns = ['Date', 'PnL']
    daily_pnl['Cumulative'] = daily_pnl['PnL'].cumsum()
    
    fig_timeline = go.Figure()
    
    colors = ['#10b981' if x >= 0 else '#ef4444' for x in daily_pnl['Cumulative']]
    
    fig_timeline.add_trace(go.Scatter(
        x=daily_pnl['Date'],
        y=daily_pnl['Cumulative'],
        mode='lines',
        fill='tozeroy',
        line=dict(color='#00d4ff', width=4),
        fillcolor='rgba(0, 212, 255, 0.2)'
    ))
    
    fig_timeline.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Poppins'),
        xaxis=dict(
            gridcolor='rgba(0, 212, 255, 0.15)',
            title_font=dict(color='#00d4ff')
        ),
        yaxis=dict(
            gridcolor='rgba(0, 212, 255, 0.15)',
            zeroline=True,
            zerolinecolor='#ef4444',
            zerolinewidth=2,
            title_font=dict(color='#00d4ff')
        ),
        margin=dict(t=10, b=10, l=10, r=10),
        height=400
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)
else:
    st.info("⏳ No completed signals yet")

st.markdown("---")

# Top performers
col1, col2 = st.columns(2)

with col1:
    st.markdown("## 🏆 Top 10 Winners")
    if not completed_signals.empty:
        top_winners = completed_signals.nlargest(10, 'P&L_%')[['Timestamp', 'Symbol', 'Side', 'P&L_%']]
        top_winners['Timestamp'] = top_winners['Timestamp'].dt.strftime('%d/%m %H:%M')
        st.dataframe(top_winners, use_container_width=True, hide_index=True)

with col2:
    st.markdown("## ⚠️ Top 10 Losers")
    if not completed_signals.empty:
        top_losers = completed_signals.nsmallest(10, 'P&L_%')[['Timestamp', 'Symbol', 'Side', 'P&L_%']]
        top_losers['Timestamp'] = top_losers['Timestamp'].dt.strftime('%d/%m %H:%M')
        st.dataframe(top_losers, use_container_width=True, hide_index=True)

st.markdown("---")

# Symbol performance
st.markdown("## 💎 Top Symbols")
if not completed_signals.empty:
    symbol_stats = completed_signals.groupby('Symbol').agg({
        'P&L_%': ['sum', 'count'],
        'Result': lambda x: (x.isin(['TP1_HIT', 'TP2_HIT'])).sum()
    }).reset_index()
    
    symbol_stats.columns = ['Symbol', 'Total_PnL', 'Count', 'Wins']
    symbol_stats['Win_Rate'] = (symbol_stats['Wins'] / symbol_stats['Count'] * 100).round(1)
    symbol_stats = symbol_stats.sort_values('Total_PnL', ascending=False).head(12)
    
    colors = ['#10b981' if x > 0 else '#ef4444' for x in symbol_stats['Total_PnL']]
    
    fig_symbols = go.Figure()
    
    fig_symbols.add_trace(go.Bar(
        x=symbol_stats['Symbol'],
        y=symbol_stats['Total_PnL'],
        marker=dict(
            color=colors,
            line=dict(color='#ffffff', width=2)
        ),
        text=[f"{wr}%" for wr in symbol_stats['Win_Rate']],
        textposition='outside',
        textfont=dict(size=14, color='#00d4ff')
    ))
    
    fig_symbols.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Poppins'),
        xaxis=dict(gridcolor='rgba(0, 212, 255, 0.15)'),
        yaxis=dict(
            gridcolor='rgba(0, 212, 255, 0.15)',
            zeroline=True,
            zerolinecolor='#ef4444',
            zerolinewidth=2
        ),
        margin=dict(t=30, b=10, l=10, r=10),
        height=400
    )
    
    st.plotly_chart(fig_symbols, use_container_width=True)

st.markdown("---")

# Recent signals
st.markdown("## 🔄 Recent Signals")
recent = df_filtered.sort_values('Timestamp', ascending=False).head(15)
recent_display = recent[['Timestamp', 'Symbol', 'Side', 'Entry', 'TP1', 'Confidence', 'Result', 'P&L_%']].copy()
recent_display['Timestamp'] = recent_display['Timestamp'].dt.strftime('%d/%m %H:%M')
st.dataframe(recent_display, use_container_width=True, hide_index=True)

# Sidebar stats
st.sidebar.markdown("---")
st.sidebar.markdown("## 📊 Quick Stats")

if not completed_signals.empty:
    best_symbol = completed_signals.groupby('Symbol')['P&L_%'].sum().idxmax()
    best_pnl = completed_signals.groupby('Symbol')['P&L_%'].sum().max()
    st.sidebar.metric("🏆 Best", best_symbol, f"{best_pnl:.2f}%")

if st.sidebar.button("🔄 Refresh"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("🔄 Auto-refresh: 5 min")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem;'>
    <p style='color: #00d4ff; font-weight: 700; font-size: 1.1rem; margin: 0;'>
        Made with ❤️ by FlowBot Automation
    </p>
    <p style='color: #94a3b8; margin: 0.5rem 0 0 0;'>
        Real-time Crypto Trading Analytics
    </p>
</div>
""", unsafe_allow_html=True)
