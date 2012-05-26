import wx

TELI_Xsensor = 1392
TELI_Ysensor = 1050
TELI_Ximage = 1280
TELI_Yimage = 1040

class CenterTeliImage(wx.Frame):
	''''''
	def __init__(self, parent, id, title='Center Teli Image'):
		wx.Frame.__init__(self, parent, id, title)
		panel = wx.Panel(self, -1)
		vsizer = wx.BoxSizer(wx.VERTICAL)
		spinsizer = wx.BoxSizer()
		self.widthspin = wx.SpinCtrl(panel, -1, initial=1, min=1, max=TELI_Ximage)
		self.heightspin = wx.SpinCtrl(panel, -1, initial=1, min=1, max=TELI_Yimage)
		spinsizer.Add(self.widthspin)
		spinsizer.Add(self.heightspin)
		vsizer.Add(spinsizer)
		
		self.result = wx.StaticText(panel, -1)
		vsizer.Add(self.result)
		
		button = wx.Button(panel, -1, label='Center!')
		button.Bind(wx.EVT_BUTTON, self.OnCenter)
		vsizer.Add(button, wx.GROW)
		
		panel.SetSizer(vsizer)
		panel.Fit()
                self.Fit()
		
	def OnCenter(self, evt):
		width = self.widthspin.GetValue()
		height = self.heightspin.GetValue()
		xborder, yborder = self.center_image(width, height)
		text = 'shiftX = %i, shiftY = %i'%(xborder, yborder)
		self.result.SetLabel(text)
		evt.Skip()
		
	def center_image(self, width, height):
		xborder = (TELI_Ximage-width)/2+TELI_Xsensor-TELI_Ximage
		yborder = (TELI_Yimage-height)/2+TELI_Ysensor-TELI_Yimage
		return xborder, yborder

if __name__ == "__main__":
	app = wx.PySimpleApp()
	frame = CenterTeliImage(None, -1)
	frame.Show()
	app.MainLoop()
	
