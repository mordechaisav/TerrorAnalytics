from flask import Blueprint, render_template_string
import folium

from api_queries.service import regions_max_diff, get_marker_color

regions_max_diff_bp = Blueprint('regions_max_diff', __name__)

@regions_max_diff_bp.route('/regions_diff_map', methods=['GET'])
def regions_diff_map():
    regions = regions_max_diff()

    map = folium.Map(location=[31.7683, 35.2137], zoom_start=7)

    for region in regions:
        if "lat" in region and "lon" in region:
            popup_html = f"""
                <div style="font-family: Arial, sans-serif; color: #333;">
                    <h3 style="color: #0073e6; text-align: center;">{region['region_name']} Information</h3>
                    <ul style="list-style-type: none; padding: 0;">
                        <li style="padding: 8px; border-bottom: 1px solid #ddd;">
                            <strong style="color: #333;">Percentage Change</strong>: <span style="color: #0073e6;">{region['percentage_change']}%</span>
                        </li>
                    </ul>
                </div>
            """
            marker_color = get_marker_color(region["percentage_change"])
            folium.Marker([region["lat"], region["lon"]],
                          popup=folium.Popup(popup_html, max_width=300),
                          icon=folium.Icon(color=marker_color)).add_to(map)
    map_html = map._repr_html_()

    return render_template_string('''
       <html>
           <body>
               <h1>Regions Percentage Change Map</h1>
               {{ map_html|safe }}
           </body>
       </html>
   ''', map_html=map_html)
