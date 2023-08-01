from Polygons.PolygonsControl.PolygonsControl import TabsPolygonSqlCreator
from Upload.UploadLayout import UploadLayout


def polygon_main(upload_layout: UploadLayout, key):
	polygons_plots = TabsPolygonSqlCreator(upload_layout, key)
	polygons_plots.create_polygons_plot_and_tabs()
