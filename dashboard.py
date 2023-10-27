import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

hour_df = pd.read_csv('./dashboard/hour_df.csv')
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

day_df = pd.read_csv('./dashboard/day_df.csv')
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

def create_lastday_df(df):
    data = df[df['dteday'] == df['dteday'].max()].groupby(by='hr').agg({
        'dteday': 'first',
        'casual': 'sum',
        'registered': 'sum',
        'cnt': 'sum',
        'temp': 'first',
        'windspeed': 'first',
        'hum': 'first',
        'weather_type': 'first',
        'season_name': 'first'
    }).reset_index()
    data['dteday'] = data['dteday'].dt.strftime('%d %B %Y')
    return data

def get_weather_image(weather, season):
    if weather == 'mist':
        return './dashboard/image/fog.png'
    elif weather == 'clear':
        return './dashboard/image/sun.png'
    elif (weather == 'light rain/snow') & (season == 'winter'):
        return './dashboard/image/snow.png'
    elif weather == 'light rain/snow':
        return './dashboard/image/heavy-rain.png'
    else:
        return './dashboard/image/rain.png'

min_date = hour_df['dteday'].min()
max_date = hour_df['dteday'].max()

with st.sidebar:
    st.image('./dashboard/image/bicycle.png')
    select_date = st.date_input(
        label='Pilih tanggal',
        min_value=min_date,
        max_value=max_date,
        value=min_date
    )

def main_df(df):
    return df[df['dteday'] <= str(select_date)]


# print(main_df(day_df))

st.header('Bike Sharing Dataset')

st.subheader('Daily Report')

lastday_data = create_lastday_df(main_df(hour_df))
print(day_df[day_df['weather_type'] == 'light rain/snow'])

col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])

# print('ini data last day ================\n', lastday_data)
weather = lastday_data['weather_type'].mode().values[0]
season = lastday_data['season_name'].mode().values[0]
print('ini weather ============>>>>>>> ',weather, season)

with col1:
    st.text('Date')
    st.metric(select_date.strftime('%A'), value=select_date.strftime('%d %B %Y'))
    # st.subheader(select_date.strftime('%a, %d %B %Y'))
with col2:
    st.text('Weather*')
    st.image(get_weather_image(weather, season), width=55, caption=(f"{lastday_data['temp'].mean().round(2)}°C"))
with col3:
    st.text('Season')
    st.image('./dashboard/image/season.png', width=55, caption=lastday_data['season_name'].mode().values[0])
with col4:
    st.text('Windspeed*')
    st.image('./dashboard/image/windy.png', width=55, caption=(f"{lastday_data['windspeed'].mean().round(2)} knot"))
with col5:
    st.text('Humidity*')
    st.image('./dashboard/image/humidity.png', width=55, caption=(f"{lastday_data['hum'].mean().round(2)} %"))
    st.caption('\* average')


fig, ax = plt.subplots(figsize=(11, 4))

ax.plot(lastday_data['hr'], lastday_data['casual'], label='casual user')
ax.plot(lastday_data['hr'], lastday_data['registered'], label='registered user')
ax.set_title('Daily User per Hour', loc='center', fontsize=20)
ax.set_xticks(lastday_data['hr'])
ax.legend()

st.pyplot(fig)

col0, col1, col2, col3, col4 = st.columns([1, 1, 1, 1, 1])
with col0:
    st.image('./dashboard/image/user.png', width=70)
with col1:
    casual_user = lastday_data['casual'].sum()
    st.metric('Casual', value=casual_user)
with col2:
    regist_user = lastday_data['registered'].sum()
    st.metric('Registered', value=regist_user)
with col3:
    total_user = lastday_data['cnt'].sum()
    st.metric('Total User', value=total_user)
with col4:
    ave_user = lastday_data['cnt'].mean().round()
    st.metric('Average User', value=ave_user)

st.subheader('\nWeekly Report')
st.write('')

def create_lastweek_df(df):
    data = df.sort_values(by='dteday')
    lastweek_data = data.tail(7)
    lastweek_data['dteday'] = lastweek_data['dteday'].dt.strftime('%a, %d %b')
    return lastweek_data

lastweek_data = create_lastweek_df(main_df(day_df))

col0, col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 3, 1, 3, 1, 3])

with col1:
    st.image('./dashboard/image/thermometer.png', width=50)
with col2:
    st.subheader(f"{lastweek_data.temp.mean().round(1)}°C")
    # st.text('Temp*')
with col3:
    st.image('./dashboard/image/windy.png', width=50)
with col4:
    st.subheader(f"{lastweek_data.windspeed.mean().round(1)} Knot")
    # st.text('Windspeed*')
with col5:
    st.image('./dashboard/image/humidity.png', width=50)
with col6:
    st.subheader(f"{lastweek_data.hum.mean().round(1)}%")
    # st.text('Humidity*')
st.caption('\* average')


fig, ax = plt.subplots(figsize=(11, 4))

ax.plot(lastweek_data['dteday'], lastweek_data['casual'], label='casual user')
ax.plot(lastweek_data['dteday'], lastweek_data['registered'], label='registered user')
ax.set_title('Last 7 Days User ', loc='center', fontsize=20)
ax.set_xticks(lastweek_data['dteday'])
ax.legend()

st.pyplot(fig)

col0, col1, col2, col3, col4 = st.columns([1, 1, 1, 1, 1])
with col0:
    st.image('./dashboard/image/user.png', width=70)
with col1:
    casual_user = lastweek_data['casual'].sum()
    st.metric('Casual', value=casual_user)
with col2:
    regist_user = lastweek_data['registered'].sum()
    st.metric('Registered', value=regist_user)
with col3:
    total_user = lastweek_data['cnt'].sum()
    st.metric('Total User', value=total_user)
with col4:
    ave_user = lastweek_data['cnt'].mean().round()
    st.metric('Average User', value=ave_user)

st.subheader('Monthly Report')

def create_lastmonth_df(df):
    data = df.sort_values(by='dteday')
    lastmonth_data = data.tail(30)
    lastmonth_data['dteday'] = lastmonth_data['dteday'].dt.strftime('%d')
    return lastmonth_data

lastmonth_data = create_lastmonth_df(main_df(day_df))

col0, col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 3, 1, 3, 1, 3])

with col1:
    st.image('./dashboard/image/thermometer.png', width=50)
with col2:
    st.subheader(f"{lastmonth_data.temp.mean().round(1)}°C")
    # st.text('Temp*')
with col3:
    st.image('./dashboard/image/windy.png', width=50)
with col4:
    st.subheader(f"{lastmonth_data.windspeed.mean().round(1)} Knot")
    # st.text('Windspeed*')
with col5:
    st.image('./dashboard/image/humidity.png', width=50)
with col6:
    st.subheader(f"{lastmonth_data.hum.mean().round(1)}%")
    # st.text('Humidity*')
st.caption('\* average')


fig, ax = plt.subplots(figsize=(11, 4))

ax.plot(lastmonth_data['dteday'], lastmonth_data['casual'], label='casual user')
ax.plot(lastmonth_data['dteday'], lastmonth_data['registered'], label='registered user')
ax.set_title('Last 30 Days User ', loc='center', fontsize=20)
ax.set_xticks(lastmonth_data['dteday'])
ax.legend()

st.pyplot(fig)

col0, col1, col2, col3, col4 = st.columns([1, 1, 1, 1, 1])
with col0:
    st.image('./dashboard/image/user.png', width=70)
with col1:
    casual_user = lastmonth_data['casual'].sum()
    st.metric('Casual', value=casual_user)
with col2:
    regist_user = lastmonth_data['registered'].sum()
    st.metric('Registered', value=regist_user)
with col3:
    total_user = lastmonth_data['cnt'].sum()
    st.metric('Total User', value=total_user)
with col4:
    ave_user = lastmonth_data['cnt'].mean().round()
    st.metric('Average User', value=ave_user)
