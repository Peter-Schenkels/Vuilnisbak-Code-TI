import RPi.GPIO as GPIO
import time
import signal
import sys
import lcddriver


while True:
    lcd = lcddriver.lcd()
    lcd.lcd_clear()


    GPIO.setmode(GPIO.BCM)


    pinTrigger1 = 18
    pinEcho1 = 24
    pinTrigger2 = 19
    pinEcho2 = 26
    
    

    def close(signal, frame):
            
            GPIO.cleanup() 
            sys.exit(0)
            lcd.lcd_clear()

    signal.signal(signal.SIGINT, close)

    # set GPIO input and output channels
    
    GPIO.setup(pinTrigger2, GPIO.OUT)
    GPIO.setup(pinEcho2, GPIO.IN)
    GPIO.setup(pinTrigger1, GPIO.OUT)
    GPIO.setup(pinEcho1, GPIO.IN)

    #1e sensor kalibratie
    # Calibreren	
    GPIO.output(pinTrigger1, True)	
    time.sleep(0.00001)
    GPIO.output(pinTrigger1, False)

    startTijd = time.time()
    stopTijd = time.time()

    while 0 == GPIO.input(pinEcho1):
        startTijd = time.time()

            
    while 1 == GPIO.input(pinEcho1):
        stopTijd = time.time()

            
    TimeElapsed = stopTijd - startTijd
        
    afstand = (TimeElapsed * 34300) / 2

    print ("Kalibratie waarde 1: %.1f cm" % afstand)
    time.sleep(1)
    if afstand < 400:
        
        
        lcdWaarde = "Afstand: %.1f cm" % afstand
        lcd.lcd_display_string(lcdWaarde ,1)
        lcd.lcd_display_string("Kalibratie 1 volt", 2)
        time.sleep(2)
        K1= afstand
        
    
    else:
        lcd.lcd_display_string("Kalibratie 1 mislukt", 1)
        lcd.lcd_display_string("Herstart in 2s", 2)
        time.sleep(2)
        continue
    #2e sensor kalibratie
    GPIO.output(pinTrigger2, True)	
    time.sleep(0.00001)
    GPIO.output(pinTrigger2, False)

    startTijd = time.time()
    stopTijd = time.time()

    while 0 == GPIO.input(pinEcho2):
        startTijd = time.time()

            
    while 1 == GPIO.input(pinEcho2):
        stopTijd = time.time()

            
    TimeElapsed = stopTijd - startTijd
        
    afstand = (TimeElapsed * 34300) / 2

    print ("Kalibratie waarde 2: %.1f cm" % afstand)
    time.sleep(1)
    if afstand < 400:
        
        lcdWaarde = "Afstand: %.1f cm" % afstand
        lcd.lcd_display_string(lcdWaarde ,1)
        lcd.lcd_display_string("Kalibratie 2 vol", 2)
        time.sleep(2)
        K2 = afstand
        if (K2 - K1) < 3 and (K2 - K1) > -3:
            diepte1 = K1
            diepte2 = K2
            break
        else:
            lcd.lcd_clear()
            lcd.lcd_display_string("Verschil te hoog", 1)
            time.sleep(2)
            lcd.lcd_clear()
            lcd.lcd_display_string("Sensor 1" + str(K1) + "cm", 1)
            lcd.lcd_display_string("Sensor 2" + str(K2) + "cm", 2)
            time.sleep(2)
            lcd.lcd_clear()
            lcd.lcd_display_string("Kalibratie mislukt", 1)
            lcd.lcd_display_string("Herstart in 2s", 2)
            time.sleep(2)
            
            
            
            
    
    else:
        lcd.lcd_display_string("Kalibratie 2 mislukt", 1)
        lcd.lcd_display_string("Herstart in 2s", 2)
        time.sleep(2)
                

            
while True:
	#Sensor 1
	GPIO.output(pinTrigger1, True)	
	time.sleep(0.00001)
	GPIO.output(pinTrigger1, False)

	startTijd1 = time.time()
	stopTijd1 = time.time()

	
	while 0 == GPIO.input(pinEcho1):
		startTijd1 = time.time()

	
	while 1 == GPIO.input(pinEcho1):
		stopTijd1 = time.time()

	
	TimeElapsed1 = stopTijd1 - startTijd1
    
	afstand1 = (TimeElapsed1 * 34300) / 2
	
	percentage1 = (100 - int(afstand1 / diepte1 * 100))
	print (percentage1,"% 1")
	time.sleep(0.1)
	
	#Sensor 2
	GPIO.output(pinTrigger2, True)	
	time.sleep(0.00001)
	GPIO.output(pinTrigger2, False)

	startTijd2 = time.time()
	stopTijd2 = time.time()

	
	while 0 == GPIO.input(pinEcho2):
		startTijd2 = time.time()

	
	while 1 == GPIO.input(pinEcho2):
		stopTijd2 = time.time()

	
	TimeElapsed2 = stopTijd2 - startTijd2
    
	afstand2 = (TimeElapsed2 * 34300) / 2
	
	percentage2 = (100 - int(afstand2 / diepte2 * 100))
	print (percentage2,"% 2")
	
	#Waarde berekenen
	percentage = (percentage1 + percentage2) * 0.5
	if percentage < 0:
            percentage = percentage + (-1*percentage)
	lcdWaarde = str(percentage) + "%"
	
	if percentage < 101 and percentage > -1:
            lcd.lcd_clear()
            lcd.lcd_display_string("Status: "+ lcdWaarde, 1)
    
	
	time.sleep(2)
	
	
