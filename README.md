# CodeNinjas game development with Python

Welcome to the **Pygame Development** repository. This project is designed to walkthrough basic Python games using the pygame package. Kids will be introduced to object oriented programming with **variables**, **loops**, **conditional statements**, **UI**, **Classes**, and more.

## Description

This curriculum is intended to be for kids 10+, and requires basic reading comprehension skills. Kids will be typing python code on their own, and will be introduced to text editors that are used in professional development. Because of this, keyboard proficiency is also a requirement. Each day will progressively increase in complexity, so it is recommended to complete the day's in order. 

## Requirements

Before following the setup instructions below, you will need to ensure that your device has a few softwares that we will be using. Don't worry, they are all free. 

1. Python - Ensure your computer has Python installed. If you are unsure, the easiest way to do this is to open the terminal app and type
```bash
Python --version
```
If you have Python, it will print out the version you have downloaded - For example: **Python 3.10.11**. If you don't have it, you can download it online at https://www.python.org/downloads/

2. Visual Studio Code - We will be using Visual Studio Code as a text editor because of its popularity in the industry, and ease of use. If you prefer a different text editor, you are welcome to use that, but the instructions will be done in VSCode. It can be downloaded online at https://code.visualstudio.com/download

3. Pip- Pip is a python package installer that usually comes with Python. It allows us to import packages from the internet (Pygame and Google Gemini) so that we can use it in our local projects. If you downloaded python from the link above, you should already have Pip downloaded. Verify that you have pip installed with the command below:
```bash
pip --version
```

### Special Note about Python:
Sometimes, your laptop may come pre installed with Python3 (Macbooks for example). In this case, you still will be able to complete the curriculum. All the code will be the same, but everytime we use the following command, you will need to write Python3 instead of Python. Furthermore, instead of Pip, you can use Pip3. 
```bash
Python *filename*.py
```

## Setup Instructions

The setup instructions include downloading the starter code, and setting up a Python virtual environment. These steps may seem straightforward, but since they require using the terminal I recommend having a parent assist with these steps. 


1. **Download the starter code**:
   Above this readme, towards the top of the page, you will see a big green button that says <>CODE. Click this button, and in the dropdown click download zip. Now choose the location you want your project to be stored. After it finishes downloading, find it in the file manager and extract the folder contents. Make sure to remember where you stored it, since the kids will need to navigate their to run the code. For reference, I am storing my project in documents->PythonProjects, a folder to manage my python projects. Now, when you clone the project, it makes another folder named PygameDevelopment, so you don't need to create your own folder for this week, just download the zip to where you want the project.

   You can verify the success of this step by opening the project in visual studio code. Open the app, and in the top left click File->Open Folder. This will open up the file manager. Find the folder we downloaded just before this (PygameDevelopment), select it, and click open.

   On the left of Visual Studio Code, click the file icon to open up the file heirarchy. The button looks like this:
   ![image](https://github.com/user-attachments/assets/8d77e743-cf29-4472-81c2-ba7574dd86c2)

   If the project has been downloaded succesfully, you should see a menu like this with a few python files:
   
   ![image](https://github.com/user-attachments/assets/a6ac0d8b-680a-40b3-9efd-1f8a8b3e4bab)

   Clicking on any of these python files should open up a bunch of code in the main section of vscode. If you see that, you are good to go.

3. **Setting up a Python venv**
   Why this step? When you download Python packages to import into your local code, you download a specific version. Different versions of packages may include different features. If you have 2 different Python      projects that require 2 different versions of a package, you will run into a problem if you download straight to your device. A Python venv is essentially a cache of data local to your project that stores the     packages that you have downloaded. Kids aren't required to understand WHY we do this step, but it is important to know if they wan't to develop more python projects in the future.

   Here are the steps to setting up a python venv:

   **First**, open the terminal using the same steps as before.
   
   **Second**, we need to navigate to the location of the starter code we downloaded. If you have a location you want to save it, you can navigate there by using ```cd *folderName*``` until you arrive. For my example, I will be navigating to a folder in the documents folder to store my project called PythonProjects.
   ```bash
   cd documents
   cd PythonProjects
   cd PygameDevelopment
   ```

  **Third**, now that we are in the correct spot, we need to create and activate the Python environment. To create it, in the same terminal we just opened our folder in, type
  ```bash
  python -m venv venv
  ```
  **Fourth**, now to activate it. This last step differs for Mac/Linux and windows. For Mac, In the same terminal, type
  ```bash
  source venv/bin/activate
  ```
  For Windows, type:
  ```bash
  venv\Scripts\activate
  ```
  That is all the steps for the venv! You will know your venv is setup properly if your pathname in the terminal has a (venv) out front:
  ![image](https://github.com/user-attachments/assets/644edb47-186c-475f-a55c-da55d1b49ac4)

  Now, the whole reason we created the venv is to install our required packages:
  ```bash
  pip install pygame
  ```

  We are now ready to get started with day 1.
  

## Completing the projects
   Now that our environment is setup, ninja are ready to complete the projects. Each project comes with 2 files, a skeleton code file, and a game file. 

   The skeleton code is what I chose to provide the ninja with, and we filled in the rest. The game file, is meant to be a sort of answer key. Ninja should not be given the game code, but sensei can use to reference or demonstrate a finished product. 

   Always explain code pieces that ninja are provided so they don't feel overwhelmed

   I would recommend breaking up sections of code for everything, rather than just filling in missing lines of code top to bottom.

## Note about survival game:
   Survival game is the final project for the week and introduces a cohesive game with levels, UI, and multiple game objects. Due to time and complexity restraints, I pre built many 
   of the functions for the kids myself and seperated them into files, in odrer to avoid overwhelming the kids. 
   1. classes.py - Pre built classes for all game objects except powerup
   2. UIComponents.py - Pre built functions to draw the splash screens, instructions, labels, and captions
   3. survivalSkeleton.py - The file I had the kids edit, by implementing the missing class and functions
   4. survival.py - An example answer key to survivalSkeleton.py for teachers to follow
   5. complete.py - A complete python file with all functions and classes in one, in case you don't want the game seperated out.
