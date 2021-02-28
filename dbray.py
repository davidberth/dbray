import window
import buffer


screenx, screeny = 600, 600
buffer = buffer.Buffer(screenx, screeny)

window = window.Window(600, 600)
running = True
while running:
    running = window.frame(buffer.buffer)



