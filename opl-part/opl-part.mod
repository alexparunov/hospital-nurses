/*********************************************
 * OPL 12.7.1.0 Model
 * Author: Alex and Asaf
 * Creation Date: Dec 1, 2017 at 3:50:44 PM
 *********************************************/


int nNurses=...;
int nHours=...;
int minHours=...; // each nurse should work at least minHours
int maxHours=...; // each nurse should work at most maxHours
int maxConsec=...; // maximum consecutive hours each nurse can work
int maxPresence=...; // no nurse can be present more than than maxPresence hours

range N=1..nNurses;
range H=1..nHours;
int demand[h in H]=...; // At least demand[i] hours each nurse should work


// Decision variables
dvar boolean works[n in N][h in H]; //Nurse "n" works at hour "h"
dvar boolean WA[n in N][h in H]; // WA - WorkAfter, Nurse "n" works at some hour after "h"
dvar boolean WB[n in N][h in H]; // WB - WorkBefore, Nurse "n" works at some hour before "h"
dvar boolean Rest[n in N][h in H]; // Rest - Rest, Nurse "n" rest at "h", note, this is NOT "Rest[n][h] == !(works[n][h])". Rest means the nurse work before and after.
dvar boolean used[n in N]; // nurse is working

minimize sum(n in N) used[n]; // do not change this for A

subject to {

	forall(h in H)
	  sum(n in N) works[n][h] >= demand[h];
//Each nurse should work at least minHours per hours 
    forall(n in N)
        sum(h in H) works[n][h] >= used[n]*minHours;

//Each nurse should work at most maxHours hours.
    forall(n in N)
        sum(h in H) works[n][h] <= used[n]*maxHours;
        
//Each nurse should work at most maxConsec consecutive hours.
	forall(n in N)
        forall(i in 1..(nHours-maxConsec))
            sum(j in i..(i+maxConsec)) works[n][j] <= used[n]*maxConsec;
            
//No nurse can stay at the hospital for more than maxPresence hours (e.g. if maxPresence is 7, it is OK that a nurse works at 2am and also at 8am, but it not possible that he/she works at 2am and also at 9am).
// assume we have nHours=8
// nurse start:3h , finish:7h
// WB vector will be 00111111
// WA vector will be 11111110
// if the nurse worked at hour h, she\he cannot work after h+maxPresence.
    forall(n in N)
        forall (h in H: h <= nHours-maxPresence)
            WB[n][h] + WA[n][h+maxPresence] <= 1;

//No nurse can rest for more than one consecutive hour (e.g. working at 8am, resting at 9am and 10am, and working again at 11am is not allowed, since there are two consecutive resting hours).            

    forall(n in N)
        forall (h in H: h <= nHours-1){
            WA[n][h] >=  WA[n][h+1];   // legal: 11111110, illegal: 11111010
            WB[n][h] <=  WB[n][h+1];   // legal: 00011111, illegal: 00111110
            Rest[n][h] + Rest[n][h+1] <= 1;
                                       // legal: 00010100, illegal: 00110010
		}                                       

    forall(n in N)
        forall (h in H)
            Rest[n][h] == (1-works[n][h]) - (1-WA[n][h]) - (1-WB[n][h]);
                           // WA[n][h] + WB[n][h] - works[n][h] - 1
                           // it's equivalent but it is easier for me to see it with: not(works) => (1-works)
       
 }
 
 execute { // Should not be changed. Assumes that variables works[n][h] are used.
  	for (var n in N) {
		write("Nurse ");
		if (n < 10) write(" ");
		write(n + " works:  ");
		var minHour = -1;
		var maxHour = -1;
		var totalHours = 0;
		for (var h in H) {
		  	if (works[n][h] == 1) {
		  		totalHours++;
		  		write("  W");	
		  		if (minHour == -1) minHour = h;
		  		maxHour = h;			  	
		  	}
		  	else write("  .");
   		}
   		if (minHour != -1) write("  Presence: " + (maxHour - minHour +1));
   		else write("  Presence: 0")
   		writeln ("\t(TOTAL " + totalHours + "h)");		  		  
	}		
	writeln("");
	write("Demand:          ");
	
	for (h in H) {
	if (demand[h] < 10) write(" ");
	write(" " + demand[h]);	
	}
	writeln("");
	write("Assigned:        ");
	for (h in H) {
		var total = 0;
		for (n in N)
			if (works[n][h] == 1) total = total+1;
		if (total < 10) write(" ");
		write(" " + total);		
	}		
}  
 
