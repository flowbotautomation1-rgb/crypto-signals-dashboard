# 🚀 Crypto Signals Dashboard

דשבורד אנליטיקס מתקדם לניטור ביצועי בוט הטריידינג שלך!

## 📊 מה הדשבורד כולל?

### מטריקות מרכזיות:
- **Win Rate** - אחוז הצלחה של הסיגנלים
- **Average P&L** - רווח/הפסד ממוצע לסיגנל
- **Total P&L** - רווח כולל מצטבר
- **סיגנלים פעילים/ממתינים/פג תוקף**

### ויזואליזציות:
1. **התפלגות תוצאות** - Pie chart של סטטוסים
2. **LONG vs SHORT** - השוואת ביצועים
3. **Cumulative P&L** - גרף רווח מצטבר לאורך זמן
4. **Top Winners & Losers** - 10 הסיגנלים הכי טובים והכי גרועים
5. **ביצועים לפי מטבע** - איזה מטבעות הכי רווחיים
6. **ביצועים לפי Confidence** - האם רמת ביטחון משפיעה על הצלחה

### פילטרים:
- טווח תאריכים
- כיוון (LONG/SHORT)
- תוצאה (TP1/TP2/SL/PENDING/EXPIRED)

## 🚀 איך להריץ?

### אופציה 1: הרצה מקומית

```bash
# התקן את הספריות הנדרשות
pip install streamlit pandas plotly

# הרץ את הדשבורד
streamlit run crypto_dashboard.py
```

הדשבורד יפתח בדפדפן בכתובת: `http://localhost:8501`

### אופציה 2: הרצה עם קובץ CSV מקומי

אם הקובץ CSV שלך לא בנתיב `/mnt/user-data/uploads/Signals_Log_-_Sheet1.csv`, 
פשוט שנה בשורה 51 של `crypto_dashboard.py`:

```python
df = pd.read_csv('path/to/your/signals.csv')  # שנה לנתיב שלך
```

### אופציה 3: חיבור ישיר לגוגל שיטס

אם אתה רוצה לחבר ישירות לגוגל שיטס במקום CSV, תצטרך להוסיף:

```bash
pip install gspread oauth2client
```

ואז לשנות את פונקציית `load_data()` לקריאה מגוגל שיטס.

## 🔄 עדכון אוטומטי

הדשבורד כולל cache כך שהוא לא טוען את הדאטה בכל פעם מחדש.
יש כפתור "Refresh Data" בסיידבר לעדכון ידני.

אם תרצה לרענן אוטומטית כל X זמן, אפשר להוסיף:

```python
import time

# בתחילת הקובץ
st_autorefresh = st_autorefresh(interval=300000, key="dataframerefresh")  # 5 דקות
```

## 📱 פריסה לאינטרנט

אם אתה רוצה לפרסם את הדשבורד באינטרנט:

### Streamlit Community Cloud (חינם):
1. עלה את הקוד ל-GitHub
2. התחבר ל-Streamlit Cloud
3. פרסם את האפליקציה

### Heroku / Railway / Render:
כולם תומכים בסטרימליט, פשוט צריך:
- `requirements.txt` עם הספריות
- `Procfile` עם פקודת ההרצה

## 🎨 התאמה אישית

אתה יכול לשנות:
- צבעים בקטע ה-CSS
- סוגי גרפים (יש המון אופציות ב-Plotly)
- מטריקות נוספות
- פילטרים נוספים

## 🔧 טיפים

1. **ביצועים**: אם יש לך אלפי סיגנלים, כדאי להוסיף פילטר של "חודש אחרון" כברירת מחדל
2. **גוגל שיטס**: אם הדאטה בשיטס, תוכל לסנכרן אוטומטית כל X דקות
3. **התראות**: אפשר להוסיף התראות טלגרם על Win Rate נמוך או P&L שלילי

## 💡 רעיונות לשיפורים עתידיים

- [ ] תחזית ML של סיגנלים עתידיים
- [ ] השוואה לביצועי השוק (BTC benchmark)
- [ ] דוחות PDF אוטומטיים
- [ ] התראות בזמן אמת
- [ ] A/B testing של אסטרטגיות שונות
- [ ] ניתוח עמוק של אינדיקטורים (RSI, MACD וכו')

---

**Made with ❤️ by FlowBot Automation**

אם יש לך שאלות או רעיונות לשיפורים, תמיד אפשר לפנות!
