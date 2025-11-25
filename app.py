import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np

st.set_page_config(page_title="Crypto Signals Dashboard", page_icon="📊", layout="wide", initial_sidebar_state="collapsed")

# SAAS-Style Glassmorphism CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&family=Open+Sans:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Roboto', 'Open Sans', sans-serif !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Dark SAAS Background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%) !important;
        background-attachment: fixed !important;
    }
    
    .main .block-container {
        padding: 2rem 2.5rem !important;
        max-width: 1920px !important;
    }
    
    /* Header */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, #06b6d4, #3b82f6, #8b5cf6) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        margin: 0 0 2rem 0 !important;
        letter-spacing: -0.03em !important;
    }
    
    /* Glassmorphic Cards - 3D Effect */
    [data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.4) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 24px !important;
        padding: 2rem 1.5rem !important;
        box-shadow: 
            0 8px 32px 0 rgba(0, 0, 0, 0.37),
            inset 0 1px 0 0 rgba(255, 255, 255, 0.1),
            inset 0 -1px 0 0 rgba(0, 0, 0, 0.3) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    [data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transition: left 0.6s;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: 
            0 20px 60px 0 rgba(0, 0, 0, 0.5),
            0 0 40px rgba(59, 130, 246, 0.3),
            inset 0 2px 0 0 rgba(255, 255, 255, 0.15) !important;
        border-color: rgba(59, 130, 246, 0.5) !important;
    }
    
    [data-testid="stMetric"]:hover::before {
        left: 100%;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        color: #94a3b8 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        margin-bottom: 0.75rem !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.75rem !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, #ffffff, #e0e7ff) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        line-height: 1.1 !important;
        margin: 0.5rem 0 !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        margin-top: 0.5rem !important;
    }
    
    /* Chart Containers - Glassmorphism */
    .glass-card {
        background: rgba(30, 41, 59, 0.3) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 24px !important;
        padding: 2rem !important;
        box-shadow: 
            0 8px 32px 0 rgba(0, 0, 0, 0.37),
            inset 0 1px 0 0 rgba(255, 255, 255, 0.08) !important;
        margin-bottom: 2rem !important;
        position: relative !important;
    }
    
    .glass-card::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(139, 92, 246, 0.1) 0%, transparent 70%);
        pointer-events: none;
        animation: glow 8s ease-in-out infinite;
    }
    
    @keyframes glow {
        0%, 100% { opacity: 0.3; transform: rotate(0deg); }
        50% { opacity: 0.6; transform: rotate(180deg); }
    }
    
    .section-title {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: #f1f5f9 !important;
        margin-bottom: 1.5rem !important;
        letter-spacing: -0.02em !important;
    }
    
    /* DataFrames - Glassmorphic */
    .stDataFrame {
        background: rgba(30, 41, 59, 0.3) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        overflow: hidden !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
    }
    
    .stDataFrame thead tr th {
        background: rgba(15, 23, 42, 0.8) !important;
        color: #cbd5e1 !important;
        font-weight: 700 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        padding: 1rem !important;
        border-bottom: 1px solid rgba(59, 130, 246, 0.3) !important;
    }
    
    .stDataFrame tbody tr {
        background: rgba(30, 41, 59, 0.2) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
        transition: all 0.3s ease !important;
    }
    
    .stDataFrame tbody tr:hover {
        background: rgba(59, 130, 246, 0.1) !important;
        transform: translateX(4px) !important;
    }
    
    .stDataFrame tbody tr td {
        color: #f1f5f9 !important;
        padding: 1rem !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
    }
    
    /* Info Box - Gradient */
    .stInfo {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(139, 92, 246, 0.2)) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 16px !important;
        color: #e0e7ff !important;
        padding: 1rem 1.5rem !important;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* Success Box - Green Gradient */
    .stSuccess {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(6, 182, 212, 0.2)) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-radius: 16px !important;
        color: #d1fae5 !important;
        padding: 1rem 1.5rem !important;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.2) !important;
    }
    
    /* Plotly Charts - Transparent */
    .js-plotly-plot {
        background: transparent !important;
    }
    
    /* Scrollbar - Gradient */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        border-radius: 10px;
        border: 2px solid rgba(15, 23, 42, 0.5);
        box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.7);
    }
    
    /* Divider - Gradient Line */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(59, 130, 246, 0.6) 20%,
            rgba(139, 92, 246, 0.6) 50%,
            rgba(59, 130, 246, 0.6) 80%,
            transparent
        ) !important;
        margin: 3rem 0 !important;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Select Boxes - Glassmorphic */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: rgba(30, 41, 59, 0.4) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        color: #f1f5f9 !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Date Input - Glassmorphic */
    .stDateInput > div > div {
        background: rgba(30, 41, 59, 0.4) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        color: #f1f5f9 !important;
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
    df['Entry'] = pd.to_numeric(df['Entry'], errors='coerce')
    df['SL'] = pd.to_numeric(df['SL'], errors='coerce')
    df['SL_Distance_%'] = abs((df['Entry'] - df['SL']) / df['Entry'] * 100)
    
    return df

df = load_data()

# Header with gradient
st.markdown("# 📊 Crypto Trading Signals")
st.markdown("<br>", unsafe_allow_html=True)

# Filters - Compact Row
col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
with col1:
    date_range = st.date_input("📅 Date Range", value=(df['Timestamp'].min().date(), df['Timestamp'].max().date()), label_visibility="collapsed")
with col2:
    side_filter = st.multiselect("📈 Direction", ['ALL'] + list(df['Side'].unique()), default=['ALL'], label_visibility="collapsed")
with col3:
    result_filter = st.multiselect("🎯 Status", ['ALL'] + list(df['Result'].dropna().unique()), default=['ALL'], label_visibility="collapsed")
with col4:
    last = df['Timestamp'].max()
    st.markdown(f"<p style='color: #94a3b8; font-size: 0.75rem; text-align: right; margin-top: 0.5rem;'>Updated<br>{last.strftime('%H:%M')}</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

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
wins = len(completed[completed['Result'].isin(['TP1_HIT', 'TP2_HIT'])])
losses = len(completed[completed['Result'] == 'SL_HIT'])
win_rate = (wins / completed_count * 100) if completed_count > 0 else 0
avg_pnl = completed['P&L_%'].mean() if not completed.empty else 0
total_pnl = completed['P&L_%'].sum() if not completed.empty else 0
sl_trades = df_filtered[df_filtered['Result'] == 'SL_HIT']
avg_sl_dist = sl_trades['SL_Distance_%'].mean() if not sl_trades.empty else 0

# KPI Cards - 4 Column Grid
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Win Rate", f"{win_rate:.1f}%", f"{wins}W / {losses}L")

with col2:
    delta_color = "normal" if total_pnl >= 0 else "inverse"
    st.metric("Total P&L", f"{total_pnl:+.2f}%", f"Avg: {avg_pnl:.2f}%")

with col3:
    st.metric("Signals", f"{total:,}", f"{completed_count} completed")

with col4:
    st.metric("Avg SL Distance", f"{avg_sl_dist:.2f}%", f"{len(sl_trades)} SL hits")

st.markdown("<br>", unsafe_allow_html=True)

# SL Insight Alert
if not sl_trades.empty and len(completed) >= 50:
    completed_copy = completed.copy()
    completed_copy['SL_Range'] = pd.cut(
        completed_copy['SL_Distance_%'],
        bins=[0, 2, 3, 4, 5, 6, 100],
        labels=['0-2%', '2-3%', '3-4%', '4-5%', '5-6%', '6%+']
    )
    
    range_stats = completed_copy.groupby('SL_Range', observed=True).agg({
        'Result': [
            ('total', 'count'),
            ('wins', lambda x: (x.isin(['TP1_HIT', 'TP2_HIT'])).sum())
        ]
    }).reset_index()
    
    range_stats.columns = ['SL_Range', 'Total', 'Wins']
    range_stats['Win_Rate'] = (range_stats['Wins'] / range_stats['Total'] * 100)
    range_stats_filtered = range_stats[range_stats['Total'] >= 10]
    
    if not range_stats_filtered.empty:
        best = range_stats_filtered.loc[range_stats_filtered['Win_Rate'].idxmax()]
        if best['Win_Rate'] > win_rate + 5:
            st.success(f"💡 **Optimization Opportunity:** SL range {best['SL_Range']} shows {best['Win_Rate']:.1f}% Win Rate (vs {win_rate:.1f}% overall) across {best['Total']} trades. Consider adjusting your SL strategy.")

st.markdown("<br>", unsafe_allow_html=True)

# Main Grid - 2 Columns
col_left, col_right = st.columns([1, 1])

with col_left:
    # Results Distribution
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<p class='section-title'>📊 Results Distribution</p>", unsafe_allow_html=True)
    
    result_counts = df_filtered['Result'].value_counts()
    fig1 = go.Figure(data=[go.Pie(
        labels=result_counts.index,
        values=result_counts.values,
        hole=0.65,
        marker=dict(
            colors=['#3b82f6', '#10b981', '#ef4444', '#f59e0b', '#8b5cf6'],
            line=dict(color='#0f172a', width=3)
        ),
        textfont=dict(size=13, color='white', family='Roboto', weight=600),
        textposition='outside',
        textinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>%{value} trades<br>%{percent}<extra></extra>'
    )])
    
    fig1.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f1f5f9', family='Roboto'),
        margin=dict(t=10, b=10, l=10, r=10),
        height=300,
        annotations=[dict(
            text=f'<b>{total}</b><br><span style="font-size:12px; color:#94a3b8;">Total Signals</span>',
            x=0.5, y=0.5,
            font_size=28,
            font_color='#f1f5f9',
            font_family='Roboto',
            showarrow=False
        )]
    )
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    # Long vs Short Performance
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<p class='section-title'>📈 LONG vs SHORT Performance</p>", unsafe_allow_html=True)
    
    side_stats = completed.groupby('Side').agg({
        'Result': 'count',
        'P&L_%': 'sum'
    }).reset_index()
    side_stats.columns = ['Side', 'Count', 'Total_PnL']
    side_stats['Win_Rate'] = side_stats.apply(
        lambda row: (completed[(completed['Side'] == row['Side']) & (completed['Result'].isin(['TP1_HIT', 'TP2_HIT']))].shape[0] / row['Count'] * 100) if row['Count'] > 0 else 0,
        axis=1
    )
    
    fig2 = go.Figure()
    
    fig2.add_trace(go.Bar(
        x=side_stats['Side'],
        y=side_stats['Total_PnL'],
        name='Total P&L',
        marker=dict(
            color=['#3b82f6' if side == 'LONG' else '#8b5cf6' for side in side_stats['Side']],
            line=dict(color='#0f172a', width=2)
        ),
        text=side_stats['Total_PnL'].apply(lambda x: f"{x:+.1f}%"),
        textposition='outside',
        textfont=dict(size=12, color='#f1f5f9', weight=600),
        hovertemplate='<b>%{x}</b><br>P&L: %{y:.2f}%<extra></extra>'
    ))
    
    fig2.add_trace(go.Scatter(
        x=side_stats['Side'],
        y=side_stats['Win_Rate'],
        mode='lines+markers+text',
        name='Win Rate',
        yaxis='y2',
        marker=dict(size=14, color='#10b981', line=dict(color='#f1f5f9', width=2)),
        line=dict(width=3, color='#10b981'),
        text=side_stats['Win_Rate'].apply(lambda x: f"{x:.0f}%"),
        textposition='top center',
        textfont=dict(size=11, color='#10b981', weight=600),
        hovertemplate='<b>%{x}</b><br>Win Rate: %{y:.1f}%<extra></extra>'
    ))
    
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f1f5f9', family='Roboto'),
        yaxis=dict(
            title='P&L (%)',
            gridcolor='rgba(255, 255, 255, 0.08)',
            showgrid=True,
            zeroline=True,
            zerolinecolor='rgba(239, 68, 68, 0.3)',
            title_font=dict(size=11, color='#94a3b8')
        ),
        yaxis2=dict(
            title='Win Rate (%)',
            overlaying='y',
            side='right',
            showgrid=False,
            title_font=dict(size=11, color='#94a3b8')
        ),
        margin=dict(t=40, b=10, l=10, r=10),
        height=300,
        showlegend=False,
        hovermode='x unified'
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Cumulative Performance - Full Width
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.markdown("<p class='section-title'>💰 Cumulative P&L Performance</p>", unsafe_allow_html=True)

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
        line=dict(color='#3b82f6', width=3),
        fillgradient=dict(
            type='vertical',
            colorscale=[[0, 'rgba(59, 130, 246, 0.4)'], [1, 'rgba(139, 92, 246, 0.1)']]
        ),
        hovertemplate='<b>%{x}</b><br>Cumulative P&L: %{y:.2f}%<extra></extra>'
    ))
    
    fig3.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f1f5f9', family='Roboto'),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.08)',
            showgrid=True,
            title_font=dict(size=11, color='#94a3b8')
        ),
        yaxis=dict(
            title='Cumulative P&L (%)',
            gridcolor='rgba(255, 255, 255, 0.08)',
            showgrid=True,
            zeroline=True,
            zerolinecolor='rgba(239, 68, 68, 0.5)',
            zerolinewidth=2,
            title_font=dict(size=11, color='#94a3b8')
        ),
        margin=dict(t=10, b=10, l=10, r=10),
        height=300,
        hovermode='x unified'
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("No completed trades to display")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# SL ANALYSIS SECTION
st.markdown("# 🛑 Stop Loss Analysis")
st.markdown("<br>", unsafe_allow_html=True)

# SL KPIs - 5 Columns
col1, col2, col3, col4, col5 = st.columns(5)

total_sl = len(sl_trades)
total_tp = len(df_filtered[df_filtered['Result'].isin(['TP1_HIT', 'TP2_HIT'])])
sl_rate = (total_sl / len(completed) * 100) if len(completed) > 0 else 0
median_sl = sl_trades['SL_Distance_%'].median() if not sl_trades.empty else 0
avg_sl_pnl = sl_trades['P&L_%'].mean() if not sl_trades.empty else 0

with col1:
    st.metric("SL Hits", f"{total_sl}", f"{sl_rate:.1f}% of trades")

with col2:
    st.metric("Avg SL Distance", f"{avg_sl_dist:.2f}%")

with col3:
    st.metric("Median SL Distance", f"{median_sl:.2f}%")

with col4:
    st.metric("Avg SL Loss", f"{avg_sl_pnl:.2f}%")

with col5:
    st.metric("Current WR", f"{win_rate:.1f}%", f"{total_tp}W / {total_sl}L")

st.markdown("<br>", unsafe_allow_html=True)

# SL Analysis Grid - 2 Columns
col_left, col_right = st.columns([1, 1])

with col_left:
    # Win Rate by SL Distance
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<p class='section-title'>🎯 Win Rate by SL Distance Range</p>", unsafe_allow_html=True)
    
    if not completed.empty:
        completed_copy = completed.copy()
        completed_copy['SL_Range'] = pd.cut(
            completed_copy['SL_Distance_%'],
            bins=[0, 2, 3, 4, 5, 6, 100],
            labels=['0-2%', '2-3%', '3-4%', '4-5%', '5-6%', '6%+']
        )
        
        range_stats = completed_copy.groupby('SL_Range', observed=True).agg({
            'Result': [
                ('total', 'count'),
                ('wins', lambda x: (x.isin(['TP1_HIT', 'TP2_HIT'])).sum())
            ]
        }).reset_index()
        
        range_stats.columns = ['SL_Range', 'Total', 'Wins']
        range_stats['Win_Rate'] = (range_stats['Wins'] / range_stats['Total'] * 100)
        
        fig4 = go.Figure()
        
        colors = ['#3b82f6' if wr >= win_rate else '#8b5cf6' for wr in range_stats['Win_Rate']]
        
        fig4.add_trace(go.Bar(
            x=range_stats['SL_Range'],
            y=range_stats['Win_Rate'],
            marker=dict(
                color=colors,
                line=dict(color='#0f172a', width=2)
            ),
            text=range_stats['Win_Rate'].apply(lambda x: f"{x:.1f}%"),
            textposition='outside',
            textfont=dict(size=12, color='#f1f5f9', weight=600),
            hovertemplate='<b>%{x}</b><br>Win Rate: %{y:.1f}%<br>Trades: ' + range_stats['Total'].astype(str) + '<extra></extra>'
        ))
        
        # Add current WR line
        fig4.add_hline(
            y=win_rate,
            line_dash="dash",
            line_color="#10b981",
            line_width=2,
            annotation_text=f"Current WR: {win_rate:.1f}%",
            annotation_position="right",
            annotation_font_size=11,
            annotation_font_color="#10b981"
        )
        
        fig4.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f1f5f9', family='Roboto'),
            xaxis=dict(
                title='SL Distance Range',
                gridcolor='rgba(255, 255, 255, 0.08)',
                title_font=dict(size=11, color='#94a3b8')
            ),
            yaxis=dict(
                title='Win Rate (%)',
                gridcolor='rgba(255, 255, 255, 0.08)',
                showgrid=True,
                range=[0, 100],
                title_font=dict(size=11, color='#94a3b8')
            ),
            margin=dict(t=10, b=10, l=10, r=10),
            height=320,
            showlegend=False
        )
        st.plotly_chart(fig4, use_container_width=True)
        
        # Best performing range
        best = range_stats.loc[range_stats['Win_Rate'].idxmax()]
        if best['Total'] >= 10:
            st.success(f"🏆 **Best Range:** {best['SL_Range']} → {best['Win_Rate']:.1f}% WR ({best['Total']} trades)")
    else:
        st.info("Not enough data")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    # SL Distance Distribution
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<p class='section-title'>📊 SL Distance: Winners vs Losers</p>", unsafe_allow_html=True)
    
    if not completed.empty:
        tp_trades = completed[completed['Result'].isin(['TP1_HIT', 'TP2_HIT'])]
        
        fig5 = go.Figure()
        
        fig5.add_trace(go.Box(
            y=tp_trades['SL_Distance_%'],
            name='Winners',
            marker=dict(color='#10b981'),
            boxmean='sd',
            hovertemplate='<b>Winners</b><br>SL Distance: %{y:.2f}%<extra></extra>'
        ))
        
        fig5.add_trace(go.Box(
            y=sl_trades['SL_Distance_%'],
            name='Losers',
            marker=dict(color='#ef4444'),
            boxmean='sd',
            hovertemplate='<b>Losers</b><br>SL Distance: %{y:.2f}%<extra></extra>'
        ))
        
        fig5.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#f1f5f9', family='Roboto'),
            yaxis=dict(
                title='SL Distance (%)',
                gridcolor='rgba(255, 255, 255, 0.08)',
                showgrid=True,
                title_font=dict(size=11, color='#94a3b8')
            ),
            margin=dict(t=10, b=10, l=10, r=10),
            height=320,
            showlegend=True,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1,
                bgcolor='rgba(0,0,0,0)',
                font=dict(color='#f1f5f9')
            )
        )
        st.plotly_chart(fig5, use_container_width=True)
        
        # Stats
        avg_winner_sl = tp_trades['SL_Distance_%'].mean() if not tp_trades.empty else 0
        avg_loser_sl = sl_trades['SL_Distance_%'].mean() if not sl_trades.empty else 0
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"<p style='color: #10b981; font-size: 0.875rem;'><b>Winners avg:</b> {avg_winner_sl:.2f}%</p>", unsafe_allow_html=True)
        with col_b:
            st.markdown(f"<p style='color: #ef4444; font-size: 0.875rem;'><b>Losers avg:</b> {avg_loser_sl:.2f}%</p>", unsafe_allow_html=True)
    else:
        st.info("Not enough data")
    
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Recent SL Hits Table
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.markdown("<p class='section-title'>📋 Recent Stop Loss Hits</p>", unsafe_allow_html=True)

if not sl_trades.empty:
    recent_sl = sl_trades.sort_values('Timestamp', ascending=False).head(15).copy()
    recent_sl['Time'] = recent_sl['Timestamp'].dt.strftime('%b %d, %H:%M')
    recent_sl['SL Dist'] = recent_sl['SL_Distance_%'].apply(lambda x: f"{x:.2f}%")
    recent_sl['P&L'] = recent_sl['P&L_%'].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else "—")
    recent_sl['Entry_fmt'] = recent_sl['Entry'].apply(lambda x: f"{x:.4f}" if pd.notna(x) else "—")
    recent_sl['SL_fmt'] = recent_sl['SL'].apply(lambda x: f"{x:.4f}" if pd.notna(x) else "—")
    
    st.dataframe(
        recent_sl[['Time', 'Symbol', 'Side', 'Entry_fmt', 'SL_fmt', 'SL Dist', 'P&L']],
        use_container_width=True,
        hide_index=True,
        height=400,
        column_config={
            'Entry_fmt': 'Entry',
            'SL_fmt': 'SL'
        }
    )
else:
    st.info("No SL hits yet")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Bottom Section - Top Performers + Symbols
col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<p class='section-title'>🏆 Top Winners</p>", unsafe_allow_html=True)
    
    if not completed.empty:
        winners = completed.nlargest(10, 'P&L_%')[['Timestamp', 'Symbol', 'Side', 'P&L_%']].copy()
        winners['Time'] = winners['Timestamp'].dt.strftime('%b %d')
        winners['P&L'] = winners['P&L_%'].apply(lambda x: f"+{x:.2f}%")
        st.dataframe(winners[['Time', 'Symbol', 'Side', 'P&L']], use_container_width=True, hide_index=True, height=320)
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<p class='section-title'>📉 Top Losers</p>", unsafe_allow_html=True)
    
    if not completed.empty:
        losers = completed.nsmallest(10, 'P&L_%')[['Timestamp', 'Symbol', 'Side', 'P&L_%']].copy()
        losers['Time'] = losers['Timestamp'].dt.strftime('%b %d')
        losers['P&L'] = losers['P&L_%'].apply(lambda x: f"{x:.2f}%")
        st.dataframe(losers[['Time', 'Symbol', 'Side', 'P&L']], use_container_width=True, hide_index=True, height=320)
    
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Top Performing Symbols - Full Width
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.markdown("<p class='section-title'>💎 Top Performing Symbols</p>", unsafe_allow_html=True)

if not completed.empty:
    symbols = completed.groupby('Symbol').agg({
        'P&L_%': ['sum', 'count'],
        'Result': lambda x: (x.isin(['TP1_HIT', 'TP2_HIT'])).sum()
    }).reset_index()
    symbols.columns = ['Symbol', 'Total_PnL', 'Count', 'Wins']
    symbols['WR'] = (symbols['Wins'] / symbols['Count'] * 100).round(1)
    symbols = symbols.sort_values('Total_PnL', ascending=False).head(12)
    
    colors = ['#10b981' if x > 0 else '#ef4444' for x in symbols['Total_PnL']]
    
    fig6 = go.Figure()
    fig6.add_trace(go.Bar(
        x=symbols['Symbol'],
        y=symbols['Total_PnL'],
        marker=dict(color=colors, line=dict(color='#0f172a', width=2)),
        text=symbols['WR'].apply(lambda x: f"{x:.0f}%"),
        textposition='outside',
        textfont=dict(size=11, color='#94a3b8', weight=600),
        hovertemplate='<b>%{x}</b><br>P&L: %{y:.2f}%<br>WR: ' + symbols['WR'].astype(str) + '%<extra></extra>'
    ))
    
    fig6.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f1f5f9', family='Roboto'),
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.08)'),
        yaxis=dict(
            title='Total P&L (%)',
            gridcolor='rgba(255, 255, 255, 0.08)',
            zeroline=True,
            zerolinecolor='rgba(255, 255, 255, 0.15)',
            title_font=dict(size=11, color='#94a3b8')
        ),
        margin=dict(t=30, b=10, l=10, r=10),
        height=300,
        showlegend=False
    )
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.75rem;'>FlowBot Automation © 2025 | Powered by AI</p>", unsafe_allow_html=True)
