import re
import pandas as pd

def preprocess(data):
    # Universal WhatsApp regex (Android + iPhone + 12/24 hr)
    pattern = r'(\[?\d{1,2}[\/\.\-]\d{1,2}[\/\.\-]\d{2,4},\s\d{1,2}:\d{2}(?:\s?[APMapm]{2})?\]?)\s[-\]]\s'

    split_data = re.split(pattern, data)[1:]

    dates = []
    users = []
    messages = []

    # Loop through date + message pairs
    for i in range(0, len(split_data), 2):
        date = split_data[i]
        msg_block = split_data[i+1].strip()

        # Detect user : message
        if ": " in msg_block:
            user, msg = msg_block.split(": ", 1)
        else:
            user = "group_notification"
            msg = msg_block

        dates.append(date)
        users.append(user)
        messages.append(msg)

    df = pd.DataFrame({
        "date_raw": dates,
        "user": users,
        "message": messages
    })

    # Flexible date parsing
    df["date"] = pd.to_datetime(df["date_raw"].str.replace('[\[\]]', '', regex=True),
                                errors="coerce",
                                dayfirst=True)

    # Extract features
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Time period range
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append("23-00")
        elif hour == 0:
            period.append("00-01")
        else:
            period.append(f"{hour:02}-{hour+1:02}")

    df["period"] = period

    return df
