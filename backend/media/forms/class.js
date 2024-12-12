"use strict";
class Animal
{
    constructor(name,type)
    {
        this.name = name;
        this.type = type;
    }
}
class Dog extends Animal
{
    constructor(name,type,age)
    {
        super(name,type);
        this.age = age;
    }
}

let a = new Dog('Kdud','DOG',12);
console.log(a.name);