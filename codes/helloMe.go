package main;

import "fmt";

var x int = 1

func foo() *int {
	return &x
} 

func flow() *int {
	for i:=0; i<10; i++ {
		fmt.Println("Do you need my help?")
		x++			
	}
	return &x
}

func main() {
	fmt.Println("Hello, world!")
	fmt.Println("Watch me print to screen a memory address:")
	
	var y *int
	y = foo()
	fmt.Printf("%d\n", *y)

	fmt.Println("Now we see a control flow implementation here:")
	
	var z *int
	z = flow()
	fmt.Printf("%d\n", *z)
}


