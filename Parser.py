from tkinter import *
from tkinter import filedialog
import json
import csv
from pprint import pprint

class Myapp:

    Data = None # geojson Data(raw)
    parseData = None # parsed Data from geojson file
    savejson = True # init
    savecsv = False

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
        attribute_buttons = ["type","name","ALIAS","REMARK","NTFDATE","SGG_OID","COL_ADM_SE","CoreNum","area",
                            "perimeter","category","geometry"]

        # button frame 생성
        self.file_button_frame = Frame(self.button_frame,borderwidth=5)
        self.format_button_frame = Frame(self.button_frame,borderwidth=5)
        self.attribute_button_frame = Frame(self.button_frame,borderwidth=15)

        self.file_button_frame.pack(side=LEFT,expand=YES,fill=Y,anchor=N)
        self.format_button_frame.pack(side=LEFT,expand=YES,anchor=N)
        self.attribute_button_frame.pack(side=LEFT,expand=YES,anchor=N)

        Label(self.file_button_frame,text="about\nfile").pack()
        Label(self.format_button_frame,text="file\nformat").pack()
        Label(self.attribute_button_frame,text="select\nattribute").pack()

        # file_button_frame button

        # file load button
        self.load_file_button = Button(self.file_button_frame,text="load",
                                       width=button_width,padx=button_padx,pady=button_pady)

        self.load_file_button.pack(side=TOP)
        self.load_file_button.bind("<Button-1>",self.processOK)

        # file save button
        self.save_file_button = Button(self.file_button_frame,text="save",
                                       width=button_width,padx=button_padx,pady=button_pady)
        self.save_file_button.pack(side=TOP)
        self.save_file_button.bind("<Button-1>",self.savefile)

        # data show button
        self.show_button = Button(self.file_button_frame,text="show",
                                  width=button_width, padx=button_padx, pady=button_pady)
        self.show_button.pack(side=TOP)
        self.show_button.bind("<Button-1>",self.showData)

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
        self.cancel_button_frame = Frame(self.left_frame)
        self.cancel_button_frame.pack(side=BOTTOM, expand=YES, anchor=SW)
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

    """
    function processOK:
    file load 함수 - geojson파일만 해당
    """
    def processOK(self,event):

        open_file_path = filedialog.askopenfilenames(initialdir="C:/Users/LG/Downloads/Swallaby_DATA/Park_Transform",
                                                   title="choose your file",
                                                   filetypes=(("geojson files", "*.geojson"), ("all files", "*.*")))

        open_file_path = ''.join(open_file_path) # format convert to str(string)

        with open(open_file_path,'rt',encoding='UTF8') as f:
            self.Data = json.load(f)


        for feature in self.Data['features']:
            self.parseData = feature.get('properties')


        pprint(self.parseData)

    """
     function savefile:
     save buttion click:event
     boolean 변수값을 확인 후 parseData를 
     geojson 또는 csv파일로 저장
    """
    def savefile(self,event):

        if self.savejson is True and self.savecsv is False:
            SaveFilePath = filedialog.askopenfilenames(initialdir="C:/Users",
                                                        title="save file",
                                                        filetypes=(("geojson files","*.geojson"),("all files","*.*")))
            SaveFilePath = ''.join(SaveFilePath)
            print(self.savejson)
            print(self.savecsv)
            self.initValue()

        elif self.savejson is False and self.savecsv is True:
            SaveFilePath = filedialog.askopenfilenames()

            SaveFilePath = ''.join(SaveFilePath)
            print(self.savejson)
            print(self.savecsv)
            self.initValue()

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


    def showData(self,event):
        pprint(self.parseData)
        json.dumps(self.parseData)


root = Tk()
root.title("geojson Parser")

myapp = Myapp(root)
root.mainloop()