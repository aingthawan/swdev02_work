package ex6;
// Improved version on week1_sum10.java
// By AI ChatGPT

import java.io.File;
import java.util.Scanner;

public class MatrixCounter {
  private int[][] matrix;
  private int count;

  public MatrixCounter(int[][] matrix) {
    this.matrix = matrix;
    this.count = 0;
  }

  public void countRowsAndColumns() {
    // Loop through each row and column of the matrix
    for (int i = 0; i < matrix.length; i++){
      for (int j = 0; j < matrix[0].length; j++){
        // Initialize variables for the sum of the elements in the row and column
        int rowSum = 0;
        int colSum = 0;

        // Sum the elements in the row and column
        for (int k = j; k < matrix[0].length; k++){
          rowSum += matrix[i][k];
          if (rowSum == 10) {
            count++;
            break;
          } else if (rowSum > 10) {
            break;
          }
        }
        for (int l = i; l < matrix.length; l++){
          colSum += matrix[l][i];
          if (colSum == 10) {
            count++;
            break;
          } else if (colSum > 10) {
            break;
          }
        }
      }
    }
  }

  public int getCount() {
    return count;
  }

  public static void main(String[] args) throws Exception {
    // Open the input text file and create a scanner to read from it
    File file = new File("input_sum10.txt");
    Scanner scanner = new Scanner(file);

    // Read the number of matrices
    int numMatrices = scanner.nextInt();

    // Loop through each matrix
    for (int m = 0; m < numMatrices; m++) {
      // Read the size of the matrix
      int matrixSize = scanner.nextInt();

      // Create a new matrix variable
      int[][] matrix = new int[matrixSize][matrixSize];

      // Read the elements of the matrix
      for (int i = 0; i < matrixSize; i++){
        for (int j = 0; j < matrixSize; j++){
          matrix[i][j] = scanner.nextInt();
        }
      }

      // Create a MatrixCounter for the matrix
      MatrixCounter counter = new MatrixCounter(matrix);

      // Count the rows and columns with a sum of 10
      counter.countRowsAndColumns();

      // Print the result
      System.out.println(counter.getCount());
    }

    // Close the scanner
    scanner.close();
  }
}
