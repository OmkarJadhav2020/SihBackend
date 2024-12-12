function about(hobby,songs)
{
    console.log(this.firstname,this.age,hobby,songs)
}

const user1 = 
{
    firstname : 'omkar',
    age : 10,
    test : function(some)
    {
        console.log(this.firstname,some);
    }
}
const user2 = 
{
    firstname : 'rahul',
    age : 20,
}
// call -> binds method of a object to another object 
// about.call(user1,'play');
// user1.test.call(user2,'test');
//apply -> same as call (uses call internally) (pass arguement in array)
// about.apply(user2,['guitor','ter'])

//bind returns a function
const test = about.bind(user2);
test('okat','asd');