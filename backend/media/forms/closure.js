// // functions and return functions

// // function outerfunction(test)
// // {
// //     function innerfunc()
// //     {
// //         return "FUCK YOU" + test;
// //     }
// //     return innerfunc;
// // }

// const ans = outerfunction('ASD');
// console.log(ans);


// function myFunc(x)
// {
//     function powerof(num)
//     {
//         return num**x;
//     }
//     return powerof;
// }

// const myFunc = power=>number=>number**power;
// const test = myFunc(2);
// const test1= myFunc(3);
// console.log(test(2));
// console.log(test1(2));

const oneTime = ()=>
{
    let counter = 0;
    function r()
    {
        if(counter==0)
        {
            counter++;
            return  "HI";
        }
        return "I have been called already";
    }
    return r;
}

const test = oneTime();

console.log(test());
console.log(test());
const test1 = oneTime();
console.log(test1());