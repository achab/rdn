import folium
import pandas as pd


# load data
df = pd.read_csv('radiologues.csv', sep=';')

# create map
m = folium.Map(
    location=[df['latitude'].mean(), df['longitude'].mean()],
    tiles='cartodbpositron',
    zoom_start=13
)

# create objects to fill map
html = """
    <p>
    Title = {title}
    </p>
    <p>
    Subtitle = {subtitle}
    </p>
    <p>
    Number = {n_doctors}
    </p>
    <p>
    Sector = {sector}
    </p>
    <p>
    Address = {address}
    </p>
"""
locations = list(df[['latitude', 'longitude']].to_numpy())
titles = df['title'].to_list()
subtitles = df['subtitle'].to_list()
n_doctors = df['n_doctors'].to_list()
sectors = df['sector'].to_list()
addresses = df['address'].to_list()

# fill map
for k in range(len(df)):
    html_k = html.format(
        title=titles[k], 
        subtitle=subtitles[k], 
        n_doctors=n_doctors[k], 
        sector=sectors[k], 
        address=addresses[k]
    )
    iframe = folium.IFrame(html=html_k, width=300, height=250)
    popup = folium.Popup(iframe, max_width=2650)
    color = 'blue'
    folium.features.RegularPolygonMarker(
        locations[k],
        radius=5,
        popup=popup, 
        color=color,
        fill_color=color
    ).add_to(m)

m.save('map.html')
