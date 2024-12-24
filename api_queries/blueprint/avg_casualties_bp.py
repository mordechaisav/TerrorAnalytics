from api_queries.service import regions_severity_locations, get_marker_color
from flask import Blueprint, render_template_string, request
import folium
regions_severity_locations_bp = Blueprint('regions_severity_locations', __name__)

@regions_severity_locations_bp.route('/regions_map', methods=['GET'])
def regions_map():

    top_limit = request.args.get('limit', default=5, type=int)


    regions = regions_severity_locations(limit=top_limit)

    # יצירת המפה
    map = folium.Map(location=[31.7683, 35.2137], zoom_start=7)


    for region in regions:
        if region["lat"] and region["lon"]:
            popup_html = f"""
                <div style="font-family: Arial, sans-serif; color: #333;">
                    <h3 style="color: #0073e6; text-align: center;">{region['region_name']} Information</h3>
                    <ul style="list-style-type: none; padding: 0;">
                        <li style="padding: 8px; border-bottom: 1px solid #ddd;">
                            <strong style="color: #333;">Average Severity</strong>: <span style="color: #0073e6;">{region['avg_sev']}</span>
                        </li>
                    </ul>
                </div>
            """
            marker_color = get_marker_color(region["avg_sev"])
            folium.Marker([region["lat"], region["lon"]],
                          popup=folium.Popup(popup_html, max_width=300),
                          icon=folium.Icon(color=marker_color)).add_to(map)

    map_html = map._repr_html_()

    # מחזיר את דף ה-HTML
    return render_template_string('''
       <html>
           <body>
               <h1>Regions Map</h1>
               <form method="get" action="/regions_map">
                   <label for="limit">Select Top N:</label>
                   <select name="limit" id="limit">
                       <option value="5" {% if request.args.get('limit') == '5' %}selected{% endif %}>Top 5</option>
                       <option value="0" {% if request.args.get('limit') == '0' %}selected{% endif %}>All</option>
                   </select>
                   <button type="submit">Filter</button>
               </form>
               {{ map_html|safe }}
           </body>
       </html>
   ''', map_html=map_html)