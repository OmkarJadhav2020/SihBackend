"use strict";
let firstname = '  omkar  ';
console.log(firstname);
//string are immutable
// firstname[0] = 'a';//not allowed
console.log(firstname[4]);//indexing
console.log(firstname.length);//length is property
firstname = firstname.trim()//removes spaces at start and end returns a string 
console.log(firstname.toUpperCase());//all capital
console.log(firstname.toLowerCase());//all lower
console.log(firstname.slice(0,2));//string slicing(end index will not be included)
