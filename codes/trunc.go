//This program accepts float input from user and truncates it to an integer.

package main;

import "fmt";

func main() {
	fmt.Print("Please enter a decimal number\nWe'll truncate it for you:\n")
	var user float64
	fmt.Scanf("%f", &user)
	
	var y int
	y = int(user)
	fmt.Println("Now the truncated version of the number you entered:\n")
	fmt.Printf("%d\n", y)
}
