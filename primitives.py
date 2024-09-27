# coding: utf-8

try :
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ("Error: PyOpenGL not installed properly !!")
  sys.exit()

size=2.0
angle_z,tr_x=0.0,0.0

def square(size) :
# face avant : sommets de couleurs RGBW
  glBegin(GL_POLYGON)
  glColor3f(1.0,0.0,0.0)   # Red 
  glVertex2f(-size,-size)
  glColor3f(0.0,1.0,0.0)   # Green
  glVertex2f(size,-size)
  glColor3f(0.0,0.0,1.0)   # Blue
  glVertex2f(size,size)
  glColor3f(1.0,1.0,1.0)   #  White
  glVertex2f(-size,size)
  glEnd()
# face arriere : couleur uniforme White
  glBegin(GL_POLYGON)
  glVertex2f(-size,-size)
  glVertex2f(-size,size)
  glVertex2f(size,size)
  glVertex2f(size,-size)
  glEnd()

def cube_colored(size) :
  glBegin(GL_QUADS)
  glColor3ub(0,255,0)            # face rouge
  glVertex3d(size,size,size)
  glVertex3d(size,size,-size)
  glVertex3d(-size,size,-size)
  glVertex3d(-size,size,size)
  glColor3ub(255,0,0)            # face verte
  glVertex3d(size,-size,size)
  glVertex3d(size,-size,-size)
  glVertex3d(size,size,-size)
  glVertex3d(size,size,size) 
  glColor3ub(0,0,255)           # face bleue
  glVertex3d(size,-size,size)
  glVertex3d(size,size,size)
  glVertex3d(-size,size,size)
  glVertex3d(-size,-size,size)
  glColor3ub(255,255,0)          #  face jaune
  glVertex3d(-size,size,size)
  glVertex3d(-size,size,-size)
  glVertex3d(-size,-size,-size)
  glVertex3d(-size,-size,size)
  glColor3ub(255,0,255)           # face magenta
  glVertex3d(-size,-size,size)
  glVertex3d(-size,-size,-size)
  glVertex3d(size,-size,-size)
  glVertex3d(size,-size,size) 
  glColor3ub(0,255,255)          # face cyan
  glVertex3d(size,size,-size)
  glVertex3d(size,-size,-size)
  glVertex3d(-size,-size,-size)
  glVertex3d(-size,size,-size)
  glEnd()

# def sphere(radius,slices=20,stacks=10) :
def sphere(radius,longitude=20,latitude=10) :
  params=gluNewQuadric()
  gluQuadricDrawStyle(params,GLU_FILL)
  gluQuadricTexture(params,GL_TRUE)
  gluSphere(params,radius,longitude,latitude)
  gluDeleteQuadric(params)

def joint(radius) :
  longitude,latitude=20,10
  sphere(radius,longitude,latitude)

def cylinder(base,top,height,slices=10,stacks=5) :
  params=gluNewQuadric()
  gluQuadricDrawStyle(params,GLU_FILL)
  gluQuadricTexture(params,GL_TRUE)
  gluCylinder(params,base,top,height,slices,stacks)
  gluDeleteQuadric(params)

def disk(inner,outer,slices=10,loops=5) :
  params=gluNewQuadric()
  gluQuadricDrawStyle(params,GLU_FILL)
  gluQuadricTexture(params,GL_TRUE)
  gluDisk(params,inner,outer,slices,loops)
  gluDeleteQuadric(params)

def stick(base,top,height,slices=10,stacks=5) :
  glPushMatrix()
  glRotatef(180,0,1,0)
  glColor3f(1,0,0)
  disk(0,base,slices,stacks)
  glPopMatrix()
  glColor3f(0,1,0)
  cylinder(base,top,height,slices,stacks)
  glPushMatrix()
  glTranslatef(0,0,height)
  glColor3f(1,0,0)
  disk(0,top,slices,stacks)
  glPopMatrix()

def cone(base,height,slices=10,stacks=5) :
  glPushMatrix()
  glRotatef(180,0,1,0)
  disk(0,base,slices,stacks)
  glPopMatrix()
  cylinder(base,0,height,slices,stacks)

def torus(inner,outer,sides=10,rings=5) :
  glutSolidTorus(inner, outer, sides, rings)

def floor(size,tiles=10) :
  tile_size=size/tiles
  for i in range(10+1) :
    for j in range(10+1) :
        glPushMatrix()
        glTranslatef(-size/2.0+tile_size*i,0.0,-size/2.0+tile_size*j)
        if (i+j)%2 == 0 :
            glColor3f(1.0,1.0,1.0)
            glRotatef(-90,1,0,0)
            glRectf(-tile_size/2.0, -tile_size/2.0, tile_size/2.0, tile_size/2.0)
        else :
            glColor3f(0.0,0.0,0.0)
            glRotatef(90,1,0,0)
            glRectf(-tile_size/2.0, -tile_size/2.0, tile_size/2.0, tile_size/2.0)
        glPopMatrix()

# TODO : create 3D axe with disk,cylinder,cone
def axe(base,height,slices=10,stacks=5) :
    base_radius = base
    handle_height = height * 0.8
    head_height = height * 0.2
    head_base = base * 1.01  

    # Handle
    glPushMatrix()
    cylinder(base_radius * 0.2, base_radius * 0.2, handle_height, slices, stacks)
    glPopMatrix()

    # Axe head
    glPushMatrix()
    glTranslatef(0, 0, handle_height)
    cone(head_base, head_height, slices, stacks)
    glPopMatrix()

   #cylinder(base,base,height)

# TODO : redefine with 3D axes when fonction above (axe()) implemented
def wcs(size) :
   base = 0.2 * size
   height = 3 * size
   # Draw X-axis in red
   glColor3ub(255, 0, 0)  # Red
   glPushMatrix()
   glRotatef(+90, 0, 1, 0)
   axe(base=base, height=height)
   glPopMatrix()

   # Draw Y-axis in green
   glColor3ub(0, 255, 0)  # Green
   glPushMatrix()
   glRotatef(-90, 1, 0, 0)
   axe(base=base, height=height)
   glPopMatrix()

   # Draw Z-axis in blue
   glColor3ub(0, 0, 255)  # Blue
   glPushMatrix()
   glRotatef(0, 1, 0, 0)
   axe(base=base, height=height)
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
##  glutIdleFunc(animation)

def display() :
  global size
  gl_init()
  shoulder,elbow=30.0,45.0
  
  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity()
  position=0,0,5    # camera position    (default on Z axis)
  # position=1,2,3  
  direction=0,0,0   # camera direction   (default WCS origin)
  viewup=0,1,0      # camera viewup axis (default vertical axis)

  gluLookAt(
    position[0],position[1],position[2],
    direction[0],direction[1],direction[2],
    viewup[0],viewup[1],viewup[2]
  )
  # Primitives to display
  # floor(10*size) 
  # glPushMatrix()
  # glColor3f(1.0,0.0,1.0)
  # # glTranslatef(0.0,0.5,0.0)  # positioning object on floor
  # # glutWireTeapot(size/5.0)
  # wcs(size)
  # square(size/5.0)
  # glPopMatrix()

# https://stackoverflow.com/questions/49236745/opengl-translation-before-and-after-a-rotation
  glPushMatrix()
  glTranslatef (-1.0, 0.0, 0.0)
  glRotatef (shoulder, 0.0, 0.0, 1.0)
  glTranslatef (1.0, 0.0, 0.0)
  glPushMatrix();
  glScalef (2.0, 0.4, 1.0)
  glutWireCube (1.0)
  glPopMatrix()
  glTranslatef (1.0, 0.0, 0.0)
  glRotatef (elbow, 0.0, 0.0, 1.0)
  glTranslatef (1.0, 0.0, 0.0)
  glPushMatrix()
  glScalef (2.0, 0.4, 1.0)
  glutWireCube (1.0)
  glPopMatrix()
  glPopMatrix()
  glutSwapBuffers()

def reshape(width,height) :
  glViewport(0,0, width,height)
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  fovy,ratio,near,far=60.0,width*1.0/height,0.1,50.0
  gluPerspective(fovy,ratio,near,far)

if __name__ == "__main__" :
  glutInit(sys.argv)
  glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)
  glutInitWindowSize(1200,1000)
  glutInitWindowPosition(100,100)
  glutCreateWindow ("Primitives : Dupont Jean")

  glut_event()

  glutMainLoop()
