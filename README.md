# My Awesome Project

Welcome to the **Pygame Development** repository. This project is designed to walkthrough basic Python games using the pygame package. Kids will be introduced to object oriented programming with **variables**, **loops**, **conditional statements**, **UI**, **APIs**, and more. Towards the end of camp we will be demonstrating how to incorporate **generative artificial intelligence** into video games by using **Google Gemini's** chatbot (LLM).

## Description

This curriculum is intended to be for kids 11+, and requires basic reading comprehension skills. Kids will be typing python code on their own, and will be introduced to text editors that are used in professional development. Because of this, keyboard proficiency is also a requirement. Each day will progressively increase in complexity, so it is recommended to complete the day's in order. 

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
   Above this readme, towards the top of the page, you will see a big green button that says <>CODE. 

   ```bash
   git clone https://github.com/your-username/my-awesome-project.git
   ```
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
  
# Day 1
Objective: [Describe the goal for Day 1, e.g., "Set up your local development environment."]
Tasks:
Install Node.js
Set up a GitHub repository
Create a README.md file
Resources:
[Link to relevant documentation or tutorials]
# Day 2
Objective: [Describe the goal for Day 2, e.g., "Build your first component."]
Tasks:
Create a basic HTML file
Add some CSS styling
Write a simple JavaScript function
Resources:
[Link to relevant documentation or tutorials]
# Day 3
Objective: [Describe the goal for Day 3, e.g., "Learn about version control."]
Tasks:
Commit changes to Git
Create and switch branches
Merge branches and resolve conflicts
Resources:
[Link to relevant documentation or tutorials]
# Day 4
Objective: [Describe the goal for Day 4, e.g., "Implement a feature."]

Tasks:
Add a new feature to your project
Write tests for your feature
Review and refactor your code

Resources:
[Link to relevant documentation or tutorials]
# Day 5
Objective: [Describe the goal for Day 5, e.g., "Deploy your project."]

Tasks:
Set up a deployment pipeline
Deploy your project to a hosting service
Verify that everything is working correctly

Resources:
[Link to relevant documentation or tutorials]

# Common Mistakes
Here are some common pitfalls and how to avoid them:

Not Committing Often: Make regular commits to avoid losing work.
Ignoring Merge Conflicts: Always resolve merge conflicts carefully.
Not Testing Code: Write and run tests to ensure your code works as expected.
Neglecting Documentation: Keep your README.md and other documentation up to date.
Forgetting to Push Changes: Regularly push your changes to the remote repository to keep it up to date.
