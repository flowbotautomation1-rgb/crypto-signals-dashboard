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

# CSS מותאם אישית
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# טעינת הדאטה - תומך בשתי שיטות
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_data():
    """
    טוען דאטה מגוגל שיטס או מקובץ CSV מקומי
    """
    try:
        # נסיון לטעון מגוגל שיטס
        sheet_url = st.secrets.get("GOOGLE_SHEET_URL", None)
        
        if sheet_url:
            # המרת URL של שיטס לפורמט CSV
            if "/edit" in sheet_url:
                sheet_url = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")
                sheet_url = sheet_url.replace("/edit?usp=sharing", "/export?format=csv")
            
            df = pd.read_csv(sheet_url)
            st.sidebar.success("✅ מחובר לגוגל שיטס")
        else:
            # fallback לקובץ מקומי
            df = pd.read_csv('Signals_Log_-_Sheet1.csv')
            st.sidebar.info("📁 קורא מקובץ מקומי")
    
    except Exception as e:
        st.error(f"❌ שגיאה בטעינת הדאטה: {str(e)}")
        st.stop()
    
    # המרת תאריכים
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['Check_Date'] = pd.to_datetime(df['Check_Date'], errors='coerce')
    
    # ניקוי ערכים
    df['P&L_%'] = pd.to_numeric(df['P&L_%'], errors='coerce')
    df['Actual_RR'] = pd.to_numeric(df['Actual_RR'], errors='coerce')
    df['Confidence'] = pd.to_numeric(df['Confidence'], errors='coerce')
    
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"לא ניתן לטעון את הדאטה. בדוק את ההגדרות בקובץ secrets.toml")
    st.info("כדי להתחבר לגוגל שיטס, הוסף את ה-URL בקובץ .streamlit/secrets.toml")
    st.code("""
# .streamlit/secrets.toml
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit#gid=0"
    """)
    st.stop()

# כותרת ראשית
st.markdown('<h1 class="main-header">🚀 Crypto Trading Signals Dashboard</h1>', unsafe_allow_html=True)

# הצגת מידע על עדכון אחרון
last_update = df['Timestamp'].max()
st.sidebar.markdown(f"**🕐 עדכון אחרון:**  \n{last_update.strftime('%d/%m/%Y %H:%M')}")

# פילטרים בסיידבר
st.sidebar.header("⚙️ פילטרים")

# בחירת טווח תאריכים
date_range = st.sidebar.date_input(
    "בחר טווח תאריכים",
    value=(df['Timestamp'].min().date(), df['Timestamp'].max().date()),
    min_value=df['Timestamp'].min().date(),
    max_value=df['Timestamp'].max().date()
)

# פילטר לפי כיוון
side_filter = st.sidebar.multiselect(
    "כיוון",
    options=['ALL'] + list(df['Side'].unique()),
    default=['ALL']
)

# פילטר לפי תוצאה
result_filter = st.sidebar.multiselect(
    "תוצאה",
    options=['ALL'] + list(df['Result'].dropna().unique()),
    default=['ALL']
)

# החלת פילטרים
df_filtered = df.copy()

# פילטר תאריכים
if len(date_range) == 2:
    df_filtered = df_filtered[
        (df_filtered['Timestamp'].dt.date >= date_range[0]) & 
        (df_filtered['Timestamp'].dt.date <= date_range[1])
    ]

# פילטר כיוון
if 'ALL' not in side_filter and side_filter:
    df_filtered = df_filtered[df_filtered['Side'].isin(side_filter)]

# פילטר תוצאה
if 'ALL' not in result_filter and result_filter:
    df_filtered = df_filtered[df_filtered['Result'].isin(result_filter)]

# חישוב מטריקות
completed_signals = df_filtered[df_filtered['Result'].isin(['TP1_HIT', 'TP2_HIT', 'SL_HIT'])]
total_signals = len(df_filtered)
completed_count = len(completed_signals)
pending_count = len(df_filtered[df_filtered['Result'] == 'PENDING'])
expired_count = len(df_filtered[df_filtered['Result'] == 'EXPIRED'])

# Win Rate
wins = len(completed_signals[completed_signals['Result'].isin(['TP1_HIT', 'TP2_HIT'])])
losses = len(completed_signals[completed_signals['Result'] == 'SL_HIT'])
win_rate = (wins / completed_count * 100) if completed_count > 0 else 0

# Average P&L
avg_pnl = completed_signals['P&L_%'].mean() if not completed_signals.empty else 0
total_pnl = completed_signals['P&L_%'].sum() if not completed_signals.empty else 0

# מטריקות עיקריות
st.markdown("### 📊 סטטיסטיקות כלליות")
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

# שורה שנייה של גרפים
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 התפלגות תוצאות")
    result_counts = df_filtered['Result'].value_counts()
    fig_results = px.pie(
        values=result_counts.values,
        names=result_counts.index,
        title="התפלגות סטטוסים",
        color_discrete_sequence=px.colors.qualitative.Set3,
        hole=0.4
    )
    fig_results.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_results, use_container_width=True)

with col2:
    st.markdown("### 📈 LONG vs SHORT")
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
        yaxis='y',
        marker_color='lightblue'
    ))
    fig_side.add_trace(go.Scatter(
        name='Avg P&L %',
        x=side_stats['Side'],
        y=side_stats['Avg_PnL'],
        yaxis='y2',
        mode='lines+markers',
        marker=dict(size=12, color='red'),
        line=dict(width=3)
    ))
    
    fig_side.update_layout(
        title='LONG vs SHORT Performance',
        yaxis=dict(title='Count'),
        yaxis2=dict(title='Avg P&L %', overlaying='y', side='right'),
        hovermode='x'
    )
    st.plotly_chart(fig_side, use_container_width=True)

st.divider()

# ביצועים לאורך זמן
st.markdown("### 📅 ביצועים לאורך זמן")
if not completed_signals.empty:
    daily_pnl = completed_signals.groupby(completed_signals['Check_Date'].dt.date)['P&L_%'].agg(['sum', 'mean', 'count']).reset_index()
    daily_pnl.columns = ['Date', 'Total_PnL', 'Avg_PnL', 'Count']
    daily_pnl['Cumulative_PnL'] = daily_pnl['Total_PnL'].cumsum()
    
    fig_timeline = go.Figure()
    
    fig_timeline.add_trace(go.Scatter(
        x=daily_pnl['Date'],
        y=daily_pnl['Cumulative_PnL'],
        mode='lines+markers',
        name='Cumulative P&L',
        line=dict(color='green', width=3),
        fill='tozeroy'
    ))
    
    fig_timeline.update_layout(
        title='Cumulative P&L Over Time',
        xaxis_title='Date',
        yaxis_title='Cumulative P&L %',
        hovermode='x unified'
    )
    st.plotly_chart(fig_timeline, use_container_width=True)
else:
    st.info("אין עדיין סיגנלים שהושלמו להצגת גרף זמן")

st.divider()

# Top Performers
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏆 Top 10 Winners")
    if not completed_signals.empty:
        top_winners = completed_signals.nlargest(10, 'P&L_%')[['Timestamp', 'Symbol', 'Side', 'Entry', 'P&L_%', 'Result']]
        top_winners['Timestamp'] = top_winners['Timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        st.dataframe(
            top_winners,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("אין עדיין נתונים")

with col2:
    st.markdown("### ⚠️ Top 10 Losers")
    if not completed_signals.empty:
        top_losers = completed_signals.nsmallest(10, 'P&L_%')[['Timestamp', 'Symbol', 'Side', 'Entry', 'P&L_%', 'Result']]
        top_losers['Timestamp'] = top_losers['Timestamp'].dt.strftime('%Y-%m-%d %H:%M')
        st.dataframe(
            top_losers,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("אין עדיין נתונים")

st.divider()

# ניתוח לפי מטבע
st.markdown("### 💎 ביצועים לפי מטבע")
if not completed_signals.empty:
    symbol_stats = completed_signals.groupby('Symbol').agg({
        'P&L_%': ['mean', 'sum', 'count'],
        'Result': lambda x: (x.isin(['TP1_HIT', 'TP2_HIT'])).sum()
    }).reset_index()
    
    symbol_stats.columns = ['Symbol', 'Avg_PnL', 'Total_PnL', 'Count', 'Wins']
    symbol_stats['Win_Rate'] = (symbol_stats['Wins'] / symbol_stats['Count'] * 100).round(1)
    symbol_stats = symbol_stats.sort_values('Total_PnL', ascending=False).head(15)
    
    fig_symbols = px.bar(
        symbol_stats,
        x='Symbol',
        y='Total_PnL',
        color='Win_Rate',
        title='Top 15 Symbols by Total P&L',
        labels={'Total_PnL': 'Total P&L %', 'Win_Rate': 'Win Rate %'},
        color_continuous_scale='RdYlGn',
        text='Win_Rate'
    )
    fig_symbols.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    st.plotly_chart(fig_symbols, use_container_width=True)
    
    st.dataframe(
        symbol_stats.sort_values('Win_Rate', ascending=False),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("אין עדיין נתונים מספיקים לניתוח לפי מטבע")

st.divider()

# ניתוח Confidence
st.markdown("### 🎯 ביצועים לפי רמת Confidence")
if not completed_signals.empty:
    confidence_bins = [0, 60, 70, 80, 90, 100]
    confidence_labels = ['50-60', '60-70', '70-80', '80-90', '90-100']
    completed_signals['Confidence_Range'] = pd.cut(
        completed_signals['Confidence'],
        bins=confidence_bins,
        labels=confidence_labels,
        include_lowest=True
    )
    
    confidence_stats = completed_signals.groupby('Confidence_Range').agg({
        'P&L_%': ['mean', 'count'],
        'Result': lambda x: (x.isin(['TP1_HIT', 'TP2_HIT'])).sum()
    }).reset_index()
    
    confidence_stats.columns = ['Confidence_Range', 'Avg_PnL', 'Count', 'Wins']
    confidence_stats['Win_Rate'] = (confidence_stats['Wins'] / confidence_stats['Count'] * 100).round(1)
    
    fig_confidence = px.scatter(
        confidence_stats,
        x='Confidence_Range',
        y='Win_Rate',
        size='Count',
        color='Avg_PnL',
        title='Win Rate vs Confidence Level',
        labels={'Win_Rate': 'Win Rate %', 'Confidence_Range': 'Confidence Range'},
        color_continuous_scale='RdYlGn'
    )
    st.plotly_chart(fig_confidence, use_container_width=True)
else:
    st.info("אין עדיין נתונים לניתוח Confidence")

st.divider()

# סיגנלים אחרונים
st.markdown("### 🔄 סיגנלים אחרונים (20)")
recent_signals = df_filtered.sort_values('Timestamp', ascending=False).head(20)
recent_signals_display = recent_signals[[
    'Timestamp', 'Symbol', 'Side', 'Entry', 'SL', 'TP1', 'TP2',
    'Confidence', 'Result', 'P&L_%', 'Check_Date'
]].copy()

recent_signals_display['Timestamp'] = recent_signals_display['Timestamp'].dt.strftime('%Y-%m-%d %H:%M')
recent_signals_display['Check_Date'] = recent_signals_display['Check_Date'].dt.strftime('%Y-%m-%d %H:%M')

st.dataframe(
    recent_signals_display,
    use_container_width=True,
    hide_index=True
)

# סטטיסטיקות נוספות בסיידבר
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Quick Stats")
st.sidebar.metric("Best Symbol", 
                 completed_signals.groupby('Symbol')['P&L_%'].sum().idxmax() if not completed_signals.empty else "N/A",
                 f"{completed_signals.groupby('Symbol')['P&L_%'].sum().max():.2f}%" if not completed_signals.empty else "0%")
st.sidebar.metric("Worst Symbol", 
                 completed_signals.groupby('Symbol')['P&L_%'].sum().idxmin() if not completed_signals.empty else "N/A",
                 f"{completed_signals.groupby('Symbol')['P&L_%'].sum().min():.2f}%" if not completed_signals.empty else "0%")

# הוספת refresh button
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# מידע על עדכון
st.sidebar.markdown("---")
st.sidebar.info("הדאטה מתעדכן אוטומטית כל 5 דקות")

# פוטר
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Made with ❤️ by FlowBot Automation | Data syncs every 4 hours from n8n bot</div>",
    unsafe_allow_html=True
)
