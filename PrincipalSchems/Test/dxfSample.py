import ezdxf #'0.13.1'
#Specify version with dxf
doc = ezdxf.new("R2010", setup=True)

#Layer definition
doc.layers.new(name="MyLine1", dxfattribs={'linetype': 'DASHED', 'color': 7})
doc.layers.new(name="MyLine2", dxfattribs={'linetype': 'CONTINUOUS', 'color': 1})
doc.layers.new(name="MyLine3", dxfattribs={'linetype': 'CENTER', 'color': 2})

#add new entities to the modelspace
msp = doc.modelspace()

#Add a straight line
msp.add_line([0, 0], [100, 0], dxfattribs={'layer': 'MyLine1'})
msp.add_line([100, 0], [100, 100], dxfattribs={'layer': 'MyLine1'})
msp.add_line([100, 100], [0, 100], dxfattribs={'layer': 'MyLine1'})
msp.add_line([0, 100], [0, 0], dxfattribs={'layer': 'MyLine1'})

#center[50, 50],Addition of a circle with a radius of 50
msp.add_circle(center=[50, 50], radius=50, dxfattribs={'layer': 'MyLine2'})

#Add arc
msp.add_arc(center=[50, 50], radius=40,
            start_angle=0, end_angle=90, dxfattribs={'layer': 'MyLine2'})
msp.add_arc(center=[50, 50], radius=40,
            start_angle=90, end_angle=360, dxfattribs={'layer': 'MyLine3'})

#[50, 50]Add a point at the position of
msp.add_point([50, 50], dxfattribs={'layer': 'MyLine1'})

#Save image
doc.saveas('sample.dxf')