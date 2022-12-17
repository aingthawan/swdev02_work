import java.io.File;
import java.util.Scanner;

/**
 * sum10
 */
public class sum10_v2 {
  public static void main(String[] args) throws Exception {

    // Open the txt input file    +   new scanner
    File file = new File("input_sum10.txt");
    Scanner scanner = new Scanner(file);

    // Read the first line of the file to get the number of matrices
    int numMatrices = scanner.nextInt();

    // Loop through each matrix
    for (int m = 0; m < numMatrices; m++) {
      // Read the matrix size
      int matrixSize = scanner.nextInt();

      // Create new matrix variable
      int[][] matrix = new int[matrixSize][matrixSize];

      // Loop to read input matrix
      for (int i = 0; i < matrixSize; i++){
        for (int j = 0; j < matrixSize; j++){
          matrix[i][j] = scanner.nextInt();          
        }
      }

      // Count the number of rows and columns with sum equal to 10
      int tenCount = 0;
      for (int i = 0; i < matrixSize; i++){
        for (int j = 0; j < matrixSize; j++){
         
          //reset count
          int r_sum = 0;
          int d_sum = 0;

          // Sum elements in row
          for (int k = j; k < matrixSize; k++){
            r_sum = r_sum + matrix[i][k];
            if (r_sum == 10){
              tenCount += 1;
            }else if (r_sum > 10){
              break;
            }
          }

          // Sum elements in column
          for (int l = i; l < matrixSize; l++){
            d_sum = d_sum + matrix[l][i];
            if (d_sum == 10){
              tenCount += 1;
            }else if (d_sum > 10){
              break;
            }
          }
        }
      }

      // Print result
      System.out.println(tenCount);
    }

    // Close scanner
    scanner.close();
  }
}
