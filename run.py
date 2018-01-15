import matplotlib.pylab as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    graph_date = open('data.txt','r').read();
    lines = graph_date.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x,y = line.split(',')
            
            xs.append(x)
            ys.append(y)
            
    ax1.clear()
    ax1.plot(xs,ys)
    
def addPointX(last, current,deltaTime,counter):
    Value = abs(current - last)/deltaTime
    f = open('data.txt',"a+")
    line = str(counter)+','+str(Value)+'\n'
    f.write(line)
    f.close()
    counter +=1
    
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
