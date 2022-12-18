//Aing K.
//Equation solver for x1 to x8

import java.io.File;
import java.util.Scanner;

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

        
        int A[] = new int[n];
        
        //array for keeping x1 to x8
        int x[] = new int[8];
        // Track seen number (DICT)
        Set<Integer> seenNumbers = new HashSet<>();


        for(int i=0; i<n; i++){
            A[i] = sc.nextInt();
        }

        ///////////////////////////////////////////////////

        //create a function to find x1 and x2 which c1 = x1 + x2
        for(int i=0; i<n; i++){
            for(int j=0; j<n; j++){
                if(A[i] + A[j] == c1){
                    x[0] = A[i];
                    x[1] = A[j];
                }
            }
        }


    
    sc.close();
    }
}
