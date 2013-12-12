// imports serial lib
import processing.serial.*;
Serial arduinoPort;
// imports sound lib
import ddf.minim.*;
AudioPlayer aid;
Minim minim;
// font settings
PFont myFont;
PFont symbolFont;
// defines if input is through serial or keyboard
boolean serialInput=true;
// which button is currently selected - 8 is none for now
int selectedButton=8;
//which menu is currently selected and where it's buttons lead to. 0 is not used
int currentMenu=1;
boolean pushButton=false;
// declaration of variables related to aid menu
boolean aidStart = true, flashCounterUp=true;
int aidFlashCounter=0;
// chosen preset sentence, preset sentence being shown and imported preset strings
int currentPreset=1;
int showPreset=0;
String[] presetText1, presetText2, presetText3;
// writer settings
char alphabet[] =
{'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9'};
char alphabetCaps[] =
{'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','1','2','3','4','5','6','7','8',
'9'};
char symbols[] =
{'.',',',';',':','-','+','!','?','(',')','*','<','>','@','"','#','%','&','/','$','�','�','=','�','�','{','1','2','3','4','5','6','7','8','9'}
; int currentAlphabetType=0;
int textCursor=0;
int writerPanel=0; //writerPanel: 0-main, 1-abcde, 2-...
StringBuilder userText = new StringBuilder("");
char alphabetFull[][]= new char[3][26];
//visual settings
int buttonRadius=140, buttonScattering=280;
//defines which number is attributed to which menu, for ease of programme read
// Everytime you add a new menu, you must change menuDefinitions and menuTitle instancing and definitions
int menuMain=1, menuHelp=2, menuMessage=3, menuPredf=4, menuPredf1=5, menuPredf2=6,
menuPredf3=7, menuWriter=8, menuWeb=9, menuMouse=10;
// the array where each menu's defns and titles are stored
int[][] menuDefinitions = new int[11][8]; //[number of menus][numer of choices in each menu]
String[] menuTitle = new String[11]; //[number of menus]
//the counter that specifies when selection is nullified and the
//number of loops it will hold the selection
int loopCounter=0, holdTime=80;
void setup() {
// Visual definitions
size(1024,768);
smooth();
// Serial communication definitions
println(Serial.list());
arduinoPort = new Serial(this, Serial.list()[1], 115200);
// audio definitions
minim = new Minim(this);
aid = minim.loadFile("7NL10002.mp3", 2048);
//aid.loop();
//aid.pause();
myFont = createFont("Aharoni Negrito", 80, true, symbols);
symbolFont = loadFont("LaGirouette-70.vlw");
//symbolFont = loadFont("Aharoni-Bold-48.vlw");
textFont(myFont);
textAlign(CENTER, CENTER);
//temp test setups | MUST CREATE EXTERNAL EDITOR IMPORT - not
menuTitle[1]="main";
menuTitle[2]="aid";
menuTitle[3]="message";
menuTitle[4]="preset";
menuTitle[5]="set 1";
menuTitle[6]="set 2";
menuTitle[7]="set 3";
menuTitle[8]="writer";
menuTitle[9]="web";
menuTitle[10]="mouse";
//GLOBAL MENU NAVIGATION
menuDefinitions[menuMain][0]=menuHelp;
menuDefinitions[menuMain][2]=menuMessage;
menuDefinitions[menuMain][4]=menuMouse;
menuDefinitions[menuMain][6]=menuWeb;
menuDefinitions[menuHelp][6]=menuMain;
menuDefinitions[menuMessage][0]=menuWriter;
menuDefinitions[menuMessage][2]=menuPredf;
menuDefinitions[menuMessage][6]=menuMain;
menuDefinitions[menuPredf][0]=menuPredf1;
menuDefinitions[menuPredf][2]=menuPredf2;
menuDefinitions[menuPredf][4]=menuPredf3;
menuDefinitions[menuPredf][6]=menuMessage;
menuDefinitions[menuPredf1][0]=1;
menuDefinitions[menuPredf1][2]=1;
menuDefinitions[menuPredf1][4]=1;
menuDefinitions[menuPredf1][6]=menuPredf;
menuDefinitions[menuPredf2][0]=1;
menuDefinitions[menuPredf2][2]=1;
menuDefinitions[menuPredf2][4]=1;
menuDefinitions[menuPredf2][6]=menuPredf;
menuDefinitions[menuPredf3][0]=1;
menuDefinitions[menuPredf3][2]=1;
menuDefinitions[menuPredf3][4]=1;
menuDefinitions[menuPredf3][6]=menuPredf;
menuDefinitions[menuWriter][0]=1;
menuDefinitions[menuWriter][1]=1;
menuDefinitions[menuWriter][2]=1;
menuDefinitions[menuWriter][3]=1;
menuDefinitions[menuWriter][4]=1;
menuDefinitions[menuWriter][5]=1;
menuDefinitions[menuWriter][6]=1;
menuDefinitions[menuWriter][7]=1;
menuDefinitions[menuWeb][6]=menuMain;
menuDefinitions[menuMouse][6]=menuMain;
presetText1 = loadStrings("preset1.txt");
presetText2 = loadStrings("preset2.txt");
presetText3 = loadStrings("preset3.txt");
alphabetFull[0] = alphabet;
alphabetFull[1] = alphabetCaps;
alphabetFull[2] = symbols;
}
void draw() {
background(255);
menuSwitch();
if (serialInput) {
callSerial();
}
else numLockInput();
loopCounterIncrm();
}
// always close Minim audio classes when you are done with them
void stop()
{
aid.close();
minim.stop();
super.stop();
}
// serial communication protocol
void callSerial() {
String myString = arduinoPort.readStringUntil(' '); //the ascii value of the "|" character
if(myString != null ){
if(selectedButton!=int(trim(myString)) && int(trim(myString)) <8){
pushButton=false;
selectedButton=int(trim(myString));
loopCounter=0;
println(selectedButton);
} else if (int(trim(myString)) ==8){
pushButton=true;
println("les go");
}
}}
// keyboard input - whenever a key is pressed, if the the respective button is not null,
// it is selected and the loop counter is reset
void numLockInput() {
if(keyPressed) {
if (key == '1' && menuDefinitions[currentMenu][5]!=0) {
selectedButton=5;
loopCounter=0;
}
if (key == '2' && menuDefinitions[currentMenu][4]!=0) {
selectedButton=4;
loopCounter=0;
}
if (key == '3' && menuDefinitions[currentMenu][3]!=0) {
selectedButton=3;
loopCounter=0;
}
if (key == '4' && menuDefinitions[currentMenu][6]!=0) {
selectedButton=6;
loopCounter=0;
}
if (key == '6' && menuDefinitions[currentMenu][2]!=0) {
selectedButton=2;
loopCounter=0;
}
if (key == '7' && menuDefinitions[currentMenu][7]!=0) {
selectedButton=7;
loopCounter=0;
}
if (key == '8' && menuDefinitions[currentMenu][0]!=0) {
selectedButton=0;
loopCounter=0;
}
if (key == '9' && menuDefinitions[currentMenu][1]!=0) {
selectedButton=1;
loopCounter=0;
}
if (key == 'p') {
saveFrame("testPrints-####.png");
}
}
}

void large_GUI() {
// menu title
fill(0);
textSize(80);
text(menuTitle[currentMenu], width/2, height/2);
// if a button is selected draw it in bold
if(selectedButton<8) {
strokeWeight(14);
ellipse(width/2+cos(3*PI/2+(selectedButton)*PI/4)*buttonScattering,height/2+sin(3*PI/2+
(selectedButton)*PI/4)*buttonScattering,buttonRadius,buttonRadius);
}
// draw the circle buttons and the text inside
int n;
for (n=0; n<8; n++) {
if( menuDefinitions[currentMenu][n]!=0 ) {
fill(255);
strokeWeight(4);
ellipse(width/2+cos(3*PI/2+n*PI/4)*buttonScattering,height/2+sin(3*PI/2+n*PI/4)*buttonScattering,
buttonRadius,buttonRadius);
fill(0);
textSize(25);
text(menuTitle[menuDefinitions[currentMenu][n]], width/2+cos(3*PI/2+n*PI/4)*buttonScattering, height/2+sin(3*PI/2+n*PI/4)*buttonScattering);
}
}
//what happens when enter is pressed - REPLACE BY BLINK - JUNTAR COM FUNCAO DE BAIXO
if(keyPressed) {
if (key == '5') {
if(selectedButton<8) {
currentMenu=menuDefinitions[currentMenu][selectedButton];
loopCounter=0;
selectedButton=8;
}
}
}
if(pushButton && selectedButton!=8) {
pushButton=false;
currentMenu=menuDefinitions[currentMenu][selectedButton];
loopCounter=0;
selectedButton=8;
}
}
void menuSwitch() {
switch (currentMenu) {
//if emergency menu
case 2:
if(aidStart) {
aid.loop();
aidStart=false;
}
aidTitleFlash();
break;
//preset menu
case 5:
small_GUI();
presets_GUI(presetText1);
break;
case 6:
small_GUI();
presets_GUI(presetText2);
break;
case 7:
small_GUI();
presets_GUI(presetText3);
break;
// writer menu
case 8:
writer_GUI();
break;
//else is Large GUI
default:
stopAidSound();
large_GUI();
break;
}
}
//loop counter that runs in the end of every cycle to determine how long a button stays toggled
void loopCounterIncrm() {
loopCounter+=1;
if (loopCounter>holdTime) {
loopCounter=0;
selectedButton=8;
}
}
void aidTitleFlash(){
aidFlashCounter = (flashCounterUp) ? aidFlashCounter+2 : aidFlashCounter-2;
if(aidFlashCounter>=254) flashCounterUp=false;
if(aidFlashCounter<=0) flashCounterUp=true;
background(255-aidFlashCounter);
large_GUI();
textSize(80);
fill(255,0,0,aidFlashCounter);
text(menuTitle[currentMenu], width/2, height/2);
}
//stop the aid Sound when leaving aid request
void stopAidSound() {
aid.pause();
aid.rewind();
aidStart=true;
aidFlashCounter=0;
}
void small_GUI() {
// GUI border
strokeWeight(1);
fill(255);
ellipse(0,height/3,600,350);
// menu title
//pushStyle();
fill(0);
textSize(30);
text(menuTitle[currentMenu], width/8, height/3);
//popStyle();
// if a button is selected draw it in bold
if(selectedButton!=8) {
//pushStyle();
strokeWeight(5);
ellipse(width/8+cos(3*PI/2+(selectedButton)*PI/4)*buttonScattering/3,height/3+sin(3*PI/2+
(selectedButton)*PI/4)*buttonScattering/3,buttonRadius/3,buttonRadius/3);
//popStyle();
}
// draw the circle buttons and the text inside
for (int n=0; n<8; n++) {
if( menuDefinitions[currentMenu][n]!=0 ) {
fill(255);
strokeWeight(1);
ellipse(width/8+cos(3*PI/2+n*PI/4)*buttonScattering/3,height/3+sin(3*PI/2+n*PI/4)*buttonScattering/3,buttonRadius/3,buttonRadius/3);
fill(0);
// textSize(25);
// text(menuTitle[menuDefinitions[currentMenu][n]],width/2+cos(3*PI/2+n*PI/4)*buttonScattering, height/2+sin(3*PI/2+n*PI/4)*buttonScattering);
pushMatrix();
translate(width/8,height/3);
textFont(symbolFont);
rotate(PI*n/4);
text("X", 0, -buttonScattering/3-10);
popMatrix();
textFont(myFont);
}
}
}
void presets_GUI(String[] presetText) {
//what happens when enter is pressed - REPLACE BY BLINK
if(keyPressed) {
if (key == '5') {
if(selectedButton==0) {
if(currentPreset>1) {
currentPreset -= 1;
}
loopCounter=0;
selectedButton=8;
}
if(selectedButton==2) {
showPreset=currentPreset;
loopCounter=0;
selectedButton=8;
}
if(selectedButton==4) {
if(currentPreset<presetText1.length-1) {
currentPreset += 1;
}
loopCounter=0;
selectedButton=8;
}
if(selectedButton==6) {
currentMenu=menuDefinitions[currentMenu][selectedButton];
currentPreset=1;
showPreset=0;
loopCounter=0;
selectedButton=8;
}
}
}
if(selectedButton==2) {
strokeWeight(3);
line(width/2.5, height/3+18, width-width/10, height/3+18);
}
// Writes the presents options
pushStyle();
textAlign(LEFT,CENTER);
for(int n=-3; n<=3; n++) {
if(currentPreset+n >= 0 && currentPreset+n <= presetText1.length-1) {
textSize(25-2*abs(n));
fill(0,255-sqrt(abs(n))*125);
text(presetText[currentPreset+n], width/2.5-sq(abs(n))*10, height/3+n*50);
}
}
strokeWeight(1);
line(width/2.5, height/3+18, width-width/10, height/3+18);
popStyle();
textSize(100);
rectMode(CENTER);
text(presetText[showPreset],width/2,height*.75,width-width/20,height/3);
}
void writer_GUI() {
// if a button is selected draw it in bold
if(selectedButton!=8) {
strokeWeight(5);
ellipse(width/2+cos(3*PI/2+(selectedButton)*PI/4)*buttonScattering/2,height*.27+sin(3*PI/2+
(selectedButton)*PI/4)*buttonScattering/2,buttonRadius/2,buttonRadius/2);
}
// draw the circle buttons
for (int n=0; n<8; n++) {
fill(255);
strokeWeight(2);
ellipse(width/2+cos(3*PI/2+n*PI/4)*buttonScattering/2,height*.27+sin(3*PI/2+n*PI/4)*buttonScattering/2,buttonRadius/2,buttonRadius/2);
fill(0);
}
// draw the text inside the buttons
for (int n=0; n<8; n++) {
if(writerPanel==0) {
textSize(18);
if(n>=0 && n<=4)
for(int i=0; i<7; i++) {
text(alphabetFull[currentAlphabetType][alphabetFull[currentAlphabetType].length/5*n+i]+ "",width/2+cos(3*PI/2+n*PI/4)*buttonScattering/2+cos(i*2*PI/8+10*PI/8)*24, height*.27+sin(3*PI/2+n*PI/4)*buttonScattering/2+sin(i*2*PI/8+10*PI/8)*24);
}
if(n==4) text(alphabetFull[currentAlphabetType][alphabetFull[currentAlphabetType].length/5*n] +
"" + alphabetFull[currentAlphabetType][alphabetFull[currentAlphabetType].length/5*n+1] + "" +
alphabetFull[currentAlphabetType][alphabetFull[currentAlphabetType].length/5*n+2] + "\n" +
alphabetFull[currentAlphabetType][alphabetFull[currentAlphabetType].length/5*n+3]+ "" +
alphabetFull[currentAlphabetType][alphabetFull[currentAlphabetType].length/5*n+4]+ "" +
alphabetFull[currentAlphabetType][alphabetFull[currentAlphabetType].length/5*n+5],
width/2+cos(3*PI/2+n*PI/4)*buttonScattering/2, height*.27+sin(3*PI/2+n*PI/4)*buttonScattering/2);
if(n==5) text("text\ntools", width/2+cos(3*PI/2+n*PI/4)*buttonScattering/2, height*.27+sin(3*PI/2
+n*PI/4)*buttonScattering/2);
if(n==7) text("caps\nsymb", width/2+cos(3*PI/2+n*PI/4)*buttonScattering/2, height*.27+sin(3*PI/2
+n*PI/4)*buttonScattering/2);
}
else if(writerPanel>0 && writerPanel<=5) {
if(n!=7) {
textSize(20);
text(alphabetFull[currentAlphabetType][n+(writerPanel-1)*7], width/2+cos(10*PI/8+n*PI/4)*buttonScattering/2,height*.27+sin(10*PI/8+n*PI/4)*buttonScattering/2);
}
}
if(writerPanel==6){
if(n==1) text("para\ngraph", width/2+cos(3*PI/2+n*PI/4)*buttonScattering/2, height*.27+sin(3*PI/2
+n*PI/4)*buttonScattering/2);
if(n==2) text("space", width/2+cos(3*PI/2+n*PI/4)*buttonScattering/2, height*.27+sin(3*PI/2+n*PI
/4)*buttonScattering/2);
if(n==3) text("cursor\nright", width/2+cos(3*PI/2+n*PI/4)*buttonScattering/2, height*.27+sin(3*PI/
2+n*PI/4)*buttonScattering/2);
if(n==5) text("cursor\nleft", width/2+cos(3*PI/2+n*PI/4)*buttonScattering/2, height*.27+sin(3*PI/2
+n*PI/4)*buttonScattering/2);
if(n==7) text("back\nspace", width/2+cos(3*PI/2+n*PI/4)*buttonScattering/2, height*.27+sin(3*PI/
2+n*PI/4)*buttonScattering/2);
}
if(n==6) text("<", width/2+cos(3*PI/2+n*PI/4)*buttonScattering/2, height*.27+sin(3*PI/2+n*PI/4)*buttonScattering/2);
}
//what happens when enter is pressed - REPLACE BY BLINK
if(pushButton || (keyPressed && key == '5' && selectedButton!=8)) {
//If the main panel is active
if(writerPanel==0) {
//If letter or text tool buttons are selected
if(selectedButton>=0 && selectedButton<=5) {
writerPanel=selectedButton+1;
loopCounter=0;
selectedButton=8;
}
if(selectedButton==6) {
currentMenu=menuMessage;
loopCounter=0;
selectedButton=8;
}
if(selectedButton==7) {
currentAlphabetType += 1;
if(currentAlphabetType > 2) currentAlphabetType =0;
loopCounter=0;
selectedButton=8;
}
}
//if the letter panels are activated
else if(writerPanel>0 && writerPanel<=5) {
//if the letter buttons are selected
if(selectedButton>=0 && selectedButton<=5) {
userText.insert(textCursor,alphabetFull[currentAlphabetType][selectedButton+1+(writerPanel-
1)*7]);
textCursor +=1;
writerPanel=0;
loopCounter=0;
selectedButton=8;
}
if(selectedButton==6) {
writerPanel=0;
loopCounter=0;
selectedButton=8;
}
if(selectedButton==7) {
userText.insert(textCursor,alphabetFull[currentAlphabetType][(writerPanel-1)*7]);
textCursor +=1;
writerPanel=0;
loopCounter=0;
selectedButton=8;
}
}
//if the text tool panel is activated
else if(writerPanel==6) {
switch(selectedButton) {
//paragraph
case 1:
userText.insert(textCursor,'\n');
textCursor+=1;
writerPanel=0;
loopCounter=0;
selectedButton=8;
break;
//space
case 2:
userText.insert(textCursor,' ');
textCursor+=1;
writerPanel=0;
loopCounter=0;
selectedButton=8;
break;
//cursorRight
case 3:
if(textCursor+1<userText.length()){
textCursor+=1;
writerPanel=0;
loopCounter=0;
selectedButton=8;
}
break;
//cursorLeft
case 5:
if(textCursor-1>=0){
textCursor-=1;
writerPanel=0;
loopCounter=0;
selectedButton=8;
}
break;
//back to menu
case 6:
writerPanel=0;
loopCounter=0;
selectedButton=8;
break;
case 7:
if(textCursor-1>=0){
userText.deleteCharAt(textCursor-1);
textCursor-=1;
writerPanel=0;
loopCounter=0;
selectedButton=8;
}
break;
}
}
}
//text box
strokeWeight(2);
rectMode(CORNER);
fill(245);
// rect(width/2,height*.75,width*.8,height*.4);
rect(width*.05,height*.55,width*.9,height*.40);
fill(0);
textSize(20);
//cursorTimer+=1;
//if(cursorTimer>100) cursorTimer=0;
//if(cursorTimer>50) userText.insert(textCursor,'|');
//else userText.insert(textCursor," ");
userText.insert(textCursor,'|');
textAlign(LEFT,TOP);
text(userText.toString(),width*.06,height*.56,width*.88,height*.38);
textAlign(CENTER,CENTER);
userText.deleteCharAt(textCursor);
}
