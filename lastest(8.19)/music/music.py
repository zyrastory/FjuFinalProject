from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
import sys


"""
url= C.QUrl.fromLocalFile("./some.mp3")
content= M.QMediaContent(url)

player = M.QMediaPlayer()
player.setMedia(content)
player.play()

player.stateChanged.connect( app.quit )
app.exec()
"""
app=QCoreApplication(sys.argv)
playlist = QMediaPlaylist()
url = QUrl.fromLocalFile("./some.mp3")
url2 = QUrl.fromLocalFile("./one.mp3")
playlist.addMedia(QMediaContent(url))
playlist.addMedia(QMediaContent(url2))
playlist.setPlaybackMode(QMediaPlaylist.Loop)

player = QMediaPlayer()
player.setPlaylist(playlist)
player.play()

app.exec()