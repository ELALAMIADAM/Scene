# coding: utf-8
from math import pi,sin,cos,radians
try :
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ("Error: PyOpenGL not installed properly !!")
  sys.exit()

from math import pi,sin,cos,radians
from primitives import floor,wcs
from primitives import square,cube_colored,axe,wcs,cylinder

size=2.0
angle_z,tr_x=0.0,0.0

class Model :
  def __init__(self,size=1.0,orientation=[0.0,0.0,0.0],position=[0.0,0.0,0.0]) :
    self.size=size
    self.orientation=orientation
    self.position=position

  # getter/setter
  def set_size(self,size) :
    self.size=size
  def get_size(self) :
    return self.size
  def set_orientation(self,orientation) :
    self.orientation=orientation
  def get_orientation(self) :
    return self.orientation
  def set_position(self,position) :
    self.position=position
  def get_position(self) :
    return self.position

  def draw(self) :
    glPushMatrix()
    x,y,z=self.position[0],self.position[1],self.position[2]
    glTranslatef(x,y,z)
    phi,theta,psi=self.orientation[0],self.orientation[1],self.orientation[2]
    glRotatef(phi,1,0,0)
    glRotatef(theta,0,1,0)
    glRotatef(psi,0,0,1)
    self.create()
    glPopMatrix()

  def create(self) :
    cube_colored(self.size)

class Car(Model) :
  def __init__(self,size=1.0,orientation=[0.0,0.0,0.0],position=[0.0,0.0,0.0]) :
    Model.__init__(self,size,orientation,position)
    self.wcs_visible=True

  def create(self):
    glPushMatrix()  # car creation
    self.body(4)
    
    # Positioning right front wheel
    glPushMatrix()
    glTranslatef(self.size, 0, 2 * self.size)
    self.wheel(bolts=3, scaling=0.2)
    glPopMatrix()
    
    # Positioning left front wheel
    glPushMatrix()
    glTranslatef(-self.size, 0, 2 * self.size)
    self.wheel(bolts=3, scaling=0.2)
    glPopMatrix()
    
    # Positioning right back wheel
    glPushMatrix()
    glTranslatef(self.size, 0, -2 * self.size)
    self.wheel(bolts=3, scaling=0.2)
    glPopMatrix()
    
    # Positioning left back wheel
    glPushMatrix()
    glTranslatef(-self.size, 0, -2 * self.size)
    self.wheel(bolts=3, scaling=0.2)
    glPopMatrix()
    
    glPopMatrix()  # end car creation

  def wheel(self, bolts=5, scaling=1.0):
    dimension = self.size * scaling
    glLineWidth(3)

    # Draw the main wheel as a cylinder
    glPushMatrix()
    glRotatef(90, 0, 1, 0)  # Rotate to place the cylinder on the ground
    glutWireTorus(0.1 * dimension, dimension, 32, 32)  # Draw the wheel as a torus
    glPopMatrix()

    angle = 360.0 / bolts
    for i in range(bolts):
        glPushMatrix()
        glRotatef(angle * i, 0.0, 0.0, 1.0)  # Rotate around the wheel's axis
        glTranslatef(0.5 * dimension, 0.0, 0.0)  # Position the bolts
        glutWireCylinder(0.05 * dimension, 0.05 * dimension, 16, 16)  # Draw the bolt as a cylinder
        glPopMatrix()
    
    glLineWidth(1)

  def body(self,scaling=1.0) :
    dimension=self.size*scaling
    glColor3f(0,0,0)
    glPushMatrix()     # body tranformation
    glScalef(1,1,dimension)
    glLineWidth(5)
    glutWireCube(self.size) #     body primitive
    glPopMatrix()      # end body tranformation

    
class Crane(Model):
    def __init__(self, size=1.0, orientation=[0.0, 0.0, 0.0], position=[0.0, 0.0, 0.0]):
        Model.__init__(self, size, orientation, position)
        self.arm_angle = 45.0  # arm angle rotation
        self.forearm_angle = 30.0  # forearm angle rotation

    # Getter and setter methods
    def set_arm_angle(self, angle):
        self.arm_angle = angle

    def get_arm_angle(self):
        return self.arm_angle

    def set_forearm_angle(self, angle):
        self.forearm_angle = angle

    def get_forearm_angle(self):
        return self.forearm_angle

    def create(self):
        glPushMatrix()

        # Cockpit: a red cube
        glTranslatef(0, 0, -self.size / 2)
        glRotatef(self.arm_angle, 1, 0, 0)
        wcs(self.size)  # Assuming this function sets up the coordinate system
        glColor3f(1.0, 0.0, 0.0)
        cube_colored(0.2 * self.size)  # Creating a red cube for the cockpit

        # Forearm: a green cylinder
        glTranslatef(0, 0, -self.size / 4)
        glRotatef(self.forearm_angle, 1, 0, 0)
        glColor3f(0.0, 1.0, 0.0)
        cylinder(0.1 * self.size, 0.1 * self.size, 0.5 * self.size, slices=10, stacks=5)  # Green cylinder for the forearm

        # Joint: a red sphere
        glColor3f(1.0, 0.0, 0.0)
        glTranslatef(0, 0, -0.25 * self.size)
        glutWireSphere(0.1 * self.size, 10, 10)  # Red sphere for the joint

        # Arm: a green cylinder
        glTranslatef(0, 0, -0.25 * self.size)
        glColor3f(0.0, 1.0, 0.0)
        cylinder(0.1 * self.size, 0.1 * self.size, 0.5 * self.size, slices=10, stacks=5)  # Green cylinder for the arm

        glPopMatrix()
def gl_init() :
#  glClearColor(1.0,1.0,1.0,0.0);
  glClearColor(0.5,0.5,0.5,0.0)
  glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
  glEnable(GL_DEPTH_TEST)
  glEnable(GL_CULL_FACE)

def glut_event():
  glutDisplayFunc(display)
  glutReshapeFunc(reshape)
  glutKeyboardFunc(on_normal_key_action)
  glutSpecialFunc(on_special_key_action);

def display() :
  global size,model
  global angle_z,tr_x
  glClearColor(0.5,0.5,0.5,0.0)
  glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
  glEnable(GL_DEPTH_TEST)
  glEnable(GL_CULL_FACE)
  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()
  # position=0,0,1    # camera position    (default on Z axis)
  position=1,2,3  
  direction=0,0,0   # camera direction   (default WCS origin)
  viewup=0,1,0      # camera viewup axis (default vertical axis)
  gluLookAt(
    position[0],position[1],position[2],
    direction[0],direction[1],direction[2],
    viewup[0],viewup[1],viewup[2]
  )
  # Scene modeling  : begin
  # floor(10*size) 
  glPushMatrix()
  # glColor3f(1.0,0.0,1.0)
  # glTranslatef(0.0,0.5,0.0)  # positioning object on floor
  # glutWireTeapot(size/5.0)
  #wcs(size)
  # glLineWidth(3)
  # glBegin(GL_LINES)
  # glColor3f(1.0,1.0,1.0)
  # glVertex2f(0,0)
  # glVertex2f(size/2,size/2)
  # glEnd()
  # glPushMatrix()
  # # glRotatef(angle_z,0,0,1)
  # glTranslatef(tr_x,0,0)
  # glRotatef(45.0,0,0,1)
  # wcs(0.75*size)
  # glutWireCube(size)
  # glPopMatrix()
  # glPopMatrix()
  model.draw()  # Scene modeling  : end
  crane.draw()
  glPopMatrix()  
  glutSwapBuffers()

def reshape(width,height) :
  glViewport(0,0, width,height)
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  fovy,ratio,near,far=60.0,width*1.0/height,0.1,50.0
  gluPerspective(fovy,ratio,near,far)

def on_normal_key_action(key,x,y) :
  print("on_normal_key_action")
  global size
  global angle_z,tr_x
  if key==b'h':
    print("----------------------------------------") 
    print("Documentation Interaction  : Nom-Prenom ") 
    print("h : afficher cette aide")
    print("s : sortie d'application")
    print("----------------------------------------") 
    print("---------") 
    print("Affichage")
    print("---------") 
    print("c/C : afficher faces CW/faces CCW")
    print("p/f/l : afficher sommets/faces/aretes")
    print("r/R : redimensionner le modele")
    print("i : retour etat initial")
    print("---------") 
  elif key== b'c' :
    glFrontFace(GL_CW)
  elif key== b'C' :
    glFrontFace(GL_CCW)
  elif key== b'f':
    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
  elif key== b'l':
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
  elif key== b'p' :
    glPolygonMode(GL_FRONT_AND_BACK,GL_POINT);
  elif key== b'i':
    print("retour etat initial")
    size=2.0
  elif key== b'r' :
    print("r : redimensionner (agrandir) le modele")
    size=size+0.1     
  elif key== b'R' :
    print("R : redimensionner (reduire) le modele")  
    size=size-0.1  
  elif key== b's' :
    print("sortie d'application")
  elif key== b't' :
    print("translater (sens positif) le modele suivant l'axe 0y")
    tr_x=tr_x+0.1
  elif key== b'T' :
    print("tranlater (sens négatif) le modele suivant l'axe 0y")
    tr_x=tr_x-0.1
  elif key== b'y' :
    print("rotation (CCW) du modele autour de l'axe 0y")
    angle_z=angle_z+1
  elif key== b'y' :
    print("rotation (CW) du modele autour de l'axe 0y")
    angle_z=angle_z-1
  else :
    print("interaction non implementee sur la touche :",key)
  glutPostRedisplay()
  
def on_special_key_action(key,x,y) :
  global size,model
  print("on_special_key_action")
  position=model.get_position()
  orientation=model.get_orientation()
  if key ==  GLUT_KEY_UP :
      position[0]+=0.1*size*sin(radians(orientation[1]))
      position[2]+=0.1*size*cos(radians(orientation[1]))
  elif  key ==  GLUT_KEY_DOWN :
      position[0]-=0.1*size*sin(radians(orientation[1]))
      position[2]-=0.1*size*cos(radians(orientation[1]))
  elif key ==  GLUT_KEY_LEFT :
      orientation[1]+=5
  elif  key ==  GLUT_KEY_RIGHT :
      orientation[1]-=5
  else :
    print("interaction non implementee sur la touche speciale :",key)
  model.set_position(position)
  model.set_orientation(orientation)
  glutPostRedisplay()

if __name__ == "__main__" :

  glutInit(sys.argv)
  glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)
  glutInitWindowSize(600,500)
  glutInitWindowPosition(100,100)
  glutCreateWindow ("ENIB S9 REV : Models")

  glut_event()
  model=Car(size/5)
  crane=Crane(size/5)
  glutMainLoop()
