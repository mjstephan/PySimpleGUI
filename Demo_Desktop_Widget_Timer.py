import PySimpleGUI as sg
import time

# ----------------  Create Form  ----------------
sg.ChangeLookAndFeel('Black')
sg.SetOptions(element_padding=(0, 0))

form_rows = [[sg.Text('')],
             [sg.Text('', size=(8, 2), font=('Helvetica', 20), justification='center', key='text')],
             [sg.ReadFormButton('Pause', key='button', button_color=('white', '#001480')),
              sg.ReadFormButton('Reset', button_color=('white', '#007339')),
              sg.Exit(button_color=('white', 'firebrick4'))]]

form = sg.FlexForm('Running Timer', no_titlebar=True, auto_size_buttons=False, keep_on_top=True, grab_anywhere=True)
form.Layout(form_rows)

# ----------------  main loop  ----------------
current_time = 0
paused = False
start_time = int(round(time.time() * 100))
while (True):
    # --------- Read and update window --------
    if not paused:
        button, values = form.ReadNonBlocking()
        current_time = int(round(time.time() * 100)) - start_time
    else:
        button, values = form.Read()
    # --------- Do Button Operations --------
    if values is None or button == 'Exit':
        break
    if button is 'Reset':
        start_time = int(round(time.time() * 100))
        current_time = 0
        paused_time = start_time
    elif button == 'Pause':
        paused = True
        paused_time = int(round(time.time() * 100))
        element = form.FindElement('button')
        element.Update(text='Run')
    elif button == 'Run':
        paused = False
        start_time = start_time + int(round(time.time() * 100)) - paused_time
        element = form.FindElement('button')
        element.Update(text='Pause')

    # --------- Display timer in window --------
    form.FindElement('text').Update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
                                                                  (current_time // 100) % 60,
                                                                  current_time % 100))
    time.sleep(.01)

# --------- After loop --------

# Broke out of main loop. Close the window.
form.CloseNonBlockingForm()
