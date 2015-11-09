--- spell.py	(original)
+++ spell.py	(refactored)
@@ -62,7 +62,7 @@
 def best_guess_if_rwe(previous_word, current_word):
     min_error_count = float('inf')
     min_error_word = ""
-    for key, value in following_word[previous_word].iteritems():
+    for key, value in following_word[previous_word].items():
         edit_distance = editdistance.eval(key, current_word)
         if edit_distance < min_error_count:
             min_error_count = edit_distance
@@ -80,20 +80,20 @@
             correct_word = row['CorrectWord']
             if not exists(prev_word):
                 continue
-            print "Count: ", count_seen_wordpair(prev_word, word), "\t",
+            print("Count: ", count_seen_wordpair(prev_word, word), "\t", end=' ')
             if not count_seen_wordpair(prev_word, word):
-                print "Pair with error: ", prev_word, word, "\t",
+                print("Pair with error: ", prev_word, word, "\t", end=' ')
                 guess = best_guess_if_rwe(prev_word, word)
-                print "Best guess: ", guess, "\t",
-                print "Correct word: ", correct_word
+                print("Best guess: ", guess, "\t", end=' ')
+                print("Correct word: ", correct_word)
             elif word != correct_word:
-                print "Not a real word error: ", word, "\t",
-                print "Correct word: ", correct_word
+                print("Not a real word error: ", word, "\t", end=' ')
+                print("Correct word: ", correct_word)
             prev_word = guess
 
 create_dicts()
