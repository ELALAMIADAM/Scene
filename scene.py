# coding: utf-8

try :
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ("Error: PyOpenGL not installed properly !!")
  sys.exit()

from math import pi,sin,cos,radians
from primitives import wcs,floor
from models import Model,Car,Crane

def gl_init() :
#  glClearColor(1.0,1.0,1.0,0.0);
  glClearColor(0.5,0.5,0.5,0.0)
  glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
  glEnable(GL_DEPTH_TEST)
  glEnable(GL_CULL_FACE)

def glut_event(scene):
  glutDisplayFunc(scene.display)
  glutReshapeFunc(scene.reshape)
  glutKeyboardFunc(scene.on_normal_key_action)
  glutSpecialFunc(scene.on_special_key_action)
##  glutIdleFunc(scene.animation)

class Scene :
  def __init__(self,size) :
    self.size=size
    self.spin=0.0
    self.angle=0.0
    self.axes=[0,1,0]
    #self.model=Model(size)
    self.model=Car(size)
    self.crane=Crane(size)
    self.c_rho,self.c_phi,self.c_theta=10,0,0
    self.c_position=[self.c_rho*sin(radians(self.c_phi)),0,self.c_rho*cos(radians(self.c_phi))]
    self.c_direction=[0,0,0]
    self.c_viewup=[0,1,0]
    self.perspective=[60.0,1.0,0.1,50.0]  # fovy,ratio,near,far


  def display(self) :
    global wcs_on
    gl_init()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # View : camera
    pos_x,pos_y,pos_z=self.c_position
    dir_x,dir_y,dir_z=self.c_direction
    vup_x,vup_y,vup_z=self.c_viewup
    gluLookAt(pos_x,pos_y,pos_z,dir_x,dir_y,dir_z,vup_x,vup_y,vup_z)
   
    # Model : scene objects modeling + transformations
    glRotatef(self.spin,0,1,0)
    floor(10*self.size)
    
    #wcs(2*self.size)  # WCS en 3D
    
    # Positioning object to catch
    glPushMatrix()
    glTranslatef(-3,0.5,3)
    glRotatef(45,0,1,0)
    glColor3f(1.0,0.0,1.0)
    glutSolidTeapot(self.size/5.0)
    glPopMatrix()

    # Object to control
    glPushMatrix()
    ox,oy,oz=self.axes
    glRotatef(self.angle,ox,oy,oz)
    self.model.draw()
    glPopMatrix()
   
    glutSwapBuffers()

  def reshape(self,width,height) :
    glViewport(0,0, width,height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    self.perspective[1]=width*1.0/height
    fovy,ratio,near,far=self.perspective
    gluPerspective(fovy,ratio,near,far)

  def on_normal_key_action(self,key, x, y) :
    speed=1.0
    if key==b'h':
      print("----------------------------------------\n")
      print("Documentation interaction  : Nom-Prenom \n") 
      print("----------------------------------------\n") 
      print("h : afficher cette aide \n");
      print("v/e/f : afficher sommets/aretes/faces")
      print("c/C : afficher les faces CW/CCW \n")
      print("p/P : lancer/Arreter l'animation \n")
      print("r/R : redimensionner l'objet \n")
      print("t/T : modifier l'angle de rotation \n")
      print("x : rotation autour de l'axe Ox\n")
      print("y : rotation autour de l'axe Oy\n")
      print("z : rotation autour de l'axe Oz\n")
      print("i : état initial \n")
      print("w : deplacer vers l'arriere \n")
      print("a : deplacer vers la gauche \n")
      print("s : deplacer vers l'avant\n")
      print("d : deplacer vers la droite \n")
      print("u/U : deplacer la camera en hauteur \n")
      print("key up : avancer la camera\n")
      print("key down : reculer la camera\n")
      print("key left: tourner la camera sur la gauche\n")
      print("key right: tourner la camera sur la droite\n")
      print("b : sortie d'application \n")
    elif key==b'v' :
      glPolygonMode(GL_FRONT_AND_BACK,GL_POINT)
    elif key==b'e':
      glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    elif key==b'f':
      glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    elif key==b'c' :
      glFrontFace(GL_CW)
    elif key==b'C' :
      glFrontFace(GL_CCW)
    elif key==b'p': 
      glutIdleFunc(self.animation)
    elif key==b'P': 
      glutIdleFunc(None)
    elif key==b'r' :
      self.size-=0.1
    elif key==b'R' :
      self.size+=0.1
    elif key==b't' :
      self.angle+=1.0
    elif key==b'T' :
      self.angle-=1.0
    elif key==b'x' :
      self.axes[0],self.axes[1],self.axes[2]=1,0,0
    elif key==b'y' :
      self.axes[0],self.axes[1],self.axes[2]=0,1,0
    elif key==b'z' :
      self.axes[0],self.axes[1],self.axes[2]=0,0,1
    elif key==b'' :
      self.axes[0],self.axes[1],self.axes[2]=0,1,0
      self.angle=0.0
    elif  key == b'w' :
      pass
    elif  key == b'a' :
      pass
    elif  key == b's' :
      pass
    elif  key == b'd' :
      pass
    elif  key == b'u' :
      self.c_theta+=0.1*speed
      self.c_position[1]=self.c_rho*sin(radians(self.c_theta))*cos(radians(self.c_phi))
    elif  key == b'U' :
      self.c_theta-=0.1*speed
      self.c_position[1]=self.c_rho*sin(radians(self.c_theta))*cos(radians(self.c_phi))
    elif key==b'b' :
      exit(0)
    else :
      pass
    glutPostRedisplay()

  def on_mouse_action(self,button,state,x,y) :
    if  button==GLUT_LEFT_BUTTON :
      if state==GLUT_DOWN :
        print("button down")
      else:
        print("button up")
    else :
      pass
    glutPostRedisplay()

  def on_special_key_action(self,key, x, y) :
    speed=0.1
    if key ==  GLUT_KEY_UP :
        self.c_rho=self.c_rho-speed
        self.c_position[0]=self.c_rho*sin(radians(self.c_phi))
        self.c_position[2]=self.c_rho*cos(radians(self.c_phi))
    elif  key ==  GLUT_KEY_DOWN :
        self.c_rho=self.c_rho+speed
        self.c_position[0]=self.c_rho*sin(radians(self.c_phi))
        self.c_position[2]=self.c_rho*cos(radians(self.c_phi))
    elif key ==  GLUT_KEY_LEFT :
        self.c_phi=self.c_phi-5*speed
        self.c_position[0]=self.c_rho*sin(radians(self.c_phi))
        self.c_position[2]=self.c_rho*cos(radians(self.c_phi))
    elif  key ==  GLUT_KEY_RIGHT :
        self.c_phi=self.c_phi+5*speed
        self.c_position[0]=self.c_rho*sin(radians(self.c_phi))
        self.c_position[2]=self.c_rho*cos(radians(self.c_phi))
    else :
        pass
    glutPostRedisplay()

  def animation(self) :
    self.spin+=0.1
    if self.spin%360==0 :
      self.spin=0   
    glutPostRedisplay()

if __name__ == "__main__" :
  glutInit(sys.argv)
  glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)
  glutInitWindowSize(1200,1000)
  glutInitWindowPosition(100,100)
  glutCreateWindow ("Scene : Dupont Jean")

  size=1.0
  scene=Scene(size)
  glut_event(scene)

  glutMainLoop()
