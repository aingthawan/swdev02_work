import java.io.File;
import java.util.Scanner;

/**
 * sum10
 */
public class sum10 {
  public static void main(String[] args) throws Exception {

    // Open the txt input file    +   new scanner
    File file = new File("input_sum10test.txt");
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
       
        //reset count
        r_sum = 0;
        d_sum = 0;

        for (int k = j; k < matrixSize; k++){
          r_sum = r_sum + matrix[i][k];
          if (r_sum == 10){
            tenCount += 1;
          }
        }

        for (int l = i; l < matrixSize; l++){
          d_sum = d_sum + matrix[l][i];
          if (d_sum == 10){
            tenCount += 1;
          }
        }
      }
    }
    System.out.println(tenCount);

  }
}