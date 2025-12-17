# GFPGANImageRestoreApp

flow: 
1: Design a simple interface for user

2: When user open folder, let the user choose the image then open up the image as input

3: use the GFPGAN API to generate the image

4: output the result to user, can let the user download.

If you want to run this app on local, clone this repo then execute the command: python3 -m streamlit run ./src/main.py

If you find your package dependency is not matched with the code, and you want to build docker image, execute the command: docker build -t ai-image-fixer .

Then execute: docker run -p 8501:8501 ai-image-fixer
