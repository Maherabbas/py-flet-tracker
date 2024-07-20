import flet as ft
from pynput import keyboard, mouse
from threading import Timer
import math as Math
from pyautogui import screenshot
import os
import time

def convertHMS(value:int):
    if value == 0:
        return "00:00:00"
    h = Math.floor(value / 3600)
    m = Math.floor((value - h * 3600)/ 60)
    s = value - h * 3600 - m * 60
    
    if h < 10:
        h = f"0{h}"
    if m < 10:
        m = f"0{m}"
    if s < 10:
        s = f"0{s}"
    
    return f"{h}:{m}:{s}"
    
def main(page: ft.Page):
    page.title = "Tracker Demo"
    page.window.width = 476
    page.window.height = 768
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    is_tracker=ft.Ref[bool]()
    is_tracker.current = False
    img_thread = ft.Ref[bool]()
    img_thread.current = False
    mouseCount = ft.Ref[int]()
    mouseCount.current = 0
    keyboardCount = ft.Ref[int]()
    keyboardCount.current= 0
    btn_label = ft.Ref[ft.FilledButton]()
    tracker_label = ft.Text(value="Tracker is: Stop", text_align=ft.MainAxisAlignment.CENTER)
    mouse_count_label = ft.Text(value=f"Mouse count: {str(mouseCount.current)}", text_align=ft.MainAxisAlignment.CENTER)
    keyboard_count_label = ft.Text(value=f"Keyboard count: {str(keyboardCount.current)}", text_align=ft.MainAxisAlignment.CENTER)
    
    track_time = ft.Ref[int]()
    track_time.current = 0
    time_label = ft.Text(value=f"00:00:00", text_align=ft.MainAxisAlignment.CENTER)
    
    def mouseClick(x,y,button, pressed):
        if pressed:
            if(is_tracker.current is True):
                # print(f'mouse click {mouseCount.current}')
                mouseCount.current = mouseCount.current + 1
                mouse_count_label.value = f"Mouse count: {str(mouseCount.current)}"
                page.update()
            
        
    def keyPress(key):
        if(is_tracker.current is True):
            # print(f"Key press: {keyboardCount.current}")
            keyboardCount.current = keyboardCount.current + 1
            keyboard_count_label.value = f"Keyboard count: {str(keyboardCount.current)}"
            page.update()
        
    mListner = mouse.Listener(on_click=mouseClick)
    kListner = keyboard.Listener(on_press=keyPress)
    mListner.start()
    kListner.start()
    
    def updateTrackTime():
        if is_tracker.current is True:
            track_time.current = track_time.current + 1
            time_label.value = convertHMS(track_time.current)
            tt_thread = Timer(1.0, updateTrackTime)    
            if tt_thread.is_alive() is False:
                tt_thread.start()
                
            page.update()
                
    def takeSS():
        if is_tracker.current is True:
            ss_thread = Timer(60, takeSS)    
            if img_thread.current is True:
                image = screenshot()
                time_sec = time.time()
                folder = "./images"
                if os.path.exists(folder) is False:
                    os.mkdir(folder)
                    
                image_name = f"{folder}/{time_sec}.webp"
                image.save(image_name)
                
            if ss_thread.is_alive() is False :
                img_thread.current = True
                ss_thread.start()
                
            
            # if ss_thread.is_alive() is False:
            #     ss_thread.start()
            
        
    def trackerToggle(e):
        if(is_tracker.current is True):
            is_tracker.current = False
            tracker_label.value = "Tracker is: Stop"
            btn_label.current.text = "Start"
            
        else :
            mouseCount.current = 0
            keyboardCount.current = 0
            mouse_count_label.value = f"Mouse count: {str(mouseCount.current)}"
            keyboard_count_label.value = f"Keyboard count: {str(keyboardCount.current)}"
            is_tracker.current = True
            tracker_label.value = "Tracker is: Start"
            btn_label.current.text = "Stop"
            updateTrackTime()
            takeSS()
            
        page.update()
        

    page.add(
        ft.Column([
            tracker_label,
            time_label,
            mouse_count_label,
            keyboard_count_label,
            ft.FilledButton(ref=btn_label, text="Start", on_click=trackerToggle)
        ],alignment=ft.MainAxisAlignment.CENTER,)
    )

def appRun():
    ft.app(main)

if __name__ == "__main__":
    appRun()