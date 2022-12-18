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
        for(i = 0; i < n; i++) {
            for(j = 0; j < n; j++) {
                if((A[i] + A[j] == c1) && (i != j)) {
                    x[0] = A[i];
                    x[1] = A[j];
                    seenNumbers.add(x[0]);
                    seenNumbers.add(x[1]);
                    System.out.println("x1 = " + x[0] + " x2 = " + x[1]);

                    
                }
            }
        }    
    }
}
