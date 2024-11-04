# Set up a new DXF document:
import ezdxf
from ezdxf.enums import MTextEntityAlignment
from ezdxf.addons import TablePainter

doc = ezdxf.new("R2000")  # required for lineweight support
doc.header["$LWDISPLAY"] = 1  # show lineweights
doc.styles.add("HEAD", font="OpenSans-ExtraBold.ttf")
doc.styles.add("CELL", font="OpenSans-Regular.ttf")
# Create a new TablePainter object with four rows and four columns,
# the insert location is the default render location but can be overriden in the render() method:
table = TablePainter(
    insert=(0, 0), nrows=4, ncols=4, cell_width=6.0, cell_height=2.0
)
# Create a new CellStyle object for the table-header called “head”:
table.new_cell_style(
    "head",
    text_style="HEAD",
    text_color=ezdxf.colors.BLUE,
    char_height=0.7,
    bg_color=ezdxf.colors.LIGHT_GRAY,
    align=MTextEntityAlignment.MIDDLE_CENTER,
)
# Redefine the default CellStyle for the content cells:
# reset default cell style
default_style = table.get_cell_style("default")
default_style.text_style = "CELL"
default_style.char_height = 0.5
default_style.align = MTextEntityAlignment.BOTTOM_LEFT
# Set the table-header content:
for col in range(4):
    table.text_cell(0, col, f"Head[{col}]", style="head")

# Set the cell content:
for row in range(1, 4):
    for col in range(4):
        # cell style is "default"
        table.text_cell(row, col, f"Cell[{row}, {col}]")

# Add a red frame around the table-header:
# new cell style is required
red_frame = table.new_cell_style("red-frame")
red_borderline = table.new_border_style(color=ezdxf.colors.RED, lineweight=35)
# set the red borderline style for all cell borders
red_frame.set_border_style(red_borderline)
# create the frame object
table.frame(0, 0, 4, style="red-frame")
# Render the table into the modelspace and export the DXF file:
# render the table, shifting the left-bottom of the table to the origin:
table.render(doc.modelspace(), insert=(0, table.table_height))

th = table.table_height
tw = table.table_width
doc.set_modelspace_vport(height=th * 1.5, center=(tw / 2, th / 2))
doc.saveas("table_tutorial.dxf")
