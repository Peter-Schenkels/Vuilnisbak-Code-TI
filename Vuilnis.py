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
