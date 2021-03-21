from tkinter import Label,CENTER,Button,OptionMenu,NW,StringVar,Canvas,messagebox
from PIL import ImageTk,Image  
import tkinter as tk
import bluetooth,tkinter.colorchooser,serial,sys,serial.tools.list_ports,time,ast,os 
import serial.tools.list_ports
from tkinter.ttk import Progressbar

 
   
class tkinterApp(tk.Tk):                                                #Define the Base start with frames
       
    def __init__(self, *args, **kwargs):                                #__init__ function for class tkinterAPP          
        tk.Tk.__init__(self, *args, **kwargs)                           #__init__ function for class TK
          
        container = tk.Frame(self)                                      #Creating a container
        container.pack(side = "top", fill = "both", expand = True)      #Pack the Container 
   
        container.grid_rowconfigure(0, weight = 1)                      #Configure the container grid method (rows)
        container.grid_columnconfigure(0, weight = 1)                   #Configure the container grid method (columns)
   
        self.frames = {}                                                #Initialize frame to an empty array
   
        for F in (StartPage, Update_Firmware):                            #Iterate through a tuple consisting of the different page layouTS3
            frame = F(container, self) 
            self.frames[F] = frame                                      #Iterate through all the page frames as defined
            frame.grid(row = 0, column = 0, sticky ="nsew")             #Pack the frame to the grid 
   
        self.show_frame(StartPage)                                      #Load the Start Page Frame
   
    # to display the current frame passed as 
    # parameter 
    def show_frame(self, cont): 
        frame = self.frames[cont] 
        frame.tkraise() 

#----------------------------------------------Start Page---------------------------------------------------#

class StartPage(tk.Frame):                                              #Define the Launch Page
    def __init__(self, parent, controller):  
        #__init__    
            #Create the Window and find the windows    
                tk.Frame.__init__(self, parent)
                self.find_comports()
            
        #Top Menu
            #Set the Theme Variables
                topmenu_textcolor   =   'white'     #The text color for all the widgets on the canvas
                topmenu_bgcolor     =   '#383a39'   #The background color for all the widgets on the canvas

            #Create the Canvas           
                global top_menu
                top_menu = tk.Canvas(self, height=140, width=1400, bg=topmenu_bgcolor)                                   
                top_menu.grid(row = 0, column = 0,)  

            #Program Title   
                program_title = Label(top_menu, text="R4LA LED Configurator", font=("Helvetica", 18, "bold", "italic"), fg=topmenu_textcolor, bg=topmenu_bgcolor)                                  
                program_title.place(relx=0.2, rely=0.5, anchor=CENTER)                                  

            #Configure Button
                Configure_Button = Button(top_menu, height=5, width=12, text='Configure', command = self.Configure_FUNC)            
                Configure_Button.place(relx=0.9, rely=0.17)

            #COM Port Drop Down Menu
                COM_Port_Dropdown_Menu = OptionMenu(top_menu,COMport_start_text, *COMport_results,)
                COM_Port_Dropdown_Menu.place(relx=0.81,rely=0.17,anchor=NW)

        #Side Menu (Presets Need improvement)
            #Set the Theme Variables
                _sidemenu_textcolor  =   'white'     #The text color for all the widgets on the canvas
                sidemenu_bgcolor    =   '#2e2e2e'   #The background color for all the widgets on the canvas

            #Create the Canvas
                side_menu = tk.Canvas(self, height=671, width=200, bd=0, bg=sidemenu_bgcolor)
                side_menu.place(x=0, y=142, anchor=NW)

        #Content Window
            #Create the Main Canvas
                global Content_Window_Canvas
                Content_Window_Canvas = tk.Canvas(self, height=671, width=1194, bg='grey')
                Content_Window_Canvas.place(x=202, y=142, anchor=NW)

            #Create the Options Sub-Canvas
                options_canvas = Canvas(Content_Window_Canvas,bg='grey',highlightthickness=0)
                options_canvas.place(x=2,y=2,anchor=NW)

            #Create the LED Sub-Canvas
                global LED_Canvas            
                LED_Canvas = Canvas(Content_Window_Canvas, bg='grey',highlightthickness=0)
                LED_Canvas.place(relx=0.5,rely=0.5,anchor=CENTER)

            #Clear all LEDs Button
                Clear_LED_Colors_BTN = Button(options_canvas, text="Clear LEDs", width=12, command=self.Clear_LED_Colors_FUNC)
                Clear_LED_Colors_BTN.grid(row=1, column=1)
                
            #Fill all LEDs Button
                fill_colors_btn = Button(options_canvas, text='Fill LEDs', width=12, command=self.Fill_Colors_FUNC)
                fill_colors_btn.grid(row=1, column=2)

            #Color Chooser
                color_chooser = Button(options_canvas, text="Select Color", command=self.openColorDialog)
                color_chooser.grid(row=2,column=1)

            #Color Preview
                global color_preview
                color_preview = Label(options_canvas, width=2, text="", bg='black')
                color_preview.grid(row=2,column=2)

            #Bottom LED Section Label
                B_LED_Label = Label(LED_Canvas, text="Bottom LEDs", font='Calibri' '24', bg='grey',fg='white')
                B_LED_Label.grid(row=0,column=0,columnspan=46)
            
            #Bottom LED Section Spacer
                Bottom_LED_Space = Label(LED_Canvas,bg='grey',width=3)
                Bottom_LED_Space.grid(row=4,column=0,columnspan=46)

            #Center Spacer
                Center_Space = Label(LED_Canvas,bg='grey',width=3)
                Center_Space.grid(row=0,column=23,rowspan=12)

            #Top LED Section Label
                T_LED_Label = Label(LED_Canvas, text="Top LEDs", font='Calibri' '24', bg='grey',fg='white')
                T_LED_Label.grid(row=8,column=0,columnspan=46)    
            
            #Top LED Section Spacer
                Top_LED_Space = Label(LED_Canvas,bg='grey',width=3)
                Top_LED_Space.grid(row=12,column=0,columnspan=46)
          
            #LED Variables
                global NUMLEDs
                NUMLEDs = 443

            #Generate the Dictionary
                global set_color
                set_color = {}
                for i in range(NUMLEDs+1):
                    set_color['led{}'.format(i)] = '0x000000'

            #Create the LEDs
                global LED_List
                LED_List = []

                for i in range(NUMLEDs+1):
                    LED_List.append('led'+str(i))

                for i in range(NUMLEDs+1):
                    globals()[LED_List[i]] = Button(LED_Canvas,height=1,width=2,text='led{}'.format(i),fg='black',bg='black')
                    globals()[LED_List[i]].bind("<Button-1>",self.Change_LED_Color_FUNC)

            #Place the LEDs on the Canvas:
                #BS1 Widget Cluster
                globals()[LED_List[60]].grid(row=5, column=22)       
                globals()[LED_List[61]].grid(row=6, column=21)
                globals()[LED_List[62]].grid(row=5, column=21)
                globals()[LED_List[63]].grid(row=5, column=20)
                globals()[LED_List[64]].grid(row=6, column=20)
                globals()[LED_List[65]].grid(row=7, column=20)
                globals()[LED_List[66]].grid(row=7, column=19)
                globals()[LED_List[67]].grid(row=5, column=19)
                globals()[LED_List[68]].grid(row=5, column=18)
                globals()[LED_List[69]].grid(row=6, column=18)
                globals()[LED_List[70]].grid(row=7, column=18)
                globals()[LED_List[71]].grid(row=7, column=17)
                globals()[LED_List[72]].grid(row=6, column=17)
                globals()[LED_List[73]].grid(row=5, column=17)
                globals()[LED_List[74]].grid(row=5, column=16)
                globals()[LED_List[75]].grid(row=6, column=16)
                globals()[LED_List[76]].grid(row=7, column=16)
                globals()[LED_List[77]].grid(row=7, column=15)
                globals()[LED_List[78]].grid(row=6, column=15)
                globals()[LED_List[79]].grid(row=5, column=15)
                globals()[LED_List[80]].grid(row=5, column=14)
                globals()[LED_List[81]].grid(row=6, column=14)
                globals()[LED_List[82]].grid(row=7, column=14)
                globals()[LED_List[83]].grid(row=7, column=13)
                globals()[LED_List[84]].grid(row=6, column=13)
                globals()[LED_List[85]].grid(row=5, column=13)
                globals()[LED_List[86]].grid(row=5, column=12)
                globals()[LED_List[87]].grid(row=6, column=12)
                globals()[LED_List[88]].grid(row=7, column=12)
                globals()[LED_List[89]].grid(row=7, column=11)
                globals()[LED_List[90]].grid(row=6, column=11)
                globals()[LED_List[91]].grid(row=5, column=11)
                globals()[LED_List[92]].grid(row=5, column=10)
                globals()[LED_List[93]].grid(row=6, column=10)
                globals()[LED_List[94]].grid(row=7, column=10)
                globals()[LED_List[95]].grid(row=7, column=9)
                globals()[LED_List[96]].grid(row=6, column=9)
                globals()[LED_List[97]].grid(row=5, column=9)
                globals()[LED_List[98]].grid(row=5, column=8)
                globals()[LED_List[99]].grid(row=6, column=8)
                globals()[LED_List[100]].grid(row=7, column=8)
                globals()[LED_List[101]].grid(row=7, column=7)
                globals()[LED_List[102]].grid(row=6, column=7)
                globals()[LED_List[103]].grid(row=5, column=7)
                globals()[LED_List[104]].grid(row=5, column=6)
                globals()[LED_List[105]].grid(row=6, column=6)
                globals()[LED_List[106]].grid(row=7, column=6)
                globals()[LED_List[107]].grid(row=7, column=5)
                globals()[LED_List[108]].grid(row=6, column=5)
                globals()[LED_List[109]].grid(row=5, column=5)
                globals()[LED_List[110]].grid(row=5, column=4)
                globals()[LED_List[111]].grid(row=6, column=4)
                globals()[LED_List[112]].grid(row=7, column=4)
                globals()[LED_List[113]].grid(row=7, column=3)
                globals()[LED_List[114]].grid(row=6, column=3)
                globals()[LED_List[115]].grid(row=5, column=3)
                globals()[LED_List[116]].grid(row=5, column=2)
                globals()[LED_List[117]].grid(row=6, column=2)
                globals()[LED_List[118]].grid(row=7, column=2)          
                globals()[LED_List[119]].grid(row=6, column=1)
                
                #BS2 Widget Cluster
                globals()[LED_List[0]].grid(row=3, column=22)  
                globals()[LED_List[1]].grid(row=2, column=21)
                globals()[LED_List[2]].grid(row=3, column=21)
                globals()[LED_List[3]].grid(row=3, column=20)
                globals()[LED_List[4]].grid(row=2, column=20)
                globals()[LED_List[5]].grid(row=1, column=20)
                globals()[LED_List[6]].grid(row=1, column=19)
                globals()[LED_List[7]].grid(row=3, column=19)
                globals()[LED_List[8]].grid(row=3, column=18)
                globals()[LED_List[9]].grid(row=2, column=18)
                globals()[LED_List[10]].grid(row=1, column=18)
                globals()[LED_List[11]].grid(row=1, column=17)
                globals()[LED_List[12]].grid(row=2, column=17)
                globals()[LED_List[13]].grid(row=3, column=17)
                globals()[LED_List[14]].grid(row=3, column=16)
                globals()[LED_List[15]].grid(row=2, column=16)
                globals()[LED_List[16]].grid(row=1, column=16)
                globals()[LED_List[17]].grid(row=1, column=15)
                globals()[LED_List[18]].grid(row=2, column=15)
                globals()[LED_List[19]].grid(row=3, column=15)
                globals()[LED_List[20]].grid(row=3, column=14)
                globals()[LED_List[21]].grid(row=2, column=14)
                globals()[LED_List[22]].grid(row=1, column=14)
                globals()[LED_List[23]].grid(row=1, column=13)
                globals()[LED_List[24]].grid(row=2, column=13)
                globals()[LED_List[25]].grid(row=3, column=13)
                globals()[LED_List[26]].grid(row=3, column=12)
                globals()[LED_List[27]].grid(row=2, column=12)
                globals()[LED_List[28]].grid(row=1, column=12)
                globals()[LED_List[29]].grid(row=1, column=11)
                globals()[LED_List[30]].grid(row=2, column=11)
                globals()[LED_List[31]].grid(row=3, column=11)
                globals()[LED_List[32]].grid(row=3, column=10)
                globals()[LED_List[33]].grid(row=2, column=10)
                globals()[LED_List[34]].grid(row=1, column=10)
                globals()[LED_List[35]].grid(row=1, column=9)
                globals()[LED_List[36]].grid(row=2, column=9)
                globals()[LED_List[37]].grid(row=3, column=9)
                globals()[LED_List[38]].grid(row=3, column=8)
                globals()[LED_List[39]].grid(row=2, column=8)
                globals()[LED_List[40]].grid(row=1, column=8)
                globals()[LED_List[41]].grid(row=1, column=7)
                globals()[LED_List[42]].grid(row=2, column=7)
                globals()[LED_List[43]].grid(row=3, column=7)
                globals()[LED_List[44]].grid(row=3, column=6)
                globals()[LED_List[45]].grid(row=2, column=6)
                globals()[LED_List[46]].grid(row=1, column=6)
                globals()[LED_List[47]].grid(row=1, column=5)
                globals()[LED_List[48]].grid(row=2, column=5)
                globals()[LED_List[49]].grid(row=3, column=5)
                globals()[LED_List[50]].grid(row=3, column=4)
                globals()[LED_List[51]].grid(row=2, column=4)
                globals()[LED_List[52]].grid(row=1, column=4)
                globals()[LED_List[53]].grid(row=1, column=3)
                globals()[LED_List[54]].grid(row=2, column=3)
                globals()[LED_List[55]].grid(row=3, column=3)
                globals()[LED_List[56]].grid(row=3, column=2)
                globals()[LED_List[57]].grid(row=2, column=2)
                globals()[LED_List[58]].grid(row=1, column=2)          
                globals()[LED_List[59]].grid(row=2, column=1)

                #BS3 Widget Cluster
                globals()[LED_List[324]].grid(row=5, column=24)  
                globals()[LED_List[325]].grid(row=6, column=25)
                globals()[LED_List[326]].grid(row=5, column=25)
                globals()[LED_List[327]].grid(row=5, column=26)
                globals()[LED_List[328]].grid(row=6, column=26)
                globals()[LED_List[329]].grid(row=7, column=26)
                globals()[LED_List[330]].grid(row=7, column=27)
                globals()[LED_List[331]].grid(row=5, column=27)
                globals()[LED_List[332]].grid(row=5, column=28)
                globals()[LED_List[333]].grid(row=6, column=28)
                globals()[LED_List[334]].grid(row=7, column=28)
                globals()[LED_List[335]].grid(row=7, column=29)
                globals()[LED_List[336]].grid(row=6, column=29)
                globals()[LED_List[337]].grid(row=5, column=29)
                globals()[LED_List[338]].grid(row=5, column=30)
                globals()[LED_List[339]].grid(row=6, column=30)
                globals()[LED_List[340]].grid(row=7, column=30)
                globals()[LED_List[341]].grid(row=7, column=31)
                globals()[LED_List[342]].grid(row=6, column=31)
                globals()[LED_List[343]].grid(row=5, column=31)
                globals()[LED_List[344]].grid(row=5, column=32)
                globals()[LED_List[345]].grid(row=6, column=32)
                globals()[LED_List[346]].grid(row=7, column=32)
                globals()[LED_List[347]].grid(row=7, column=33)
                globals()[LED_List[348]].grid(row=6, column=33)
                globals()[LED_List[349]].grid(row=5, column=33)
                globals()[LED_List[350]].grid(row=5, column=34)
                globals()[LED_List[351]].grid(row=6, column=34)
                globals()[LED_List[352]].grid(row=7, column=34)
                globals()[LED_List[353]].grid(row=7, column=35)
                globals()[LED_List[354]].grid(row=6, column=35)
                globals()[LED_List[355]].grid(row=5, column=35)
                globals()[LED_List[356]].grid(row=5, column=36)
                globals()[LED_List[357]].grid(row=6, column=36)
                globals()[LED_List[358]].grid(row=7, column=36)
                globals()[LED_List[359]].grid(row=7, column=37)
                globals()[LED_List[360]].grid(row=6, column=37)
                globals()[LED_List[361]].grid(row=5, column=37)
                globals()[LED_List[362]].grid(row=5, column=38)
                globals()[LED_List[363]].grid(row=6, column=38)
                globals()[LED_List[364]].grid(row=7, column=38)
                globals()[LED_List[365]].grid(row=7, column=39)
                globals()[LED_List[366]].grid(row=6, column=39)
                globals()[LED_List[367]].grid(row=5, column=39)
                globals()[LED_List[368]].grid(row=5, column=40)
                globals()[LED_List[369]].grid(row=6, column=40)
                globals()[LED_List[370]].grid(row=7, column=40)
                globals()[LED_List[371]].grid(row=7, column=41)
                globals()[LED_List[372]].grid(row=6, column=41)
                globals()[LED_List[373]].grid(row=5, column=41)
                globals()[LED_List[374]].grid(row=5, column=42)
                globals()[LED_List[375]].grid(row=6, column=42)
                globals()[LED_List[376]].grid(row=7, column=42)
                globals()[LED_List[377]].grid(row=7, column=43)
                globals()[LED_List[378]].grid(row=6, column=43)          
                globals()[LED_List[379]].grid(row=5, column=43)
                globals()[LED_List[380]].grid(row=5, column=44)
                globals()[LED_List[381]].grid(row=6, column=44)
                globals()[LED_List[382]].grid(row=7, column=44)          
                globals()[LED_List[383]].grid(row=6, column=45)

                #BS4 WidgetCluster
                globals()[LED_List[384]].grid(row=3, column=24)
                globals()[LED_List[385]].grid(row=2, column=25)
                globals()[LED_List[386]].grid(row=3, column=25)
                globals()[LED_List[387]].grid(row=3, column=26)
                globals()[LED_List[388]].grid(row=2, column=26)
                globals()[LED_List[389]].grid(row=1, column=26)
                globals()[LED_List[390]].grid(row=1, column=27)
                globals()[LED_List[391]].grid(row=3, column=27)
                globals()[LED_List[392]].grid(row=3, column=28)
                globals()[LED_List[393]].grid(row=2, column=28)
                globals()[LED_List[394]].grid(row=1, column=28)
                globals()[LED_List[395]].grid(row=1, column=29)
                globals()[LED_List[396]].grid(row=2, column=29)
                globals()[LED_List[397]].grid(row=3, column=29)
                globals()[LED_List[398]].grid(row=3, column=30)
                globals()[LED_List[399]].grid(row=2, column=30)
                globals()[LED_List[400]].grid(row=1, column=30)
                globals()[LED_List[401]].grid(row=1, column=31)
                globals()[LED_List[402]].grid(row=2, column=31)
                globals()[LED_List[403]].grid(row=3, column=31)
                globals()[LED_List[404]].grid(row=3, column=32)
                globals()[LED_List[405]].grid(row=2, column=32)
                globals()[LED_List[406]].grid(row=1, column=32)
                globals()[LED_List[407]].grid(row=1, column=33)
                globals()[LED_List[408]].grid(row=2, column=33)
                globals()[LED_List[409]].grid(row=3, column=33)
                globals()[LED_List[410]].grid(row=3, column=34)
                globals()[LED_List[411]].grid(row=2, column=34)
                globals()[LED_List[412]].grid(row=1, column=34)
                globals()[LED_List[413]].grid(row=1, column=35)
                globals()[LED_List[414]].grid(row=2, column=35)
                globals()[LED_List[415]].grid(row=3, column=35)
                globals()[LED_List[416]].grid(row=3, column=36)
                globals()[LED_List[417]].grid(row=2, column=36)
                globals()[LED_List[418]].grid(row=1, column=36)
                globals()[LED_List[419]].grid(row=1, column=37)
                globals()[LED_List[420]].grid(row=2, column=37)
                globals()[LED_List[421]].grid(row=3, column=37)
                globals()[LED_List[422]].grid(row=3, column=38)
                globals()[LED_List[423]].grid(row=2, column=38)
                globals()[LED_List[424]].grid(row=1, column=38)
                globals()[LED_List[425]].grid(row=1, column=39)
                globals()[LED_List[426]].grid(row=2, column=39)
                globals()[LED_List[427]].grid(row=3, column=39)
                globals()[LED_List[428]].grid(row=3, column=40)
                globals()[LED_List[429]].grid(row=2, column=40)
                globals()[LED_List[430]].grid(row=1, column=40)
                globals()[LED_List[431]].grid(row=1, column=41)
                globals()[LED_List[432]].grid(row=2, column=41)
                globals()[LED_List[433]].grid(row=3, column=41)
                globals()[LED_List[434]].grid(row=3, column=42)
                globals()[LED_List[435]].grid(row=2, column=42)
                globals()[LED_List[436]].grid(row=1, column=42)
                globals()[LED_List[437]].grid(row=1, column=43)
                globals()[LED_List[438]].grid(row=2, column=43)           
                globals()[LED_List[439]].grid(row=3, column=43)
                globals()[LED_List[440]].grid(row=3, column=44)
                globals()[LED_List[441]].grid(row=2, column=44)
                globals()[LED_List[442]].grid(row=1, column=44)          
                globals()[LED_List[443]].grid(row=2, column=45)

                #TS1 Widget Cluster
                globals()[LED_List[273]].grid(row=13, column=24)
                globals()[LED_List[274]].grid(row=14, column=24)
                globals()[LED_List[275]].grid(row=15, column=24)
                globals()[LED_List[276]].grid(row=15, column=25)
                globals()[LED_List[277]].grid(row=14, column=25)
                globals()[LED_List[278]].grid(row=13, column=25)
                globals()[LED_List[279]].grid(row=13, column=26)
                globals()[LED_List[280]].grid(row=15, column=26)
                globals()[LED_List[281]].grid(row=14, column=27)
                globals()[LED_List[282]].grid(row=13, column=28)        
                globals()[LED_List[283]].grid(row=14, column=28)
                globals()[LED_List[284]].grid(row=15, column=28)
                globals()[LED_List[285]].grid(row=15, column=29)
                globals()[LED_List[286]].grid(row=14, column=29)
                globals()[LED_List[287]].grid(row=13, column=29)
                globals()[LED_List[288]].grid(row=13, column=30)
                globals()[LED_List[289]].grid(row=14, column=30)
                globals()[LED_List[290]].grid(row=15, column=30)
                globals()[LED_List[291]].grid(row=15, column=31)
                globals()[LED_List[292]].grid(row=14, column=31)      
                globals()[LED_List[293]].grid(row=13, column=31)
                globals()[LED_List[294]].grid(row=13, column=32)
                globals()[LED_List[295]].grid(row=14, column=32)
                globals()[LED_List[296]].grid(row=15, column=32)
                globals()[LED_List[297]].grid(row=15, column=33)
                globals()[LED_List[298]].grid(row=14, column=33)
                globals()[LED_List[299]].grid(row=13, column=33)
                globals()[LED_List[300]].grid(row=13, column=34)
                globals()[LED_List[301]].grid(row=14, column=34)
                globals()[LED_List[302]].grid(row=15, column=34)       
                globals()[LED_List[303]].grid(row=15, column=35)
                globals()[LED_List[304]].grid(row=14, column=35)
                globals()[LED_List[305]].grid(row=13, column=35)
                globals()[LED_List[306]].grid(row=13, column=36)
                globals()[LED_List[307]].grid(row=14, column=36)
                globals()[LED_List[308]].grid(row=15, column=36)
                globals()[LED_List[309]].grid(row=15, column=37)
                globals()[LED_List[310]].grid(row=14, column=37)
                globals()[LED_List[311]].grid(row=13, column=37)           
                globals()[LED_List[312]].grid(row=13, column=38)   
                globals()[LED_List[313]].grid(row=14, column=38)
                globals()[LED_List[314]].grid(row=15, column=38)
                globals()[LED_List[315]].grid(row=15, column=39)
                globals()[LED_List[316]].grid(row=14, column=39)
                globals()[LED_List[317]].grid(row=13, column=39)
                globals()[LED_List[318]].grid(row=13, column=40)
                globals()[LED_List[319]].grid(row=14, column=40)
                globals()[LED_List[320]].grid(row=15, column=40)
                globals()[LED_List[321]].grid(row=15, column=41)
                globals()[LED_List[322]].grid(row=14, column=41)
                globals()[LED_List[323]].grid(row=13, column=41)

                #TS2 Widget Cluster
                globals()[LED_List[222]].grid(row=9, column=24)
                globals()[LED_List[223]].grid(row=10, column=24)
                globals()[LED_List[224]].grid(row=11, column=24)
                globals()[LED_List[225]].grid(row=11, column=25)
                globals()[LED_List[226]].grid(row=10, column=25)
                globals()[LED_List[227]].grid(row=9, column=25)
                globals()[LED_List[228]].grid(row=9, column=26)
                globals()[LED_List[229]].grid(row=11, column=26)
                globals()[LED_List[230]].grid(row=10, column=27)
                globals()[LED_List[231]].grid(row=9, column=28)       
                globals()[LED_List[232]].grid(row=10, column=28)
                globals()[LED_List[233]].grid(row=11, column=28)
                globals()[LED_List[234]].grid(row=11, column=29)
                globals()[LED_List[235]].grid(row=10, column=29)
                globals()[LED_List[236]].grid(row=9, column=29)
                globals()[LED_List[237]].grid(row=9, column=30)
                globals()[LED_List[238]].grid(row=10, column=30)
                globals()[LED_List[239]].grid(row=11, column=30)
                globals()[LED_List[240]].grid(row=11, column=31)
                globals()[LED_List[241]].grid(row=10, column=31)        
                globals()[LED_List[242]].grid(row=9, column=31)
                globals()[LED_List[243]].grid(row=9, column=32)
                globals()[LED_List[244]].grid(row=10, column=32)
                globals()[LED_List[245]].grid(row=11, column=32)
                globals()[LED_List[246]].grid(row=11, column=33)
                globals()[LED_List[247]].grid(row=10, column=33)
                globals()[LED_List[248]].grid(row=9, column=33)
                globals()[LED_List[249]].grid(row=9, column=34)
                globals()[LED_List[250]].grid(row=10, column=34)
                globals()[LED_List[251]].grid(row=11, column=34)       
                globals()[LED_List[252]].grid(row=11, column=35)
                globals()[LED_List[253]].grid(row=10, column=35)
                globals()[LED_List[254]].grid(row=9, column=35)
                globals()[LED_List[255]].grid(row=9, column=36)
                globals()[LED_List[256]].grid(row=10, column=36)
                globals()[LED_List[257]].grid(row=11, column=36)
                globals()[LED_List[258]].grid(row=11, column=37)
                globals()[LED_List[259]].grid(row=10, column=37)
                globals()[LED_List[260]].grid(row=9, column=37)           
                globals()[LED_List[261]].grid(row=9, column=38)   
                globals()[LED_List[262]].grid(row=10, column=38)
                globals()[LED_List[263]].grid(row=11, column=38)
                globals()[LED_List[264]].grid(row=11, column=39)
                globals()[LED_List[265]].grid(row=10, column=39)
                globals()[LED_List[266]].grid(row=9, column=39)
                globals()[LED_List[267]].grid(row=9, column=40)
                globals()[LED_List[268]].grid(row=10, column=40)
                globals()[LED_List[269]].grid(row=11, column=40)
                globals()[LED_List[270]].grid(row=11, column=41)
                globals()[LED_List[271]].grid(row=10, column=41)
                globals()[LED_List[272]].grid(row=9, column=41)

                #TS3 Widget Cluster          
                globals()[LED_List[120]].grid(row=15, column=22)       
                globals()[LED_List[121]].grid(row=14, column=22)
                globals()[LED_List[122]].grid(row=13, column=22)
                globals()[LED_List[123]].grid(row=13, column=21)
                globals()[LED_List[124]].grid(row=14, column=21)
                globals()[LED_List[125]].grid(row=15, column=21)
                globals()[LED_List[126]].grid(row=15, column=20)
                globals()[LED_List[127]].grid(row=13, column=20)
                globals()[LED_List[128]].grid(row=14, column=19)
                globals()[LED_List[129]].grid(row=15, column=18)
                globals()[LED_List[130]].grid(row=14, column=18)       
                globals()[LED_List[131]].grid(row=13, column=18)
                globals()[LED_List[132]].grid(row=13, column=17)
                globals()[LED_List[133]].grid(row=14, column=17)
                globals()[LED_List[134]].grid(row=15, column=17)
                globals()[LED_List[135]].grid(row=15, column=16)
                globals()[LED_List[136]].grid(row=14, column=16)
                globals()[LED_List[137]].grid(row=13, column=16)
                globals()[LED_List[138]].grid(row=13, column=15)
                globals()[LED_List[139]].grid(row=14, column=15)
                globals()[LED_List[140]].grid(row=15, column=15)       
                globals()[LED_List[141]].grid(row=15, column=14)
                globals()[LED_List[142]].grid(row=14, column=14)
                globals()[LED_List[143]].grid(row=13, column=14)
                globals()[LED_List[144]].grid(row=13, column=13)
                globals()[LED_List[145]].grid(row=14, column=13)
                globals()[LED_List[146]].grid(row=15, column=13)
                globals()[LED_List[147]].grid(row=15, column=12)
                globals()[LED_List[148]].grid(row=14, column=12)
                globals()[LED_List[149]].grid(row=13, column=12)
                globals()[LED_List[150]].grid(row=13, column=11)     
                globals()[LED_List[151]].grid(row=14, column=11)
                globals()[LED_List[152]].grid(row=15, column=11)
                globals()[LED_List[153]].grid(row=15, column=10)
                globals()[LED_List[154]].grid(row=14, column=10)
                globals()[LED_List[155]].grid(row=13, column=10)
                globals()[LED_List[156]].grid(row=13, column=9)
                globals()[LED_List[157]].grid(row=14, column=9)
                globals()[LED_List[158]].grid(row=15, column=9)
                globals()[LED_List[159]].grid(row=15, column=8)           
                globals()[LED_List[160]].grid(row=14, column=8)   
                globals()[LED_List[161]].grid(row=13, column=8)
                globals()[LED_List[162]].grid(row=13, column=7)
                globals()[LED_List[163]].grid(row=14, column=7)
                globals()[LED_List[164]].grid(row=15, column=7)
                globals()[LED_List[165]].grid(row=15, column=6)
                globals()[LED_List[166]].grid(row=14, column=6)
                globals()[LED_List[167]].grid(row=13, column=6)
                globals()[LED_List[168]].grid(row=13, column=5)
                globals()[LED_List[169]].grid(row=14, column=5)
                globals()[LED_List[170]].grid(row=15, column=5)

                #TS4 Widget Cluster
                globals()[LED_List[171]].grid(row=11, column=22)        
                globals()[LED_List[172]].grid(row=10, column=22)
                globals()[LED_List[173]].grid(row=9, column=22)
                globals()[LED_List[174]].grid(row=9, column=21)
                globals()[LED_List[175]].grid(row=10, column=21)
                globals()[LED_List[176]].grid(row=11, column=21)
                globals()[LED_List[177]].grid(row=11, column=20)
                globals()[LED_List[178]].grid(row=9, column=20)
                globals()[LED_List[179]].grid(row=10, column=19)
                globals()[LED_List[180]].grid(row=11, column=18)
                globals()[LED_List[181]].grid(row=10, column=18)       
                globals()[LED_List[182]].grid(row=9, column=18)
                globals()[LED_List[183]].grid(row=9, column=17)
                globals()[LED_List[184]].grid(row=10, column=17)
                globals()[LED_List[185]].grid(row=11, column=17)
                globals()[LED_List[186]].grid(row=11, column=16)
                globals()[LED_List[187]].grid(row=10, column=16)
                globals()[LED_List[188]].grid(row=9, column=16)
                globals()[LED_List[189]].grid(row=9, column=15)
                globals()[LED_List[190]].grid(row=10, column=15)
                globals()[LED_List[191]].grid(row=11, column=15)        
                globals()[LED_List[192]].grid(row=11, column=14)
                globals()[LED_List[193]].grid(row=10, column=14)
                globals()[LED_List[194]].grid(row=9, column=14)
                globals()[LED_List[195]].grid(row=9, column=13)
                globals()[LED_List[196]].grid(row=10, column=13)
                globals()[LED_List[197]].grid(row=11, column=13)
                globals()[LED_List[198]].grid(row=11, column=12)
                globals()[LED_List[199]].grid(row=10, column=12)
                globals()[LED_List[200]].grid(row=9, column=12)
                globals()[LED_List[201]].grid(row=9, column=11)        
                globals()[LED_List[202]].grid(row=10, column=11)
                globals()[LED_List[203]].grid(row=11, column=11)
                globals()[LED_List[204]].grid(row=11, column=10)
                globals()[LED_List[205]].grid(row=10, column=10)
                globals()[LED_List[206]].grid(row=9, column=10)
                globals()[LED_List[207]].grid(row=9, column=9)
                globals()[LED_List[208]].grid(row=10, column=9)
                globals()[LED_List[209]].grid(row=11, column=9)
                globals()[LED_List[210]].grid(row=11, column=8)           
                globals()[LED_List[211]].grid(row=10, column=8)   
                globals()[LED_List[212]].grid(row=9, column=8)
                globals()[LED_List[213]].grid(row=9, column=7)
                globals()[LED_List[214]].grid(row=10, column=7)
                globals()[LED_List[215]].grid(row=11, column=7)
                globals()[LED_List[216]].grid(row=11, column=6)
                globals()[LED_List[217]].grid(row=10, column=6)
                globals()[LED_List[218]].grid(row=9, column=6)
                globals()[LED_List[219]].grid(row=9, column=5)
                globals()[LED_List[220]].grid(row=10, column=5)
                globals()[LED_List[221]].grid(row=11, column=5)


    #Search for Bluetooth COM Ports on the Computer
    def find_comports(self):    #Find Avaliable COM Ports
        try:
            global COMport_start_text
            COMport_start_text = StringVar(self)
            COMport_start_text.set("COM Port")

            global COMport_results
            COMport_results = ['']                                                               
            ports = serial.tools.list_ports.comports()
            for port, _desc, _hwin in sorted(ports):
                COMport_results.append(port)

        except:
            messagebox.showwarning('Warning','Could not find COM Ports')

    def Configure_FUNC(self):
        self.Create_Packets()
        self.Send_Packets()

    def Create_Packets(self):
        #Create a List of FastLED compadible LED codes
            CLC = []            
            for _key,value in set_color.items():
                CLC.append(str(value[0:8]))

        #Fill Packet 1 (Controller variables to define function)
            global Packet_1
            Packet_1 = 'NEW,'
            
        #Fill Packet 2 (Motor 2 Bottom LED Section)
            global Packet_2
            Packet_2 = ' ,'
            i=0 #Starting LED Number
            while i <= 59:
                Packet_2 += str(CLC[i])
                Packet_2 += ','
                i += 1

        #Fill Packet 3 (Motor 1 Bottom LED Section)
            global Packet_3
            Packet_3 = ' ,'
            i=60 #Starting LED Number
            while i <= 119:
                Packet_3 += str(CLC[i])
                Packet_3 += ','
                i += 1
        
        #Fill Packet 4 (Motor _ Top LED Section)
            global Packet_4
            Packet_4 = ' ,'
            i=120
            while i <= 170:
                Packet_4 += str(CLC[i])
                Packet_4 += ','
                i += 1

        #Fill Packet 5 (Motor _ Top LED Section)
            global Packet_5
            Packet_5 = ' ,'
            i=171
            while i <= 221:
                Packet_5 += str(CLC[i])
                Packet_5 += ','
                i += 1

        #Fill Packet 6 (Motor _ Top LED Section)
            global Packet_6
            Packet_6 = ' ,'
            i=222
            while i <= 272:
                Packet_6 += str(CLC[i])
                Packet_6 += ','
                i += 1
            
        #Fill Packet 7 (Motor _ Top LED Section)
            global Packet_7
            Packet_7 = ' ,'
            i=273
            while i <= 323:
                Packet_7 += str(CLC[i])
                Packet_7 += ','
                i += 1

        #Fill Packet 8 (Motor _ Bottom LED Section)
            global Packet_8
            Packet_8 = ' ,'
            i=324
            while i <= 383:
                Packet_8 += str(CLC[i])
                Packet_8 += ','
                i += 1
            
        #Fill Packet 9 (Motor _ Bottom LED Section)
            global Packet_9
            Packet_9 = ' ,'
            i=384
            while i <= 443:
                Packet_9 += str(CLC[i])
                Packet_9 += ','
                i += 1

    def Send_Packets(self):

        #Send the Data to the LED Controller
            try:
                Serial_Port = serial.Serial(COMport_start_text.get())
                Encoded_Packet_1 = Packet_1.encode()
                Encoded_Packet_2 = Packet_2.encode()
                Encoded_Packet_3 = Packet_3.encode()
                Encoded_Packet_4 = Packet_4.encode()
                Encoded_Packet_5 = Packet_5.encode()
                Encoded_Packet_6 = Packet_6.encode()
                Encoded_Packet_7 = Packet_7.encode()
                Encoded_Packet_8 = Packet_8.encode()
                Encoded_Packet_9 = Packet_9.encode()
            
                Serial_Port.write(Encoded_Packet_1)           
                time.sleep(2)
                Serial_Port.write(Encoded_Packet_2)
                time.sleep(2)
                Serial_Port.write(Encoded_Packet_3)
                time.sleep(2)
                Serial_Port.write(Encoded_Packet_4)
                time.sleep(2)
                Serial_Port.write(Encoded_Packet_5)  
                time.sleep(2)
                Serial_Port.write(Encoded_Packet_6)
                time.sleep(2)
                Serial_Port.write(Encoded_Packet_7)
                time.sleep(2)
                Serial_Port.write(Encoded_Packet_8)
                time.sleep(2)
                Serial_Port.write(Encoded_Packet_9)
                time.sleep(2)
                messagebox.showinfo('Success','Data Successfully Sent to R4LA')
            except:
                messagebox.showwarning('Warning','Could not connect to R4LA')

    def Fill_Colors_FUNC(self):    #Update the UI with the filled LED color
        i=0
        for key, _val in set_color.items():  
            UI_ledcolor = '#' + FastLED_color[2:8]
            set_color[key] = FastLED_color
        while i <=443:
            globals()[LED_List[i]].config(bg=UI_ledcolor,fg=UI_ledcolor)
            i=i+1
        else:
            pass
    
    def openColorDialog(self):  #Color Chooser Box
        colorDialog = tkinter.colorchooser.Chooser(self)
        color = colorDialog.show()
        
        # show the chosen RBG value
        global led_color
        led_color = color[1]
        global FastLED_color
        FastLED_color = "0x"+led_color[1:7]
        color_preview.config(bg=led_color)
    
    def Change_LED_Color_FUNC(self,event):  #Changes the Preview LED Color and set the color in the dictionary
        try: #Run if a color was selected
            event.widget.config(bg=led_color, fg=led_color)
            set_color[event.widget['text']] = FastLED_color
        except: #Run if no color was selected
            event.widget.config(bg='#000000', fg='#000000')
            set_color[event.widget['text']] = '0x000000'

    def Clear_LED_Colors_FUNC(self):     #Clear All LED Colors
        for key, _val in set_color.items():  
            globals()[key].config(bg='#000000',fg='#000000')
            set_color[key] = '0x000000'

            #------------------------------------------------------------------------------------#


#----------------------------------------------Connected Page---------------------------------------------------#
  
class Update_Firmware(tk.Frame): 
      
    def __init__(self, parent, controller): 
          
        tk.Frame.__init__(self, parent)
  
# Driver Code 
app = tkinterApp()              #Start the main program class
app.geometry('1400x817')        #Define the start window size
app.title('R4LA Configurator')
app.mainloop()                  #Run the tkinter gui builder