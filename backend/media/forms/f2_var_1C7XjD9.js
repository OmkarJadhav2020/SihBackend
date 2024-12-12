//use variable To store data 

//Old way
// var firstname = "OMKAR";
// console.log(firstname);
// firstname = 'Rahul';//value can be changed
// console.log(firstname);
// new1 = 'hello';//this is allowed but creates error 
//to overcome this error use "use strict";

// "use strict";
// var new1 = 'hello';//this is allowed but creates error 
// console.log(new1);


//Rules
// 1. Var name cannot start with no
// 2. Use only dollar and underscore Symbol
// 3. Spaces not allowed 
// 4. Start with small letter and use camelcase(varName) 
// Snakecase(var_name)


//New way(why = block scope vs function scope)
// cannot allow double declareation of same variable (allowed using var) 
// "use strict";
// let firstname = 'Omkar';
// console.log(firstname);

//Constants
const pi = 3.14;
// pi = 12;//not allowed
console.log(pi);