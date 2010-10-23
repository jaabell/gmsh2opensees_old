/* Geometria basica para amplificacion topografica */
/*
                       B                                                      
                     <-->________________________(4)        _ _                
                       / (5)                      |  H1      |                  
(7)___________________/___________________________|(3)       |  
  |                   (6)                         |          |                  
H1|                                               | H2 - H1  | H2               
  |-----------------------------------------------|         _|_                 
 (1)                                             (2)                          
  <--------------------- L ---------------------->                            
                                                                              
*/

// Parametros globales geometria
L = 2000;  // [m] Largo total del modelo
H1 = 300;  // [m] Altura minima del modelo
H2 = 400;  // [m] Altura maxima del modelo
B = 100;   // [m] Longitud horizontal del talud

tam = 60;  // tamaño de elementos 


//Puntos
x1 = L/2 - B/2;
x2 = L/2 + B/2;

Point(1) = {0, 0, 0, tam};
Point(2) = {L, 0, 0, tam};
Point(3) = {L, H1, 0, tam};
Point(4) = {L, H2, 0, tam};
Point(5) = {x2, H2, 0, tam/2};
Point(6) = {x1, H1, 0, tam/4};
Point(7) = {0, H1, 0, tam};

//Lineas
l1 = newl; Line(l1) = {1, 2};
l2 = newl; Line(l2) = {2, 3};
l3 = newl; Line(l3) = {3, 4};
l4 = newl; Line(l4) = {4, 5};
l5 = newl; Line(l5) = {5, 6};
l6 = newl; Line(l6) = {6, 7};
l7 = newl; Line(l7) = {7, 1};
l8 = newl; Line(l8) = {6, 3};

// Definir superficies de mesheo
Line Loop(1) = {l1, l2, -l8, l6, l7};
Line Loop(2) = {l3, l4, l5, l8};
Plane Surface(1) = {1};
Plane Surface(2) = {2};

// Grupos Fisicos
Physical Line(9) = {6, 5, 4};
BordeLibre = 9;

Physical Line(10) = {7};
BordeIzq = 10;

Physical Line(11) = {2, 3};
BordeDer = 11;

Physical Line(12) = {1};
Roca = 12;

Physical Surface(13) = {2};
Arriba = 13;

Physical Surface(14) = {1};
Abajo = 14;

