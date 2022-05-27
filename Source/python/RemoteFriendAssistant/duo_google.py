from pynput.keyboard import Key, Controller
from mysql.connector import Error
from google_speech import Speech
from threading import Thread
from gpiozero import Button
from subprocess import call
import RPi.GPIO as GPIO
import mysql.connector
import webbrowser
import pyautogui
import signal
import time
import sys
import os


Flag = 0
Stop = 0
digit = 0
letter = 0
call_flag = 0
call_counter = 0
contacts_counter = -1
names = []
numbers = []
number = ""
name = ""
selection_btn = Button(2)
append_btn = Button(3)
stop_btn = Button(4)


def stop():
    global Flag
    Flag = 4
    print(Flag)
    
def append():
    global digit
    global number
    
    os.system("pkill mpg321")
    if digit != -1:
        number += str(digit)
        print("Whole number: " + number)
    digit = -1
    
#def stop_while_loop():
#    GPIO.setwarnings(False) # Ignore warning for now
#    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
#    GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 3 to be an input pin and set initial value to be pulled low (off)
#    GPIO.add_event_detect(3, GPIO.RISING, callback=stop) # Setup event on pin 3 rising edge
#
#def append_digit_to_number():
#    GPIO.setwarnings(False) # Ignore warning for now
#    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
#    GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 3 to be an input pin and set initial value to be pulled low (off)
#    GPIO.add_event_detect(7, GPIO.RISING, callback=append) # Setup event on pin 3 rising edge


#def enter_digit(digit):
    
#call_counter = 0

def increase_digit():
    global digit
    digit += 1
    os.system("pkill mpg321")
    print(digit)
    
    if digit == 0:
        os.system("mpg321 /home/pi/duo_sound_files/zero.mp3 &")
    elif digit == 1:
        os.system("mpg321 /home/pi/duo_sound_files/one.mp3 &")
    elif digit == 2:
        os.system("mpg321 /home/pi/duo_sound_files/two.mp3 &")
    elif digit == 3:
        os.system("mpg321 /home/pi/duo_sound_files/three.mp3 &")
    elif digit == 4:
        os.system("mpg321 /home/pi/duo_sound_files/for.mp3 &")
    elif digit == 5:
        os.system("mpg321 /home/pi/duo_sound_files/five.mp3 &")
    elif digit == 6:
        os.system("mpg321 /home/pi/duo_sound_files/six.mp3 &")
    elif digit == 7:
        os.system("mpg321 /home/pi/duo_sound_files/seven.mp3 &")
    elif digit == 8:
        os.system("mpg321 /home/pi/duo_sound_files/eight.mp3 &")
    elif digit == 9:
        os.system("mpg321 /home/pi/duo_sound_files/nine.mp3 &")
    elif digit > 9:
        os.system("mpg321 /home/pi/duo_sound_files/zero.mp3 &")
        digit = 0


def increase_letter():
    global digit
    digit += 1
    
    os.system("pkill mpg321")
    if digit == 1:
        os.system("mpg321 /home/pi/duo_sound_files/letters/a.mp3 &")
    elif digit == 2:
        os.system("mpg321 /home/pi/duo_sound_files/letters/b.mp3 &")
    elif digit == 3:
        os.system("mpg321 /home/pi/duo_sound_files/letters/v.mp3 &")
    elif digit == 4:
        os.system("mpg321 /home/pi/duo_sound_files/letters/g.mp3 &")    
    elif digit == 5:
        os.system("mpg321 /home/pi/duo_sound_files/letters/d.mp3 &")
    elif digit == 6:
        os.system("mpg321 /home/pi/duo_sound_files/letters/e.mp3 &")
    elif digit == 7:
        os.system("mpg321 /home/pi/duo_sound_files/letters/j.mp3 &")
    elif digit == 8:
        os.system("mpg321 /home/pi/duo_sound_files/letters/z.mp3 &")
    elif digit == 9:
        os.system("mpg321 /home/pi/duo_sound_files/letters/i.mp3 &")
    elif digit == 10:
        os.system("mpg321 /home/pi/duo_sound_files/letters/i_short.mp3 &")
    elif digit == 11:
        os.system("mpg321 /home/pi/duo_sound_files/letters/k.mp3 &")
    elif digit == 12:
        os.system("mpg321 /home/pi/duo_sound_files/letters/l.mp3 &")
    elif digit == 13:
        os.system("mpg321 /home/pi/duo_sound_files/letters/m.mp3 &")
    elif digit == 14:
        os.system("mpg321 /home/pi/duo_sound_files/letters/n.mp3 &")
    elif digit == 15:
        os.system("mpg321 /home/pi/duo_sound_files/letters/o.mp3 &")
    elif digit == 16:
        os.system("mpg321 /home/pi/duo_sound_files/letters/p.mp3 &")
    elif digit == 17:
        os.system("mpg321 /home/pi/duo_sound_files/letters/r.mp3 &")
    elif digit == 18:
        os.system("mpg321 /home/pi/duo_sound_files/letters/s.mp3 &")
    elif digit == 19:
        os.system("mpg321 /home/pi/duo_sound_files/letters/t.mp3 &")
    elif digit == 20:
        os.system("mpg321 /home/pi/duo_sound_files/letters/u.mp3 &")
    elif digit == 21:
        os.system("mpg321 /home/pi/duo_sound_files/letters/f.mp3 &")
    elif digit == 22:
        os.system("mpg321 /home/pi/duo_sound_files/letters/h.mp3 &")
    elif digit == 23:
        os.system("mpg321 /home/pi/duo_sound_files/letters/c.mp3 &")
    elif digit == 24:
        os.system("mpg321 /home/pi/duo_sound_files/letters/chy.mp3 &")
    elif digit == 25:
        os.system("mpg321 /home/pi/duo_sound_files/letters/sh.mp3 &")
    elif digit == 26:
        os.system("mpg321 /home/pi/duo_sound_files/letters/sht.mp3 &")
    elif digit == 27:
        os.system("mpg321 /home/pi/duo_sound_files/letters/er_short.mp3 &")
    elif digit == 28:
        os.system("mpg321 /home/pi/duo_sound_files/letters/yu.mp3 &")
    elif digit == 29:
        os.system("mpg321 /home/pi/duo_sound_files/letters/q.mp3 &")
def append_name():
    global name
    global digit
    
    if digit == 1:
        name += "а"
    elif digit == 2:
        name += "б"
    elif digit == 3:
        name += "в"
    elif digit == 4:
        name += "г"
    elif digit == 5:
        name += "д"
    elif digit == 6:
        name += "е"
    elif digit == 7:
        name += "ж"
    elif digit == 8:
        name += "з"
    elif digit == 9:
        name += "и"
    elif digit == 10:
        name += "й"
    elif digit == 11:
        name += "к"
    elif digit == 12:
        name += "л"
    elif digit == 13:
        name += "м"
    elif digit == 14:
        name += "н"
    elif digit == 15:
        name += "о"
    elif digit == 16:
        name += "п"
    elif digit == 17:
        name += "р"
    elif digit == 18:
        name += "с"
    elif digit == 19:
        name += "т"
    elif digit == 20:
        name += "у"
    elif digit == 21:
        name += "ф"
    elif digit == 22:
        name += "х"
    elif digit == 23:
        name += "ц"
    elif digit == 24:
        name += "ч"
    elif digit == 25:
        name += "ш"
    elif digit == 26:
        name += "щ"
    elif digit == 27:
        name += "ь"
    elif digit == 28:
        name += "ю"
    elif digit == 29:
        name += "я"
        
    digit = 0
    print("Whole name: " + name)
        
def end_session():
    global Flag
    Flag = 3



def insert_values_into_table(name, number):

    try:
        connection = mysql.connector.connect(host='localhost',
                                     database='DuoContacts',
                                     user='DuoUser',
                                     password='DuoPass')
        
        cursor = connection.cursor()
        mySql_insert_query = """INSERT INTO Contacts (name, number) 
                        VALUES (%s, %s) """
    
        record = (name, number)
        cursor.execute(mySql_insert_query, record)
        connection.commit()

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")





def save():
    global digit
    global Flag
    global name
    global number
    global selection_btn
    global append_btn
    global stop_btn
    
    os.system("mpg321 /home/pi/duo_sound_files/please_enter_phone_number.mp3 &")
    digit = -1
    while True:
        selection_btn.when_pressed = increase_digit
        append_btn.when_pressed = append
        if len(number) == 12:
            break
    

    digit = 0
    
    os.system("mpg321 /home/pi/duo_sound_files/enter_name.mp3")
    # enter name here
    while True:
        selection_btn.when_pressed = increase_letter
        append_btn.when_pressed = append_name
        stop_btn.when_pressed = end_session
        if Flag == 3:
            break
    
    
    # Save number to db code goes here...
    os.system("mpg321 /home/pi/duo_sound_files/saving_number_to_db.mp3 &")
    
    insert_values_into_table(str(name), str(number))
    
    time.sleep(1)
    os.system("mpg321 /home/pi/duo_sound_files/number_saved.mp3 &")
    
    Flag = 0
    name = ""
    number = ""
    
    
def increase_call_flag():
    global call_flag
    call_flag += 1
    
    os.system("pkill mpg321")
    if call_flag == 1:
        os.system("mpg321 /home/pi/duo_sound_files/call.mp3 &")
    elif call_flag == 2:
        os.system("mpg321 /home/pi/duo_sound_files/chosen_from_db.mp3 &")
    elif call_flag > 2:
        os.system("mpg321 /home/pi/duo_sound_files/call.mp3 &")
        call_flag = 1
def choose_option():
    global Flag
    
    os.system("pkill mpg321")
    Flag = 6
def call():
    global digit
    global Flag
    global name
    global call_flag
    global number
    global selection_btn
    global append_btn
    global stop_btn
    global contacts_counter
    global names
    global call_counter
    global numbers
    
    os.system("mpg321 /home/pi/duo_sound_files/call_or_choose_from_db.mp3 &")
    
    
    while True:
        selection_btn.when_pressed = increase_call_flag
        append_btn.when_pressed = choose_option
        if Flag == 6:
            break
            
    if call_flag == 1:
        digit = -1
        while True:
            selection_btn.when_pressed = increase_digit
            append_btn.when_pressed = append
            if len(number) == 12:
                break


        time.sleep(1)
        
        os.system("pkill mpg321")
        os.system("mpg321 /home/pi/duo_sound_files/calling_number.mp3 &")

        time.sleep(2.5)
        
        os.system('mpg321 please_wait.mp3 &')
        
        
        # Make duo call
        for i in range(8):
            pyautogui.press("tab")
        
        pyautogui.press("enter")
        time.sleep(5)  
        pyautogui.typewrite(number)
        
        time.sleep(5)  
        pyautogui.press("tab")
        pyautogui.press("enter")
        
        time.sleep(5)
        # Allow usage of camera and mic
        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.press("enter")
        pyautogui.press("enter")
    

            
            
            
    elif call_flag == 2:

        connection = mysql.connector.connect(host='localhost',
                                     database='DuoContacts',
                                     user='DuoUser',
                                     password='DuoPass')
        
        sql_select_Query = "select * from Contacts"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)

        records = cursor.fetchall()
        print("Total number of rows in table: ", cursor.rowcount)
        
        print("\nPrinting each row")
        for row in records:
            print("Name = ", row[0])
            print("Number = ", row[1])

            names.append(row[0])
            numbers.append(row[1])

        print(names)
        print(numbers)
        
        
        while True:
            selection_btn.when_pressed = contacts_counter_increase
            append_btn.when_pressed = select_contact
            stop_btn.when_pressed = stop_selection
            if Flag == 10:
                break
    Flag = 0
    name = ""
    number = ""
def stop_selection():
    global Flag
    Flag = 10
    
def contacts_counter_increase():
    global names
    global numbers
    global contacts_counter
    
    os.system("pkill mpg321")
    if len(names) < 1:
        lang = "bg"
        speech = Speech("няма запазени номера", lang)
        speech.save("/home/pi/duo_sound_files/no_numbers_saved.mp3")
        os.system('mpg321 /home/pi/duo_sound_files/no_numbers_saved.mp3 &')
    elif contacts_counter < len(names)-1:
        contacts_counter += 1
    else:
        contacts_counter = 0
    print(names[contacts_counter])
    
    lang = "bg"
    speech = Speech(names[contacts_counter], lang)
    speech.save("/home/pi/duo_sound_files/curr_name.mp3")
    os.system('mpg321 /home/pi/duo_sound_files/curr_name.mp3 &')
    
    
def select_contact():
    global names
    global numbers
    global call_counter
    global contacts_counter
    
    lang = "bg"
    text = "обаждането към " + names[contacts_counter] + " е изпратено"
    speech = Speech(text, lang)
    speech.save("/home/pi/duo_sound_files/curr_name.mp3")
    os.system('mpg321 /home/pi/duo_sound_files/curr_name.mp3 &')
    
    time.sleep(2.5)
        
    os.system('mpg321 please_wait.mp3 &')
    #if call_counter == 0:

    if call_counter == 0:
        call_counter = call_counter + 1
        
        # Make duo call
        for i in range(8):
            pyautogui.press("tab")
        
        pyautogui.press("enter")
        time.sleep(5)  
        pyautogui.typewrite(numbers[contacts_counter])
        
        time.sleep(5)  
        pyautogui.press("tab")
        pyautogui.press("enter")
        
        time.sleep(5)
        # Allow usage of camera and mic
        pyautogui.press("tab")
        pyautogui.press("tab")
        pyautogui.press("enter")
        pyautogui.press("enter")
    else:
        # Make duo call
        pyautogui.press("tab")
        
        pyautogui.press("enter")
        time.sleep(5)  
        pyautogui.typewrite(numbers[contacts_counter])
        
        time.sleep(5)  
        pyautogui.press("tab")
        pyautogui.press("enter")
        
        
def save_or_call_menu():
    global digit
    digit += 1
    
    os.system("pkill mpg321")
    
    if digit == 1:
        os.system("mpg321 /home/pi/duo_sound_files/save.mp3 &")
    elif digit == 2:
        os.system("mpg321 /home/pi/duo_sound_files/call.mp3 &")
    elif digit > 2:
        digit = 1
        os.system("mpg321 /home/pi/duo_sound_files/save.mp3 &")
        
def save_or_call_init():
    global Flag
    global digit
    
    os.system("pkill mpg321")
    
    if digit == 1:
        Flag = 1
    elif digit == 2:
        Flag = 2

def make_call():
    global Flag
    global digit
    global number
    global Stop
    global selection_btn
    global append_btn
    global stop_btn

    os.system("mpg321 /home/pi/duo_sound_files/save_or_call.mp3")
    while True: 
        while True:
            selection_btn.when_pressed = save_or_call_menu
            append_btn.when_pressed = save_or_call_init
            stop_btn.when_pressed = stop
            if Flag == 1:
                break
            elif Flag == 2:
                break
            elif Flag == 4:
                break
            elif Flag == 10:
                break
        
        if Flag == 1:
            save()
        
        elif Flag == 2:
            call()
        
        elif Flag == 4:
            os.system('mpg321 /home/pi/duo_sound_files/duo_quit.mp3 &')
            time.sleep(2)
            break
        
        elif Flag == 10:
            os.system('mpg321 /home/pi/duo_sound_files/duo_quit.mp3 &')
            time.sleep(2)
            break
        
        
        # call_counter = 1
        # elif call_counter == 1:
        #    webbrowser.open('https://duo.google.com/?web&utm_source=marketing_page_button_main') 
        #    time.sleep(15)
            
            # Make duo call
        #    for i in range(7):
        #        pyautogui.press("tab")
            
        #    pyautogui.press("enter")
        #    time.sleep(5)  
        #    pyautogui.typewrite('0899348344')
        #    time.sleep(5)  
        #    pyautogui.press("tab")
        #    pyautogui.press("enter")
        
    # Kill process forcefully
    with open('process_pid.txt') as f:
        pid = f.readline()
    duo_pid = int(pid)
    os.kill(duo_pid, signal.SIGKILL)
    
            
if __name__ == '__main__':
    print("friend assistance functionality")
    make_call()
    