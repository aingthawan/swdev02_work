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
    Set<Integer> seenNumbers = new HashSet<>();

    ///// Main Method
    public static void main(String[] args) throws FileNotFoundException {

        readFile("input_ex7.txt");
        System.out.println(Arrays.toString(A));

        // if (seenNumbers.contains(num)) {
        //     System.out.println("Theres a repeated element in the array!");
        //     //exit program
        //     System.exit(0);
        //   } else {
        //     // add the number to the set
        //     seenNumbers.add(num); 
        // }








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
