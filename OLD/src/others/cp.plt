set xrange [0:160]
set yrange [0:35]

plot   'cp2014.txt' using 1:2 t 'r1'
replot 'cp2014.txt' using 1:3 t 'r2' 
replot 'cp2014.txt' using 1:4 t 'r3' 
replot 'cp2014.txt' using 1:5 t 'r4' 
replot 'cp2014.txt' using 1:6 t 'r5' 
replot 'cp2014.txt' using 1:7 t 'r6' 
replot 'cp2014.txt' using 1:8 t 'bl' 
 
save  'cp.plt'
