import fitz  
import math
from geopy.geocoders import Nominatim
import re
import folium
import csv

def create_combined_pdf(input_path, output_path, map_path="points_map.html", page_num=0):
  
    doc = fitz.open(input_path)
    page = doc[page_num]
    text_dict = page.get_text("dict")
    drawings = page.get_drawings()


    geolocator = Nominatim(user_agent="my_geocoder_app")
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
    
  
    outpdf = fitz.open()
    outpage = outpdf.new_page(width=page.rect.width, height=page.rect.height)
    
   
    shape = outpage.new_shape()


    file=open("output2.txt", 'w')
    
    pattern = r'S\d_([A-Za-z]+)_D\d+_([A-Za-z]+)_B\d+_([A-Za-z]+)\.pdf$'

    # Search for pattern
    match = re.search(pattern, input_path)

    if match:
        state = match.group(1).capitalize()
        district = match.group(2)
        bloc = match.group(3)
    else:
        print("Pattern not found!")



    for d in drawings:
        
        try:
            #using conditions for specific elements

            if len(d['items'])==7:    
                for i in range(0,7):
                    if (d['items'][i][0]=='l'):
                        arr=True
                    else:
                        arr=False

            if len(d['items'])==3:     
                for i in range(0,3):
                    if (d['items'][i][0]=='l'):
                        tri=True
                    else:
                        tri=False

            if len(d['items'])==14:      
                for i in range(0,14):
                    if (d['items'][i][0]=='l'):
                        spl=True
                    else:
                        spl=False

            if len(d['items'])==9:
                for i in range(0,9):
                    if (d['items'][i][0]=='l'):
                        oclan=True
                    else:
                        oclan=False

            if len(d['items'])==10:
                for i in range(0,10):
                    if (d['items'][i][0]=='l'):
                        spl5=True
                    else:
                        spl5=False

    
            if (len(d['items'])==8 and d['items'][0][0] == "l"):    #splitter (4 pointed star)
                file.write('\nsplitter')
                file.write('\n')
                file.write(str(d))
                for i in range(0,8,1):
                    shape.draw_line(d['items'][i][1], d['items'][i][2])
                shape.draw_line(d['items'][0][1], d['items'][0][2])
    
          
            elif d['items'][0][0] == "re":  # rectangle
                file.write("\nrect")
                file.write('\n')
                file.write(str(d))
                shape.draw_rect(d['items'][0][1])

            elif d['items'][0][0] == "qu":  # quad
                file.write("\nquad")
                file.write('\n')
                file.write(str(d))
                shape.draw_quad(d['items'][0][1])

            elif (d['items'][0][0] == "c" and len(d['items'])==4) :  # circle
                file.write("\ncircle")
                file.write('\n')
                file.write(str(d))
                for i in range(0,4,1):
                    shape.draw_bezier(d['items'][i][1], d['items'][i][2], d['items'][i][3], d['items'][i][4])
                
            elif (len(d['items'])==7 and arr==True):     #arrows
                file.write("\narrow")
                file.write('\n')
                file.write(str(d))
                for i in range(0,7):
                    shape.draw_line(d['items'][i][1], d['items'][i][2])


            elif (len(d['items'])==3 and tri==True):     #triangle
                file.write("\ntriangle")
                file.write('\n')
                file.write(str(d))
                for i in range(0,3):
                    shape.draw_line(d['items'][i][1], d['items'][i][2])

            elif (len(d['items'])==14 and spl==True):      #splitter (7 pointed)
                file.write("\n7splitter7")
                file.write('\n')
                file.write(str(d))
                for i in range(0,14,1):
                    shape.draw_line(d['items'][i][1], d['items'][i][2])
                shape.draw_line(d['items'][0][1], d['items'][0][2])

            elif (len(d['items'])==10 and spl5==True):      #splitter (5 pointed)
                file.write("\n5splitter5")
                file.write('\n')
                file.write(str(d))
                for i in range(0,10,1):
                    shape.draw_line(d['items'][i][1], d['items'][i][2])
                shape.draw_line(d['items'][0][1], d['items'][0][2])

            elif (len(d['items'])==9 and oclan==True):      #OCLAN (cube)
                file.write("\nOCLAN")
                file.write('\n')
                file.write(str(d))
                for i in range(0,9,1):
                    shape.draw_line(d['items'][i][1], d['items'][i][2])

            elif (d['items'][0][0] == "l" and len(d['items'])==2):  # cross (inside circle) (BHQ - PoP)
                file.write("\ncross")
                file.write('\n')
                file.write(str(d))
                shape.draw_line(d['items'][0][1], d['items'][0][2]) 
                shape.draw_line(d['items'][1][1], d['items'][1][2]) 



            elif (d['items'][0][0] == "l" and len(d['items'])==1):  # line
                file.write("\nline")
                file.write('\n')
                file.write(str(d))
                shape.draw_line(d['items'][0][1], d['items'][0][2]) 



                
            elif (len(d['items'])==6):      #OLTE (cylinder)
                file.write("\nOLTE")
                file.write('\n')
                file.write(str(d))  
                for i in range (0,5):
                    if i==2:
                        continue
                    shape.draw_bezier(d['items'][i][1], d['items'][i][2], d['items'][i][3], d['items'][i][4])
                shape.draw_line(d['items'][2][1], d['items'][2][2])
                shape.draw_line(d['items'][5][1], d['items'][5][2])

                try:
                    shape.finish(
                        fill=d["fill"],
                        fill_opacity= d.get("fill_opacity", 1),
                        even_odd=d.get("even_odd", True),
                        closePath=d["closePath"],
                        stroke_opacity=1,
                        )
                    continue
                except TypeError:
                    continue

            elif (len(d['items'])==8):
                file.write("\nOLTE2")
                file.write('\n')
                file.write(str(d))  
                for i in range (0,7):
                    if i==4:
                        continue
                    shape.draw_bezier(d['items'][i][1], d['items'][i][2], d['items'][i][3], d['items'][i][4])
                shape.draw_line(d['items'][4][1], d['items'][4][2])
                shape.draw_line(d['items'][7][1], d['items'][7][2])

            else:
                continue

            stroke = d.get("stroke_opacity", 1)
            stroke = 1 if stroke is None else stroke
            fo = d.get("fill_opacity", 1)
            fo = 1 if fo is None else fo

            file.write('\n'+('-' * 20))

            

            try:
                finish_kwargs = {
                    "fill": d.get("fill"),
                    "even_odd": d.get("even_odd", True),
                    "stroke_opacity": d.get("stroke_opacity", 1),
                    "fill_opacity": d.get("fill_opacity", 1),
                }

                # Only add if not None
                if d.get("color") is not None:
                    finish_kwargs["color"] = d["color"]
                if d.get("dashes") is not None:
                    finish_kwargs["dashes"] = d["dashes"]
                if d.get("closePath") is not None:
                    finish_kwargs["closePath"] = d["closePath"]
                if d.get("lineJoin") is not None:
                    finish_kwargs["lineJoin"] = d["lineJoin"]
                if d.get("lineCap") is not None:
                    finish_kwargs["lineCap"] = d["lineCap"][0] if isinstance(d["lineCap"], tuple) else d["lineCap"]
                if d.get("width") is not None:
                    finish_kwargs["width"] = d["width"]

                shape.finish(**finish_kwargs)

                shape.commit()
            except TypeError:
                 file.write("error")
                 file.write('\n'+('-' * 40))
                 continue
            

        except ValueError:
            continue
            
        shape.commit()
            

    
    for block in text_dict.get("blocks", []):
        file.write(f"Block bbox: {block.get('bbox', '')}\n")
        for line in block.get("lines", []):
            file.write(f" {line}\n")
            file.write(f"  Line bbox: {line.get('bbox', '')}\n")
            angle_deg = math.degrees(math.atan2(line["dir"][1], line["dir"][0]))
            for span in line.get("spans", []):
                file.write(f"    Span text: {span.get('text', '')}\n")
                file.write(f"    Font: {span.get('font', '')}, Size: {span.get('size', '')}, Color: {span.get('color', '')}\n")
                file.write(f"    Origin: {span.get('origin', '')}\n")
                file.write(f"    Rotation degrees: {angle_deg}\n")
                file.write(f"        {line["dir"][1]}, {line["dir"][0]}  \n")
                file.write("    " + "-"*20 + "\n")
        file.write("-"*40 + "\n")


    for block in text_dict.get("blocks", []):
        for line in block.get("lines", []):
            angle_deg = math.degrees(math.atan2(line["dir"][1], line["dir"][0]))
            valid_angles = [0, 90, 180, 270]
            angle = min(valid_angles, key=lambda x: abs(x - angle_deg))
            
            for span in line["spans"]:
                outpage.insert_text(
                    point=span["origin"],
                    text=span["text"],
                    fontsize=span["size"],
                    fontname="helv",
                    rotate=angle,  
                    color=(0,0,0)
                )
                text=span["text"]
                address = str(text) + ', ' + str(bloc) + ', ' + str(district) + ', '+ str(state)    
                
                location = geolocator.geocode(address, timeout= 10)    
                
                if location:
                    lat=location.latitude
                    lon=location.longitude
                    print(f"Address: {location.address}")
                    print(f"Latitude: {location.latitude}")
                    print(f"Longitude: {location.longitude}")
                    folium.Marker(location=[lat, lon],
                                  tooltip=str(text),
                                  popup=str(text)).add_to(m)
                else:
                    print("Location not found.")

    outpdf.save(output_path)
    print(f"Combined PDF saved to {output_path}")



    file.close()

    f=open('rajasthan_olte.csv', 'r')
    reader=csv.reader(f)
    next(reader)

    #plotting all the points on a map using folium
    for row in reader:
        lat=row[4]
        lon=row[5]
        folium.Marker(location=[lat, lon], 
                    popup=row[3],
                    tooltip=row[3],
                    icon=folium.Icon(color='red')).add_to(m)
    m.save("points_map.html")


input_path="C391_S8_RAJASTHAN_D3_Banswara_B6_Kushalgarh.pdf"  #example



create_combined_pdf(
    input_path,
    output_path="combined_output1.pdf",
    map_path="points_map.html",
    page_num=0
)



