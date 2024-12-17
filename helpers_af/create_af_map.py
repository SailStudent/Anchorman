from staticmap import StaticMap, CircleMarker

def create_map(lat1, lon1, zoom=12):
    m = StaticMap(800, 600, url_template='https://a.tile.osm.org/{z}/{x}/{y}.png')

    m.add_marker(CircleMarker((lon1, lat1), 'green', 24))

    image = m.render(zoom=zoom)
    image.save(".output/map.png")
    return ".output/map.png"

def create_map_two_cities(lat1, lon1, lat2, lon2):
    m = StaticMap(800, 600, url_template='https://a.tile.osm.org/{z}/{x}/{y}.png')

    m.add_marker(CircleMarker((lon1, lat1), 'green', 24))
    m.add_marker(CircleMarker((lon2, lat2), 'gold', 24))

    image = m.render()
    image.save(".output/map.png")
    return ".output/map.png"
