#!/bin/bash -       
#==============================================================================
#title           : send_PyOpenGL.sh
#description     : This script will compress all .py files in the current directory and 
#                  send it to /home/TP/TPrendu/nedelec/REV/PyOpenGL
#author		     : Maël CREAC'H 
#date            : 14/11/2023
#revision        : 12/09/2024
#version         : 0.4
#usage		     : bash send_PyOpenGL.sh
#bash_version    : 4.4.20(1)-release
#==============================================================================
read -p "Saisir le nom des membres du projet sous la forme NOM1_NOM2 :" project_members
read -p "Vous confirmez que le nom des membres du projet est bien sous le bon format ? ${project_members} (Y/N): " confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1
folder_name=${project_members}_Scene
rsync -av --exclude='*.sh' --exclude='Tests' --exclude='__pycache__' ./ ./${folder_name}
tar zcvf ${folder_name}.tgz ${folder_name}/
rm -r ${folder_name}
cp ${folder_name}.tgz /home/TP/TPrendu/nedelec/REV/Scene
rm -r ${folder_name}.tgz
exit
