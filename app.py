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

# CSS מתקדם - Dark Mode עם Neon/Glow Effects
st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Header styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 50%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: left;
        margin-bottom: 2rem;
        text-shadow: 0 0 30px rgba(6, 182, 212, 0.3);
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(6, 182, 212, 0.2);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4), 0 0 20px rgba(6, 182, 212, 0.1);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: rgba(6, 182, 212, 0.5);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5), 0 0 40px rgba(6, 182, 212, 0.2);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        color: #94a3b8;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #06b6d4;
        text-shadow: 0 0 20px rgba(6, 182, 212, 0.5);
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid rgba(6, 182, 212, 0.2);
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
        color: #06b6d4;
        font-weight: 700;
        text-shadow: 0 0 15px rgba(6, 182, 212, 0.4);
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%);
        box-shadow: 0 6px 25px rgba(6, 182, 212, 0.6);
        transform: translateY(-2px);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background: #1e293b;
        border-radius: 12px;
        border: 1px solid rgba(6, 182, 212, 0.2);
        overflow: hidden;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(6, 182, 212, 0.5), transparent);
        margin: 2rem 0;
    }
    
    /* Headers */
    h3 {
        color: #e2e8f0;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 0 0 10px rgba(6, 182, 212, 0.2);
    }
    
    /* Info boxes */
    .stInfo, .stSuccess, .stWarning {
        background: #1e293b;
        border-left: 4px solid #06b6d4;
        border-radius: 8px;
    }
    
    /* Select boxes and inputs */
    .stSelectbox, .stMultiSelect, .stDateInput {
        background: #1e293b;
    }
    
    .stSelectbox > div > div {
        background-color: #334155;
        border: 1px solid rgba(6, 182, 212, 0.3);
        border-radius: 8px;
        color: #e2e8f0;
    }
    
    /* Plotly charts container */
    .js-plotly-plot {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
        border-radius: 16px;
        padding: 1rem;
        border: 1px solid rgba(6, 182, 212, 0.2);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    
    /* Custom metric card animation */
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 5px rgba(6, 182, 212, 0.5); }
        50% { box-shadow: 0 0 20px rgba(6, 182, 212, 0.8); }
    }
    
    /* Success/Positive values */
    .positive {
        color: #10b981;
        text-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
    }
    
    /* Negative values */
    .negative {
        color: #ef4444;
        text-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1e293b;
        border-radius: 12px;
        padding: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
        color: white;
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.4);
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
            st.sidebar.success("✅ מחובר לגוגל שיטס")
        else:
            df = pd.read_csv('Signals_Log_-_Sheet1.csv')
            st.sidebar.info("📁 קורא מקובץ מקומי")
    
    except Exception as e:
        st.error(f"❌ שגיאה בטעינת הדאטה: {str(e)}")
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
    st.error(f"לא ניתן לטעון את הדאטה")
    st.stop()

# Header
st.markdown('<h1 class="main-header">🚀 Crypto Trading Signals Dashboard</h1>', unsafe_allow_html=True)

# Last update info
last_update = df['Timestamp'].max()
col_update1, col_update2, col_update3 = st.columns([2, 1, 1])
with col_update1:
    st.markdown(f"**🕐 Last Update:** {last_update.strftime('%d/%m/%Y %H:%M')}")

# Sidebar filters
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

# Calculate metrics
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

# Main metrics
st.markdown("### 📊 Key Performance Indicators")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="🎯 Win Rate",
        value=f"{win_rate:.1f}%",
        delta=f"{wins}W / {losses}L"
    )

with col2:
    st.metric(
        label="💰 Avg P&L",
        value=f"{avg_pnl:.2f}%",
        delta=f"Total: {total_pnl:.2f}%"
    )

with col3:
    st.metric(
        label="📈 Total Signals",
        value=total_signals,
        delta=f"Completed: {completed_count}"
    )

with col4:
    st.metric(
        label="⏳ Pending",
        value=pending_count,
        delta=f"{(pending_count/total_signals*100):.1f}%" if total_signals > 0 else "0%"
    )

with col5:
    st.metric(
        label="⌛ Expired",
        value=expired_count,
        delta=f"{(expired_count/total_signals*100):.1f}%" if total_signals > 0 else "0%"
    )

st.divider()

# Charts row 1
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Results Distribution")
    result_counts = df_filtered['Result'].value_counts()
    
    fig_results = go.Figure(data=[go.Pie(
        labels=result_counts.index,
        values=result_counts.values,
        hole=0.6,
        marker=dict(
            colors=['#06b6d4', '#10b981', '#ef4444', '#f59e0b', '#8b5cf6'],
            line=dict(color='#1e293b', width=2)
        ),
        textfont=dict(size=14, color='white', family='Inter'),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig_results.update_layout(
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0', family='Inter'),
        margin=dict(t=30, b=30, l=30, r=30),
        legend=dict(
            bgcolor='rgba(30, 41, 59, 0.8)',
            bordercolor='rgba(6, 182, 212, 0.3)',
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig_results, use_container_width=True)

with col2:
    st.markdown("### 📈 LONG vs SHORT Performance")
    side_stats = df_filtered.groupby('Side').agg({
        'Result': 'count',
        'P&L_%': 'mean'
    }).reset_index()
    side_stats.columns = ['Side', 'Count', 'Avg_PnL']
    
    fig_side = go.Figure()
    
    fig_side.add_trace(go.Bar(
        name='Signal Count',
        x=side_stats['Side'],
        y=side_stats['Count'],
        marker=dict(
            color='#06b6d4',
            line=dict(color='#0891b2', width=2)
        ),
        text=side_stats['Count'],
        textposition='outside',
        yaxis='y'
    ))
    
    fig_side.add_trace(go.Scatter(
        name='Avg P&L %',
        x=side_stats['Side'],
        y=side_stats['Avg_PnL'],
        mode='lines+markers',
        marker=dict(size=15, color='#10b981', line=dict(color='#059669', width=2)),
        line=dict(width=3, color='#10b981'),
        yaxis='y2'
    ))
    
    fig_side.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0', family='Inter'),
        yaxis=dict(title='Signal Count', gridcolor='rgba(6, 182, 212, 0.1)'),
        yaxis2=dict(title='Avg P&L %', overlaying='y', side='right', gridcolor='rgba(16, 185, 129, 0.1)'),
        hovermode='x unified',
        margin=dict(t=30, b=30, l=30, r=30),
        legend=dict(
            bgcolor='rgba(30, 41, 59, 0.8)',
            bordercolor='rgba(6, 182, 212, 0.3)',
            borderwidth=1
        )
    )
    
    st.plotly_chart(fig_side, use_container_width=True)

st.divider()

# Performance over time
st.markdown("### 📅 Cumulative Performance")
if not completed_signals.empty:
    daily_pnl = completed_signals.groupby(completed_signals['Check_Date'].dt.date)['P&L_%'].agg(['sum', 'count']).reset_index()
    daily_pnl.columns = ['Date', 'Total_PnL', 'Count']
    daily_pnl['Cumulative_PnL'] = daily_pnl['Total_PnL'].cumsum()
    
    fig_timeline = go.Figure()
    
    fig_timeline.add_trace(go.Scatter(
        x=daily_pnl['Date'],
        y=daily_pnl['Cumulative_PnL'],
        mode='lines',
        name='Cumulative P&L',
        line=dict(color='#06b6d4', width=3),
        fill='tozeroy',
        fillcolor='rgba(6, 182, 212, 0.2)',
        hovertemplate='Date: %{x}<br>Cumulative P&L: %{y:.2f}%<extra></extra>'
    ))
    
    fig_timeline.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0', family='Inter'),
        xaxis=dict(
            title='Date',
            gridcolor='rgba(6, 182, 212, 0.1)',
            showgrid=True
        ),
        yaxis=dict(
            title='Cumulative P&L %',
            gridcolor='rgba(6, 182, 212, 0.1)',
            showgrid=True,
            zeroline=True,
            zerolinecolor='rgba(239, 68, 68, 0.3)',
            zerolinewidth=2
        ),
        hovermode='x unified',
        margin=dict(t=30, b=30, l=30, r=30)
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)
else:
    st.info("⏳ No completed signals yet to display timeline")

st.divider()

# Top performers
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏆 Top 10 Winners")
    if not completed_signals.empty:
        top_winners = completed_signals.nlargest(10, 'P&L_%')[['Timestamp', 'Symbol', 'Side', 'Entry', 'P&L_%', 'Result']]
        top_winners['Timestamp'] = top_winners['Timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        st.dataframe(top_winners, use_container_width=True, hide_index=True)
    else:
        st.info("⏳ No data yet")

with col2:
    st.markdown("### ⚠️ Top 10 Losers")
    if not completed_signals.empty:
        top_losers = completed_signals.nsmallest(10, 'P&L_%')[['Timestamp', 'Symbol', 'Side', 'Entry', 'P&L_%', 'Result']]
        top_losers['Timestamp'] = top_losers['Timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        st.dataframe(top_losers, use_container_width=True, hide_index=True)
    else:
        st.info("⏳ No data yet")

st.divider()

# Symbol performance
st.markdown("### 💎 Performance by Symbol")
if not completed_signals.empty:
    symbol_stats = completed_signals.groupby('Symbol').agg({
        'P&L_%': ['mean', 'sum', 'count'],
        'Result': lambda x: (x.isin(['TP1_HIT', 'TP2_HIT'])).sum()
    }).reset_index()
    
    symbol_stats.columns = ['Symbol', 'Avg_PnL', 'Total_PnL', 'Count', 'Wins']
    symbol_stats['Win_Rate'] = (symbol_stats['Wins'] / symbol_stats['Count'] * 100).round(1)
    symbol_stats = symbol_stats.sort_values('Total_PnL', ascending=False).head(15)
    
    fig_symbols = go.Figure()
    
    colors = ['#10b981' if x > 0 else '#ef4444' for x in symbol_stats['Total_PnL']]
    
    fig_symbols.add_trace(go.Bar(
        x=symbol_stats['Symbol'],
        y=symbol_stats['Total_PnL'],
        marker=dict(
            color=colors,
            line=dict(color='#1e293b', width=1)
        ),
        text=symbol_stats['Win_Rate'].apply(lambda x: f'{x:.1f}%'),
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Total P&L: %{y:.2f}%<br>Win Rate: %{text}<extra></extra>'
    ))
    
    fig_symbols.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e2e8f0', family='Inter'),
        xaxis=dict(title='Symbol', gridcolor='rgba(6, 182, 212, 0.1)'),
        yaxis=dict(
            title='Total P&L %',
            gridcolor='rgba(6, 182, 212, 0.1)',
            zeroline=True,
            zerolinecolor='rgba(239, 68, 68, 0.3)',
            zerolinewidth=2
        ),
        margin=dict(t=30, b=30, l=30, r=30)
    )
    
    st.plotly_chart(fig_symbols, use_container_width=True)
    
    st.dataframe(
        symbol_stats.sort_values('Win_Rate', ascending=False),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("⏳ Not enough data for symbol analysis")

st.divider()

# Recent signals
st.markdown("### 🔄 Recent Signals (Latest 20)")
recent_signals = df_filtered.sort_values('Timestamp', ascending=False).head(20)
recent_signals_display = recent_signals[[
    'Timestamp', 'Symbol', 'Side', 'Entry', 'SL', 'TP1', 'TP2',
    'Confidence', 'Result', 'P&L_%'
]].copy()

recent_signals_display['Timestamp'] = recent_signals_display['Timestamp'].dt.strftime('%Y-%m-%d %H:%M')

st.dataframe(recent_signals_display, use_container_width=True, hide_index=True)

# Sidebar stats
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Stats")

if not completed_signals.empty:
    best_symbol = completed_signals.groupby('Symbol')['P&L_%'].sum().idxmax()
    best_pnl = completed_signals.groupby('Symbol')['P&L_%'].sum().max()
    worst_symbol = completed_signals.groupby('Symbol')['P&L_%'].sum().idxmin()
    worst_pnl = completed_signals.groupby('Symbol')['P&L_%'].sum().min()
    
    st.sidebar.metric("🏆 Best Symbol", best_symbol, f"{best_pnl:.2f}%")
    st.sidebar.metric("⚠️ Worst Symbol", worst_symbol, f"{worst_pnl:.2f}%")
else:
    st.sidebar.info("⏳ No completed signals yet")

# Refresh button
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("🔄 Data auto-refreshes every 5 minutes")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #94a3b8; padding: 2rem 0;'>
        <p style='margin: 0; font-size: 0.9rem;'>Made with ❤️ by <span style='color: #06b6d4; font-weight: 600;'>FlowBot Automation</span></p>
        <p style='margin: 0.5rem 0 0 0; font-size: 0.8rem;'>Data syncs every 4 hours from n8n bot | Real-time analytics dashboard</p>
    </div>
    """,
    unsafe_allow_html=True
)
