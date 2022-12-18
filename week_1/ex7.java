//Aing K.
//Equation solver for x1 to x8

import java.io.File;
import java.util.Scanner;
import java.util.HashSet;  
import java.util.Set;    

/**
 * ex7
 */
public class ex7 {
    public static void main(String[] args) throws Exception {
        // Open the txt input file    +   new scanner
        File file = new File("input_ex7.txt");
        Scanner sc = new Scanner(file);

        // Read 3 inputs from header
        int n = sc.nextInt();
        int c1 = sc.nextInt();
        int c2 = sc.nextInt();
        
        //array for keeping x1 to x8
        int x[] = new int[8];
        // Track seen number (DICT)
        Set<Integer> seenNumbers = new HashSet<>();

        //Read n inputs from file
        int A[] = new int[n];
        for(int i=0; i<n; i++){
            A[i] = sc.nextInt();
        }
        sc.close();

        ///////////////////////////////////////////////////

        // Create a function to find x1 and x2 where c1 = x1 + x2
        int i, j, k, l;
        int p, q, r, s;
        int an;
        for(i = 0; i < n; i++) {
            for(j = 0; j < n; j++) {
                if((A[i] + A[j] == c1) && !(seenNumbers.contains(A[i])) && !(seenNumbers.contains(A[j]))) {
                    x[0] = A[i];
                    x[1] = A[j];
                    seenNumbers.add(x[0]);
                    seenNumbers.add(x[1]);
                    System.out.println(" ");
                    System.out.println("x1 = " + x[0] + " x2 = " + x[1]);

                    for(k = 0; k < n; k++){
                        for(l = 0; l < n; l++){
                            if((A[l] == A[k] + x[0]) && !(seenNumbers.contains(A[k])) && !(seenNumbers.contains(A[l]))){
                                x[2] = A[k];
                                x[3] = A[l];
                                seenNumbers.add(x[2]);
                                seenNumbers.add(x[3]);
                                System.out.println("x3 = " + x[2] + " x4 = " + x[3]);

                                for(p = 0; p < n; p++){
                                    for(q = 0; q < n; q++){
                                        if((A[q] == c2 + A[p]) && !(seenNumbers.contains(A[p])) && !(seenNumbers.contains(A[q]))){
                                            x[5] = A[p];
                                            x[7] = A[q];
                                            seenNumbers.add(x[5]);
                                            seenNumbers.add(x[7]);
                                            System.out.println("x6 = " + x[5] + " x8 = " + x[7]);

                                            for(r = 0; r < n; r++){
                                                for(s = 0; s < n; s++){
                                                    if((A[s] == A[r] + A[5])){
                                                        x[4] = A[r];
                                                        x[6] = A[s];
                                                        seenNumbers.add(x[4]);
                                                        seenNumbers.add(x[6]);
                                                        System.out.println("x5 = " + x[4] + " x7 = " + x[6]);

                                                        // for(an = 0; an < 8; an++){
                                                        //     System.out.println(x[an]);
                                                        // }
                                                    }
                                                }
                                            }

                                        }
                                    }
                                }

                            }
                        }
                    }
                    
                }
            }
            seenNumbers = new HashSet<>();
        }    
    }
}
