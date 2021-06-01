import bpy
from bpy.props import *

import numpy as np

bl_info = {
    "name": "hexPalette",
    "author": "luis alberto rodriguez montilla",
    "version": (0),
    "blender": (2, 72, 2),
    "location": "UV/Image Editor(IMAGE_EDITOR) > TOOLS > Tools",
    "warning": "",
    "description": "paste all hex(AA BB CC) color in the box or folder , select >>hex palette<< like ative palette, this change the first palette name to Hex palette and add colors",
    "wiki_url": ""
                "",
    "category": "PALETTE",
}




		

def initSceneProperties():
	
 #string%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	bpy.types.Scene.MyString = StringProperty(
        name = "String")

 #string%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	return
 
# initSceneProperties(bpy.context.scene)
 
#
#    Menu in UI region
#
class UIPanel(bpy.types.Panel):
	bl_label = "Hex Palette"
	bl_space_type = "IMAGE_EDITOR"
	# bl_region_type = "UI"
	bl_region_type = "TOOLS"
	bl_category = "Tools"
	# bl_context  = "Paint"

	def draw(self, context):
		layout = self.layout
		scn = context.scene
		layout.prop(scn, "MyString")		
		layout.operator("create_empty_palette.create_hex_palette_")
		layout.operator("pluss_palette.pluss_palette_to_exist")      #idname_must.be_all_lowercase_and_contain_one_dot
		layout.operator("path_file.txt")

class OBJECT_OT_FromPathfilet(bpy.types.Operator):
	bl_idname = "path_file.txt"
	bl_label = "Select txt file"

	filepath = bpy.props.StringProperty(subtype="FILE_PATH") 
	#somewhere to remember the address of the file


	def execute(self, context):
		display = self.filepath  
		display = str(display)
		display = display.replace("\\" , "/")

		f = open(display, "r")
		stringData=f.read()
		
		stringData=strRemoveSpace(stringData)
		stringData=strRemoveSpecial(stringData)

		arrStrToPalette(stringData)
	
		return {'FINISHED'}
	def invoke(self, context, event): # See comments at end  [1]

		context.window_manager.fileselect_add(self) 
		#Open browser, take reference to 'self' 
		#read the path to selected file, 
		#put path in declared string type data structure self.filepath

		return {'RUNNING_MODAL'}  
		# Tells Blender to hang on for the slow user input

class OBJECT_OT_CreateEmptyPalette(bpy.types.Operator):
	bl_idname = "create_empty_palette.create_hex_palette_"
	bl_label = "create empty hex palette "
	def execute(self, context):
		if not bpy.data.palettes:
			bpy.ops.palette.new()
			bpy.data.palettes[0].name="Hex palette"
		elif bpy.data.palettes[0].name!="Hex palette":
			bpy.data.palettes[0].name="Hex palette"

		return{'FINISHED'} 

class OBJECT_OT_PlussPal(bpy.types.Operator):
	
	
	bl_idname = "pluss_palette.pluss_palette_to_exist"
	bl_label = "Pluss palette"
	
	
	def execute(self, context):
		
		arrStrToPalette(OBJECT_OT_Scn.defineVar_(self,context))
	

		return{'FINISHED'} 
		
		

class OBJECT_OT_Scn(bpy.types.Operator):

	def defineVar_(self, context):
		
		scn = context.scene
		MyString = scn["MyString"]
		
		
		MyString=strRemoveSpace(MyString)
		MyString=str(strRemoveSpecial(MyString))
		
		
	
		return MyString
		
		
		
def arrStrToPalette(myStr):

	tempVarLenColor=len(bpy.data.palettes[0].colors)
	tempArr=[]
	tempArra2=[]
	# print(tempVarLenColor)
	for i in strToArray3d(myStr):
		bpy.ops.palette.color_add()
		num_=0
		tempArr.append(hex_to_rgb(i))
		for i in tempArr:
			
			a=str(i)
			a=strRemoveSpace(a)
			a=a.replace(")","")
			a=a.replace("(","")
			b=a.split(',')#convierte un string a array
			x=np.array(b)
			x=np.asfarray(x,float)#convierte array de string a float
			

			for i in range(len(x)):
				x[i]=rgbTr(x[i])
				
			
			bpy.data.palettes[0].colors[tempVarLenColor+num_].color=x
			tempArra2.append(x)
			
			num_=num_+1		
	return tempArra2
			


def strRemoveSpecial(text):
	import re
	text = re.sub("[^a-zA-Z0-9]+", "",text)
	return text
	
def arrayStringHexToPalettee(arrayStrinngHex,bolPlussPalette):
	numPal=len(bpy.data.palettes[0].colors)
	num_=0

	if bolPlussPalette==True:
		for i in range(len(arrayStrinngHex)):
			
			bpy.ops.palette.color_add()
			bpy.data.palettes[0].colors[num_+numPal].color=createArray3d(hex_to_rgb(arrayStrinngHex[num_]))
			
			num_= num_+1
			

			
			

def hex_to_rgb(hex):
	return str(tuple(int(hex[i:i+2],16) for i in (0,2,4)))
	


#convierte un string de la forma (123)
def strToArray3d(strV):
    myStringArr=[]
    num_=0
    for x in range(len(strV)):
        if num_%6 == 0 and num_!= 0:
            myStringArr.append(strV[num_-6:-len(strV)+(num_)])
        
            
        if num_== len(strV)-1:
            myStringArr.append(strV[(num_+1)-6:])
      
     
        num_ = num_+ 1
    return myStringArr
	
	
        
def rgbTr(rgbNum):
	if rgbNum==0.00:
		return 0.00
	else:
		
		result=  float(((rgbNum*100)/255)/100)
		return  "{0:.3f}".format(result)
	
def strRemoveSpace(strVar):
		
	strVar = strVar.replace(" ", "")
	strVar = ''.join(strVar.split())
	return strVar

	
 
def register():

	
	bpy.utils.register_module(__name__)#register others class
	initSceneProperties()




def unregister():

	bpy.utils.unregister_module(__name__)#unregister others class

	


if __name__ == "__main__":
    register()