import java.io.File;
import java.util.Scanner;

/**
 * sum10
 */
public class sum10 {
  public static void main(String[] args) throws Exception {

    // Open the txt input file    +   new scanner
    File file = new File("input_sum10test2.txt");
    Scanner scanner = new Scanner(file);

    // Read the first libe of txt file for matrix size
    int matrixSize = scanner.nextInt();

    // Create new matrix variable
    int[][] matrix = new int[matrixSize][matrixSize];

    // Loop read input matrix
    for (int i = 0; i < matrixSize; i++){
      for (int j = 0; j < matrixSize; j++){
        matrix[i][j] = scanner.nextInt();          
      }
    }

    // Close scanner
    scanner.close();

    int r_sum;
    int d_sum;
    int tenCount = 0;

    for (int i = 0; i < matrixSize; i++){
      for (int j = 0; j < matrixSize; j++){
        System.out.print(matrix[i][j] + " ");
      }
      System.out.println();
    }
    System.out.println();
    System.out.println("=======================================");
    System.out.println();

    for (int i = 0; i < matrixSize; i++){
      for (int j = 0; j < matrixSize; j++){
        System.out.print(matrix[i][j] + " ");
        
        r_sum = 0;
        d_sum = 0;

        System.out.print(" Go R : ");
        for (int k = j+1; k < matrixSize; k++){
          //System.out.print(matrix[i][k]);
          r_sum = r_sum + matrix[i][k];
        }
        System.out.print(r_sum);

        System.out.print(" Go D : ");
        for (int l = i+1; l < matrixSize; l++){
          //System.out.print(matrix[l][i]);
          d_sum = d_sum + matrix[l][i];
        }
        System.out.print(d_sum);


        System.out.println();
      }
    }


  }
}