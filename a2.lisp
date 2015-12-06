(setf dove 998)(setf tiger 999) (setf fighter 1007)
(setf doors (list dove dove dove tiger tiger tiger tiger))
(setf calced (car nil))
(setf probl nil)
(setf actual nil)

;List of gladiators with size some size x
(defun gladlist (x) (make-list x :initial-element fighter))

;Create the list that holds the pair of (surviving, probability)
(defun makeprobl (x) (loop for n from 0 to x do (setf probl (cons (list n 0) probl))) (setf probl (reverse probl)))

;Create the list that holds the pair of (surviving, occurece)
(defun makeactual (x) (loop for n from 0 to x do (setf actual (cons (list n 0) actual))) (setf actual (reverse actual)))

;Add the probability to probl
(defun updateprobl (n nprob) (setf (second (nth n probl)) (+ nprob (second (nth n probl)))) )

;Add the probability to probl
(defun divprobl (n) (setf (second (nth n probl)) (/ (second (nth n probl)) 2 )))

(defun finalizeprobl (n) (loop for x from 0 to n do (divprobl x)))

(defun finalizeprobltwo (n) (loop for x from 1 to n do (divprobl x)))

(defun printprobl(n) (finalizeprobl n) (finalizeprobltwo n) (loop for elem in probl do (print elem)))

;Add the acutal value to actual
(defun updateactual (n nval) (setf (second (nth n actual)) (+ nval (second (nth n actual)))))

;Use this function to shuffle lists
;knuth's shuffle algorithm
(defun shuffle (seq)
  (let ((n (length seq)))
    (dotimes (i n seq)
             (rotatef (elt seq i)
                      (elt seq (+ i (random (- n i))))))))
;Remove first occurence of element in a list
(defun remonce ( x l )
    (if l
        (if (equal x (car l))
            (cdr l)
            (cons (car l) (remonce x (cdr l)))
        )
    )
)

;Retrieve a random element from list
(defun randelem (l) (nth (random (length l)) l))

;Composition of all the functions into the main callable function
(defun intoArena (glad ldoor)
        (if(find fighter glad)
          (if (find tiger ldoor)
              (if  (=  (randelem ldoor) tiger )
                  (intoArena (remonce fighter glad) ldoor)
                  (intoArena  glad (remonce tiger ldoor)))
              (list glad ldoor))
          (list glad ldoor) ) )

;Runs the game simulation
(defun tothegames (x) (intoarena (gladlist x) doors))

(defun calculateprob (prev tdv tti gld ctu) (progn (processright prev tdv tti gld ctu) (processleft prev tdv tti gld ctu)))

(defun processleft (prev tdv tti gld ctu)  (if (= ctu 0)
                                             (updateprobl gld (float prev))
                                             (progn (processleft    (* prev (/ tti (+     tti    3)))           3      tti     (- gld 1) (- ctu 1))
                                                    (processright     (* prev (/ 3   (+  (- tti 1) 3)))         3    (- tti 1)     gld   (- ctu 1)) )))

(defun processright (prev tdv tti gld ctu) (if (= tti 0)
                                             (updateprobl gld (float prev))
                                             (if (= ctu 0 )
                                                (updateprobl gld (float prev))
                                                (progn (processleft     (* prev (/ tti (+     tti    3)))         3      tti     (- gld 1) (- ctu 1))
                                                       (processright    (* prev (/ 3   (+  (- tti 1) 3)))         3    (- tti 1)     gld   (- ctu 1)) )) )  )


(defun maincalc (prev tdv tti gld ctu)
       (progn (makeprobl gld)
              (calculateProb prev tdv tti gld ctu)))

(defun mainrun(g r) (progn (makeactual g)
                          (loop for x from 1 to r do (updateactual  (length (nth 0 (tothegames g)))  1  )   ))
                          (divup r))

(defun divup (r) (loop for parr in actual do (print (list (nth 0 parr) (float (/ (nth 1 parr) r))))) )
;Main run of the program
(print (tothegames 10))
