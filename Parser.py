from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import json
import csv
from pprint import pprint

class Myapp:

    Data = None # geojson Data(raw)
    parseData = None # parsed Data from geojson file
    savejson = True # init
    savecsv = False
    file_loaded = False

    type = False
    name = False
    ALIAS = False
    REMARK = False
    NTFDATE = False
    SGG_OID = False
    COL_ADM_SE = False
    CoreNum = False
    area = False
    perimeter = False
    category = False
    geometry = False

    # GUI widgets
    def __init__(self,parent):

        attribute_button_width = 10
        button_width = 6
        button_padx = "2m"
        button_pady = "1m"

        self.fb = IntVar() # for format button
        self.fb.set(0) # initializing the choice, i.e. Geojson

        self.myparent = parent
        self.myparent.geometry("640x500")

        self.myContainer = Frame(parent)
        self.myContainer.pack(expand=YES,fill=BOTH)

        # left frame
        self.left_frame = Frame(self.myContainer)
        self.left_frame.pack(side=LEFT,expand=NO,padx=10, pady=5, ipadx=5, ipady=5)

        # Message Frame:LEFTSide
        introMsg = "geojson Parser\ncheck attribute you want to parse\nSwallaby Inc."
        Label(self.left_frame,text=introMsg,justify=LEFT).pack(side=TOP,anchor=W)

        # Button Container - Frame:LeftSide
        self.button_frame = Frame(self.left_frame)
        self.button_frame.pack(side=TOP,expand=NO,fill=Y, ipadx=5, ipady=5)

        # output container - frame:rightSide
        self.right_frame = Frame(self.myContainer,background="white")
        self.right_frame.pack(side=RIGHT,expand=YES,fill=BOTH)


        # button
        format_buttons = ["geojson","csv"]

        # button frame 생성
        self.file_button_frame = Frame(self.button_frame,borderwidth=5)
        self.format_button_frame = Frame(self.button_frame,borderwidth=5)
        self.attribute_button_frame = Frame(self.button_frame,borderwidth=15)

        self.file_button_frame.pack(side=LEFT,expand=YES,fill=Y,anchor=N)
        self.format_button_frame.pack(side=LEFT,expand=YES,anchor=N)
        self.attribute_button_frame.pack(side=LEFT,expand=YES,anchor=N)

        Label(self.file_button_frame,text="about\nfile").pack()
        Label(self.format_button_frame,text="file\nformat").pack()
        Label(self.attribute_button_frame,text="select").pack()

        # file_button_frame button

        # file load button
        self.load_file_button = Button(self.file_button_frame,text="load",
                                       width=button_width,padx=button_padx,pady=button_pady)

        self.load_file_button.pack(side=TOP)
        self.load_file_button.bind("<Button-1>",self.processOK)

        # data show button
        self.parse_button = Button(self.file_button_frame, text="parse",
                                   width=button_width, padx=button_padx, pady=button_pady)
        self.parse_button.pack(side=TOP)
        self.parse_button.bind("<Button-1>", self.dataParser)

        # file save button
        self.save_file_button = Button(self.file_button_frame,text="save",
                                       width=button_width,padx=button_padx,pady=button_pady)
        self.save_file_button.pack(side=TOP)
        self.save_file_button.bind("<Button-1>",self.savefile)

        # file_format frame button: RadioButton
        for var,format_button in enumerate(format_buttons):
            button = Radiobutton(self.format_button_frame,
                                text=format_button,
                                indicatoron=1,
                                variable= self.fb,
                                command = self.setFormat,
                                value= var)
            button.pack(side=TOP,anchor=W)



        # attribute button : CheckBox
        '''
        for var,option in enumerate(attribute_buttons):
            button = Checkbutton(self.attribute_button_frame,
                                 text=str(option),
                                 anchor=W
                                 ) # more to do

            button["width"] = attribute_button_width # 10
            button.pack(side=TOP,anchor=W)
        '''
        type_button = Checkbutton(self.attribute_button_frame,
                                  text='type',
                                  anchor=W,
                                  command=self.setType,
                                  width=attribute_button_width).pack(side=TOP)

        name_button = Checkbutton(self.attribute_button_frame,
                                  text='name',
                                  anchor=W,
                                  command=self.setName,
                                  width=attribute_button_width).pack(side=TOP)

        ALIAS_button = Checkbutton(self.attribute_button_frame,
                                  text='ALIAS',
                                  anchor=W,
                                   command=self.setALIAS,
                                  width=attribute_button_width).pack(side=TOP)

        REMARK_button = Checkbutton(self.attribute_button_frame,
                                  text='REMARK',
                                  anchor=W,
                                  command=self.setRemark,
                                  width=attribute_button_width).pack(side=TOP)

        NTFDATE_button = Checkbutton(self.attribute_button_frame,
                                  text='NTFDATE',
                                  anchor=W,
                                  command=self.setNTFDATE,
                                  width=attribute_button_width).pack(side=TOP)

        SGG_OID_button = Checkbutton(self.attribute_button_frame,
                                  text='SGG_OID',
                                  anchor=W,
                                  command=self.setSGG_OID,
                                  width=attribute_button_width).pack(side=TOP)

        COL_ASM_SE_button = Checkbutton(self.attribute_button_frame,
                                  text='COL_ASM_SE',
                                  anchor=W,
                                  command=self.setCOL_ADM_SE,
                                  width=attribute_button_width).pack(side=TOP)

        CoreNum_button = Checkbutton(self.attribute_button_frame,
                                  text='type',
                                  anchor=W,
                                  command=self.setCoreNum,
                                  width=attribute_button_width).pack(side=TOP)

        area_button = Checkbutton(self.attribute_button_frame,
                                  text='area',
                                  anchor=W,
                                  command=self.setArea,
                                  width=attribute_button_width).pack(side=TOP)

        perimeter_button = Checkbutton(self.attribute_button_frame,
                                  text='perimeter',
                                  anchor=W,
                                  command=self.setPerimeter,
                                  width=attribute_button_width).pack(side=TOP)

        category_button = Checkbutton(self.attribute_button_frame,
                                  text='category',
                                  anchor=W,
                                  command=self.setCategory,
                                  width=attribute_button_width).pack(side=TOP)

        geometry_button = Checkbutton(self.attribute_button_frame,
                                  text='geometry',
                                  anchor=W,
                                  command=self.setGeometry,
                                  width=attribute_button_width).pack(side=TOP)
        # Exit Button

        # frame 생성
        self.cancel_button_frame = Frame(self.left_frame)
        self.cancel_button_frame.pack(side=BOTTOM, expand=YES, anchor=SW)

        # exit button 생성
        self.cancel_button = Button(self.cancel_button_frame ,text="exit",
                                    width = button_width, padx=button_padx, pady=button_pady)

        self.cancel_button.pack(side=BOTTOM, anchor=S)

        self.cancel_button.bind("<Button-1>",self.processCancel) # exit button event
        self.cancel_button.bind("<Return>",self.processCancel)  # exit button event

        # Text Widget - Show Parsed Data
        data_text = Text(self.right_frame,width=100)
        data_text.pack(side=TOP,fill=BOTH,expand=YES)
        data_text.insert(END,"데헷")

        # right_frame : scroll bar 생성
        yscrollbar = Scrollbar(data_text)
        yscrollbar.pack(side=RIGHT, fill=Y)
        yscrollbar.config(command=data_text.yview)

    # end GUI widgets

    # functions
    """
    function processOK:
    file load method - geojson valid
    """
    def processOK(self,event):

        try:

            open_file_path = filedialog.askopenfilenames(initialdir="C:/Users/LG/Downloads/Swallaby_DATA/Park_Transform",
                                                         title="choose your file",
                                                         filetypes=(("geojson files", "*.geojson"), ("all files", "*.*")))

            open_file_path = ''.join(open_file_path) # format convert to str(string)

            with open(open_file_path,'rt',encoding='UTF8') as f: # exception handling
                self.Data = json.load(f)
                print(type(self.Data))
        except FileNotFoundError as e:

            messagebox.showwarning("File load Warning","No File loaded:\n"+str(e)) # alert Error Msg.

        else:

            #pprint(self.Data)
            self.file_loaded = True
            self.showData()
            messagebox.showinfo("Success","Successfully loaded:\n"+open_file_path)
            f.close()

    """
     function savefile:
     save buttion click:event
     boolean var: savejson,savecsv 확인 후 parseData를 
     geojson 또는 csv파일로 저장
    """
    def savefile(self,event):

        if self.file_loaded is False:

          messagebox.showinfo("Error","No geojson file loaded")

        elif self.savejson is True and self.savecsv is False:
            SaveFilePath = filedialog.askopenfilenames(initialdir="C:/Users",
                                                        title="save file",
                                                        filetypes=(("geojson files","*.geojson"),("all files","*.*")))
            SaveFilePath = ''.join(SaveFilePath)
            print(self.savejson)
            print(self.savecsv)

            self.initValue()

        elif self.savejson is False and self.savecsv is True:
            SaveFilePath = filedialog.askopenfilenames(initialdir="C:/Users",
                                                       title="save file",
                                                       filetypes=(("csv files","*.csv"),("all files","*.*")))
            SaveFilePath = ''.join(SaveFilePath)
            print(self.savejson)
            print(self.savecsv)

            self.initValue()

    # attribute 변경 함수들
    def setType(self):
        self.type = not self.type
        print(self.type)

    def setName(self):
        self.name = not self.name
        print(self.name)

    def setALIAS(self):
        self.ALIAS = not self.ALIAS
        print(self.ALIAS)

    def setRemark(self):
        self.REMARK = not self.REMARK
        print(self.REMARK)

    def setNTFDATE(self):
        self.NTFDATE = not self.NTFDATE
        print(self.NTFDATE)

    def setSGG_OID(self):
        self.SGG_OID = not self.SGG_OID
        print(self.SGG_OID)

    def setCOL_ADM_SE(self):
        self.COL_ADM_SE = not self.COL_ADM_SE
        print(self.COL_ADM_SE)

    def setCoreNum(self):
        self.CoreNum = not self.CoreNum
        print(self.CoreNum)

    def setArea(self):
        self.area = not self.area
        print(self.area)

    def setPerimeter(self):
        self.perimeter = not self.perimeter
        print(self.perimeter)

    def setCategory(self):
        self.category = not self.category
        print(self.category)

    def setGeometry(self):
        self.geometry = not self.geometry
        print(self.geometry)
    """
    function processCancel:
    exit button click:event
    프로세스 종료
    """
    def processCancel(self,event):
        self.myparent.destroy()

    """
    function initValue
    boolean 변수를 초기값으로 설정
    """
    def initValue(self):

        self.savejson = True
        self.savecsv = False

        self.type = False
        self.name = False
        self.ALIAS = False
        self.REMARK = False
        self.NTFDATE = False
        self.SGG_OID = False
        self.COL_ADM_SE = False
        self.CoreNum = False
        self.area = False
        self.perimeter = False
        self.category = False
        self.geometry = False
    """
    function setFormat:
    radiobuttion click(geojson,csv):
    저장할 file format 설정
    """
    def setFormat(self):

        if self.fb.get() is 0:

            self.savejson = True
            self.savecsv = False
            print("save file format:geojson")

        elif self.fb.get() is 1:

            self.savecsv = True
            self.savejson = False
            print("save file format:CSV")


    def showData(self):

        if self.Data is None:
            messagebox.showerror("Error", "no geojson file loaded")

    def dataParser(self,event):
        if self.Data is None:
            messagebox.showwarning("Warning","님 파일로드 안했다니깐...")
        else:
            print("Data Parse Logic Start")

            if self.geometry is False:
                for element in self.Data:
                    element.pop('geometry',None) # 고쳐라

            pprint(self.Data)

    # end Functions


root = Tk()
root.title("geojson Parser")

myapp = Myapp(root)
root.mainloop()