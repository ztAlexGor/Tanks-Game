(import [pandas :as pd])
(import [numpy :as np])
;(import [matplotlib.pyplot :as plt])
;(import [sklearn.linear_model [LinearRegression]])
;(import [csv_writer [write_result]])

(setv columns ["stupid" "smart" "algorithm" "map" "duration" "victory" "score"])
(setv data_frame (pd.read_csv "game stat.csv" :usecols columns))

(setv res (np.array data_frame.score))

(res.reshape -1 1)

(setv d 0)
(setv m 0)
(for [x res]
    (+= m (/ x (len res)))
    (+= d (/(* x x) (len res))))

(-= d (* m m))

(print "Expected value" (round m 2))
(print "Dispersion" (round d 2))