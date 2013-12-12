/*
* Oscilloscope for EOG
*
*
* by Jo�o B�rcia
*
* built upon an oscilloscope proposal by
* (c) 2008 Sofian Audry (info@sofianaudry.com)
*
*
*
*/
import processing.serial.*;
Serial port; // Create object from Serial class
float val, val2; // Data received from the serial port
float[] values, values2, values3;
float threshold = 512;
float distance;
float spread = 1;

void setup()
{
	size(640, 480);
	// Open the port that the board is connected to and use the same speed (9600 bps)
	println(Serial.list());
	port = new Serial(this, Serial.list()[1], 115200);
	values = new float[width];
	values2 = new float[width];
	values3 = new float[width];
	smooth();
	PFont font;
	textFont(font);
}

void serialEvent(Serial myPort)
{
	String myString = myPort.readStringUntil('|'); //the ascii value of the "|" character

	if( myString != null ) {
		myString = trim(myString); //remove whitespace around our values
		int inputs[] = int(split(myString, ','));
		
		//now assign your values in processing
		if(inputs.length == 5){
			val = inputs[1];
			val2 = inputs[2];
			distance = inputs[3];
			println(inputs[3]);
		}
	}
}

float getY(float val)
{
	return (float)(val / 1023.0f * height) - 1;
}

void draw()
{
	strokeWeight(1);
	scale(spread,1);

	for (int i = 0; i< (width - 1); i++) {
		values[i] = values[i + 1];
		values2[i] = values2[i + 1];
		values3[i] = values3[i + 1];
	}
	
	// values[width-1] = val;
	values[width-1] = val;
	values2[width-1] = val2;
	values3[width-1] = distance;
	background(255);
	stroke(255);
	//line(0,480-threshold/1023*height,width,480-threshold/1023*height);
	
	for (int x = 1; x < width; x++) {
		stroke(180, 0, 0);
		line(width - x, height - 1 - getY(values[x - 1]), width - 1 - x, height - 1 - getY(values[x - 1]));
		stroke(0, 180, 0);
		line(width - x, height - 1 - getY(values2[x - 1]), width - 1 - x, height - 1 - getY(values2[x - 1]));
		stroke(0, 200);
		// line(width-x, height-1-getY(values3[x-1])*100,
		// width-1-x, height-1-getY(values3)*100);[/color]
		line(width - x, height - (9 - values3[x - 1]) * 18, width - 1 - x, height - (9 - values3[x - 1]) * 18);
	}

	for (int i = 0; i < 10; i += 1) {
		stroke(0, 40);
		line(0, height - 18 * i, width, height - 18 * i);
	}
	
	textSize(30);
	textAlign(LEFT);
	scale((1 / spread), 1);
	fill(180, 0, 0);
	text("Ver = " + val * 5 / 1024 + "V", width - 250, 70);
	fill(0,180,0);
	text("Hor = " + val2 * 5 / 1024 + "V", width - 250 , 35);
	fill(255);
	//text("Tresh = " + threshold, width-200,height-115);
	fill(0);
	//text("Signal = " + distance, width-200,150);
	textSize(15);
	textAlign(LEFT, CENTER);
	text("BLINK", 10, height - 18 * 1);
	text("UP-RIGHT", 10, height - 18 * 2);
	text("RIGHT", 10, height - 18 * 3);
	text("DOWN-RIGHT", 10, height - 18 * 4);
	text("DOWN", 10, height - 18 * 5);
	text("DOWN-LEFT", 10, height - 18 * 6);
	text("LEFT", 10, height - 18 * 7);
	text("UP-LEFT", 10, height - 18 * 8);
	text("UP", 10, height - 18 * 9);
}

void keyPressed() {
	if (key == '+') {
		threshold += 1;
	}

	if (key == '-') {
		threshold -= 1;
	}

	if (key == 'p') {
		saveFrame("finals/osciloTestPrints-####.png");;
	}
}
