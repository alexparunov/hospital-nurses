/*********************************************
 * OPL 12.7.1.0 Model
 * Author: alex and asaf
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
int demandH[n in N]=...; // At least demandH[i] hours each nurse should work

// Decision variables
dvar boolean nh[n in N][h in H]; //Nurse "n" works at hour "h"

