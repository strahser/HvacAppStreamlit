import io
import base64

import pandas as pd
from PIL import Image

from SQL.SqlModel import SqlConnector


def image_to_byte_array(image_path) -> str:
	im = Image.open(image_path)
	data = io.BytesIO()
	im.save(data, "JPEG")
	encoded_img_data = base64.b64encode(data.getvalue())
	img_data = encoded_img_data.decode('utf-8')
	return img_data

def _create_chart_from_df(table_name,x_value,y_value):
	df = pd.read_sql(f"select * from {table_name}", con=SqlConnector.conn_sql)
	ax = df.plot(kind='bar', x=x_value, y=y_value)
	fig_ = ax.get_figure()
	my_stringIObytes = io.BytesIO()
	fig_.savefig(my_stringIObytes, format='jpg')
	my_stringIObytes.seek(0)
	my_base64_jpgData = base64.b64encode(my_stringIObytes.read())
	img_data = my_base64_jpgData.decode('utf-8')
	return img_data