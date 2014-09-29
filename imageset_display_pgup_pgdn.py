#!/usr/bin/python
# imageClient.py
import Tkinter as tk
from PIL import Image, ImageTk
import sys
import urllib2
import time
from threading import *
eventdisplay=Event(); eventdisplay.clear()    #used for display thread
eventprevious = Event(); eventprevious.clear()#used for turining to previous picture thread
eventnext = Event(); eventnext.clear()#used for turning to next picture thread
eventscore = Event(); eventscore.clear()#used for calculating new score thread
eventhistory = Event(); eventhistory.clear()#used for history recording thread
mainloop =Event(); mainloop.clear()#used for control TK display
lck = Lock()#used for protecting data from chaging by anoher thread

newscore=4#default score is 4 sec
active=False#used for active threads
list=[]#image list used for holding pictures
historylist=[]#user history list used for recording history
fihish=0#used for quit thread
i=0#contrl integer, not necessary
c=0#contrl integer, not necessary
d=0 #contrl integer, not necessary
e=0 #contrl integer, not necessary
f=0 #contrl integer, not necessary
keep=1#used for keeping display loop
q=1
SERVER="http://dimboola.infotech.monash.edu.au"#image loading URL,
  
PROGRAM="~ajh/cgi-bin/imageServer.py"#modified Marc Cheong and John Hurst, 20100730:163804

number=38
task='image'
data='5.8'
running = True
pictureNo=0 #total number of the pictures 
print ''
print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
print '                    WELCOME           '
print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

while running: #the process of getting images,modified Marc Cheong and John Hurst, 20100730:163804
              print ''
              guess = int(raw_input('Enter an image number or press 0 for quit to futher option:'))
              number=guess
              task='image'
              data='5.8'

              #the URL in string format
              parms="task=%s&number=%d&data=%s" % (task,number,data)

              #  full URL location
              imageServer=urllib2.urlopen("%s/%s?%s" % (SERVER,PROGRAM,parms))

              # now do different things, depending on the task chosen
              if task=='image' and guess>=1:
                # read the picture file through bytes 
                bytes=imageServer.read()
                # open a file and write the image to it
                pictureNo=pictureNo+1
                imageFName='image'+str(pictureNo)+'.jpg'
                list.append(imageFName)
                imageFile=open(imageFName,'wb') # deal with by binary writes
                for b in bytes:
                    imageFile.write(b)
                imageFile.close()
                print ''
                print 'picture is loaded, the currently total number is ',pictureNo
	      elif guess==0:
		 
                 running=False
              else:
		 
                 running = False
print ''
print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
print 'all pictures are ready to display'                         #pictures are ready to display
print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
print ''
class Program(Thread):
   def __init__(self,label):
      Thread.__init__(self,name=label)
      self.label = label
   def start(self):
      Thread.start(self)
   def run(self):
       global newscore,keep,lck,pictureNo,q,root,c,d,e,f,finish
       global eventdisplay,eventprevious,eventnext,eventscore,eventhistory,eventcontrol
       while keep:	 
         if self.label == "display":                               #the thread of displaying picture
            if fihish==1:
                 sys.exit()
                 root.destroy()
                 root.quit()
	    if active==False:
	 	    eventdisplay.wait();
		    eventdisplay.clear();
		    global i
		    root = tk.Tk()
	    	    #create a container as root to hold the set of picture
                   
		      
		     		      
                      
                    #using PIL to display picture
                    image1 = ImageTk.PhotoImage( Image.open( list[i]))

                    #set attribute, height and weight
                    w = image1.width()
                    h = image1.height()

                    #set tposition to display 
                    x = 0
                    y = 0

                    w = image1.width()
                    h = image1.height()

                    
                    root.geometry("%dx%d+%d+%d" % (w, h, x, y))

                    # create a label and set it to display
                    label_image = tk.Label(image = image1)

                    # package the GUI
                    label_image.pack()


                    # let it to display
                    
                      
                      
                    i=i+1 #the first one should be index as 1 

                    #To display the images one by one
                    while 1==1:
                     if c==1: 
                      if i==pictureNo:
                          i=0
                      mainloop.set()
                      eventdisplay.wait(timeout=newscore)
                      
                      
                      eventdisplay.clear()
                      
                      n=Image.open(list[i])
                     
                      
                      
                      image1.paste(n)
                      
                     else:
                      d=d+1
                      if d==pictureNo:
                          d=0
                      
                      mainloop.set()
                      eventdisplay.wait(timeout=newscore)            #option for paste the previous one to the old one
                      if e==1:
                        lck.acquire()
                        
                        f=1
                        eventdisplay.clear()
                      
                        n=Image.open(list[2-d])
                        toprevious='turn to the previous one at '+str(time.localtime())
                        historylist.append(toprevious)
                      
                        image1.paste(n)
                        e=0
                        lck.release()
                      else:
                        if f==1:
                            d=d-2
                        
                      
                        eventdisplay.clear()
                      
                        n=Image.open(list[d])                                    #normal display process
                        
                      
                      
                        image1.paste(n)
                        f=0
                     c=0  
                     
                      
		     
		    
	    
	 	      
         elif self.label == "next":                                          #event for getting next picture
            eventnext.wait();
	    eventnext.clear();
	    
	    lck.acquire()
	    
	    
	    tonext='turn to the next one '+'image at'+str(time.localtime())
	    historylist.append(tonext)
	    eventdisplay.set()
	   
	    
	    lck.release()
	    
	 elif self.label == "previous":                                     #event for getting previous picture
            eventprevious.wait(); 
	    eventprevious.clear();
	    lck.acquire()
	    
	    
	    e=1
	    
	    eventdisplay.set()
	     
	   
	      
	      
	    
	    lck.release()   
	 elif self.label == "score":                                            #event for calculate score
            eventscore.wait(); 
	    eventscore.clear();
	    print 'get an new score number ',newscore 
	   
            
	    
         elif self.label == "history":                                          #event for history, persistent
	    eventhistory.wait(); 
	    eventhistory.clear();             
            record=0                                                            #use to record the history for user action
            print ''
            print 'The previous user entry history'
            print ''
            print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
            while(record<len(historylist)):
            
            
               print historylist[record]
               record=record+1
               
	    print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
	    print ''
	    print 'all the history is listed, and you can continue to further control option'
	    print 'option:d.display p.previous n.next s.score h.history q.quit\n'
	 elif self.label == "mainloop":
	    mainloop.wait(); 
	    mainloop.clear();
	    root.mainloop();
	 else:   
		 #get picture
	    
            option=0
            		                                                            #event for control all the operation
            while 1==1:
	      option = str(raw_input('Enter an option: d.display p.previous n.next s.score h.history q.quit\n'))
	      if option=='d':
		 eventdisplay.set()                                                 #active display
              elif option=='p':
	         eventprevious.set()
		                                                                    #active get previous
              elif option=='n':
	         eventnext.set()                                                    #active get next
              elif option=='s':                                                     #active get score
                 imageNumber=0
                 total=0
		 lck.acquire()
		 while(imageNumber<pictureNo):
		   print 'Give a new score for',list[imageNumber]
		   newscore = float(raw_input('Enter an new score number for picture:'))
		   total=newscore+total
		   imageNumber=imageNumber+1
		   newscore=total/pictureNo
		   changescore='change score to at'+str(time.localtime())
		   historylist.append(changescore)
		 print ''  
		 print 'The average new score is\n',newscore
		 print ''
		 lck.release()
	         eventscore.set()            
              elif option=='h':
                 eventhistory.set()
              else: 
		 q=0                                                                 #quit the display
                 finish=1
                 print ''
                 print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
                 print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
                 print '      finish and good luck'
                 print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
                 print 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
                 print ''
		 sys.exit()
	      
  

process1 = Program("display")
process2 = Program("previous")
process3 = Program("next")
process4 = Program("score")
process5 = Program("history")
process6 = Program("control")
process7 = Program("mainloop")

process1.start()
process2.start()
process3.start()
process4.start()
process5.start()
process6.start()
process7.start()

process1.join()
process2.join()
process3.join()
process4.join()
process5.join()
process6.join()
process7.join()
