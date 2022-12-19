package ex7;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

/**
 * ex7
 */
public class ex7 {

    ///// Global Varable
    static int n;
    static int c1;
    static int c2;
    static int[] A; // Array A

    ///// Main Method
    public static void main(String[] args) throws FileNotFoundException {

        readFile("input_ex7.txt");
        System.out.println(n);
        System.out.println(c1);
        System.out.println(c2);




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
