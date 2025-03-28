import re
import pandas as pd

def preprocess(data):
    # "1/7/25, 10:40 am -" set its regular expression on pattern variable
    pattern = '\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[ap]m\s-'
    # pattern(regular expression) er upor base kore data k dui vage vag kore dewa
    message = re.split(pattern, data)[1:]
    # find all string which is follow pattern(here it is date) and store it on dates
    dates = re.findall(pattern, data)
    # create a dataframe where message and date has ploted
    df = pd.DataFrame({'user_message': message, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M\u202f%p -')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # seperate users and messages
    user = []
    message = []

    for msg in df['user_message']:
        conversation = re.split('([\w\W]+?):\s', msg)  # ^[A-Za-z\s]+:|^\+\d+: learn letter about it
        if conversation[1:]:  # user name
            user.append(conversation[1])
            message.append(conversation[2])
        else:
            user.append('group_notification')
            message.append(conversation[0])
    df.drop(columns=['user_message'], inplace=True)
    df['user'] = user
    df['message'] = message
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    # df['day'] = df['date'].dt.day_name() # we can create also date name
    df['only_date'] = df['date'].dt.date
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period


    return df

