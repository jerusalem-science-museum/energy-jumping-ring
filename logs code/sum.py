import pandas as pd
import matplotlib.pyplot as plt
import re
from datetime import datetime

def analyze_jumping_ring_log(file_path):
    # הגדרות משתנים
    data = []
    language_counts = {'hebrew': 0, 'english': 0, 'arabic': 0}
    language_changes = 0
    disconnections = 0
    
    # ביטויים רגולריים לחילוץ מידע
    ring_pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - Ring jumped! voltage: ([\d.]+) -> ([\d.]+)')
    lang_pattern = re.compile(r'your language is: (\w+)')
    conn_pattern = re.compile(r'Connected to /dev/ttyUSB0')

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # זיהוי קפיצות
            ring_match = ring_pattern.search(line)
            if ring_match:
                timestamp = datetime.strptime(ring_match.group(1), '%Y-%m-%d %H:%M:%S')
                v_start = float(ring_match.group(2))
                v_end = float(ring_match.group(3))
                data.append({'time': timestamp, 'v_start': v_start, 'v_end': v_end})
            
            # זיהוי שפות
            lang_match = lang_pattern.search(line)
            if lang_match:
                lang = lang_match.group(1)
                if lang in language_counts:
                    language_counts[lang] += 1
                    language_changes += 1
            
            # זיהוי ניתוקים
            if conn_pattern.search(line):
                disconnections += 1

    df = pd.DataFrame(data)
    if df.empty:
        print("לא נמצאו נתונים בקובץ.")
        return

    # חישובים סטטיסטיים
    days = (df['time'].max() - df['time'].min()).days + 1
    total_jumps = len(df)
    good_runs = len(df[df['v_start'] > 300])
    
    # יצירת קובץ Summary
    summary_text = f"""Summary for {file_path}
Log data time range: {df['time'].min()} to {df['time'].max()} ({days} days)

Total Ring jumped!: {total_jumps}
Total english language: {language_counts['english']}
Total hebrew language: {language_counts['hebrew']}
Total arabic language: {language_counts['arabic']}
Total language changes: {language_changes}

Average Ring jumped! per day: {total_jumps/days:.2f}
Average total language changes per day: {language_changes/days:.2f}

Good runs (>300V): {good_runs} / {total_jumps} ({(good_runs/total_jumps)*100:.2f}%)

---
Arduino disconnections: {disconnections}
"""
    
    with open('Jumping_Ring_Summary_Auto.txt', 'w', encoding='utf-8') as f:
        f.write(summary_text)
    print("קובץ Summary נוצר בהצלחה.")

    # יצירת הגרף (Plot)
    plt.figure(figsize=(12, 6))
    plt.scatter(df['time'], df['v_start'], alpha=0.5, s=10, label='Jump Voltage (V)')
    plt.axhline(y=300, color='r', linestyle='--', label='Threshold (300V)')
    plt.title('Jumping Ring - Voltage over Time')
    plt.xlabel('Date')
    plt.ylabel('Voltage (V)')
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig('Jumping_Ring_Plot_Auto.png')
    print("קובץ Plot נוצר בהצלחה.")

# הרצה (שנה את שם הקובץ לשם הקובץ שלך)
analyze_jumping_ring_log('log_2026-03-18_to_2026-04-21.txt')