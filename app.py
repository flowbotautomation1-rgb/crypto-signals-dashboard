import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# הגדרות עמוד
st.set_page_config(
    page_title="Crypto Signals Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS מקצועי וקליל
st.markdown("""
<style>
    /* Import professional font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global reset */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        letter-spacing: -0.01em;
    }
    
    /* Main background */
    .stApp {
        background: #0B1120 !important;
    }
    
    .main .block-container {
        padding: 3rem 4rem !important;
        max-width: 1600px !important;
    }
    
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Header */
    h1 {
        font-size: 2.25rem !important;
        font-weight: 600 !important;
        color: #F8FAFC !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.02em !important;
    }
    
    /* Subheaders */
    h2 {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        color: #CBD5E1 !important;
        margin: 2.5rem 0 1.25rem 0 !important;
        letter-spacing: -0.01em !important;
    }
    
    /* Last update text */
    .stMarkdown p {
        font-size: 0.875rem !important;
        color: #64748B !important;
        font-weight: 400 !important;
    }
    
    /* METRIC CARDS - Professional design */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
        padding: 2rem !important;
        border-radius: 12px !important;
        border: 1px solid rgba(148, 163, 184, 0.1) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    
    [data-testid="stMetric"]:hover {
        border-color: rgba(59, 130, 246, 0.4) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        color: #94A3B8 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin-bottom: 0.75rem !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.25rem !important;
        font-weight: 700 !important;
        color: #F8FAFC !important;
        line-height: 1 !important;
        margin: 0.5rem 0 !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        margin-top: 0.5rem !important;
    }
    
    /* Positive delta */
    [data-testid="stMetricDelta"] svg[fill="#00ff00"] {
        fill: #10B981 !important;
    }
    
    [data-testid="stMetricDelta"][data-testid*="increase"] {
        color: #10B981 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0F172A !important;
        border-right: 1px solid rgba(148, 163, 184, 0.1) !important;
        padding-top: 3rem !important;
    }
    
    [data-testid="stSidebar"] > div {
        background: transparent !important;
    }
    
    [data-testid="stSidebar"] h2 {
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        color: #CBD5E1 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin-bottom: 1.5rem !important;
    }
    
    [data-testid="stSidebar"] label {
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        color: #94A3B8 !important;
    }
    
    /* Input fields */
    .stSelectbox > div > div,
    .stMultiSelect > div > div,
    .stDateInput > div > div > input {
        background: #1E293B !important;
        border: 1px solid rgba(148, 163, 184, 0.15) !important;
        border-radius: 8px !important;
        color: #F8FAFC !important;
        font-size: 0.875rem !important;
        padding: 0.5rem 0.75rem !important;
    }
    
    /* Buttons */
    .stButton button {
        background: #3B82F6 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.625rem 1.25rem !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    
    .stButton button:hover {
        background: #2563EB !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Dataframes */
    [data-testid="stDataFrame"] {
        font-size: 0.875rem !important;
    }
    
    .stDataFrame {
        border: 1px solid rgba(148, 163, 184, 0.1) !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    
    /* Dataframe headers */
    .stDataFrame thead tr th {
        background: #1E293B !important;
        color: #CBD5E1 !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        padding: 0.875rem !important;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1) !important;
    }
    
    /* Dataframe rows */
    .stDataFrame tbody tr {
        background: #0F172A !important;
        border-bottom: 1px solid rgba(148, 163, 184, 0.05) !important;
    }
    
    .stDataFrame tbody tr:hover {
        background: #1E293B !important;
    }
    
    .stDataFrame tbody tr td {
        color: #CBD5E1 !important;
        padding: 0.875rem !important;
        font-size: 0.875rem !important;
    }
    
    /* Charts container */
    .js-plotly-plot {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        border: 1px solid rgba(148, 163, 184, 0.1) !important;
    }
    
    /* Info boxes */
    .stInfo {
        background: #1E293B !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        color: #CBD5E1 !important;
    }
    
    .stSuccess {
        background: #1E293B !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        color: #CBD5E1 !important;
    }
    
    /* Divider */
    hr {
        border: none !important;
        height: 1px !important;
        background: rgba(148, 163, 184, 0.1) !important;
        margin: 3rem 0 !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0F172A;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #334155;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #475569;
    }
    
    /* Remove emoji and icon spacing issues */
    [data-testid="stMetricLabel"]::before {
        content: '' !important;
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# טעינת דאטה
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
        st.error(f"Error loading data: {str(e)}")
        st.stop()
    
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Check_Date'] = pd.to_datetime(df['Check_Date'], errors='coerce')
    df['P&L_%'] = pd.to_numeric(df['P&L_%'], errors='coerce')
    df['Actual_RR'] = pd.to_numeric(df['Actual_RR'], errors='coerce')
    df['Confidence'] = pd.to_numeric(df['Confidence'], errors='coerce')
    return df

df = load_data()

# Header
st.markdown("# Crypto Trading Signals")
last_update = df['Timestamp'].max()
st.markdown(f"Last updated {last_update.strftime('%B %d, %Y at %H:%M')}")

# Sidebar
st.sidebar.markdown("## Filters")

date_range = st.sidebar.date_input(
    "Date Range",
    value=(df['Timestamp'].min().date(), df['Timestamp'].max().date()),
    min_value=df['Timestamp'].min().date(),
    max_value=df['Timestamp'].max().date()
)

side_filter = st.sidebar.multiselect(
    "Direction",
    options=['ALL'] + list(df['Side'].unique()),
    default=['ALL']
)

result_filter = st.sidebar.multiselect(
    "Status",
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

# Key metrics
st.markdown("## Performance Overview")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Win Rate", f"{win_rate:.1f}%", f"{wins}W / {losses}L")

with col2:
    st.metric("Avg P&L", f"{avg_pnl:.2f}%", f"Total: {total_pnl:.2f}%")

with col3:
    st.metric("Total Signals", f"{total_signals:,}", f"Completed: {completed_count}")

with col4:
    st.metric("Pending", f"{pending_count:,}", f"{(pending_count/total_signals*100):.1f}%" if total_signals > 0 else "0%")

with col5:
    st.metric("Expired", f"{expired_count:,}", f"{(expired_count/total_signals*100):.1f}%" if total_signals > 0 else "0%")

st.markdown("---")

# Charts
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("## Results Distribution")
    result_counts = df_filtered['Result'].value_counts()
    
    fig_results = go.Figure(data=[go.Pie(
        labels=result_counts.index,
        values=result_counts.values,
        hole=0.5,
        marker=dict(
            colors=['#3B82F6', '#10B981', '#EF4444', '#F59E0B', '#8B5CF6'],
            line=dict(color='#0B1120', width=2)
        ),
        textfont=dict(size=13, color='white', family='Inter'),
        textposition='outside',
        textinfo='label+percent'
    )])
    
    fig_results.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#CBD5E1', family='Inter', size=12),
        margin=dict(t=20, b=20, l=20, r=20),
        height=320
    )
    
    st.plotly_chart(fig_results, use_container_width=True)

with col2:
    st.markdown("## Long vs Short")
    side_stats = df_filtered.groupby('Side').agg({
        'Result': 'count',
        'P&L_%': 'mean'
    }).reset_index()
    side_stats.columns = ['Side', 'Count', 'Avg_PnL']
    
    fig_side = go.Figure()
    
    fig_side.add_trace(go.Bar(
        x=side_stats['Side'],
        y=side_stats['Count'],
        name='Signal Count',
        marker=dict(color='#3B82F6', line=dict(color='#0B1120', width=1)),
        text=side_stats['Count'],
        textposition='outside',
        yaxis='y'
    ))
    
    fig_side.add_trace(go.Scatter(
        x=side_stats['Side'],
        y=side_stats['Avg_PnL'],
        name='Avg P&L %',
        mode='lines+markers',
        marker=dict(size=10, color='#10B981'),
        line=dict(width=2, color='#10B981'),
        yaxis='y2'
    ))
    
    fig_side.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#CBD5E1', family='Inter', size=12),
        yaxis=dict(
            title='Count',
            gridcolor='rgba(148, 163, 184, 0.1)',
            title_font=dict(size=11)
        ),
        yaxis2=dict(
            title='Avg P&L %',
            overlaying='y',
            side='right',
            gridcolor='rgba(148, 163, 184, 0.05)',
            title_font=dict(size=11)
        ),
        hovermode='x unified',
        margin=dict(t=20, b=20, l=20, r=20),
        height=320,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            bgcolor='rgba(0,0,0,0)',
            font=dict(size=11)
        )
    )
    
    st.plotly_chart(fig_side, use_container_width=True)

st.markdown("---")

# Performance timeline
st.markdown("## Cumulative Performance")
if not completed_signals.empty:
    daily_pnl = completed_signals.groupby(completed_signals['Check_Date'].dt.date)['P&L_%'].sum().reset_index()
    daily_pnl.columns = ['Date', 'PnL']
    daily_pnl['Cumulative'] = daily_pnl['PnL'].cumsum()
    
    fig_timeline = go.Figure()
    
    colors = ['#10B981' if x >= 0 else '#EF4444' for x in daily_pnl['Cumulative']]
    
    fig_timeline.add_trace(go.Scatter(
        x=daily_pnl['Date'],
        y=daily_pnl['Cumulative'],
        mode='lines',
        fill='tozeroy',
        line=dict(color='#3B82F6', width=2),
        fillcolor='rgba(59, 130, 246, 0.1)',
        name='Cumulative P&L'
    ))
    
    fig_timeline.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#CBD5E1', family='Inter', size=12),
        xaxis=dict(
            gridcolor='rgba(148, 163, 184, 0.1)',
            title_font=dict(size=11)
        ),
        yaxis=dict(
            title='Cumulative P&L %',
            gridcolor='rgba(148, 163, 184, 0.1)',
            zeroline=True,
            zerolinecolor='rgba(148, 163, 184, 0.3)',
            zerolinewidth=1,
            title_font=dict(size=11)
        ),
        margin=dict(t=20, b=20, l=20, r=20),
        height=320,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)
else:
    st.info("No completed signals to display")

st.markdown("---")

# Top performers
col1, col2 = st.columns(2)

with col1:
    st.markdown("## Top Winners")
    if not completed_signals.empty:
        top_winners = completed_signals.nlargest(8, 'P&L_%')[['Timestamp', 'Symbol', 'Side', 'P&L_%']]
        top_winners['Timestamp'] = top_winners['Timestamp'].dt.strftime('%b %d, %H:%M')
        top_winners['P&L_%'] = top_winners['P&L_%'].apply(lambda x: f"{x:+.2f}%")
        st.dataframe(top_winners, use_container_width=True, hide_index=True, height=320)

with col2:
    st.markdown("## Top Losers")
    if not completed_signals.empty:
        top_losers = completed_signals.nsmallest(8, 'P&L_%')[['Timestamp', 'Symbol', 'Side', 'P&L_%']]
        top_losers['Timestamp'] = top_losers['Timestamp'].dt.strftime('%b %d, %H:%M')
        top_losers['P&L_%'] = top_losers['P&L_%'].apply(lambda x: f"{x:+.2f}%")
        st.dataframe(top_losers, use_container_width=True, hide_index=True, height=320)

st.markdown("---")

# Symbol performance
st.markdown("## Top Performing Symbols")
if not completed_signals.empty:
    symbol_stats = completed_signals.groupby('Symbol').agg({
        'P&L_%': ['sum', 'count'],
        'Result': lambda x: (x.isin(['TP1_HIT', 'TP2_HIT'])).sum()
    }).reset_index()
    
    symbol_stats.columns = ['Symbol', 'Total_PnL', 'Count', 'Wins']
    symbol_stats['Win_Rate'] = (symbol_stats['Wins'] / symbol_stats['Count'] * 100).round(1)
    symbol_stats = symbol_stats.sort_values('Total_PnL', ascending=False).head(12)
    
    colors = ['#10B981' if x > 0 else '#EF4444' for x in symbol_stats['Total_PnL']]
    
    fig_symbols = go.Figure()
    
    fig_symbols.add_trace(go.Bar(
        x=symbol_stats['Symbol'],
        y=symbol_stats['Total_PnL'],
        marker=dict(color=colors, line=dict(color='#0B1120', width=1)),
        text=symbol_stats['Win_Rate'].apply(lambda x: f"{x}%"),
        textposition='outside',
        textfont=dict(size=11),
        hovertemplate='<b>%{x}</b><br>Total P&L: %{y:.2f}%<br>Win Rate: %{text}<extra></extra>'
    ))
    
    fig_symbols.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#CBD5E1', family='Inter', size=12),
        xaxis=dict(gridcolor='rgba(148, 163, 184, 0.1)'),
        yaxis=dict(
            title='Total P&L %',
            gridcolor='rgba(148, 163, 184, 0.1)',
            zeroline=True,
            zerolinecolor='rgba(148, 163, 184, 0.3)',
            zerolinewidth=1,
            title_font=dict(size=11)
        ),
        margin=dict(t=40, b=20, l=20, r=20),
        height=360,
        showlegend=False
    )
    
    st.plotly_chart(fig_symbols, use_container_width=True)

st.markdown("---")

# Recent signals
st.markdown("## Recent Signals")
recent = df_filtered.sort_values('Timestamp', ascending=False).head(15)
recent_display = recent[['Timestamp', 'Symbol', 'Side', 'Entry', 'TP1', 'Confidence', 'Result', 'P&L_%']].copy()
recent_display['Timestamp'] = recent_display['Timestamp'].dt.strftime('%b %d, %H:%M')
recent_display['P&L_%'] = recent_display['P&L_%'].apply(lambda x: f"{x:+.2f}%" if pd.notna(x) else "—")
recent_display['Confidence'] = recent_display['Confidence'].apply(lambda x: f"{x:.0f}%" if pd.notna(x) else "—")
st.dataframe(recent_display, use_container_width=True, hide_index=True, height=400)

# Sidebar quick stats
st.sidebar.markdown("---")
st.sidebar.markdown("## Quick Stats")

if not completed_signals.empty:
    best_symbol = completed_signals.groupby('Symbol')['P&L_%'].sum().idxmax()
    best_pnl = completed_signals.groupby('Symbol')['P&L_%'].sum().max()
    st.sidebar.metric("Best Performer", best_symbol, f"{best_pnl:+.2f}%")

if st.sidebar.button("Refresh Data"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("Data refreshes every 5 minutes")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #64748B; font-size: 0.875rem;'>Built by FlowBot Automation</p>",
    unsafe_allow_html=True
)
