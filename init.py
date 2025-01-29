from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout, QVBoxLayout, QFrame, QPushButton, QTabWidget, QLabel, QGroupBox, QColorDialog
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from shiboken6 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds

def get_maya_window():
    get_window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(get_window), QMainWindow)

class EDG707_002(QMainWindow):
    def __init__(self):
        super(EDG707_002, self).__init__(get_maya_window())
        self.setWindowTitle("EDG AutoRig Assistant")
        self.setMaximumSize(400, 600)
        self.setWindowFlag(Qt.Tool)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame_layout = QVBoxLayout(frame)
        main_layout.addWidget(frame)


        logo = QLabel("EDG")
        logo.setAlignment(Qt.AlignCenter)
        frame_layout.addWidget(logo)

        #Tab Set
        tab_widget = QTabWidget()
        frame_layout.addWidget(tab_widget)

        #Tab 1
        tab_1 = QWidget()
        tab1_layout = QVBoxLayout(tab_1)
        
        #
        jnt_manip_grp = QGroupBox("Joint's Manipulators")
        jnt_manip_grp.setAlignment(Qt.AlignCenter)
        jnt_manip_grp_layout = QGridLayout(jnt_manip_grp)

        ikCreate_button = QPushButton("Create IK")
        poleV_button = QPushButton("Create Pole Vector")
        ribbon_tool = QPushButton("Create Ribbon")
        axis_vis = QPushButton("Local Axis Visibility")

        jnt_manip_grp_layout.addWidget(ikCreate_button, 0, 0)
        jnt_manip_grp_layout.addWidget(poleV_button, 0, 1)
        jnt_manip_grp_layout.addWidget(ribbon_tool, 1, 0)
        jnt_manip_grp_layout.addWidget(axis_vis, 1, 1)
        
        #
        ctrl_grp = QGroupBox("Controls Editor")
        ctrl_grp.setAlignment(Qt.AlignCenter)
        ctrl_grp_layout = QGridLayout(ctrl_grp)
        
        controller_button = QPushButton("Create Controller")
        grouping_button = QPushButton("Create Groups")

        ctrl_grp_layout.addWidget(controller_button, 0, 0)
        ctrl_grp_layout.addWidget(grouping_button, 0, 1)
        
        #
        color_grp = QGroupBox("Color Override")
        color_grp.setAlignment(Qt.AlignCenter)
        color_grp_layout = QVBoxLayout(color_grp)
        
        override_color = QPushButton("Change Controller Color")
        color_grp_layout.addWidget(override_color)
        
        #
        tab1_layout.addWidget(jnt_manip_grp)
        tab1_layout.addWidget(ctrl_grp)
        tab1_layout.addWidget(color_grp)
        
        tab_widget.addTab(tab_1, "AutoRig")

        #Tab 2
        tab_2 = QWidget()
        tab_2_layout = QVBoxLayout(tab_2)

        sel_grp = QGroupBox("Selection Tools")
        sel_grp.setAlignment(Qt.AlignCenter)
        sel_grp_layout = QVBoxLayout(sel_grp)

        tab_2_layout.addWidget(sel_grp)

        sel_grp.setMaximumSize(400, 120)

        sel_name_btn = QPushButton("Select by Name")
        ren_all_btn = QPushButton("Rename All")
        ren_manip_btn = QPushButton("Rename Manip")

        sel_grp_layout.addWidget(sel_name_btn)
        sel_grp_layout.addWidget(ren_all_btn)
        sel_grp_layout.addWidget(ren_manip_btn)
        
        ikCreate_button.clicked.connect(self.create_IK)
        poleV_button.clicked.connect(self.create_PoleVector)
        override_color.clicked.connect(self.controller_color)
        axis_vis.clicked.connect(self.toggle_Axis_Display_Joints)

        controller_button.clicked.connect(self.create_Controller)
        grouping_button.clicked.connect(self.create_Group)
        ribbon_tool.clicked.connect(self.show_outliner_tool)
        sel_name_btn.clicked.connect(self.sel_Tool)

        tab_widget.addTab(tab_2, "Selection")

    def controller_color(self):
        palette = QColorDialog.getColor()

        color = [palette.red()/255, palette.green()/255, palette.blue()/255]

        sel = cmds.ls(sl=1)
        for i in sel:
            shapes = cmds.listRelatives(i, s=1, f=1)
            for i in shapes:
                cmds.setAttr(f"{i}.overrideEnabled", 1)
                cmds.setAttr(f"{i}.overrideRGBColors", 1)
                cmds.setAttr(f"{i}.overrideColorRGB", color[0], color[1], color[2])

    def toggle_Axis_Display_Joints(self):
   
        jointList = cmds.ls(sl=1, type="joint")
		
        if len(jointList) == 0:
            jointList = cmds.ls(type="joint")
        for jnt in jointList:
            currentStateJnts = cmds.getAttr(jnt + ".displayLocalAxis")
            cmds.setAttr(jnt + ".displayLocalAxis", not currentStateJnts)

    def show_outliner_tool(self):
        
        self.popup = Selection_Tools(self)
        self.popup.setWindowFlags(Qt.Window)
        self.popup.show()

    def find_perf_vect(self):
        sel = cmds.ls(sl=1, type="joint")

        #Joints' vector
        f_Vec = cmds.xform(sel[0], q=1, ws=1,t=1)
        s_Vec = cmds.xform(sel[1], q=1, ws=1, t=1)
        t_Vec = cmds.xform(sel[2], q=1, ws=1,t=1)

        #Vector between two joints
        f_s_Vec = [s_Vec[i] - f_Vec[i] for i in range(3)]
        f_t_Vec = [t_Vec[i] - f_Vec[i] for i in range(3)]

        #The calculation of projection of vector a on vector b
        dot_Product = sum(f_s_Vec[i] * f_t_Vec[i] for i in range(3))
        magnitude = sum(f_t_Vec[i] **2 for i in range(3))
        projection = [dot_Product / magnitude * f_t_Vec[i] for i in range(3)]

        perpendicular = [f_s_Vec[i] - projection[i] for i in range(3)]
        
        length = sum(perpendicular[i] **2 for i in range(3)) ** 0.5
        normalized_perpendicular = [perpendicular[i] / length for i in range(3)]

        dist_multiplier = 4 #You can change this value, if you think that distance from pole vector and leg doesn't fit you
        
        pole_Vec_Pos = [s_Vec[i] + normalized_perpendicular[i] * dist_multiplier for i in range(3)]
        return pole_Vec_Pos

    def create_PoleVector(self):
        selList = cmds.ls(sl=1)
        ikSel = cmds.ls(sl=1, type="ikHandle")

        if len(selList) != 4 or len(ikSel) != 1:
            cmds.warning("Please select 3 joints and 1 ikHandle!")
            return

        pole_Vec_Pos = self.find_perf_vect()

        crcl = cmds.circle(n=f"PoleV_CTRL", nr=(0,1,0), c=(0,0,0))
        grp1 = cmds.group(crcl, n="PoleV_xform")
        grp2 = cmds.group(grp1, n=f"PoleV_adj")
        grp3 = cmds.group(grp2, n=f"PoleV_topGr")

        cmds.xform(grp3, t=pole_Vec_Pos, ws=1)

        cmds.poleVectorConstraint(crcl[0], ikSel[0], n="poleV_constraint", w=1)
        cmds.select(crcl)

    def create_IK(self):
        fSel = cmds.ls(sl=1, type="joint")
        
        cmds.select(hi=1)

        sel = cmds.ls(sl=1, type="joint")

        cmds.joint(e=1, zso=1)

        IK = cmds.ikHandle (n=sel[-1]+"_IKHandle", sj=sel[0], ee=sel[-1], sol="ikRPsolver", srp=1)
        
        cmds.select(fSel)

    def create_Controller(self):
        fSel = cmds.ls(sl=1, type="joint")

        cmds.select(hi=1)

        sel = cmds.ls(sl=1)
        selMult = cmds.ls(sl=1, type="joint")
        ikSel = cmds.ls(sl=1, type="ikHandle")

        if len(ikSel) > 0:
            for i in sel:
                crcl = cmds.circle(n=i+"_CTRL", nr=(0,1,0), c=(0,0,0))
                grp1 = cmds.group(crcl, n=i+"_xform")
                grp2 = cmds.group(grp1, n=i+"_adj")
                grp3 = cmds.group(grp2, n=i+"_topGr")
                cnstrGr = cmds.parentConstraint(i, grp3, mo=0)
                cmds.delete(cnstrGr)
            
                cnstrCtrl = cmds.parentConstraint(crcl, i, mo=0)

                if not sel:
                    cmds.circle(n="Circle_001", nr=(0,1,0), c=(0,0,0))
                    return
                return    

        for i in selMult:
            crcl = cmds.circle(n=i+"_CTRL", nr=(0,1,0), c=(0,0,0))
            grp1 = cmds.group(crcl, n=i+"_xform")
            grp2 = cmds.group(grp1, n=i+"_adj")
            grp3 = cmds.group(grp2, n=i+"_topGr")
            cnstrGr = cmds.parentConstraint(i, grp3, mo=0)
            cmds.delete(cnstrGr)
            
            cnstrCtrl = cmds.parentConstraint(crcl, i, mo=0)
            
        if not selMult:
            cmds.circle(n="Circle_001", nr=(0,1,0), c=(0,0,0))

    def create_Group(self):
        sel = cmds.ls(sl=1)

        for i in sel:
            grp1 = cmds.group(em=1, n=i+"_xform")
            grp2 = cmds.group(grp1, n=i+"_adj")
            grp3 = cmds.group(grp2, n=i+"_topGr")
            cnstr = cmds.parentConstraint(i, grp3, mo=0)
            cmds.delete(cnstr)
            par = cmds.parent(i, grp1)

        if not sel:
            grp1 = cmds.group(em=1, n="null_xform")
            grp2 = cmds.group(grp1, n="null_adj")
            grp3 = cmds.group(grp2, n="null_topGr")

    def sel_Tool(self):
        
        selected = cmds.ls(sl=1)
        
        get_word = cmds.promptDialog(
            title = "Selection Tool",
            message = "Write word you want to find",
            button = ["OK","Cancel"],
            defaultButton = "OK",
            cancelButton = "Cancel",
            dismissString = "Cancel",
        )

        if get_word == "OK":
            what_word = cmds.promptDialog(q=1, text=1)
        
        selectWord = cmds.ls(f"*{what_word}*")

        if selected == 0:
            cmds.select(selectWord)
        
        else:
            result = selectWord + selected
            cmds.select(result)

class Selection_Tools(QWidget):
    def __init__(self, parent=None):
        super(Selection_Tools, self).__init__(parent)
        self.setWindowTitle("Outliner Tools")
        self.setGeometry(400, 100, 276, 100)
        
        pop_layout = QVBoxLayout()
        
        pop_frame = QFrame()
        pop_frame.setFrameShape(QFrame.StyledPanel)
        pop_frame_layout = QVBoxLayout(pop_frame)
        pop_layout.addWidget(pop_frame)
        
        btn1 = QPushButton("Select by Name")
        btn2 = QPushButton("Rename All")
        btn3 = QPushButton("Rename Manip")
        
        pop_frame_layout.addWidget(btn1)
        pop_frame_layout.addWidget(btn2)
        pop_frame_layout.addWidget(btn3)

        self.setLayout(pop_layout)

def show_window():
    window = EDG707_002()
    window.show()

show_window()