<<<<<<< HEAD
from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QTabWidget, QLabel, QLineEdit, QGroupBox, QColorDialog, QButtonGroup, QRadioButton, QSlider
=======
from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QTabWidget, QLabel, QGroupBox, QColorDialog, QButtonGroup, QRadioButton, QSlider
>>>>>>> b3034a503f40043902171e9deea463720e1efeb6
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from shiboken6 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import maya.mel as mel

def get_maya_window():
    get_window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(get_window), QMainWindow)

class EDG707_002(QMainWindow):
    def __init__(self):
        super(EDG707_002, self).__init__(get_maya_window())
        self.setWindowTitle("EDG AutoRig Assistant")
        self.setMaximumSize(400, 600)
        self.setWindowFlag(Qt.WindowType.Tool)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame_layout = QVBoxLayout(frame)
        main_layout.addWidget(frame)


        logo = QLabel("EDG")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame_layout.addWidget(logo)

        #Tab Set
        tab_widget = QTabWidget()
        frame_layout.addWidget(tab_widget)

        #Tab 1
        tab_1 = QWidget()
        tab1_layout = QVBoxLayout(tab_1)
        
        #
        jnt_manip_grp = QGroupBox("Joint's Manipulators")
        jnt_manip_grp.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        ctrl_grp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ctrl_grp_layout = QGridLayout(ctrl_grp)
        
        controller_button = QPushButton("Create Controller")
        grouping_button = QPushButton("Create Groups")

        ctrl_grp_layout.addWidget(controller_button, 0, 0)
        ctrl_grp_layout.addWidget(grouping_button, 0, 1)
        
        #
        color_grp = QGroupBox("Color Override")
        color_grp.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        sel_grp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sel_grp_layout = QVBoxLayout(sel_grp)

        tab_2_layout.addWidget(sel_grp)

        sel_grp.setMaximumSize(400, 120)

        sel_name_btn = QPushButton("Select by Name")
        ren_all_btn = QPushButton("Rename Selected")
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
        ribbon_tool.clicked.connect(self.show_ribbon_tool)
        sel_name_btn.clicked.connect(self.sel_Tool)
        ren_all_btn.clicked.connect(self.rename_All_Tool)
        ren_manip_btn.clicked.connect(self.show_Rename_Manip)

        tab_widget.addTab(tab_2, "Selection")

<<<<<<< HEAD
    def show_ribbon_tool(self):
        
        self.rib_wid = Ribbon_Tool(self)
        self.rib_wid.setWindowFlags(Qt.WindowType.Window)
        self.rib_wid.show()

    def show_Rename_Manip(self):

        self.ren_wid = Rename_Manip(self)
        self.ren_wid.setWindowFlags(Qt.WindowType.Window)
        self.ren_wid.show()
=======
    def create_ribbon(self):
        sel = cmds.ls(sl=1, type="joint")

        if not sel:
            cmds.warning("You need to select at least 2 joints!")
            return
        curves_array = []
        dist = 1

        for i in sel:
            pos = cmds.xform(i, q=1, t=1, ws=1)

            mat = cmds.xform(i, q=1, m=1, ws=1)

            x_axis = [mat[0], mat[1], mat[2]]
            y_axis = [mat[4], mat[5], mat[6]]
            z_axis = [mat[8], mat[9], mat[10]]

            chosen_axis = z_axis

            fst_pnt = [pos[0] + chosen_axis[0]*dist, pos[1] + chosen_axis[1]*dist, pos[2] + chosen_axis[2]*dist]
            snd_pnt = [pos[0] - chosen_axis[0]*dist, pos[1] - chosen_axis[1]*dist, pos[2] - chosen_axis[2]*dist]

            cur = cmds.curve(n=f"curve_{i}", p=[fst_pnt, snd_pnt], d=1)
            
            curves_array.append(cur)

        loft = cmds.loft(curves_array, u=1, ar=1, d=3, ss=4, rn=1, po=0)
        cmds.delete(curves_array)
>>>>>>> b3034a503f40043902171e9deea463720e1efeb6

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
            message = "Select:",
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

    def rename_All_Tool(self):
        
        selected = cmds.ls(sl=1)
        
        get_word = cmds.promptDialog(
            title = "Rename Tool",
            message = "Rename to:",
            button = ["OK","Cancel"],
            defaultButton = "OK",
            cancelButton = "Cancel",
            dismissString = "Cancel",
        )

        if get_word == "OK":
            what_word = cmds.promptDialog(q=1, text=1)
        
        for i in selected:
            rename = cmds.rename(i, what_word)

class Ribbon_Tool(QWidget):
    def __init__(self, parent=None):
        super(Ribbon_Tool, self).__init__(parent)
        self.setWindowTitle("Ribbon Tools")
        self.setGeometry(400, 100, 276, 100)
<<<<<<< HEAD

        self.setWindowFlag(Qt.Tool)

=======
        
>>>>>>> b3034a503f40043902171e9deea463720e1efeb6
        pop_widget_layout = QVBoxLayout()

        radio_grp = QButtonGroup()

        numbers_layout = QHBoxLayout()
        number_labels = []
<<<<<<< HEAD

        for i in range(1, 11):
            label = QLabel(str(i))
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
=======
        
        for i in range(1, 11):
            label = QLabel(str(i))
            label.setAlignment(Qt.AlignCenter)
>>>>>>> b3034a503f40043902171e9deea463720e1efeb6
            numbers_layout.addWidget(label)
            number_labels.append(label)

        pop_frame = QFrame()
        pop_frame.setFrameShape(QFrame.Shape.StyledPanel)
        pop_frame_layout = QVBoxLayout(pop_frame)
        pop_widget_layout.addWidget(pop_frame)

        pop_inner_group = QGroupBox()
        pop_inner_group_layout = QGridLayout(pop_inner_group)
        pop_frame_layout.addWidget(pop_inner_group)

        axis_label = QLabel("Nurbs Along:")

<<<<<<< HEAD
        self.axis_x = QRadioButton("X Axis")
        self.axis_y = QRadioButton("Y Axis")
        self.axis_z = QRadioButton("Z Axis")

        self.axis_x.setChecked(True)

        number_spans_label = QLabel("Number of Spans:")
        self.s_slider = QSlider(Qt.Orientation.Horizontal)
        self.s_slider.setMinimum(1)
        self.s_slider.setMaximum(10)
        self.s_slider.setValue(4)
=======
        axis_x = QRadioButton("X Axis")
        axis_y = QRadioButton("Y Axis")
        axis_z = QRadioButton("Z Axis")
        
        number_spans_label = QLabel("Number of Spans:")
        s_slider = QSlider(Qt.Horizontal)
        s_slider.setMinimum(1)
        s_slider.setMaximum(10)
        s_slider.setValue(4)
>>>>>>> b3034a503f40043902171e9deea463720e1efeb6

        btn1 = QPushButton("Create Ribbon")
        #btn2 = QPushButton("Make nHair")

        pop_inner_group_layout.addWidget(axis_label, 0, 0)
        radio_grp.addButton(self.axis_x)
        radio_grp.addButton(self.axis_y)
        radio_grp.addButton(self.axis_z)

        pop_inner_group_layout.addWidget(self.axis_x, 1, 0)
        pop_inner_group_layout.addWidget(self.axis_y, 1, 1)
        pop_inner_group_layout.addWidget(self.axis_z, 1, 2)

        pop_inner_group_layout.addWidget(number_spans_label, 2, 0, 1, 3)
        pop_inner_group_layout.addLayout(numbers_layout, 3, 0, 1, 3)
        pop_inner_group_layout.addWidget(self.s_slider, 4, 0, 1, 3)

        pop_inner_group_layout.addWidget(btn1, 5, 0, 1, 3)
        #pop_inner_group_layout.addWidget(btn2, 6, 0, 1, 3)

        self.setLayout(pop_widget_layout)

        btn1.clicked.connect(self.create_ribbon)

    def create_ribbon(self):
        sel = cmds.ls(sl=1, type="joint")
        
<<<<<<< HEAD
        if len(sel) == 2:
            curves_array = []
            dist = 1

            for i in sel:
                pos = cmds.xform(i, q=1, t=1, ws=1)
=======
        pop_inner_group_layout.addWidget(axis_label, 0, 0)
        radio_grp.addButton(axis_x)
        radio_grp.addButton(axis_y)
        radio_grp.addButton(axis_z)
        
        pop_inner_group_layout.addWidget(axis_x, 1, 0)
        pop_inner_group_layout.addWidget(axis_y, 1, 1)
        pop_inner_group_layout.addWidget(axis_z, 1, 2)

        pop_inner_group_layout.addWidget(number_spans_label, 2, 0, 1, 3)
        pop_inner_group_layout.addLayout(numbers_layout, 3, 0, 1, 3)
        pop_inner_group_layout.addWidget(s_slider, 4, 0, 1, 3)

        pop_inner_group_layout.addWidget(btn1, 5, 0, 1, 3)
        pop_inner_group_layout.addWidget(btn2, 6, 0, 1, 3)

        self.setLayout(pop_widget_layout)

        btn1.clicked.connect(self.call_ribbon_from_up)

    def call_ribbon_from_up(self):
        EDG707_002.create_ribbon(self)
>>>>>>> b3034a503f40043902171e9deea463720e1efeb6

                mat = cmds.xform(i, q=1, m=1, ws=1)

                x_axis = [mat[0], mat[1], mat[2]]
                y_axis = [mat[4], mat[5], mat[6]]
                z_axis = [mat[8], mat[9], mat[10]]

                if self.axis_x.isChecked():
                    chosen_axis = x_axis
                elif self.axis_y.isChecked():
                    chosen_axis = y_axis
                else:
                    chosen_axis = z_axis

                fst_pnt = [pos[0] + chosen_axis[0]*dist, pos[1] + chosen_axis[1]*dist, pos[2] + chosen_axis[2]*dist]
                snd_pnt = [pos[0] - chosen_axis[0]*dist, pos[1] - chosen_axis[1]*dist, pos[2] - chosen_axis[2]*dist]

                cur = cmds.curve(n=f"curve_{i}", p=[fst_pnt, snd_pnt], d=1)

                curves_array.append(cur)

            spans = self.s_slider.value()
            jnts_cnt_nHair = len(sel)-1 
            edges = spans * jnts_cnt_nHair +1

            loft = cmds.loft(curves_array, u=1, ar=1, d=3, ss=spans, rn=1, po=0)

            existing_follicles = set(cmds.ls(type="follicle"))

            nHair = mel.eval(f"createHair {edges} 1 3 1 0 1 1 1 0 1 1 1")

            created_follicles = set(cmds.ls(type="follicle")) - existing_follicles

            cmds.delete(curves_array)

            # Delete Additional Hair Object (Not needed for Ribbon)
            hair = cmds.listRelatives(["*hairSystemShape*", "*pfxHairShape*"], parent=1)
            nucl = cmds.ls(type="nucleus")
            if len(hair)>0:
                cmds.delete(hair, nucl)

            fol_sh = cmds.ls("*loftedSurface*Follicle*", type="follicle") #Shape
            fol = cmds.listRelatives(fol_sh, p=1) #Parent
            fol_child = cmds.listRelatives(fol, c=1) #All
            fol_parent_grp = cmds.listRelatives(fol, p=1)

            fol_child_grp = [] #Filtered

            for i in fol_child:
                if i not in fol_sh:
                    fol_child_grp.append(i)

            cmds.delete(fol_child_grp)
            # Deleted

            created_follicles_nonShape = cmds.listRelatives(created_follicles, p=1)
            
            #Create Joints in the position of follicles
            for i in created_follicles_nonShape:
                cmds.select(clear=True)
                jnt2create = cmds.joint(n=i+"_JNT", p=[0,0,0])
                jnt_constr = cmds.parentConstraint(i, jnt2create)
                cmds.delete(jnt_constr)

        else:
            cmds.warning("You need to select 2 joints!")

class Rename_Manip(QWidget):
    def __init__(self, parent=None):
        super(Rename_Manip, self).__init__(parent)

        self.setWindowTitle("Renaming Control")
        self.setGeometry(500, 200, 276, 100)

        self.setWindowFlag(Qt.WindowType.Tool)

        self.sel_widget_layout = QVBoxLayout()

        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_layout = QVBoxLayout(self.frame)

        self.txt_bef = QLabel("Search for:")
        self.txt_1 = QLineEdit()
        self.txt_aft = QLabel("Replace with:")
        self.txt_2 = QLineEdit()
        self.ok_btn = QPushButton("Ok")

        self.frame_layout.addWidget(self.txt_bef)
        self.frame_layout.addWidget(self.txt_1)
        self.frame_layout.addWidget(self.txt_aft)
        self.frame_layout.addWidget(self.txt_2)
        self.frame_layout.addWidget(self.ok_btn)
        self.sel_widget_layout.addWidget(self.frame)                

        self.setLayout(self.sel_widget_layout)

        self.ok_btn.clicked.connect(self.rename_selected)

    def rename_selected(self):
        search_text = self.txt_1.text()
        replace_text = self.txt_2.text()

        sel_obj = cmds.ls(sl=True)

        for i in sel_obj:
            # Replace only part of the name
            new_name = i.replace(search_text, replace_text)
            
            # Rename only if the name has changed
            if new_name != i:
                cmds.rename(i, new_name)


def show_window():                                          
    window = EDG707_002()
    window.show()

show_window()