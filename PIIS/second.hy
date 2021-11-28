(import [random[randint]])

(defn createMap [sizeX sizeY]
    (setv m [])
    (for [i (range sizeX)]
        (m.append [])
        (for [j (range sizeY)]
            (setv t (get m i))
            (t.append (randint 0 1))))
    m)
    

(setv pole (createMap 5 5))
(setv player [0 2 1 0])
(setv enemy [3 2 1 0])

; (for [x pole]
;     (print x))

(defn minimax [depth turn]
    ; (setv v 0)

    (if (= depth 0)
        (setv v -10000))
    
    (if (= (get player 2) 0)
        (setv v -10000))

    (if (= (get enemy 2) 0)
        (setv v 10000))
    
    
    v
)




(setv val (minimax 4 1))
(print val)