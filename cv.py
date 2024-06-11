import cv2
import glass as gl
import effect as eff
import bgm as bgrem
import bgm
import numpy as np
from PIL import Image
global fourcc;
global out;
out = None;
def setid(vid):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        global out
        if (vid==None):
          vid="oopp"
        path="static/output/"+vid+".avi";
        print (path)
        out = cv2.VideoWriter(path,fourcc, 20.0, (300,152))
def clear():
	global out;
	out.release()

def fun(img,theme,glass,effect,bg):
  global out;
  # image=cv2.cvtColor(np.array(img),cv2.COLOR_RGB2BGR)
  image = np.array(img)
  image = image[:, :, ::-1].copy() 
  #gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
  print(image.shape)
  ds_factor = 0.5
  image=cv2.flip(image, 1);
  themes=['Nature','Cruz','Sage','Sentosa','Boardwalk','Keylime','Dean',"Lucky","Arizona","Brite"];
  if theme!="0" and theme!=None:
    if theme=="Brite":
      alpha=float(2);
      beta=int(40);
    if theme=='Nature':
      alpha=float(1.4)
      beta=int(30);
    elif theme=='Cruz':
      alpha=float(1.8);
      beta=int(30);
    elif theme=='Sage':
      alpha=float(2.3);
      beta=int(40);
    elif theme=='Sentosa':
      alpha=float(1.4);
      beta=int(70);
    elif theme=='Boardwalk':
      alpha=float(.4);
      beta=int(30);
    elif theme=='Keylime':
      alpha=float(2.8);
      beta=int(80);
    elif theme=='Dean':
      alpha=float(2.4);
      beta=int(90);
    elif theme=='Lucky':
      alpha=float(1);
      beta=int(39);
    elif theme=='Arizona':
      alpha=float(2.96)
      beta=int(98)
      # print(alpha,beta,theme)
    if(glass!="0" and glass!=None):
      image=gl.fun(image,cv2.imread("glass/"+glass))
      image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
  else:
    if(bg!=0 and bg!=None):
      bgm="bgm/"+bg+".jpg"
      image=bgrem.fun(image,bgm)
    if(glass!="0" and glass!=None):
      image=gl.fun(image,cv2.imread("glass/"+glass))
    if(effect!="0" and effect!=None):
      if(effect=="1"):
        image=eff.cartoon(image)
      elif(effect=="3"):
        image=eff.bl_white(image)
      elif(effect=="2"):
        image=eff.fun(image)
  pil_img=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
  impil=Image.fromarray(pil_img)
  image= cv2.resize(image, (300,152), interpolation = cv2.INTER_AREA)
  out.write(image)
  print(image.shape)
  return impil

 