// For ease of read define Horizontal and Vertical
#define HORIZONTAL 0
#define VERTICAL 1
// Include Timer One interrupt helper library
#include "TimerOne.h"
// Include PROGMEM library to store comparison matrixes
#include <avr/pgmspace.h>
byte const nMax=50;             // The maximum index value for the Value Buffer
int valBuffer[2][nMax];          // Value Buffer where current readings are stored for average
int valBufferOffseted[2][nMax];  // Value Buffer where offseted current readings are stored for analysis
int currentSignal=0;             // What signal is going on now? (0=neutral)
long dcOffset[2];                // Stores current dcOffset
int n=0;                         // Current index
int shiftedBufferIndex=0;        // Index for comparison
int minThreshold=550;
int minDistance=minThreshold;
boolean printInfo=false;         // Flag which defines if info should be printed or not
boolean firstAverage=true;       // Flag which defines if the average has not yet been calculated, in order to store the 50 (nMax) first values
long getHorFromFlash;            // Get the Horizontal values from Flash to RAM
long getVerFromFlash;            // Get the Vertical values from Flash to RAM
// Distance values
long distanceBlink[2], distanceUp[2], distanceUpRight[2], distanceRight[2], distanceDownRight[2],
distanceDown[2], distanceDownLeft[2], distanceLeft[2], distanceUpLeft[2];             // Euclidean Hor and Ver distances being calculated
long calculatedDistances[9];             // Euclidean total distances to each signal
float horBoost = 4;                // Enhances the importance the horizontal distance has in the calculated distance, due to the low amplitude of the signal
long averageForOffset[2];
// Comparison Matrixes
prog_uint16_t comparisonBlink[2][nMax] PROGMEM = {
 {
   524,514,503,527,536,524,537,546,522,513,523,505,490,508,509,492,507,521,506,507,525,513,500,519,519,499,511,523,504,505,522,511,500,519,519,500,512,524,505,505,523,512,499,518,519,499,511,
522,503,504          }
 ,
 {
   496,555,582,639,813,933,924,920,934,859,774,750,662,552,526,497,410,388,413,364,341,393,386,351,393,420,381,397,449,416,403,460,454,419,461,485,441,455,504,469,452,507,497,457,498,519,471,
484,531,494          }
};
prog_uint16_t comparisonUp[2][nMax] PROGMEM = {
 {
   514,516,516,516,520,524,522,524,523,520,520,521,520,520,519,521,518,519,520,518,517,518,517,516,517,517,515,515,514,511,509,509,508,505,506,508,506,508,510,509,510,512,511,510,512,513,509,
511,513,512          }
 ,
 {
   518,524,540,609,739,832,871,885,880,855,843,828,805,797,789,773,762,757,739,719,704,691,660,631,600,572,544,530,503,464,410,347,299,275,284,286,284,305,314,317,331,350,355,366,382,384,388,
404,410,413          }
};
prog_uint16_t comparisonUpRight[2][nMax] PROGMEM = {
 {
   524,513,494,527,551,550,588,628,617,617,642,626,600,617,615,581,588,602,573,563,585,569,545,563,562,528,536,550,521,512,533,514,487,503,495,453,452,459,422,413,441,431,412,438,445,420,434,
456,434,435          }
 ,
 {
   497,544,530,520,632,729,754,810,851,793,750,766,723,672,710,712,676,686,724,687,672,703,685,644,669,682,637,645,661,596,572,603,567,525,560,557,487,473,479,417,380,401,367,331,380,388,339,
348,375,340          }
};
prog_uint16_t comparisonRight[2][nMax] PROGMEM = {
 {
   489,518,531,512,554,618,628,651,706,702,676,697,693,646,644,657,617,596,619,595,559,578,580,540,546,561,511,475,479,429,366,369,366,331,346,381,366,369,414,413,399,439,455,426,444,477,454,
452,489,478          }
 ,
 {
   528,487,530,563,546,603,688,676,658,689,644,555,550,537,463,460,494,451,430,476,465,426,469,493,447,467,512,471,456,508,493,453,493,515,465,477,522,484,469,520,509,470,510,528,477,492,537,
499,483,535          }
};
prog_uint16_t comparisonDownRight[2][nMax] PROGMEM = {
 {
   483,508,547,517,536,615,616,603,665,675,625,643,667,609,590,627,590,549,587,584,525,548,576,525,518,564,533,490,524,512,444,447,455,388,370,415,393,373,432,444,406,443,482,441,445,499,475,
446,498,503          }
 ,
 {
   551,495,510,551,508,484,527,501,437,455,445,353,339,363,305,267,318,309,263,316,352,313,348,412,384,377,449,460,453,549,628,634,706,788,761,734,766,721,645,665,668,596,600,636,581,554,605,
583,533,574          }
};
prog_uint16_t comparisonDown[2][nMax] PROGMEM = {
 {
   519,502,514,526,509,507,522,511,497,513,513,495,505,516,499,499,517,507,496,514,514,498,508,520,503,503,520,510,499,515,518,502,512,523,506,505,521,511,499,516,517,499,509,521,504,503,520,
511,499,517          }
 ,
 {
   530,516,471,472,464,400,374,367,318,282,282,271,245,246,266,246,251,291,284,282,331,346,337,375,409,388,409,481,557,657,803,885,891,898,874,799,767,764,712,672,682,661,618,626,634,588,583,
607,579,556          }
};
prog_uint16_t comparisonDownLeft[2][nMax] PROGMEM = {
 {
   516,491,490,485,446,428,428,404,386,398,397,383,401,417,407,418,443,437,436,462,469,456,471,486,471,475,496,485,479,501,511,517,559,604,615,638,661,644,623,628,613,584,586,588,562,558,570,
552,540,554          }
 ,
 {
   513,510,491,484,471,430,403,394,355,314,314,294,277,272,281,279,273,296,302,304,330,343,347,374,397,393,402,429,427,429,472,536,617,732,828,861,867,854,799,751,734,705,668,659,650,622,611,
618,599,581          }
};
prog_uint16_t comparisonLeft[2][nMax] PROGMEM = {
 {
   505,503,485,457,444,432,410,400,399,385,376,385,388,386,402,416,414,424,441,441,445,463,468,464,477,486,484,497,523,537,554,584,601,600,609,617,611,614,621,614,610,617,607,587,584,581,564,
559,562,551          }
 ,
 {
   520,543,586,588,592,609,594,572,570,567,535,523,522,496,482,489,479,462,471,481,464,471,492,481,478,500,504,503,527,548,540,548,563,545,532,542,533,513,524,533,515,517,529,512,507,524,522,
507,517,526          }
};
prog_uint16_t comparisonUpLeft[2][nMax] PROGMEM = {
 {
   485,477,472,447,426,424,412,396,403,409,402,410,427,425,426,444,448,444,460,469,463,470,486,481,479,493,493,485,499,509,506,520,545,552,563,588,595,590,600,602,589,590,598,587,581,592,585,
568,570,568          }
 ,
 {
   558,575,612,696,745,751,785,811,778,757,762,724,688,695,679,639,644,648,616,606,625,603,579,600,595,569,579,592,563,557,580,554,539,562,544,477,447,435,398,396,415,384,355,372,365,342,355,
378,365,370          }
};
void setup() {
 // Initialize Serial communication
 Serial.begin(115200);
 // Set pins 0 and 1 as input
 pinMode(HORIZONTAL, INPUT);
 pinMode(VERTICAL, INPUT);
 Timer1.initialize(14000);         // initialize timer1, and set a 14ms period
 Timer1.attachInterrupt(collectData);  // attaches collectData() as a timer overflow interrupt
 // Reset Value Buffer
 for(int i=0; i<nMax; i++){
   valBuffer[HORIZONTAL][i]=0;
   valBuffer[VERTICAL][i]=0;
 }
 // Reset dcOffset
 dcOffset[HORIZONTAL]=0;
 dcOffset[VERTICAL]=0;
}
void collectData() {
 // Read input values
 int valHor=analogRead(HORIZONTAL);
 int valVer=analogRead(VERTICAL);
 averageForOffset[HORIZONTAL]=0;
 averageForOffset[VERTICAL]=0;
 //Average algorithm
 //if(!firstAverage){
 for(int i=0; i<nMax; i++){
   averageForOffset[HORIZONTAL]+=valBuffer[HORIZONTAL][n];
   averageForOffset[VERTICAL]+=valBuffer[VERTICAL][n];
 }
 averageForOffset[HORIZONTAL]=512-averageForOffset[HORIZONTAL]/nMax;
 averageForOffset[VERTICAL]=512-averageForOffset[VERTICAL]/nMax;
 if(averageForOffset[HORIZONTAL]>dcOffset[HORIZONTAL]) dcOffset[HORIZONTAL]+=1;
 else if(averageForOffset[HORIZONTAL]<dcOffset[HORIZONTAL]) dcOffset[HORIZONTAL]-=1;
 if(averageForOffset[VERTICAL]>dcOffset[VERTICAL]) dcOffset[VERTICAL]+=1;
 else if(averageForOffset[VERTICAL]<dcOffset[VERTICAL]) dcOffset[VERTICAL]-=1;
 //}
 
 // Send raw captures values to valBuffer to calculate averages
 valBuffer[HORIZONTAL][n]=valHor;
 valBuffer[VERTICAL][n]=valVer;
 // Send to Value Buffer the value of the reading, with respective offset
 valBufferOffseted[HORIZONTAL][n]=valHor+dcOffset[HORIZONTAL];
 valBufferOffseted[VERTICAL][n]=valVer+dcOffset[VERTICAL];
 // Test value buffer for perfect neutral
 //  valBufferOffseted[HORIZONTAL][n]=512;
 //  valBufferOffseted[VERTICAL][n]=512;
 // Reset distances
 distanceBlink[0]=0;
 distanceBlink[1]=0;
 distanceUp[0]=0;
 distanceUp[1]=0;
 distanceUpRight[0]=0;
 distanceUpRight[1]=0;
 distanceRight[0]=0;
 distanceRight[1]=0;
 distanceDownRight[0]=0;
 distanceDownRight[1]=0;
 distanceDown[0]=0;
 distanceDown[1]=0;
 distanceDownLeft[0]=0;
 distanceDownLeft[1]=0;
 distanceLeft[0]=0;
 distanceLeft[1]=0;
 distanceUpLeft[0]=0;
 distanceUpLeft[1]=0;
 for (int i=0; i<50; i++) {
   shiftedBufferIndex=n+i;
   if(i+n>nMax-1) shiftedBufferIndex=n+i-nMax;
   getHorFromFlash = pgm_read_word_near(&(comparisonBlink[HORIZONTAL]));
   getVerFromFlash = pgm_read_word_near(&(comparisonBlink[VERTICAL]));
   distanceBlink[HORIZONTAL]+=sq(valBufferOffseted[HORIZONTAL][shiftedBufferIndex]-getHorFromFlash);




distanceBlink[VERTICAL]+=sq(valBufferOffseted[VERTICAL][shiftedBufferIndex]-getVerFromFlash);
   getHorFromFlash = pgm_read_word_near(&(comparisonUp[HORIZONTAL]));
   getVerFromFlash = pgm_read_word_near(&(comparisonUp[VERTICAL]));
   distanceUp[HORIZONTAL]+=sq(valBufferOffseted[HORIZONTAL][shiftedBufferIndex]-getHorFromFlash);
   distanceUp[VERTICAL]+=sq(valBufferOffseted[VERTICAL][shiftedBufferIndex]-getVerFromFlash);
   getHorFromFlash = pgm_read_word_near(&(comparisonUpRight[HORIZONTAL]));
   getVerFromFlash = pgm_read_word_near(&(comparisonUpRight[VERTICAL]));
   distanceUpRight[HORIZONTAL]+=sq(valBufferOffseted[HORIZONTAL][shiftedBufferIndex]-getHorFromFlash);




distanceUpRight[VERTICAL]+=sq(valBufferOffseted[VERTICAL][shiftedBufferIndex]-getVerFromFlash);
   getHorFromFlash = pgm_read_word_near(&(comparisonRight[HORIZONTAL]));
   getVerFromFlash = pgm_read_word_near(&(comparisonRight[VERTICAL]));
   distanceRight[HORIZONTAL]+=sq(valBufferOffseted[HORIZONTAL][shiftedBufferIndex]-getHorFromFlash);




distanceRight[VERTICAL]+=sq(valBufferOffseted[VERTICAL][shiftedBufferIndex]-getVerFromFlash);
   getHorFromFlash = pgm_read_word_near(&(comparisonDownRight[HORIZONTAL]));
   getVerFromFlash = pgm_read_word_near(&(comparisonDownRight[VERTICAL]));
   distanceDownRight[HORIZONTAL]+=sq(valBufferOffseted[HORIZONTAL][shiftedBufferIndex]-getHorFromFlash);




distanceDownRight[VERTICAL]+=sq(valBufferOffseted[VERTICAL][shiftedBufferIndex]-getVerFromFlash);
   getHorFromFlash = pgm_read_word_near(&(comparisonDown[HORIZONTAL]));
   getVerFromFlash = pgm_read_word_near(&(comparisonDown[VERTICAL]));
   distanceDown[HORIZONTAL]+=sq(valBufferOffseted[HORIZONTAL][shiftedBufferIndex]-getHorFromFlash);




distanceDown[VERTICAL]+=sq(valBufferOffseted[VERTICAL][shiftedBufferIndex]-getVerFromFlash);
   getHorFromFlash = pgm_read_word_near(&(comparisonDownLeft[HORIZONTAL]));
   getVerFromFlash = pgm_read_word_near(&(comparisonDownLeft[VERTICAL]));
   distanceDownLeft[HORIZONTAL]+=sq(valBufferOffseted[HORIZONTAL][shiftedBufferIndex]-getHorFromFlash);




distanceDownLeft[VERTICAL]+=sq(valBufferOffseted[VERTICAL][shiftedBufferIndex]-getVerFromFlash);
   getHorFromFlash = pgm_read_word_near(&(comparisonLeft[HORIZONTAL]));
   getVerFromFlash = pgm_read_word_near(&(comparisonLeft[VERTICAL]));
   distanceLeft[HORIZONTAL]+=sq(valBufferOffseted[HORIZONTAL][shiftedBufferIndex]-getHorFromFlash);




distanceLeft[VERTICAL]+=sq(valBufferOffseted[VERTICAL][shiftedBufferIndex]-getVerFromFlash);
   getHorFromFlash = pgm_read_word_near(&(comparisonUpLeft[HORIZONTAL]));
   getVerFromFlash = pgm_read_word_near(&(comparisonUpLeft[VERTICAL]));
   distanceUpLeft[HORIZONTAL]+=sq(valBufferOffseted[HORIZONTAL][shiftedBufferIndex]-getHorFromFlash);




distanceUpLeft[VERTICAL]+=sq(valBufferOffseted[VERTICAL][shiftedBufferIndex]-getVerFromFlash);






}
 // AQUI CALCULAR AS DISTANCIAS SOMADAS DE TODOS
 calculatedDistances[0]=sqrt(distanceUp[HORIZONTAL]*horBoost+distanceUp[VERTICAL]/horBoost);
 calculatedDistances[1]=sqrt(distanceUpRight[HORIZONTAL]*horBoost+distanceUpRight[VERTICAL]/horBoost);
 calculatedDistances[2]=sqrt(distanceRight[HORIZONTAL]*horBoost+distanceRight[VERTICAL]/horBoost);
 calculatedDistances[3]=sqrt(distanceDownRight[HORIZONTAL]*horBoost+distanceDownRight[VERTICAL]
/horBoost);
 calculatedDistances[4]=sqrt(distanceDown[HORIZONTAL]*horBoost+distanceDown[VERTICAL]/horBoost)
;
 calculatedDistances[5]=sqrt(distanceDownLeft[HORIZONTAL]*horBoost+distanceDownLeft[VERTICAL]/horBoost);
 calculatedDistances[6]=sqrt(distanceLeft[HORIZONTAL]*horBoost+distanceLeft[VERTICAL]/horBoost);
 calculatedDistances[7]=sqrt(distanceUpLeft[HORIZONTAL]*horBoost+distanceUpLeft[VERTICAL]/horBoost);
 calculatedDistances[8]=sqrt(distanceBlink[HORIZONTAL]*horBoost+distanceBlink[VERTICAL]/horBoost);
 //  // AQUI CALCULAR QUAL O MENOR
 currentSignal=9;
 minDistance=minThreshold;
 if(calculatedDistances[8]<420) currentSignal=8;
 minDistance=580;
 for (int i=0; i<8; i=i+4){
   if (minDistance>calculatedDistances[i]){
     minDistance = calculatedDistances[i];
     currentSignal = i;
   }
 }
 minDistance=700;
 for (int i=1; i<8; i=i+2){
   if (minDistance>calculatedDistances[i]){
     minDistance = calculatedDistances[i];
     currentSignal = i;
   }
 }
 minDistance=780;
 for (int i=2; i<8; i=i+4){
   if (minDistance>calculatedDistances[i]){
     minDistance = calculatedDistances[i];
     currentSignal = i;
   }
 }
 // increment and loop if the end is reached
 if(n<nMax-1) n+=1;
 else n=0;
 // Set print flag to true
 printInfo=true;
}
void loop() {
 // Print each data collection information
 if(printInfo){
     Serial.print("blah");
     Serial.print(",");
     Serial.print(valBufferOffseted[HORIZONTAL][n]);
     Serial.print(",");
     Serial.print(valBufferOffseted[VERTICAL][n]);
     Serial.print(",");
     Serial.print(currentSignal);
     Serial.print(",");
     Serial.println("|");
   if(currentSignal!=9){
     Serial.print(currentSignal);
     Serial.println(" ");
   }
   printInfo=false;
 }
}

