package ex7;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.HashSet;
import java.util.Arrays;   // to print array
import java.util.Set;      // import for use Set<Integer>  

/**
 * ex7
 */
public class ex7 {

    ///// Global Variable
    static int n;
    static int c1;
    static int c2;
    static int[] A; // Array A
    // array of n integers
    static int[] ans = new int[8]; // Array ans
    static Set<Integer> seenNumbers = new HashSet<>();

    ///// Main Method
    public static void main(String[] args) throws FileNotFoundException {

        readFile("input_ex7.txt");
        //System.out.println(Arrays.toString(A));
        System.out.println("[x1 x2 x3 x4 x5 x6 x7 x8]");

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if ( (i != j) && (!seenNumbers.contains(A[i])) && (!seenNumbers.contains(A[j])) ) {
                    if ( (A[i] + A[j]) == c1 ) {
                        //System.out.println("x1 : " + A[i] + ", x2 : " + A[j] );
                        seenNumbers.add(A[i]); // x1
                        ans[0] = A[i];
                        seenNumbers.add(A[j]); // x2
                        ans[1] = A[j];


                        for (int k = 0; k < n; k++){
                            for (int l = 0; l < n; l++){
                                if ( (k != l) && (!seenNumbers.contains(A[k])) && (!seenNumbers.contains(A[l])) ) {
                                    if ( (A[i] + A[k]) == A[l] ) {
                                        //System.out.println("x3 : " + A[k] + ", x4 : " + A[l] );
                                        seenNumbers.add(A[k]); // x3
                                        ans[2] = A[k];
                                        seenNumbers.add(A[l]); // x4
                                        ans[3] = A[l];


                                        for (int p = 0; p < n; p++){
                                            for (int q = 0; q < n; q++){
                                                if ( (p != q) && (!seenNumbers.contains(A[p])) && (!seenNumbers.contains(A[q])) ) {
                                                    if ( (A[p] + c2) == A[q] ) {
                                                        //System.out.println("x6 : " + A[p] + ", x8 : " + A[q] );
                                                        seenNumbers.add(A[p]); // x6
                                                        ans[5] = A[p];
                                                        seenNumbers.add(A[q]); // x8
                                                        ans[7] = A[q];


                                                        for (int r = 0; r < n; r++){
                                                            for (int s = 0; s < n; s++){
                                                                if ( (r != s) && (!seenNumbers.contains(A[r])) && (!seenNumbers.contains(A[s])) ) {
                                                                    if ( (A[p] + A[r]) == A[s] ) {
                                                                        //System.out.println("x5 : " + A[r] + ", x7 : " + A[s] );
                                                                        seenNumbers.add(A[r]); // x5
                                                                        ans[4] = A[r];
                                                                        seenNumbers.add(A[s]); // x7
                                                                        ans[6] = A[s];
                                                                    }
                                                                }
                                                            }
                                                        }
                                                        System.out.println(Arrays.toString(ans));
                                                        System.out.println("");

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
   

    /////   Open and Read file
    public static void readFile(String str) throws FileNotFoundException {

        // Open the txt input file    +   new scanner
        File file = new File(str);
        Scanner sc = new Scanner(file);

        // Read 3 inputs from header
        n = sc.nextInt();
        c1 = sc.nextInt();
        c2 = sc.nextInt();

        A = new int[n];
        for (int i = 0; i < n; i++) {
            A[i] = sc.nextInt();
        }

        sc.close();
    }
}
