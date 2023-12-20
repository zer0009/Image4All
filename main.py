import PySimpleGUI as sg
import cv2
from PIL import Image
import operator
from scipy.ndimage import generic_filter
from pylab import *  # to use mean , median , max , min , range
import os.path
import PIL.Image
import io
import base64

from utilts import general_processing, general_processing_color, stretch_operation, outlier

global filename


def convert_to_bytes(file_or_bytes, re_size=None):
    if isinstance(file_or_bytes, str):
        image = PIL.Image.open(file_or_bytes)
    else:
        try:
            image = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception:
            dataBytesIO = io.BytesIO(file_or_bytes)
            image = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = image.size
    if re_size:
        new_width, new_height = re_size
        scale = min(new_height / cur_height, new_width / cur_width)
        image = image.resize((int(cur_width * scale), int(cur_height * scale)), PIL.Image.ANTIALIAS)
    bio = io.BytesIO()
    image.save(bio, format="PNG")
    del image
    return bio.getvalue()


def image_after(image, path_filename):
    imageName = path_filename.split(".")
    len1 = len(imageName)
    newImageName = filename.replace("." + imageName[len1 - 1], "1." + imageName[len1 - 1])
    cv2.imwrite(newImageName, image)
    window['-IMAGE-'].update(data=convert_to_bytes(newImageName, re_size=new_size))


# --------------------------------- Define Layout ---------------------------------
sg.theme('DarkGrey13')
section1 = [
    [sg.Button('Adding'),
     sg.Button('Subtract'),
     sg.Button('Multiply'),
     sg.Button('Power'),
     sg.Button('Blue'),
     sg.Button('Green'),
     sg.Button('Red'),
     sg.Button('look-up')],
    [sg.Button('generic_filter'),
     sg.Button('equalizeHist'),
     sg.Button('stretch'),
     sg.Button('blur'),
     sg.Button('GaussianBlur'),
     sg.Button('Laplacian')], [
        sg.Button('medianBlur'),
        sg.Button('outlier'),
        sg.Button('blue <=> red'),
        sg.Button('blue <=> green'),
        sg.Button('green <=> red')], [
        sg.Button('green <=> blue'),
        sg.Button('red <=> blue'),
        sg.Button('red <=> green'),
        # sg.Button('Hist', enable_events=True)
    ]]
# First the window layout...2 columns

left_col = [[sg.Text('Folder'), sg.In(size=(25, 1), enable_events=True, key='-FOLDER-'), sg.FolderBrowse()],
            [sg.Listbox(values=[], enable_events=True, size=(40, 20), key='-FILE LIST-')],
            [sg.Text('Resize to'), sg.In(key='-W-', size=(5, 1)), sg.In(key='-H-', size=(5, 1))], section1[0],
            section1[1], section1[2], section1[3],
            [sg.Slider(range=(1, 255), orientation='h', size=(34, 20), default_value=85, enable_events=True,
                       change_submits=True, key='change')],
            [sg.InputCombo(('Adding', 'Subtract'), size=(20, 1), key='op'),
             sg.Slider(range=(1, 100), orientation='h', size=(34, 20),
                       default_value=85)]]
# For now will only show the name of the file that was chosen
images_col = [[sg.Text('You choose from the list:')],
              [sg.Text(size=(40, 1), key='-TOUT-')],
              [sg.Image(key='-IMAGE-')]]

# ----- Full layout -----
layout = [
    [sg.Column(left_col, element_justification='c'), sg.VSeperator(),
     sg.Column(images_col, element_justification='c')]]

# --------------------------------- Create Window ---------------------------------
window = sg.Window('Multiple Format Image Viewer', layout, resizable=True)

# ----- Run the Event Loop -----
# --------------------------------- Event Loop ---------------------------------
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    value_changing = int(values['change'])

    if event == '-FOLDER-':  # Folder name was filled in, make a list of files in the folder
        folder = values['-FOLDER-']
        try:
            file_list = os.listdir(folder)  # get list of files in folder
        except:
            file_list = []
        f_names = [f for f in file_list if os.path.isfile(
            os.path.join(folder, f)) and f.lower().endswith((".png", ".jpg", "jpeg", ".tiff", ".bmp"))]
        window['-FILE LIST-'].update(f_names)
    elif event == '-FILE LIST-':  # A file was chosen from the listbox
        try:
            filename = os.path.join(values['-FOLDER-'], values['-FILE LIST-'][0])
            window['-TOUT-'].update(filename)

            if values['-W-'] and values['-H-']:
                new_size = int(values['-W-']), int(values['-H-'])
            else:
                # new_size = None
                new_size = int(720), int(480)
            window['-IMAGE-'].update(data=convert_to_bytes(filename, re_size=new_size))
        except Exception as E:
            print(f'** Error {E} **')
            pass  # something weird happened making the full filename
    try:
        global img, image1, blue, green, red
        try:
            img = cv2.imread(filename, 0)
            # image1 = cv2.imread(filename, 1)
            # blue = image1[:, :, 0]
            # green = image1[:, :, 1]
            # red = image1[:, :, 2]
        except Exception as E:
            print(f'** Error {E} **')
            sg.Popup('Select an Image!')
        if values['op'] == 'Adding':
            processing = cv2.add(img, value_changing)
            image_after(processing, filename)
        if values['op'] == 'Subtract':
            processing = cv2.add(img, -value_changing)
            image_after(processing, filename)
        if event == 'Multiply':
            processing = cv2.multiply(img, 0.8)
            image_after(processing, filename)
        if event == 'Power':
            # processing = cv2.pow(img, 1.2)
            # image_after(processing, filename)
            general_processing(img, operator.pow, 1.2)
        if event == 'Blue':
            general_processing_color(blue, operator.add, value_changing, image1)
        if event == 'Green':
            general_processing_color(green, operator.add, value_changing, image1)
        if event == 'Red':
            general_processing_color(red, operator.add, value_changing, image1)
        if event == 'look-up':
            look_up = cv2.applyColorMap(img, cv2.COLORMAP_TURBO)
            image_after(look_up, filename)
        if event == 'generic_filter':
            newImage = generic_filter(img, min, size=(3, 3))
            image_after(newImage, filename)
        if event == 'equalizeHist':
            eq = cv2.equalizeHist(img)
            image_after(eq, filename)
        if event == 'stretch':
            stretch_operation(img)
            image_after(img, filename)
        if event == 'blur':
            newImage = cv2.blur(img, (9, 9))
            image_after(newImage, filename)
        if event == 'GaussianBlur':
            newImage = cv2.GaussianBlur(img, (3, 3), sigmaX=0, sigmaY=0)
            image_after(newImage, filename)
        if event == 'Laplacian':
            newImage = cv2.Laplacian(img, cv2.CV_16S, (3, 3))
            image_after(newImage, filename)
        if event == 'medianBlur':
            newImage = cv2.medianBlur(img, 9)  # 3, 5, 7 , 9
            image_after(newImage, filename)
        if event == 'outlier':
            outlier(img)
            image_after(img, filename)
        if event == 'blue <=> red':
            image1[:, :, 0] = red
            image_after(image1, filename)
        if event == 'blue <=> green':
            image1[:, :, 0] = green
            image_after(image1, filename)
        if event == 'green <=> red':
            image1[:, :, 1] = red
            image_after(image1, filename)
        if event == 'green <=> blue':
            image1[:, :, 1] = blue
            image_after(image1, filename)
        if event == 'red <=> blue':
            image1[:, :, 2] = blue
            image_after(image1, filename)
        if event == 'red <=> green':
            image1[:, :, 2] = green
            image_after(image1, filename)
    except Exception as E:
        print(f'** Error {E} **')
        sg.Popup('No Image Found', 'Please Select an Image!')
        pass  # something weird happened making the full filename

# --------------------------------- Close & Exit ---------------------------------
window.close()
