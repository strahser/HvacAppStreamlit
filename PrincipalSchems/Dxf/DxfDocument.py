import ezdxf


class DxfDocument:
	doc = ezdxf.new(dxfversion='R2010')
	msp = doc.modelspace()
