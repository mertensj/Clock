#!/usr/bin/env python

#############################################################################
##
##
#############################################################################

from PyQt4 import QtCore, QtGui


class PyAnalogClock(QtGui.QWidget):

	"""PyAnalogClock(QtGui.QWidget)
	
	Provides an analog clock custom widget with signals, slots and properties.
	The implementation is based on the Analog Clock example provided with both
	Qt and PyQt.
	"""
	
	# Emitted when the clock's time changes.
	timeChanged = QtCore.pyqtSignal(QtCore.QTime)
	
	# Emitted when the clock's time zone changes.
	timeZoneChanged = QtCore.pyqtSignal(int)
	
	def __init__(self, parent=None):
	
		super(PyAnalogClock, self).__init__(parent)
		
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		#self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
		#self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
		#self.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
		screen = QtGui.QDesktopWidget().screenGeometry()
		self.setGeometry(screen.width()-210,screen.height()/4, 200, 200)
		#self.setWindowTitle(QtCore.QObject.tr(self, "Analog Clock"))
		#self.resize(200, 200)
		#self.hide()
				
		self.timeZoneOffset = 0
		
		timer = QtCore.QTimer(self)
		timer.timeout.connect(self.update)
		timer.timeout.connect(self.updateTime)
		timer.start(1000)
		
		self.hourHand = QtGui.QPolygon([
			QtCore.QPoint(7, 8),
			QtCore.QPoint(-7, 8),
			QtCore.QPoint(0, -75)
		])
		self.hourHand2 = QtGui.QPolygon([
			QtCore.QPoint(7, 8),
			QtCore.QPoint(-7, 8),
			QtCore.QPoint(0, -45)
		])
		self.minuteHand = QtGui.QPolygon([
			QtCore.QPoint(7, 8),
			QtCore.QPoint(-7, 8),
			QtCore.QPoint(0, -99)
		])
		
		self.minuteHand2 = QtGui.QPolygon([
			QtCore.QPoint(7, 8),
			QtCore.QPoint(-7, 8),
			QtCore.QPoint(0, -60)
		])
		
		#self.hourColor = QtGui.QColor(0, 127, 0)
		#self.minuteColor = QtGui.QColor(0, 127, 127, 191)
		self.hourColor = QtGui.QColor(QtCore.Qt.black)
		self.minuteColor = QtGui.QColor(QtCore.Qt.white)
	
		action1 = QtGui.QAction("E&xit", self, 
								shortcut="Ctrl+Q",
								triggered=self.close)
	
		self.addAction(action1)
		self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
	
	def paintEvent(self, event):
	
		side = min(self.width(), self.height())
		time = QtCore.QTime.currentTime()
		time = time.addSecs(self.timeZoneOffset * 3600)
		
		painter = QtGui.QPainter()
		painter.begin(self)
		painter.setRenderHint(QtGui.QPainter.Antialiasing)
		painter.translate(self.width() / 2, self.height() / 2)
		painter.scale(side / 200.0, side / 200.0)
		
		painter.setPen(QtCore.Qt.NoPen)
		painter.setBrush(QtGui.QBrush(self.hourColor))
		
		painter.save()
		painter.rotate(30.0 * ((time.hour() + time.minute() / 60.0)))
		painter.drawConvexPolygon(self.hourHand)
		painter.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.black)))
		painter.drawConvexPolygon(self.hourHand2)
		painter.restore()
		
		#painter.setPen(self.hourColor)
		painter.setPen(QtGui.QPen(self.hourColor, 2, QtCore.Qt.SolidLine))
		
		for i in range(0, 12):
			painter.drawLine(80, 0, 96, 0)
			painter.rotate(30.0)
		
		painter.setPen(QtCore.Qt.NoPen)
		painter.setBrush(QtGui.QBrush(self.minuteColor))
		
		painter.save()
		painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
		painter.drawConvexPolygon(self.minuteHand)
		painter.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.black)))
		painter.drawConvexPolygon(self.minuteHand2)
		painter.restore()
		
		painter.setPen(QtGui.QPen(self.minuteColor))
		
		for j in range(0, 60):
			if (j % 5) != 0:
				painter.drawLine(90, 0, 96, 0)
			painter.rotate(6.0)
		
		painter.end()
	
	def minimumSizeHint(self):
	
		return QtCore.QSize(50, 50)
	
	def sizeHint(self):
	
		return QtCore.QSize(100, 100)
	
	def updateTime(self):
	
		self.timeChanged.emit(QtCore.QTime.currentTime())
	
	# The timeZone property is implemented using the getTimeZone() getter
	# method, the setTimeZone() setter method, and the resetTimeZone() method.
	
	# The getter just returns the internal time zone value.
	def getTimeZone(self):
	
		return self.timeZoneOffset
	
	# The setTimeZone() method is also defined to be a slot. The @pyqtSlot
	# decorator is used to tell PyQt which argument type the method expects,
	# and is especially useful when you want to define slots with the same
	# name that accept different argument types.
	
	@QtCore.pyqtSlot(int)
	def setTimeZone(self, value):
	
		self.timeZoneOffset = value
		self.timeZoneChanged.emit(value)
		self.update()
	
	# Qt's property system supports properties that can be reset to their
	# original values. This method enables the timeZone property to be reset.
	def resetTimeZone(self):
	
		self.timeZoneOffset = 0
		self.timeZoneChanged.emit(0)
		self.update()
	
	# Qt-style properties are defined differently to Python's properties.
	# To declare a property, we call pyqtProperty() to specify the type and,
	# in this case, getter, setter and resetter methods.
	timeZone = QtCore.pyqtProperty(int, getTimeZone, setTimeZone, resetTimeZone)


	def keyPressEvent(self, event):	
		if event.key() == QtCore.Qt.Key_Escape:
			self.close()

	def mousePressEvent(self, event):
		if (event.button() == QtCore.Qt.LeftButton):
			self.drag_position = event.globalPos() - self.pos();
			event.accept();
 
	def mouseMoveEvent(self, event):
		if (event.buttons() == QtCore.Qt.LeftButton):
			self.move(event.globalPos().x() - self.drag_position.x(),
				event.globalPos().y() - self.drag_position.y());
			event.accept(); 



def sigint_handler(*args):
	"""Handler for the SIGINT signal."""
	QtGui.QApplication.quit()

if __name__ == "__main__":

	import sys
	import signal
    
	signal.signal(signal.SIGINT, sigint_handler)
	app = QtGui.QApplication(sys.argv)
	clock = PyAnalogClock()
	clock.show()
	sys.exit(app.exec_())
