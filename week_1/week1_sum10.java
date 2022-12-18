// Aing K.
// Sum10 Matrix

import java.io.File;
import java.util.Scanner;

public class week1_sum10 {
  public static void main(String[] args) throws Exception {
    File file = new File("input_sum10.txt");    // Open the txt input file    
    Scanner scanner = new Scanner(file);                 // new scanner
    int numMatrices = scanner.nextInt();                 // Read number of matrices
    
    for (int m = 0; m < numMatrices; m++) {               // Loop each matrix
      int matrixSize = scanner.nextInt();                 // Read the matrix size
      int[][] matrix = new int[matrixSize][matrixSize];   // new matrix variable
      for (int i = 0; i < matrixSize; i++){               // Loop to read input matrix
        for (int j = 0; j < matrixSize; j++){
          matrix[i][j] = scanner.nextInt();          
        }
      }
      int tenCount = 0;                            // Counting Variable
      for (int i = 0; i < matrixSize; i++){
        for (int j = 0; j < matrixSize; j++){
          int r_sum = 0;                           //reset count variables
          int d_sum = 0;

          for (int k = j; k < matrixSize; k++){    // loop sum elements in row
            r_sum = r_sum + matrix[i][k];
            if (r_sum == 10){
              tenCount += 1;
            }else if (r_sum > 10){
              break;
            }
          }
          for (int l = i; l < matrixSize; l++){   // loop sum elements in column
            d_sum = d_sum + matrix[l][i];
            if (d_sum == 10){
              tenCount += 1;
            }else if (d_sum > 10){
              break;
            }
          }
        }
      }
      System.out.println(tenCount);               // Print result
    }
    scanner.close();                              // Close scanner
  }
}
