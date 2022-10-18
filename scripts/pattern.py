import rospy
import time

MAXLIN = 0.22
MAXANG = 2.84

class Pattern :
    def __init__(self, flag, ratio, initialTime):
        self.MAX = 3 #second
        self.flag = flag
        self.ratio = ratio
        self.currentTime = rospy.Time.now()
        self.Time = self.currentTime - initialTime

        self.cycle()

    def cycle(self):
        if self.flag is 'linear':
            self.linear(self.ratio)
            time.sleep(self.MAX)
            #self.linear(0)
            
        elif self.flag is 'angular':
            self.angular(self.ratio)
            time.sleep(self.MAX)
            self.angular(0)

    def linear(self, ratio):  # ratio: 0 ~ 100
        linearVal = (ratio/100.00) * MAXLIN 
        print("LINEAR VELOCITY : %f" %linearVal)

        return linearVal

    def angular(self, ratio): # ratio: 0 ~ 100 
        angularVal = (ratio/100.00) * MAXANG
        print("ANGULAR VELOCITY : %f" %angularVal)

        return angularVal
