import RPi.GPIO as GPIO
import time
import signal
import sys
import lcddriver
import psycopg2
percentage = 0
startUp = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO13


while True:
	while True:
	    lcd = lcddriver.lcd()
	    lcd.lcd_clear()
	
	    GPIO.setmode(GPIO.BCM)
	
	    pinTrigger1 = 18
	    pinEcho1 = 24
	    pinTrigger2 = 19
	    pinEcho2 = 26
	    pinTrigger3 = 21
	    pinEcho3 = 20
		
	
	    def close(signal, frame):
	
	        GPIO.cleanup()
	        sys.exit(0)
	        lcd.lcd_clear()
	
	
	    signal.signal(signal.SIGINT, close)
	
	    # set GPIO input and output channels
	    GPIO.setup(pinTrigger3, GPIO.OUT)
	    GPIO.setup(pinEcho3, GPIO.IN)
	    GPIO.setup(pinTrigger2, GPIO.OUT)
	    GPIO.setup(pinEcho2, GPIO.IN)
	    GPIO.setup(pinTrigger1, GPIO.OUT)
	    GPIO.setup(pinEcho1, GPIO.IN)
	    # Connecten database
	    
	    try:
	        conn = psycopg2.connect("dbname='lpdstrtn' " "user='lpdstrtn' " "host='dumbo.db.elephantsql.com' " "password='OQBOtTdWyf5xbdDqwGFyi_T_rQ2KcjNw'")
	        
	            
	           
	    except:
	        lcd.lcd_display_string("Connectie", 1)
	        lcd.lcd_display_string("Mislukt", 2)
	        print("I am unable to connect to the database.")
	
	        time.sleep(2)
	        startUp = 0
	        continue
	    if startUp == 0:
		    cur = conn.cursor()
		    lcd.lcd_display_string("Connectie", 1)
		    lcd.lcd_display_string("Voltooid", 2)
		    time.sleep(2)
		    startUp = 1
	
	
	    def updatevolume(containernummer, volume):
	        sql = "UPDATE container SET volume = %s WHERE containernummer = %s"
	        try:
	            cur.execute(sql, (volume, containernummer))
	            conn.commit()
	        except:
	            print("Can't UPDATE container")
	            startUp = 2
	            lcd.lcd_clear()
	            lcd.lcd_display_string("Connectie fout", 1)
	            
	
	
	    # 1e sensor kalibratie
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
	        lcd.lcd_display_string(lcdWaarde, 1)
	        lcd.lcd_display_string("Kalibratie 1 volt", 2)
	        time.sleep(2)
	        K1 = afstand
	
	
	    else:
	        lcd.lcd_display_string("Kalibratie 1 mislukt", 1)
	        lcd.lcd_display_string("Herstart in 2s", 2)
	        time.sleep(2)
	        continue
	        
	    # 3e sensor kalibratie
	    GPIO.output(pinTrigger3, True)
	    time.sleep(0.00001)
	    GPIO.output(pinTrigger3, False)
	
	    startTijd = time.time()
	    stopTijd = time.time()
	
	    while 0 == GPIO.input(pinEcho3):
	        startTijd = time.time()
	
	    while 1 == GPIO.input(pinEcho3):
	        stopTijd = time.time()
	
	    TimeElapsed = stopTijd - startTijd
	
	    afstand = (TimeElapsed * 34300) / 2
	
	    print ("Kalibratie waarde 1: %.1f cm" % afstand)
	    time.sleep(1)
	    if afstand < 400:
	
	        lcdWaarde = "Afstand: %.1f cm" % afstand
	        lcd.lcd_display_string(lcdWaarde, 1)
	        lcd.lcd_display_string("Kalibratie 3 volt", 2)
	        time.sleep(2)
	        K3 = afstand
	
	
	    else:
	        lcd.lcd_display_string("Kalibratie 3 mislukt", 1)
	        lcd.lcd_display_string("Herstart in 2s", 2)
	        time.sleep(2)
	        continue
	    # 2e sensor kalibratie
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
	        lcd.lcd_display_string(lcdWaarde, 1)
	        lcd.lcd_display_string("Kalibratie 2 vol", 2)
	        time.sleep(2)
	        K2 = afstand
	    else:
	    	lcd.lcd_display_string("Kalibratie 3 mislukt", 1)
	    	lcd.lcd_display_string("Herstart in 2s", 2)
	    	time.sleep(2)
	    	continue
	    if (K2 - K1) < 4 and (K2 - K1) > - 4:
	        if (K3 - K1) < 4 and (K3 - K1) > - 4:
	            if (K2 - K3) < 4 and (K2 - K3) > - 4:
	                diepte1 = K1
	                diepte2 = K2
	                diepte3 = K3
	                break
	            else:
	                    lcd.lcd_clear()
	                    lcd.lcd_display_string("Verschil te hoog", 1)
	                    time.sleep(2)
	                    
	                 
	                    lcd.lcd_clear()
	                    lcd.lcd_display_string("Kalibratie mislukt", 1)
	                    lcd.lcd_display_string("Herstart in 2s", 2)
	                    time.sleep(2)
	        else:
	                lcd.lcd_clear()
	                lcd.lcd_display_string("Verschil te hoog", 1)
	                
	                time.sleep(2)
	                lcd.lcd_clear()
	                
	               
	                lcd.lcd_display_string("Kalibratie mislukt", 1)
	                lcd.lcd_display_string("Herstart in 2s", 2)
	                time.sleep(2)
	    else:
	        lcd.lcd_clear()
	        lcd.lcd_display_string("Verschil te hoog", 1)
	        
	        time.sleep(2)
	        lcd.lcd_clear()
	        
	        lcd.lcd_display_string("Kalibratie mislukt", 1)
	        lcd.lcd_display_string("Herstart in 2s", 2)
	        time.sleep(2)
	        button_state = GPIO.input(13)
	        if button_state == False:
	        	print('Reset')
	        	lcd.lcd_clear()
	        	lcd.lcd_display_string("Reset", 1)
	        	time.sleep(2)
	        	continue
	     
	
	
	
	    
	
	    
	while True:
	    # Sensor 1
	    
	    #sensor instellen
	    GPIO.output(pinTrigger1, True)
	    time.sleep(0.00001)
	    GPIO.output(pinTrigger1, False)
	    
	
		#tijd instellen
	    startTijd1 = time.time()
	    stopTijd1 = time.time()
		
		#afstand berekenen
	    while 0 == GPIO.input(pinEcho1):
	        startTijd1 = time.time()
	
	    while 1 == GPIO.input(pinEcho1):
	        stopTijd1 = time.time()
	
	    TimeElapsed1 = stopTijd1 - startTijd1
	
	    afstand1 = (TimeElapsed1 * 34300) / 2
	    
	    if afstand1 > 400:
	    	print("mislukt")
	    	print(afstand1, "sensor 1")
	    	continue
			
	    percentage1 = (100 - int(afstand1 / diepte1 * 100))
	    print (percentage1, "% 1")
	    time.sleep(0.1)
	
	    # Sensor 2
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
	    if afstand2 > 400:
	    	print("mislukt")
	    	print(afstand2, "sensor 2")
	    	continue
	
	    percentage2 = (100 - int(afstand2 / diepte2 * 100))
	    print (percentage2, "% 2")
	    # Sensor 3
	    GPIO.output(pinTrigger3, True)
	    time.sleep(0.00001)
	    GPIO.output(pinTrigger3, False)
	
	    startTijd3 = time.time()
	    stopTijd3 = time.time()
	
	    while 0 == GPIO.input(pinEcho3):
	        startTijd3 = time.time()
	
	    while 1 == GPIO.input(pinEcho3):
	        stopTijd3 = time.time()
	
	    TimeElapsed3 = stopTijd3 - startTijd3
	
	    afstand3 = (TimeElapsed3 * 34300) / 2
	    
	    if afstand1 > 400:
	    	print("mislukt")
	    	print(afstand1, "sensor 1")
	    	continue
	
	    percentage3 = (100 - int(afstand3 / diepte3 * 100))
	    print (percentage3, "% 3")
	    time.sleep(0.1)
	    # Waarde berekenen
	  
	    percentage = int((percentage1 + percentage2 + percentage3) / 3)
	    
	    if percentage < 0:
	        percentage = 0
	        
	    lcdWaarde = str(percentage) + "%"   
	   
	    
	    
		
	    # updatevolume(containernummer, volume)
	    print(percentage)
	    if percentage > 0 and percentage < 101:
	    	updatevolume(101, percentage)
	    else:
	    	updatevolume(101, 100)
	    	
	    if startUp == 2:
	    	startUp = 0
	    	print("continue")
	    	continue
	    print(percentage)
	    
	        
	    lcd.lcd_clear()
	    lcd.lcd_display_string("Status: "+ lcdWaarde, 1)
	    button_state = GPIO.input(13)
	    if button_state == False:
	    	print('reset')
	    	lcd.lcd_clear()
	    	lcd.lcd_display_string("Reset", 1)
	    	
	    	time.sleep(2)
	    	break
	    	
	         
	    time.sleep(3)
	    if button_state == False:
	    	print('reset')
	    	lcd.lcd_clear()
	    	lcd.lcd_display_string("Reset", 1)
	    	
	    	time.sleep(2)
	    	break
	    	
	         
	    time.sleep(3)
	    if button_state == False:
	    	print('reset')
	    	lcd.lcd_clear()
	    	lcd.lcd_display_string("Reset", 1)
	    	startUp = 0
	    	
	    	time.sleep(2)
	    	break
	    	
	         
	    time.sleep(3)
	    if button_state == False:
	    	print('reset')
	    	lcd.lcd_clear()
	    	lcd.lcd_display_string("Reset", 1)
	    	time.sleep(3)
	    	break
	    	
	         
	    time.sleep(3)
	startUp = 0
